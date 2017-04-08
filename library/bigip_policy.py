#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
---
module: bigip_policy
short_description: Manage general policy configuration on a BIG-IP.
description:
  - Manages general policy configuration on a BIG-IP. This module is best
    used in conjunction with the C(bigip_policy_rule) module. This module
    can handle general configuration like setting the draft state of the policy,
    the description, and things unrelated to the policy rules themselves.
    It is also the first module that should be used when creating rules as
    the C(bigip_policy_rule) module requires a policy parameter.
version_added: "2.4"
options:
  description:
    description:
      - The description to attach to the Partition.
    required: False
    default: None
  name:
    description:
      - The name of the policy to create.
    required: True
  state:
    description:
      - When C(state) is C(present), ensures that the policy exists and is
        published. When C(state) is C(absent), ensures that the policy is removed,
        even if it is currently drafted. When C(state) is C(draft), ensures that
        the policy exists and is drafted.
    required: False
    default: present
    choices:
      - present
      - absent
      - draft
  strategy:
    description:
      - Specifies the method to determine which actions get executed in the
        case where there are multiple rules that match. When creating new
        policies, the default is C(first).
    default: None
    required: False
    choices:
      - first
      - all
      - best
      - Custom strategy
notes:
   - Requires the f5-sdk Python package on the host. This is as easy as
     pip install f5-sdk
requirements:
  - f5-sdk
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
vars:
    policy_rules:
        - name: rule1
          actions:
              - forward: "yes"
                select: "yes"
                pool: "pool-svrs"
          conditions:
              - http_uri: "yes"
                path: "yes"
                starts-with:
                    - /euro
          ordinal: 8
        - name: HomePage
          actions:
              - forward: yes
                select: yes
                pool: "pool-svrs"
          conditions:
              - http-uri: yes
                path: yes
                starts-with:
                    - /HomePage/
          ordinal: 4

- name: Create policies
  bigip_policy:
      name: "Policy-Foo"
      state: present
  delegate_to: localhost

- name: Add a rule to the new policy
  bigip_policy_rule:
      policy: "Policy-Foo"
      name: "ABC"
      ordinal: 11
      conditions:
          - http_uri: "yes"
            path: "yes"
            starts_with:
                - "/ABC"
      actions:
          - forward: "yes"
            select: "yes"
            pool: "pool-svrs"

- name: Add multiple rules to the new policy
  bigip_policy_rule:
      policy: "Policy-Foo"
      name: "{{ item.name }}"
      ordinal: "{{ item.ordinal }}"
      conditions: "{{ item.conditions }}"
      actions: "{{ item.actions }}"
  with_items:
      - policy_rules
