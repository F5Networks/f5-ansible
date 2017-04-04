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
module: iworkflow_local_connector_node
short_description: Manages L2/L3 configuration of a BIG-IP via iWorkflow.
description:
  - Manages L2/L3 configuration of a BIG-IP via iWorkflow. This module is
    useful in the event that you have a new BIG-IP that does not yet have
    VLANs and Self-IPs configured on it. You can use this module on a
    discovered, managed, device to configure those settings via iWorkflow.
    You B(do not) need touse this module if you have an existing BIG-IP
    that has its L2/L3 configuration already complete. In that cae, it is
    sufficient to just use the C(iworkflow_managed_device) module and
    iWorkflow will automatically discover the node information for you.
version_added: 2.3
options:
  connector:
    description:
      - Name of the local connector to add the device(s) to.
    required: True
  devices:
    description:
      - List of hostname or IP addresses of the devices to associate with the
        connector. This parameter is required when C(state) is C(present).
    required: True
    default: None
    aliases:
      - device
  key_content:
    description:
      - Private key content to use when iWorkflow attempts to communicate with
        the remote device. If your remote BIG-IP requires key based authentication
        (for example it is located in a public cloud), you can provide that
        value here. Either one of C(key_src), C(key_content), or
        C(username_credential) must be provided.
    required: False
    default: None
  key_src:
    description:
      - Private key to use when iWorkflow attempts to communicate with the
        remote device. If your remote BIG-IP requires key based authentication
        (for example it is located in a public cloud), you can provide that
        value here. Either one of C(key_src), C(key_content), or
        C(username_credential) must be provided.
    required: False
    default: None
  username_credential:
    description:
      - Username that you wish to connect to the remote BIG-IP with over
        SSH. This parameter is required when C(state) is C(present).
    required: True
  password_credential:
    description:
      - Password of the user that you wish to connect to the remote BIG-IP
        with over SSH. The C(password_credential) and C(private_key) parameters
        are mutually exclusive. You may use one or the other.
    required: False
    default: None
  host:
    description:
      - The hostname or IP address of the remote BIG-IP that is to be
        configured.
    required: True
    aliases:
      - address
      - ip
  interfaces:
    description:
      - A list of network interface configuration details that iWorkflow
        should apply to the remote BIG-IP. This list should include the
        following keys; C(local_address), C(subnet_address). Also, optionally,
        the following keys can be provided C(gateway_address), C(name).
        The first item in the list is B(always) the management interface
        of the BIG-IP. All remaining items in the list apply to the interfaces
        in ascending order that they appear on the device (eth1, eth2, etc).
        This parameter is only required when C(state) is C(present).
    required: False
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
  - Requires the netaddr Python package on the host. This is as easy as pip
    install netaddr.
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

import os
from netaddr import IPAddress, AddrFormatError

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


class F5PrivateKeyContent(object):
    _name = 'key_content'

    def __get__(self, instance, owner):
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value


class F5PrivateKeySource(object):
    _name = 'key_src'

    def __get__(self, instance, owner):
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        if not value:
            return
        if os.path.exists(value):
            instance.__dict__[self._name] = value
        else:
            raise F5ModuleError(
                "The specified key doesnt not exist"
            )
        with open(value, 'r') as fh:
            instance.key_content = fh.read()


class iWorkflowBigIpConnectorNodeParams(object):
    device_ref = None
    device = None
    name = None
    username_credential = None
    password_credential = None
    key_src = F5PrivateKeySource()
    key_content = F5PrivateKeyContent()
    host = None
    interfaces = None

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


