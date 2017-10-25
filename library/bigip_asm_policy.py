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
module: bigip_asm_policy
short_description: Manage BIG-IP ASM policies
description:
   - Manage BIG-IP ASM policies
version_added: "2.5"
options:
  active:
    description:
      - If C(yes) will apply and activate existing inactive policy. If C(no), it will
        deactivate existing active policy. Generally should be C(yes) only in cases where
        you want to activate new or existing policy.
    default: no
    choices:
      - yes
      - no
  name:
    description:
      - The ASM policy to manage or create.
    required: True
  state:
    description:
      - When C(state) is C(present), and C(file) or C(template) parameter is provided,
        new ASM policy is imported and created with the given C(name).
      - When C(state) is present and no C(file) or C(template) parameter is provided 
        new blank ASM policy is created with the given C(name).
      - When C(state) is C(absent), ensures that the policy is removed, even if it is
        currently active.
    choices:
      - present
      - absent
  file:
    description:
      - Full path to a policy file to be imported into the BIG-IP ASM.
  template:
    description:
     - An ASM policy built-in template. If the template does not exist we will raise an error.
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
  - Wojciech Wypior (@wojtek0806)
'''

EXAMPLES = r'''
- name: Import and activate ASM policy
  bigip_asm_policy:
    server: bigip.localhost.localdomain
    user: admin
    password: admin
    name: new_asm_policy
    file: /root/asm_policy.xml
    active: yes
    state: present
  delegate_to: localhost

- name: Import ASM policy from template
  bigip_asm_policy:
    server: bigip.localhost.localdomain
    user: admin
    password: admin
    name: new_sharepoint_policy
    template: POLICY_TEMPLATE_SHAREPOINT_2007_HTTP
    state: present
  delegate_to: localhost

- name: Create blank ASM policy
  bigip_asm_policy:
    server: bigip.localhost.localdomain
    user: admin
    password: admin
    name: new_blank_policy
    state: present
  delegate_to: localhost
  
- name: Create blank ASM policy and activate
  bigip_asm_policy:
    server: bigip.localhost.localdomain
    user: admin
    password: admin
    name: new_blank_policy
    active: yes
    state: present
  delegate_to: localhost

- name: Activate ASM policy
  bigip_asm_policy:
    server: bigip.localhost.localdomain
    user: admin
    password: admin
    name: inactive_policy
    active: yes
    state: present
  delegate_to: localhost

- name: Deactivate ASM policy
  bigip_asm_policy:
    server: bigip.localhost.localdomain
    user: admin
    password: admin
    name: active_policy
    state: present
  delegate_to: localhost
'''

RETURN = r'''
active:
  description: Set when activating/deactivating ASM policy
  returned: changed
  type: bool
  sample: yes
state:
  description: Action performed on the target device.
  returned: changed
  type: string
  sample: absent
file:
  description: Local path to ASM policy XML file.
  returned: changed
  type: string
  sample: /root/some_policy.xml
template:
  description: Name of the built-in ASM policy template
  returned: changed
  type: string
  sample: POLICY_TEMPLATE_SHAREPOINT_2007_HTTP
name:
  description: Name of the ASM policy to be managed/created
  returned: changed
  type: string
  sample: Asm_APP1_Transparent