'''

import re
from ansible.module_utils.f5_utils import *
from distutils.version import LooseVersion
from icontrol.exceptions import iControlUnexpectedHTTPError


class Parameters(AnsibleF5Parameters):
    api_attributes = ['strategy', 'description']
    updatables = ['strategy', 'description']
    returnables = ['strategy', 'description']

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result

    @property
    def strategy(self):
        if self._values['strategy'] is None:
            return None

        # Look for 'first' from Ansible or REST
        elif self._values['strategy'] == 'first':
            return self._get_builtin_strategy('first')
        elif 'first-match' in self._values['strategy']:
            return str(self._values['strategy'])

        # Look for 'all' from Ansible or REST
        elif self._values['strategy'] == 'all':
            return self._get_builtin_strategy('all')
        elif 'all-match' in self._values['strategy']:
            return str(self._values['strategy'])

        else:
            # Look for 'best' from Ansible or REST
            if self._values['strategy'] == 'best':
                return self._get_builtin_strategy('best')
            elif 'best-match' in self._values['strategy']:
                return str(self._values['strategy'])
            else:
                # These are custom strategies. The strategy may include the
                # partition, but if it does not, then we add the partition
                # that is provided to the module.
                return self._get_custom_strategy_name()

    def _get_builtin_strategy(self, strategy):
        return '/{0}/{1}-match'.format(
            self.partition, strategy
        )

    def _get_custom_strategy_name(self):
        strategy = self._values['strategy']
        if re.match(r'(\/[a-zA-Z_0-9.-]+){2}', strategy):
            return strategy
        elif re.match(r'[a-zA-Z_0-9.-]+', strategy):
            return '/{0}/{1}'.format(self.partition, strategy)
        else:
            raise F5ModuleError(
                "The provided strategy name is invalid!"
            )

    @strategy.setter
    def strategy(self, value):
        self._values['strategy'] = value


class BaseTrafficPolicyManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = attr1
        self.changes = Parameters(changed)
        if changed:
            return True
        return False

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def _validate_creation_parameters(self):
        if self.want.strategy is None:
            self.want.strategy = 'first'


class SimpleTrafficPolicyManager(BaseTrafficPolicyManager):
    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def read_current_from_device(self):
        resource = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result = resource.attrs
        return Parameters(result)

    def exists(self):
        return self.client.api.tm.ltm.policys.policy.exists(
            name=self.want.name,
            partition=self.want.partition
        )

    def update_on_device(self):
        params = self.want.api_params()
        resource = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.modify(**params)
        return resource

    def create(self):
        self._validate_creation_parameters()

        self._set_changed_options()
        if self.client.check_mode:
            return True

        self.update_on_device()
        return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True

        self.update_on_device()
        return True


class ComplexTrafficPolicyManager(BaseTrafficPolicyManager):
    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:

            if state in ["present", "draft"]:
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def should_update(self):
        result = self._update_changed_options()
        drafted = self.draft_status_changed()
        if any(x is True for x in [result, drafted]):
            return True
        return False

    def draft_status_changed(self):
        if self.draft_exists() and self.want.state == 'draft':
            drafted = False
        elif not self.draft_exists() and self.want.state == 'present':
            drafted = False
        else:
            drafted = True
        return drafted

    def present(self):
        if self.draft_exists() or self.policy_exists():
            return self.update()
        else:
            return self.create()

    def read_current_from_device(self):
        if self.draft_exists():
            resource = self.client.api.tm.ltm.policys.policy.load(
                name=self.want.name,
                partition=self.want.partition,
                subPath = 'Drafts'
            )
        else:
            resource = self.client.api.tm.ltm.policys.policy.load(
                name=self.want.name,
                partition=self.want.partition
            )
        result = Parameters(resource.attrs)
        return result

    def policy_exists(self):
        params = dict(
            name=self.want.name,
            partition=self.want.partition
        )
        result = self.client.api.tm.ltm.policys.policy.exists(**params)
        return result

    def draft_exists(self):
        params = dict(
            name=self.want.name,
            partition=self.want.partition,
            subPath='Drafts'
        )
        result = self.client.api.tm.ltm.policys.policy.exists(**params)
        return result

    def _create_new_policy_draft(self):
        params = dict(
            name=self.want.name,
            partition=self.want.partition,
            subPath='Drafts',
            strategy=self.want.strategy
        )
        self.client.api.tm.ltm.policys.policy.create(**params)
        return True

    def _create_existing_policy_draft(self):
        params = dict(
            name=self.want.name,
            partition=self.want.partition,
        )
        resource = self.client.api.tm.ltm.policys.policy.load(**params)
        resource.draft()
        return True

    def update_on_device(self):
        params = self.want.api_params()
        resource = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.name,
            partition=self.want.partition,
            subPath='Drafts'
        )
        resource.modify(**params)

    def publish(self):
        resource = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.name,
            partition=self.want.partition,
            subPath='Drafts'
        )
        resource.publish()
        return True

    def create(self):
        self._validate_creation_parameters()

        self._set_changed_options()
        if self.client.check_mode:
            return True

        if not self.draft_exists():
            self._create_new_policy_draft()

        # Because we always need to modify drafts, "creating on the device"
        # is actually identical to just updating.
        self.update_on_device()

        if self.want.state == 'draft':
            return True
        else:
            return self.publish()

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True

        if not self.draft_exists():
            self._create_existing_policy_draft()

        if self._update_changed_options():
            self.update_on_device()

        if self.want.state == 'draft':
            return True
        else:
            return self.publish()


class ModuleManager(object):
    def __init__(self, client):
        self.client = client

    def exec_module(self):
        if self.version_is_less_than_12():
            manager = self.get_manager('simple_traffic')
        else:
            manager = self.get_manager('complex_traffic')
        return manager.exec_module()

    def get_manager(self, type):
        if type == 'traffic':
            return SimpleTrafficPolicyManager(self.client)
        elif type =='complex_traffic':
            return ComplexTrafficPolicyManager(self.client)

    def version_is_less_than_12(self):
        version = self.client.api.tmos_version
        if LooseVersion(version) < LooseVersion('12.1.0'):
            return True
        else:
            return False


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(
                required=True
            ),
            description=dict(
                required=False,
                default=None
            ),
            strategy=dict(
                required=False,
                default=None
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present', 'draft']
            )
        )
        self.f5_product_name = 'bigip'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
