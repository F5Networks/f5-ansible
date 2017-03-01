#!/usr/bin/python
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
module: iworkflow_license_pool
short_description: Manage license pools in iWorkflow.
description:
  - Manage license pools in iWorkflow.
version_added: 2.3
options:
  name:
    description:
      - Name of the license pool to create
    required: true
  state:
    description:
      - Whether the license pool should exist, or not. A state of C(present)
        will attempt to activate the license pool if C(accept_eula) is set
        to C(yes).
    required: false
    default: present
    choices:
      - present
      - absent
  base_key:
    description:
      - Key that the license server uses to verify the functionality that
        you are entitled to license.
  accept_eula:
    description:
      - Specifies that you accept the EULA that is part of iWorkflow. Note
        that this is required to activate the license pool. If this is not
        specified, or it is set to C(no), then the pool will remain in a state
        of limbo until you specify to accept the EULA.
    required: true
    choices:
      - yes
      - no
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 1.5.0
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
from ansible.module_utils.f5_utils import *


def connect_to_f5(**kwargs):
    return ManagementRoot(kwargs['server'],
                          kwargs['user'],
                          kwargs['password'],
                          port=kwargs['server_port'],
                          token='local')


class iWorkflowLicensePoolParams(object):
    name = None
    base_key = None
    state = None
    license_text = None
    total_device_licenses = None
    free_device_licenses = None

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


class iWorkflowLicensePoolModule(AnsibleModule):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(iWorkflowLicensePoolModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )

    def __set__(self, instance, value):
        if isinstance(value, iWorkflowLicensePoolModule):
            instance.params = iWorkflowLicensePoolParams.from_module(self.params)
        else:
            super(iWorkflowLicensePoolModule, self).__set__(instance, value)

    def init_meta_args(self):
        args = dict(
            accept_eula=dict(
                type='bool',
                default=None,
                choices=BOOLEANS
            ),
            base_key=dict(
                required=False
            ),
            name=dict(
                required=True
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


class iWorkflowLicensePoolManager(object):
    params = iWorkflowLicensePoolParams()
    current = iWorkflowLicensePoolParams()
    module = iWorkflowLicensePoolModule()

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
        pools = self.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.params.name)
            )
        )
        if len(pools) == 1:
            return True
        elif len(pools) == 0:
            return False
        else:
            raise F5ModuleError(
                "Multiple license pools with the provided name were found!"
            )

    def present(self):
        if self.exists():
            return self.update_license_pool()
        else:
            return self.create_license_pool()

    def pool_is_licensed(self, current):
        if current.state == 'LICENSED':
            return True
        return False

    def pool_is_unlicensed_eula_unaccepted(self, current):
        if current.state != 'LICENSED' and not self.params.accept_eula:
            return True
        return False

    def update_license_pool(self):
        current = self.read_current()
        if self.pool_is_licensed(current):
            return False
        if self.pool_is_unlicensed_eula_unaccepted(current):
            raise F5ModuleError(
                "You must accept the license EULA with the accept_eula parameter"
            )
        if self.module.check_mode:
            return True
        self.reactivate_license_pool_on_device()
        return True

    def reactivate_license_pool_on_device(self):
        pools = self.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.params.name)
            )
        )
        pool = pools.pop()
        pool.modify(
            state='RELICENSE',
            method='AUTOMATIC'
        )
        return self.wait_for_license_pool_state_to_activate(pool)

    def create_license_pool(self):
        if self.module.check_mode:
            return True
        if self.params.base_key is None:
            raise F5ModuleError(
                "You must specify a 'base_key' when creating a license pool"
            )
        if self.params.accept_eula in BOOLEANS_FALSE:
            raise F5ModuleError(
                "You must accept the EULA before creating a license pool."
            )
        self.create_license_pool_on_device()
        return True

    def read_current(self):
        pools = self.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.params.name)
            )
        )
        pool = pools.pop()

        current = iWorkflowLicensePoolParams()
        current.name = str(pool.name)
        if hasattr(pool, 'baseRegKey'):
            current.base_key = str(pool.baseRegKey)
        if hasattr(pool, 'state'):
            current.state = str(pool.state)
        if hasattr(pool, 'licenseText'):
            current.license_text = str(pool.licenseText)
        if hasattr(pool, 'totalDeviceLicenses'):
            current.total_device_licenses = str(pool.totalDeviceLicenses)
        if hasattr(pool, 'freeDeviceLicenses'):
            current.free_device_licenses = str(pool.freeDeviceLicenses)
        self.current = current
        return self.current

    def create_license_pool_on_device(self):
        if self.params.base_key is None:
            raise F5ModuleError(
                "You must accept the EULA with the 'accept_eula' option "
                "when creating a new license pool."
            )
        pool = self.api.cm.shared.licensing.pools_s.pool.create(
            name=self.params.name,
            baseRegKey=self.params.base_key,
            method="AUTOMATIC"
        )
        return self.wait_for_license_pool_state_to_activate(pool)

    def wait_for_license_pool_state_to_activate(self, pool):
        error_values = ['EXPIRED', 'FAILED']
        # Wait no more than 5 minutes
        for x in range(1, 30):
            pool.refresh()
            if pool.state == 'LICENSED':
                return True
            elif pool.state == 'WAITING_FOR_EULA_ACCEPTANCE':
                pool.modify(
                    eulaText=pool.eulaText,
                    state='ACCEPTED_EULA'
                )
            elif pool.state in error_values:
                raise F5ModuleError(pool.errorText)
            time.sleep(10)

    def absent(self):
        if self.exists():
            return self.remove_license_pool()
        return False

    def remove_license_pool(self):
        if self.module.check_mode:
            return True
        self.remove_license_pool_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the license pool")
        return True

    def remove_license_pool_from_device(self):
        pools = self.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.params.name)
            )
        )
        pool = pools.pop()
        pool.delete()


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module = iWorkflowLicensePoolModule()

    try:
        obj = iWorkflowLicensePoolManager()
        obj.module = module
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