'''

import os
import time
from icontrol.exceptions import iControlUnexpectedHTTPError
from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError
from ansible.module_utils.six import iteritems
from collections import defaultdict

try:
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        if params:
            self.update(params=params)

    def update(self, params=None):
        if params:
            for k, v in iteritems(params):
                if self.api_map is not None and k in self.api_map:
                    map_key = self.api_map[k]
                else:
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have
                        # an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    updatables = [
        'active'
    ]

    returnables = [
        'name', 'template', 'file', 'active'
    ]

    api_attributes = [
        'name', 'file'
    ]
    api_map = {
        'filename': 'file'
    }

    @property
    def template(self):
        if self._values['template'] is None:
            return None
        return self._values['template']

    @property
    def template_link(self):
        if self._values['template_link'] is not None:
            return self._values['template_link']
        collection = self._templates_from_device()
        for resource in collection:
            if resource.name == self.template.upper():
                return dict(link=resource.selfLink)
        return None

    def _templates_from_device(self):
        collection = self.client.api.tm.asm.policy_templates_s.get_collection()
        return collection

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


class Changes(Parameters):
    pass


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)
        self.changes = Changes()

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

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Changes(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = attr1
        if changed:
            self.changes = Changes(changed)
            return True
        return False

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def absent(self):
        if not self.exists():
            return False
        else:
            return self.remove()

    def exists(self):
        policies = self.client.api.tm.asm.policies_s.get_collection()
        if any(p.name == self.want.name for p in policies):
            return True
        return False

    def create(self):
        task = None
        self._set_changed_options()
        if self.client.check_mode:
            return True
        if self.want.template is None and self.want.path is None:
            self.create_blank()
            return True
        if self.want.template is not None:
            task = self.create_policy_from_template_on_device()
        if self.want.path is not None:
            task = self.import_to_device()

        if not task:
            return False
        if not self.wait_for_task(task):
            raise F5ModuleError('Import policy task failed.')

        if self.want.active:
            self.activate()
            return True
        else:
            return True

    def update(self):
        self.have = Parameters(policy.attrs)
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        if self.update_on_device():
            return True
        else:
            return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update_on_device(self):
        if self.want.active:
            if self.is_activated():
                return False
            else:
                if self.client.check_mode:
                    return True
                self.activate()
                return True
        else:
            if not self.is_activated():
                return False
            if self.client.check_mode:
                return True
            self.deactivate()
            return True

    def create_blank(self):
        self.create_on_device()
        if self.policy_exists_on_device():
            return True
        else:
            raise F5ModuleError(
                'Failed to create ASM policy: {0}'.format(self.want.name)
            )

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError(
                'Failed to delete ASM policy: {0}'.format(self.want.name)
            )
        return True

    def activate(self):
        task = self.apply_on_device()
        if self.wait_for_task(task):
            return True
        else:
            raise F5ModuleError('Apply policy task failed.')

    def deactivate(self):
        result = self.deactivate_on_device()
        if result:
            return True
        else:
            raise F5ModuleError('Policy deactivation failed.')

    def wait_for_task(self, task):
        while True:
            task.refresh()
            if task.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        if task.status == 'FAILURE':
            return False
        if task.status == 'COMPLETED':
            return True

    def is_activated(self):
        result = self.policy_active()
        if self.client.check_mode:
            return True
        return result

    def policy_active(self):
        if self.want.policy.active is True:
            return True
        else:
            return False

    def read_current_from_device(self):
        policies = self.client.api.tm.asm.policies_s.get_collection()
        for policy in policies:
            if policy.name == self.want.name:
                return Parameters(policy.attrs)

    def import_to_device(self):
        self.client.api.tm.asm.file_transfer.uploads.upload_file(self.want.file)
        time.sleep(2)
        name = os.path.split(self.want.file)[1]
        tasks = self.client.api.tm.asm.tasks
        result = tasks.import_policy_s.import_policy.create(
            name=self.want.name, filename=name
        )
        return result

    def apply_on_device(self):
        policy = self.read_current_from_device()
        tasks = self.client.api.tm.asm.tasks
        result = tasks.apply_policy_s.apply_policy.create(
            policyReference={'link': policy.selflink}
        )
        return result

    def deactivate_on_device(self):
        policy = self.read_current_from_device()
        policy.modify(active=False)
        if policy.active is False:
            return True
        else:
            return False

    def create_policy_from_template_on_device(self):
        result = self.client.api.tm.asm.tasks.import_policy_s.import_policy.create(
            name=self.want.name,
            policyTemplateReference=self.want.template_link
        )
        return result

    def create_on_device(self):
        result = self.client.api.tm.asm.policies_s.policy.create(name=self.want.name)
        return result

    def remove_from_device(self):
        policies = self.client.api.tm.asm.policies_s.get_collection()
        resource = next((p for p in policies if p.name == self.want.name), None)
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(
                required=True,
            ),
            file=dict(),
            template=dict(),
            active=dict(
                default='no',
                type='bool'
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
        f5_product_name=spec.f5_product_name,
        mutually_exclusive=[
            ['file', 'template']
        ]
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
