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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: bigip_iapp_service
short_description: Manages TCL iApp services on a BIG-IP.
description:
  - Manages TCL iApp services on a BIG-IP.
version_added: "2.4"
options:
  name:
    description:
      - The name of the iApp service that you want to deploy.
    required: True
  template:
    description:
      - The iApp template from which to instantiate a new service. This
        template must exist on your BIG-IP before you can successfully
        create a service. This parameter is required if the C(state)
        parameter is C(present).
    required: False
    default: None
  parameters:
    description:
      - A hash of all the required template variables for the iApp template.
        This parameter is mutually exclusive with C(parameters_src). Either
        one of them is required if C(state) parameter is C(present).
    required: False
    default: None
  parameters_src:
    description:
      - Path of file containing the parameters body. This parameter is mutually
        exclusive with C(parameters). Either one of them is required if
        C(state) is C(present).
    required: False
    default: None
  state:
    description:
      - When C(present), ensures that the iApp service is created and running.
        When C(absent), ensures that the iApp service has been removed.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

import json

try:
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *


_CONNECTION = None


def setup_connection(**kwargs):
    global _CONNECTION
    _CONNECTION = ManagementRoot(
        kwargs['server'],
        kwargs['user'],
        kwargs['password'],
        port=kwargs['server_port'],
        token='tmos'
    )


def _get_connection():
    if _CONNECTION is None:
        setup_connection()
    return _CONNECTION


class F5AnsibleModule(AnsibleModule):
    def __init__(self):
        self.params = None
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(F5AnsibleModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode,
            mutually_exclusive=[
                ['parameters', 'parameters_src']
            ]
        )

    def init_meta_args(self):
        args = dict(
            name=dict(required=True),
            template=dict(
                required=False,
                default=None
            ),
            parameters=dict(
                required=False,
                default=None,
                type='dict'
            ),
            parameters_src=dict(
                required=False,
                default=None,
                type='path'
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.meta_args = args

    def init_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)


class ModuleManager(object):
    have = dict()
    want = dict()

    def __init__(self, *args, **kwargs):
        self.changes = dict()
        self.module = kwargs['module']

    def apply_changes(self):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.want = self.format_params(self.module.params)

        changed = False
        result = dict()
        state = self.want.get('state')

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.changes)
        result.update(dict(changed=changed))
        result = self.map_to_return_keys(result)
        return result

    def exists(self):
        api = _get_connection()
        return api.tm.sys.application.services.service.exists(
            name=self.want.name
        )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):
        if self.module.check_mode:
            return True
        self.update_changed_params()
        self.create_on_device(self.changes)
        return True

    def update(self):
        current = self.read_current_from_device()
        self.have = self.format_params(current)
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device(self.changes)
        return True

    def should_update(self):
        self.update_changed_params()
        if len(self.changes.keys()) > 2:
            return True
        return False

    def update_changed_params(self):
        result = dict(
            name=str(self.want['name']),
            partition=str(self.want['partition']),
        )
        self.update_attribute(result, 'mtu')
        self.changes = result

    def update_attribute(self, result, attribute, validator=None):
        want = self.want.get(attribute, None)
        have = self.have.get(attribute, None)
        if want != have and want is not None:
            result[attribute] = want
        if validator is None:
            return
        validator(want)

    def update_on_device(self, params):
        api = _get_connection()
        route = api.tm.sys.application.services.service.load(
            name=self.want.name
        )
        route.update(**params)

    def read_current_from_device(self):
        api = _get_connection()
        result = api.tm.sys.application.services.service.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if not result:
            return dict()
        current = result.to_dict()
        current.pop('_meta_data')
        return current

    def create_on_device(self, params):
        api = _get_connection()
        api.tm.sys.application.services.service.create(**params)

    def absent(self, ):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the iApp service")
        return True

    def remove_from_device():
        api = _get_connection()
        route = api.tm.sys.application.services.service.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if route:
            route.delete()


def main():
    module = F5AnsibleModule()
    setup_connection(**module.params)

    try:
        obj = ModuleManager(module=module)
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