class iWorkflowBigIpConnectorNodeModule(AnsibleModule):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(iWorkflowBigIpConnectorNodeModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode,
            mutually_exclusive=[
                ['key_src', 'password_credential'],
                ['key_content', 'password_credential'],
                ['key_src', 'key_content']
            ],
            required_if=[
                ['state', 'present', ['interfaces']]
            ]
        )

    def __set__(self, instance, value):
        if isinstance(value, iWorkflowBigIpConnectorNodeModule):
            instance.params = iWorkflowBigIpConnectorNodeParams.from_module(
                self.params
            )
        else:
            super(iWorkflowBigIpConnectorNodeModule, self).__set__(instance, value)

    def init_meta_args(self):
        args = dict(
            connector=dict(
                required=True
            ),
            device=dict(
                required=True
            ),
            key_content=dict(
                type='str',
                required=False,
                default=None
            ),
            key_src=dict(
                type='str',
                required=False,
                default=None
            ),
            username_credential=dict(
                required=False,
                default=None
            ),
            password_credential=dict(
                required=False,
                default=None
            ),
            host=dict(
                required=True
            ),
            interfaces=dict(
                type='list',
                required=False,
                default=None
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


class iWorkflowBigIpConnectorNodeManager(object):
    params = iWorkflowBigIpConnectorNodeParams()
    current = iWorkflowBigIpConnectorNodeParams()
    module = iWorkflowBigIpConnectorNodeModule()

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
        connector = self.connector_exists()

        device_refs = self.get_selflinks_from_device_addresses(
            self.params.devices
        )
        if not hasattr(connector, 'deviceReferences'):
            return False

        for reference in connector.deviceReferences:
            if str(reference['link']) in device_refs:
                return True
        return False

    def connector_exists(self):
        connector = self.get_connector_from_connector_name(
            self.params.connector
        )
        if not connector:
            raise F5ModuleError(
                "The specified connector was not found"
            )
        return connector

    def present(self):
        if self.exists():
            return False
        else:
            return self.create_connector_node()

    def create_connector_node(self):
        if self.module.check_mode:
            return True
        self.create_connector_node_on_device()
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

    def create_connector_node_on_device(self):
        params = self.get_connector_node_params()
        return True

    def get_connector_node_params(self):
        result = dict(
            state='RUNNING',
            properties=[
                dict(
                    id="BIG-IP-PROVISIONABLE",
                    provider="true"
                ),
                dict(
                    id='BIG-IP',
                    provider="true"
                ),
                dict(
                    id='ToBeConfiguredByiWorkflow',
                    value="true"
                ),
                dict(
                    id='DeviceHostname',
                    provider=self.params.host
                ),
                dict(
                    id='DeviceLeaveRootLoginEnabled',
                    provider="false"
                )
            ],
            ipAddress=self.params.device,
            cloudNodeID=self.params.device,
            networkInterfaces=self.params.interfaces,
            isBIGIP=True
        )
        if self.params.username_credential == 'admin':
            result['properties'].append(dict(
                id='BIG-IP-WITH-ADMIN-SSH',
                provider="true"
            ))
            if self.params.password_credential == 'admin':
                result['properties'].append(dict(
                    id='DeviceCreatedWithDefaultCredentials',
                    provider="true"
                ))
            else:
                result['properties'].append(dict(
                    id='DeviceCreatedWithDefaultCredentials',
                    provider="false"
                ))
        elif self.params.username_credential == 'root':
            result['properties'].append(dict(
                id='BIG-IP-WITH-ADMIN-SSH',
                provider="false"
            ))
            if self.params.password_credential == 'default':
                result['properties'].append(dict(
                    id='DeviceCreatedWithDefaultCredentials',
                    provider="true"
                ))
            else:
                result['properties'].append(dict(
                    id='DeviceCreatedWithDefaultCredentials',
                    provider="false"
                ))
        else:
            result['properties'].append(dict(
                id='BIG-IP-WITH-ADMIN-SSH',
                provider="false"
            ))
            result['properties'].append(dict(
                id='DeviceCreatedWithDefaultCredentials',
                provider="false"
            ))

        if self.params.key_content:
            result['properties'].append(dict(
                id='KeyPrivate',
                value=self.params.key_content
            ))
        if self.params.username_credential:
            result['properties'].append(dict(
                id='DeviceMgmtUser',
                provider=self.params.username_credential
            ))
        if self.params.password_credential:
            result['properties'].append(dict(
                id='DeviceMgmtPassword',
                provider=self.params.password_credential
            ))
        return result

    def get_selflinks_from_device_addresses(self, addrs):
        links = []
        dg = self.api.shared.resolver.device_groups
        for addr in addrs:
            try:
                IPAddress(addr)
                params = dict(
                    params="$filter=address+eq+'{0}'".format(addr)
                )
            except AddrFormatError:
                params = dict(
                    params="$filter=hostname+eq+'{0}'".format(addr)
                )
            devices = dg.cm_cloud_managed_devices.devices_s.get_collection(
                requests_params=dict(**params)
            )
            device = devices.pop()
            links.append(device.selfLink)
        return links

    def absent(self):
        if self.exists():
            return self.remove_connector_node()
        return False

    def remove_connector_node(self):
        if self.module.check_mode:
            return True
        self.remove_connector_node_from_device()
        if self.exists():
            raise F5ModuleError(
                "Failed to remove the device from the connector"
            )
        return True

    def remove_connector_node_from_device(self):
        connector = self.get_connector_from_connector_name(
            self.params.connector
        )
        return True


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module = iWorkflowBigIpConnectorNodeModule()

    try:
        obj = iWorkflowBigIpConnectorNodeManager()
        obj.module = module
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
