#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_policy_rule
short_description: Manage LTM policy rules on a BIG-IP
description:
  - This module will manage LTM policy rules on a BIG-IP.
version_added: 2.5
options:
  actions:
    description:
      - The actions that you want the policy rule to perform.
      - The available attributes vary by the action, however, each action requires that
        a C(type) be specified.
      - Available C(type) values are C(forward).
  append:
    description:
      - When C(yes), will append all C(conditions) and C(actions) to the
        given rule if they do not already exist.
      - When C(actions), will only append the specified actions. If C(conditions)
        are also provided, the existing conditions will be overwritten with the
        new list in the C(conditions) parameter.
      - When C(conditions), will only append the specified conditions. If C(actions)
        are also provided, the existing actions will be overwritten with the
        new list in the C(actions) parameter.
    choices:
      - yes
      - no
      - actions
      - conditions
    default: no
  policy:
    description:
      - The name of the policy that you want to associate this rule with.
    required: True
  name:
    description:
      - The name of the rule.
    required: True
  conditions:
    description:
      - A list of attributes that describe the condition.
      - See suboptions for details on how to construct each list entry.
      - The ordering of this list is important, the module will ensure the order is
        kept when modifying the task.
      - The suboption options listed below are not required for all condition types,
        read the description for more details.
    suboptions:
      type:
        description:
          - The condition type. This value controls what below options are required.
        required: true
        choices: [ http_uri ]
  state:
    description:
      - When C(present), ensures that the key is uploaded to the device. When
        C(absent), ensures that the key is removed from the device. If the key
        is currently in use, the module will not be able to remove the key.
    default: present
    choices:
      - present
      - absent
  partition:
    description:
      - Device partition to manage resources on.
    default: Common
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
  - f5-sdk >= 3.0.0
  - BIG-IP >= v12.1.0
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
vars:
  policy_rules:
    - name: rule1
      actions:
    - type: forward
      pool: pool-svrs
  conditions:
    - type: http_uri
      path_starts_with: /euro
    - name: rule2
      actions:
    - type: forward
      pool: pool-svrs
  conditions:
    - type: http_uri
      path_starts_with: /HomePage/

- name: Create policies
  bigip_policy:
    name: Policy-Foo
    state: present
  delegate_to: localhost

- name: Add a rule to the new policy
  bigip_policy_rule:
    policy: Policy-Foo
    name: rule3
    conditions:
      - type: http_uri
        path_starts_with: /ABC
    actions:
      - type: forward
        pool: pool-svrs

- name: Add multiple rules to the new policy
  bigip_policy_rule:
    policy: Policy-Foo
    name: "{{ item.name }}"
    conditions: "{{ item.conditions }}"
    actions: "{{ item.actions }}"
  with_items:
    - policy_rules
'''

RETURN = r'''

'''


from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError
from ansible.module_utils.parsing.convert_bool import BOOLEANS
from ansible.module_utils.six import iteritems
from collections import defaultdict

try:
    # Test related
    from module_utils.f5networks.common import Noop
    from module_utils.f5networks.common import fqdn_name
    import q
except ImportError:
    pass

try:
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    HAS_F5SDK = False


class Parameters(object):
    api_attributes = [
        'description'
    ]

    def __init__(self, *args, **kwargs):
        self._values = defaultdict(lambda: None)
        self._values['__warnings'] = []
        params = kwargs.get('params', None)
        q.q(params)
        if params:
            self.update(params)

    def update(self, params):
        self._values.update(params)

    @property
    def name(self):
        return self._values.get('name', None)

    @property
    def description(self):
        return self._values.get('description', None)

    @property
    def partition(self):
        return self._values.get('partition', 'Common')

    @property
    def strategy(self):
        value = self._values.get('strategy', None)
        if value is None:
            return None
        result = fqdn_name(self.partition, value)
        return result

    @property
    def policy(self):
        value = self._values.get('policy', None)
        if value is None:
            return None
        result = fqdn_name(self.partition, value)
        return result


class ApiParameters(Parameters):
    @staticmethod
    def to_params(self, changes):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleParameters(Parameters):
    @property
    def actions(self):
        pass

    @property
    def conditions(self):


class Changes(Parameters):
    returnables = []

    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class Difference(object):
    updatables = [
        'actions', 'conditions', 'description'
    ]

    def __init__(self, *args, **kwargs):
        self.want = kwargs.get('want', None)
        self.have = kwargs.get('have', None)
        if self.want is None or self.have.have is None:
            raise F5ModuleError(
                "Calculating a difference requires 'want' and 'have' params."
            )

    def compare(self):
        result = dict()
        for param in self.updatables:
            try:
                change = getattr(self, param)
            except AttributeError:
                change = self.__default(param)
            if isinstance(change, dict):
                result.update(change)
            else:
                result[param] = change
        return result

    def __default(self, param):
        want = getattr(self.want, param)
        try:
            have = getattr(self.have, param)
            if want != have:
                return want
        except AttributeError:
            return want

    @property
    def actions(self):
        pass

    @property
    def conditions(self):
        pass


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.want = ModuleParameters(params=self.client.module.params)
        self.changes = Changes()

    def _update_changed_options(self):
        """Compares what you want with what you have.

        Returns:
            bool: True when changes are present. False otherwise.
        """
        diff = Difference(self.want, self.have)
        comparison = diff.compare()
        result = [r for r in comparison if not isistance(r[1], Noop)]
        if result:
            self.changes = Changes(params=result)
            return True
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

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
        self._announce_deprecations(result)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def exists(self):
        policy = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.policy,
            partition=self.want.partition
        )
        result = policy.rules_s.rules.exists(
            name=self.want.name
        )
        return result

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        return True

    def create(self):
        self.have = ApiParameters()
        self.should_update()
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.want.api_params()
        policy = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.policy,
            partition=self.want.partition
        )
        policy.rules_s.rules.create(
            name=self.want.name,
            **params
        )

    def update_on_device(self):
        params = self.want.api_params()
        policy = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.policy,
            partition=self.want.partition
        )
        resource = policy.rules_s.rules.load(
            name=self.want.name
        )
        resource.modify(**params)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove_from_device(self):
        policy = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.policy,
            partition=self.want.partition
        )
        resource = policy.rules_s.rules.load(
            name=self.want.name
        )
        if resource:
            resource.delete()

    def read_current_from_device(self):
        resource = self.client.api.tm.ltm.policys.policy.load(
            name=self.want.policy,
            partition=self.want.partition,
            requests_params=dict(
                params='expandSubcollections=true'
            )
        )
        return ApiParameters(params=resource.attrs)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        conditions_suboption_spec = dict(
            type=dict(
                choices=[
                    'http_uri'
                ]
            )
        )
        actions_suboption_spec = dict(
            type=dict(
                choices=[
                    'forward'
                ]
            )
        )
        self.argument_spec = dict(
            append=dict(
                choices=['actions', 'conditions'] + BOOLEANS)
            ,
            actions=dict(
                type='list',
                options=actions_suboption_spec
            ),
            conditions=dict(
                type='list',
                options=conditions_suboption_spec
            ),
            name=dict(required=True),
            partition=dict(default='Common'),
            policy=dict(required=True),
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
