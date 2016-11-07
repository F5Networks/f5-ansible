#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016 F5 Networks Inc.
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

DOCUMENTATION = '''
---
module: bigip_iapp_template
short_description: Manages TCL iApps on a BIG-IP
description:
  - Manages TCL iApps on a BIG-IP
version_added: "2.3"
options:
  name:
    description:
      - The name of the template being uploaded.
    required: True
  content:
    description:
      - When used instead of 'src', sets the contents of an iRule directly to
        the specified value. This is for simple values, but can be used with
        lookup plugins for anything complex or with formatting. Either one
        of C(src) or C(content) must be provided.
  src:
    description:
      - The iRule file to interpret and upload to the BIG-IP. Either one
        of C(src) or C(content) must be provided.
    required: true
  state:
    description:
      - Whether the iRule should exist or not.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - This module can only create and delete iApp templates at this time. It
    cannot yet update an existing template.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add the iApp contained in template iapp.tmpl
  bigip_iapp_template:
      content: "{{ lookup('template', 'iapp.tmpl') }}"
      name: "my-iapp"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

try:
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


class BigIpiAppTemplateManager(object):
    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = None

    def apply_changes(self):
        result = dict()
        changed = False

        try:
            self.api = self.connect_to_bigip(**self.params)

            if self.params['state'] == "present":
                changed = self.present()
            elif self.params['state'] == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.changed_params)
        result.update(dict(changed=changed))
        return result

    def present(self):
        if self.iapp_template_exists():
            # TODO: Add ability to update existing template
            return True
        else:
            if self.present_parameters_are_valid(self.params):
                return self.ensure_iapp_template_is_present()
            else:
                raise F5ModuleError(
                    "Either 'content' or 'src' must be provided"
                )

    def present_parameters_are_valid(self, params):
        if not params['content'] and not params['src']:
            return False
        else:
            return True

    def absent(self):
        changed = False
        if self.iapp_template_exists():
            changed = self.ensure_iapp_template_is_absent()
        return changed

    def connect_to_bigip(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

    def iapp_template_exists(self):
        return self.api.tm.sys.application.templates.template.exists(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def ensure_iapp_template_is_present(self):
        params = self.get_iapp_template_creation_parameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.create_iapp_template_on_device(params)
        if self.iapp_template_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the iApp template")

    def get_iapp_template_creation_parameters(self):
        result = dict(
            name=self.params['name'],
            partition=self.params['partition']
        )

        if self.params['src']:
            with open(self.params['src']) as f:
                result['template'] = f.read()
        elif self.params['content']:
            result['template'] = self.params['content']

        return result

    def create_iapp_template_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            api.tm.sys.application.templates.template.create(**params)

    def ensure_iapp_template_is_absent(self):
        if self.params['check_mode']:
            return True
        self.delete_iapp_template_from_device()
        if self.iapp_template_exists():
            raise F5ModuleError("Failed to delete the iApp template")
        return True

    def delete_iapp_template_from_device(self):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            tpl = api.tm.sys.application.templates.template.load(
                name=self.params['name'],
                partition=self.params['partition']
            )
            tpl.delete()


class BigIpiAppTemplateModuleConfig(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.states = ['present', 'absent']

        self.initialize_meta_args()
        self.initialize_argument_spec()

    def initialize_meta_args(self):
        args = dict(
            state=dict(
                type='str',
                default='present',
                choices=self.states
            ),
            name=dict(
                type='str',
                required=True
            ),
            content=dict(required=False, default=None),
            src=dict(required=False, default=None),
        )
        self.meta_args = args

    def initialize_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)

    def create(self):
        return AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode,
            mutually_exclusive=[
                ['content', 'src']
            ]
        )


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    config = BigIpiAppTemplateModuleConfig()
    module = config.create()

    try:
        obj = BigIpiAppTemplateManager(
            check_mode=module.check_mode, **module.params
        )
        result = obj.apply_changes()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import camel_dict_to_snake_dict
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
