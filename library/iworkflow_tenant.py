#!/usr/bin/python
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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
module: iworkflow_tenant
short_description: Manage tenants in iWorkflow.
description:
  - Manage tenants in iWorkflow.
version_added: 2.3
options:
  name:
    description:
      - Name of the tenant that you want to create in iWorkflow.
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
      - Whether the managed device should exist, or not, in iWorkflow.
    required: false
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
    - f5-sdk >= 2.2.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

import time

try:
    from f5.iworkflow import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *


def connect_to_f5(**kwargs):
    return ManagementRoot(kwargs['server'],
                          kwargs['user'],
                          kwargs['password'],
                          port=kwargs['server_port'],
                          token='local')


class iWorkflowTenantParams(object):
    device = None
    description = None
    address = None
    phone = None
    email = None

    def difference(self, obj):
        """Compute difference between one object and another

        :param obj:
        Returns:
            Returns a new set with elements in s but not in t (s - t)
        """
        excluded_keys = [
            'password', 'server', 'user', 'server_port', 'validate_certs'
        ]
        return self._difference(self, obj, excluded_keys)

    def _difference(self, obj1, obj2, excluded_keys):
        """

        Code take from https://www.djangosnippets.org/snippets/2281/

        :param obj1:
        :param obj2:
        :param excluded_keys:
        :return:
        """
        d1, d2 = obj1.__dict__, obj2.__dict__
        new = {}
        for k,v in d1.items():
            if k in excluded_keys:
                continue
            try:
                if v != d2[k]:
                    new.update({k: d2[k]})
            except KeyError:
                new.update({k: v})
        return new

    @classmethod
    def from_module(cls, module):
        """Create instance from dictionary of Ansible Module params

        This method accepts a dictionary that is in the form supplied by
        the

        Args:
             module: An AnsibleModule object's `params` attribute.

        Returns:
            A new instance of iWorkflowSystemSetupParams. The attributes
            of this object are set according to the param data that is
            supplied by the user.
        """
        result = cls()
        for key in module:
            setattr(result, key, module[key])
        return result


class iWorkflowTenantModule(AnsibleModule):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(iWorkflowTenantModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )

    def __set__(self, instance, value):
        if isinstance(value, iWorkflowTenantModule):
            instance.params = iWorkflowTenantParams.from_module(
                self.params
            )
        else:
            super(iWorkflowTenantModule, self).__set__(instance, value)

    def init_meta_args(self):
        args = dict(
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
        self.meta_args = args

    def init_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)


class iWorkflowTenantManager(object):
    params = iWorkflowTenantParams()
    current = iWorkflowTenantParams()
    module = iWorkflowTenantModule()

    def __init__(self):
        self.api = None
        self.changes = None
        self.config = None

    def apply_changes(self):
        """Apply the user's changes to the device

        This method is the primary entry-point to this module. Based on the
        parameters supplied by the user to the class, this method will
        determine which `state` needs to be fulfilled and delegate the work
        to more specialized helper methods.

        Additionally, this method will return the result of applying the
        changes so that Ansible can communicate this result to the user.

        Raises:
            F5ModuleError: An error occurred communicating with the device
        """
        result = dict()
        state = self.params.state

        try:
            self.api = connect_to_f5(**self.params.__dict__)
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.params.difference(self.current)
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        tenants = self.api.cm.cloud.tenants_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.params.name)
            )
        )

        if len(tenants) == 1:
            return True
        elif len(tenants) == 0:
            return False
        else:
            raise F5ModuleError(
                "Multiple tenants with the provided name were found!"
            )

    def present(self):
        if self.exists():
            return self.update_tenant()
        else:
            return self.create_tenant()

    def create_tenant(self):
        if self.module.check_mode:
            return True
        self.create_tenant_on_device()
        return True

    def update_tenant(self):
        pass

    def read_current(self):
        tenants = self.api.cm.cloud.tenants_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.params.name)
            )
        )
        tenant = tenants.pop()

        current = iWorkflowTenantParams()

        if hasattr('description', tenant):
            current.description = str(tenant.description)
        if hasattr('addressContact', tenant):
            current.address = str(tenant.addressContact)
        if hasattr('phone', tenant):
            current.phone = str(tenant.phone)
        if hasattr('email', tenant):
            current.email = str(tenant.email)

        self.current = current
        return self.current

    def create_tenant_on_device(self):
        self.api.cm.cloud.tenants_s.tenant.create(
            name=self.params.name,
            description=self.params.description,
            addressContact=self.params.address,
            phone=self.params.phone,
            email=self.params.email
        )
        return True

    def absent(self):
        if self.exists():
            return self.remove_tenant()
        return False

    def remove_tenant(self):
        if self.module.check_mode:
            return True
        self.remove_tenant_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the tenant")
        return True

    def remove_tenant_from_device(self):
        tenants = self.api.cm.cloud.tenants_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.params.name)
            )
        )
        tenant = tenants.pop()
        tenant.delete()


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module = iWorkflowTenantModule()

    try:
        obj = iWorkflowTenantManager()
        obj.module = module
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
