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
module: iworkflow_tenant
short_description: Manage tenants in iWorkflow.
description:
  - Manage tenants in iWorkflow.
version_added: 2.4
options:
  name:
    description:
      - Name of the tenant that you want to manage.
    required: True
  description:
    description:
      - An optional description for the tenant.
    required: False
    default: None
  contact_address:
    description:
      - An optional contact address associated with the tenant.
    required: False
    default: None
  contact_phone:
    description:
      - An optional contact phone number associated with the tenant.
    required: False
    default: None
  contact_email:
    description:
      - An optional contact email address associated with the tenant.
    required: False
    default: None
  state:
    description:
      - When C(state) is C(present), ensures that the tenant exists. When
        C(state) is C(absent), ensures that the tenant is removed.
    required: False
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Tenants are not useful unless you associate them with a connector
    using the C(iworkflow_tenant_connector) module.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.3.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

RETURN = '''

'''


from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    F5ModuleError,
    HAS_F5SDK,
    iControlUnexpectedHTTPError
)


class Parameters(AnsibleF5Parameters):
    api_map = {
        'addressContact': 'address'
    }
    returnables = []

    api_attributes = [
        'description', 'addressContact', 'phone', 'email'
    ]

    updatables = []

    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
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


class ModuleManager(object):
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
        if changed:
            self.changes = Parameters(changed)
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
        return result

    def exists(self):
        collection = self.client.api.cm.cloud.tenants_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.want.name)
            )
        )
        if len(collection) == 1:
            return True
        elif len(collection) == 0:
            return False
        else:
            raise F5ModuleError(
                "Multiple tenants with the provided name were found!"
            )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def update(self):
        pass

    def read_current_from_device(self):
        collection = self.client.api.cm.cloud.tenants_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.want.name)
            )
        )
        resource = collection.pop()
        result = resource.attrs
        return Parameters(result)

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.cm.cloud.tenants_s.tenant.create(
            name=self.want.name,
            **params
        )
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the tenant")
        return True

    def remove_from_device(self):
        collection = self.client.api.cm.cloud.tenants_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.want.name)
            )
        )
        resource = collection.pop()
        resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(required=True),
            description=dict(type='str'),
            contact_address=dict(type='str'),
            contact_phone=dict(type='str'),
            contact_email=dict(type='str'),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.f5_product_name = 'iworkflow'


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
