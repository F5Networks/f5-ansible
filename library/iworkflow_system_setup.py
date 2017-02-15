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
module: iworkflow_system_setup
short_description: Manage system setup related configuration on iWorkflow
description:
  - Manage system setup related configuration on iWorkflow.
version_added: 2.3
options:
  hostname:
    description:
      - Sets the hostname of the iWorkflow device
    required: True
  management_address:
    description:
      - Management address of the iWorkflow instance.
    required: True
  dns_servers:
    description:
      - List of DNS servers to set on the iWorkflow device for name
        resolution.
    default: None
    required: False
  dns_search_domains:
    description:
      - Default search domain that should be used for DNS queries
    default: None
    required: False
  ntp_servers:
    description:
      - List of NTP servers to set on the iWorkflow device for time
        synchronization.
    default: ['pool.ntp.org']
    required: False
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Required the netaddr Python package on the host. This is as easy as pip
    install netaddr.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 1.5.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Disable iWorkflow setup screen and set accounts as unchanged
  iworkflow_system_setup:
      is_admin_password_changed: "no"
      is_root_password_changed: "no"
      is_system_setup: "yes"
      password: "secret"
      server: "mgmt.mydomain.com"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

import re
from netaddr import IPNetwork

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


class F5ManagementAddress(object):
    _name = 'management_address'

    def __get__(self, instance, owner):
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        try:
            IPNetwork(value)
            instance.__dict__[self._name] = value
        except Exception:
            raise F5ModuleError(
                "The provided management address is not a valid IP address"
            )


class F5Hostname(object):
    _name = 'hostname'

    def __get__(self, instance, owner):
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        search = re.search(r'.*([\w\-]+)\.([\w\-]+).*', value, re.I)
        if search:
            instance.__dict__[self._name] = value
        else:
            raise F5ModuleError(
                "The provided hostname must be an FQDN"
            )


class iWorkflowSystemSetupParams(object):
    hostname = F5Hostname()
    management_address = F5ManagementAddress()
    is_admin_password_changed = None
    is_root_password_changed = None
    is_system_setup = None
    dns_servers = None
    dns_search_domain = None
    ntp_servers = None
    admin_password = None
    root_password = None

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


class iWorkflowSystemSetupModule(AnsibleModule):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(iWorkflowSystemSetupModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )

    def __set__(self, instance, value):
        if isinstance(value, iWorkflowSystemSetupModule):
            instance.params = iWorkflowSystemSetupParams.from_module(self.params)
        else:
            super(iWorkflowSystemSetupModule, self).__set__(instance, value)

    def init_meta_args(self):
        args = dict(
            hostname=dict(
                required=True
            ),
            management_address=dict(
                required=True,
            ),
            dns_servers=dict(
                required=False,
                type='list',
                default=None
            ),
            dns_search_domains=dict(
                required=False,
                type='list',
                default=None
            ),
            ntp_servers=dict(
                required=False,
                type='list',
                default=['pool.ntp.org']
            )
        )
        self.meta_args = args

    def init_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)


class iWorkflowSystemSetupManager(object):
    params = iWorkflowSystemSetupParams()
    current = iWorkflowSystemSetupParams()
    module = iWorkflowSystemSetupModule()

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

        try:
            self.api = connect_to_f5(**self.params.__dict__)
            changed = self.present()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.params.difference(self.current)
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        if not self.is_system_setup():
            return False
        if not self.iworkflow_device_is_discovered():
            return False
        return True

    def is_system_setup(self):
        s = self.api.shared.system.setup.load()
        if not hasattr(s, 'isSystemSetup'):
            return False
        if s.isSystemSetup in BOOLEANS_TRUE:
            return True
        else:
            return False

    def present(self):
        if self.exists():
            return False
        else:
            return self.update_system_setup()

    def update_system_setup(self):
        if self.module.check_mode:
            return True
        params = self.get_easy_setup_params()
        self.update_easy_setup_on_device(params)
        self.update_system_setup_on_device()

        if not self.iworkflow_device_is_discovered():
            self.discover_iworkflow_device()
        return True

    def get_easy_setup_params(self):
        result = dict()
        if self.params.hostname:
            result['hostname'] = self.params.hostname
        if self.params.management_address:
            result['managementIpAddress'] = self.params.management_address
        if self.params.dns_servers:
            result['dnsServerAddresses'] = self.params.dns_servers
        if self.params.dns_search_domain:
            result['dnsSearchDomains'] = self.params.dns_search_domain
        result['ntpServerAddresses'] = self.params.ntp_servers
        return result

    def update_system_setup_on_device(self):
        c = self.api.shared.system.setup.load()
        c.update(
            isSystemSetup=True,
        )
        return True

    def update_easy_setup_on_device(self, params):
        c = self.api.shared.system.easy_setup.load()
        c.modify(**params)
        return True

    def iworkflow_device_is_discovered(self):
        d = self.api.shared.identified_devices.config.discovery.load()
        address = IPNetwork(self.params.management_address)
        if not hasattr(d, 'discoverAddress'):
            return False
        if d.discoveryAddress == str(address.ip):
            return True
        return False

    def discover_iworkflow_device(self):
        d = self.api.shared.identified_devices.config.discovery.load()
        address = IPNetwork(self.params.management_address)
        d.update(
            discoveryAddress=str(address.ip)
        )
        return True


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module = iWorkflowSystemSetupModule()

    try:
        obj = iWorkflowSystemSetupManager()
        obj.module = module
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
