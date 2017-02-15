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
module: iworkflow_local_connector_device
short_description: Manipulate cloud local connector devices in iWorkflow.
description:
  - Manipulate cloud local connector devices in iWorkflow.
version_added: 2.3
options:
  connector:
    description:
      - Name of the local connector to add the device(s) to.
    required: True
  devices:
    description:
      - List of hostname or IP addresses of the devices to associated with the
        connector. This parameter is required when C(state) is C(present)
    required: True
    default: None
    aliases:
      - device
  state:
    description:
      - When C(present), ensures that the cloud connector exists. When
        C(absent), ensures that the cloud connector does not exist.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
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


class iWorkflowBigIpConnectorDeviceParams(object):
    device_refs = None
    devices = None
    name = None

    def difference(self, obj):
        """Compute difference between one object and another

        :param obj:
        Returns:
            Returns a new set with elements in s but not in t (s - t)
        """
        excluded_keys = [
            'password', 'server', 'user', 'server_port', 'validate_certs',
            'device_refs'
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


class iWorkflowBigIpConnectorDeviceModule(AnsibleModule):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(iWorkflowBigIpConnectorDeviceModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )

    def __set__(self, instance, value):
        if isinstance(value, iWorkflowBigIpConnectorDeviceModule):
            instance.params = iWorkflowBigIpConnectorDeviceParams.from_module(
                self.params
            )
        else:
            super(iWorkflowBigIpConnectorDeviceModule, self).__set__(instance, value)

    def init_meta_args(self):
        args = dict(
            connector=dict(
                required=True
            ),
            devices=dict(
                type='list',
                aliases=['device'],
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


class iWorkflowBigIpConnectorDeviceManager(object):
    params = iWorkflowBigIpConnectorDeviceParams()
    current = iWorkflowBigIpConnectorDeviceParams()
    module = iWorkflowBigIpConnectorDeviceModule()

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
        """Checks to see if a device is associated with a connector

        :return:
        """
        connector = self.get_connector_from_connector_name(
            self.params.connector
        )
        if not connector:
            raise F5ModuleError(
                "The specified connector was not found"
            )

        device_refs = self.get_selflinks_from_device_addresses(
            self.params.devices
        )
        if not hasattr(connector, 'deviceReferences'):
            return False

        for reference in connector.deviceReferences:
            if str(reference['link']) in device_refs:
                return True
        return False

    def present(self):
        if self.exists():
            return False
        else:
            return self.create_connector_device()

    def create_connector_device(self):
        if self.module.check_mode:
            return True
        self.create_connector_device_on_device()
        return True

    def get_connector_from_connector_name(self, name):
        connector = None
        connectors = self.api.cm.cloud.connectors.locals.get_collection()
        for connector in connectors:
            if connector.displayName != "BIG-IP":
                continue
            if connector.name != name:
                continue
            break
        return connector

    def create_connector_device_on_device(self):
        device_refs = self.get_selflinks_from_device_addresses(
            self.params.devices
        )
        devices = [dict(link=link) for link in device_refs]
        connector = self.get_connector_from_connector_name(
            self.params.connector
        )
        connector.update(deviceReferences=devices)
        return True

    def get_selflinks_from_device_addresses(self, addrs):
        links = []
        dg = self.api.shared.resolver.device_groups
        for addr in addrs:
            devices = dg.cm_cloud_managed_devices.devices_s.get_collection(
                requests_params=dict(
                    params="$filter=hostname+eq+'{0}'+or+address+eq+'{0}'".format(addr)
                )
            )
            device = devices.pop()
            links.append(device.selfLink)
        return links

    def absent(self):
        if self.exists():
            return self.remove_connector_device()
        return False

    def remove_connector_device(self):
        if self.module.check_mode:
            return True
        self.remove_connector_device_from_device()
        if self.exists():
            raise F5ModuleError(
                "Failed to remove the device from the connector"
            )
        return True

    def remove_connector_device_from_device(self):
        connector = self.get_connector_from_connector_name(
            self.params.connector
        )
        current = [x['link'] for x in connector.deviceReferences]
        remove = self.get_selflinks_from_device_addresses(
            self.params.devices
        )
        result = set(current) - set(remove)
        devices = [dict(link=link) for link in result]
        connector.update(deviceReferences=devices)
        return True


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module = iWorkflowBigIpConnectorDeviceModule()

    try:
        obj = iWorkflowBigIpConnectorDeviceManager()
        obj.module = module
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
