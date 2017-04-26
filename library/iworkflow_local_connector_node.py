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
  device:
    description:
      - Managed device to create node for.
    required: True
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
      - Username used to the remote BIG-IP with over its web API. This
        parameter is required when C(state) is C(present).
    required: False
  password_credential:
    description:
      - Password of the user that you wish to connect to the remote BIG-IP
        with over SSH. The C(password_credential) and C(private_key) parameters
        are mutually exclusive. You may use one or the other.
    required: False
    default: None
  device_root_password:
    description:
      - If the C(username_credential) is C(root) but the C(password_credential)
        is not the password of the root user, then this value should be provided.
        This parameter is only relevant when creating new nodes.
    required: False
    default: None
  hostname:
    description:
      - The hostname that you want to set on the remote managed BIG-IP.
    required: False
    default: None
  interfaces:
    description:
      - A list of network interface configuration details that iWorkflow
        should apply to the remote BIG-IP. This list must include the
        following keys; C(local_address), C(subnet_address). Also, optionally,
        the following keys can be provided C(gateway_address), C(name).
        One final key, C(virtual_address), can be provided in the event that
        the cloud provider you are configuring the device on sets a public
        IP address that forwards traffic to a NAT'd private address.
        C(virtual_address) can be used in cases such as Azure public IPs,
        AWS Elastic IP paired with an ENI primary address, and OpenStack's
        Floating IP. The first item in the list is B(always) the
        management interface of the BIG-IP. All remaining items in the list
        apply to the interfaces in ascending order that they appear on the
        device (eth1, eth2, etc). This parameter is only required when
        C(state) is C(present).
    required: False
    default: None
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
  - This module does not support updating of existing nodes that were created
    with a C(cli_password_credential). The onboarding process will change your
    device's C(cli_username_credential) password, which will prevent you from
    using this module (without knowing the password) a second time.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.2.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Create node from managed device
  iworkflow_local_connector_node:
      device: "10.144.128.137"
      password_credential: "secret"
      username_credential: "admin"
      state: "present"
      connector: "Private OpenStack"
      hostname: "lb1.example.com"
      interfaces:
          - local_address: "10.144.128.137"
            subnet_address: "10.144.128/24"
          - local_address: "10.2.0.81"
            subnet_address: "10.2.0.0/24"
            name: "internal"
      server: "iwf.mydomain.com"
      password: "secret"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost

- name: Create node from managed device in Azure
  iworkflow_local_connector_node:
      device: "10.144.128.137"
      password_credential: "secret"
      username_credential: "admin"
      device_root_password: "default"
      state: "present"
      connector: "Public Azure West US"
      hostname: "lb1.example.com"
      interfaces:
          - local_address: "10.0.2.12"
            subnet_address: "10.0.2.0/24"
            virtual_address: "10.144.128.137"
          - local_address: "10.2.0.81"
            subnet_address: "10.2.0.0/24"
            name: "external"
      server: "iwf.mydomain.com"
      password: "secret"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost
'''

RETURN = '''

'''

import re
import netaddr
import time

from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    F5ModuleError,
    HAS_F5SDK,
    defaultdict,
    iteritems,
    iControlUnexpectedHTTPError
)


class Device(object):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        self._values = defaultdict(lambda: None)

    def update(self, params=None):
        params = str(params)
        resource = None
        collection = self._get_device_collection()
        if re.search(r'([0-9-a-z]+\-){4}[0-9-a-z]+', params, re.I):
            # Handle cases where the REST API sent us self links
            for device in collection:
                if str(device.product) != "BIG-IP":
                    continue
                if str(device.selfLink) != params:
                    continue
                resource = device
                break
        else:
            # Handle the case where a user sends us a list of connector names
            for device in collection:
                if str(device.product) != "BIG-IP":
                    continue

                # The supplied device can be in several formats.
                if str(device.hostname) == params:
                    # Hostname
                    #
                    # The hostname as was detected by iWorkflow. This is the
                    # name that iWorkflow displays when you view the Devices
                    # blade.
                    #
                    # Example:
                    #     sdb-test-bigip-1.localhost.localdoman
                    resource = device
                    break
                elif str(device.address) == params:
                    # Address
                    #
                    # This is the address that iWorkflow discovered the device
                    # on. This may be the management address, but it could also
                    # be a Self IP on the BIG-IP. This address is usually
                    # displayed next to the specific device in the Devices blade
                    #
                    # Example:
                    #     131.225.23.53
                    resource = device
                    break
                elif str(device.managementAddress) == params:
                    # Management Address
                    #
                    # This is the management address of the BIG-IP.
                    #
                    # Example:
                    #     192.168.10.100
                    resource = device
                    break
        if not resource:
            raise F5ModuleError(
                "Device {0} was not found".format(params)
            )
        self._values['resource'] = resource

    def _get_device_collection(self):
        dg = self.client.api.shared.resolver.device_groups
        return dg.cm_cloud_managed_devices.devices_s.get_collection()

    @property
    def selfLink(self):
        if self._values['resource'].selfLink is None:
            return None
        return str(self._values['resource'].selfLink)

    @property
    def address(self):
        if self._values['resource'].address is None:
            return None
        return str(self._values['resource'].address)

    @property
    def hostname(self):
        if self._values['resource'].hostname is None:
            return None
        return str(self._values['resource'].hostname)


class Connector(object):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        self._values = defaultdict(lambda: None)

    def update(self, params=None):
        params = str(params)
        resource = None
        collection = self._get_connector_collection()
        if re.search(r'([0-9-a-z]+\-){4}[0-9-a-z]+', params, re.I):
            # Handle cases where the REST API sent us self links
            for connector in collection:
                if str(connector.displayName) != "BIG-IP":
                    continue
                if str(connector.selfLink) != params:
                    continue
                resource = connector
                break
        else:
            # Handle the case where a user sends us a list of connector names
            for connector in collection:
                if str(connector.displayName) != "BIG-IP":
                    continue
                if str(connector.name) != params:
                    continue
                resource = connector
                break
        if not resource:
            raise F5ModuleError(
                "Connector {0} was not found".format(params)
            )
        self._values['name'] = resource.name
        self._values['selfLink'] = resource.selfLink
        self._values['resource'] = resource

    def _get_connector_collection(self):
        return self.client.api.cm.cloud.connectors.locals.get_collection()

    @property
    def name(self):
        return str(self._values['name'])

    @property
    def selfLink(self):
        return str(self._values['selfLink'])

    @property
    def resource(self):
        return self._values['resource']


class Parameters(AnsibleF5Parameters):
    api_map = {
        'ipAddress': 'ip_address',
        'cloudNodeID': 'cloud_node_id',
        'networkInterfaces': 'interfaces'
    }
    returnables = ['networkInterfaces']

    api_attributes = [
        'properties', 'ipAddress', 'cloudNodeID', 'networkInterfaces'
    ]

    updatables = []

    def __init__(self, params=None, client=None):
        self.client = client
        self._values = defaultdict(lambda: None)
        if params:
            self.update(params)

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
                        # If the mapped value does not have an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

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
        result['state'] = 'RUNNING'
        return result

    @property
    def ip_address(self):
        return self.device.address

    @property
    def cloud_node_id(self):
        # We have to provide this to iWorkflow ourselves, so the standard
        # protocol is to just make this ID the IP address of the device.
        return self.device.address

    @property
    def interfaces(self):
        result = []
        for interface in self._values['interfaces']:
            tmp = {}
            self._update_interface_local_address(interface, tmp)
            self._update_interface_subnet_address(interface, tmp)
            self._update_virtual_address(interface, tmp)
            self._update_gateway_address(interface, tmp)
            self._update_interface_name(interface, tmp)
            result.append(tmp)
        self._validate_name_in_interface(result)
        return result

    def _update_gateway_address(self, interface, tmp):
        if 'gateway_address' in interface:
            try:
                ip = netaddr.IPNetwork(interface['gateway_address'])
                tmp['gatewayAddress'] = str(ip.ip)
            except netaddr.core.AddrFormatError:
                raise F5ModuleError(
                    "The provided gateway_address for your network "
                    "interface is not in an IP address format."
                )

    def _update_virtual_address(self, interface, tmp):
        if 'virtual_address' in interface:
            try:
                ip = netaddr.IPNetwork(interface['virtual_address'])
                tmp['virtualAddress'] = str(ip.ip)
            except netaddr.core.AddrFormatError:
                raise F5ModuleError(
                    "The provided virtual_address for your network "
                    "interface is not in an IP address format."
                )

    def _update_interface_name(self, interface, tmp):
        if 'name' in interface:
            tmp['name'] = interface['name']

    def _validate_name_in_interface(self, result):
        if any('name' not in x for x in result[1:]):
            raise F5ModuleError(
                "All interfaces, except for the first (mgmt), require a name."
            )

    def _update_interface_local_address(self, interface, tmp):
        if 'local_address' not in interface:
            raise F5ModuleError(
                "local_address is a required key in interfaces."
            )
        try:
            ip = netaddr.IPNetwork(interface['local_address'])
            tmp['localAddress'] = str(ip.ip)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided local_address for your network "
                "interface is not in an IP address format."
            )

    def _update_interface_subnet_address(self, interface, tmp):
        if 'subnet_address' not in interface:
            raise F5ModuleError(
                "subnet_address is a required key in interfaces"
            )
        try:
            subnet = interface['subnet_address']
            ip = netaddr.IPNetwork(subnet)
            # The iWorkflow value for this is the true CIDR address
            tmp['subnetAddress'] = str(ip.cidr)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided subnet_address for your network "
                "interface is not in a CIDR format"
            )

    @property
    def hostname(self):
        if self._values['hostname'] is None:
            return None
        return str(self._values['hostname'])

    @property
    def connector(self):
        return self._values['connector']

    @connector.setter
    def connector(self, value):
        connector = Connector()
        connector.client = self.client
        connector.update(value)
        self._values['connector'] = connector

    @property
    def device(self):
        return self._values['device']

    @device.setter
    def device(self, value):
        device = Device()
        device.client = self.client
        device.update(value)
        self._values['device'] = device

    @property
    def properties(self):
        result = self._get_base_properties()
        result += self._set_initial_mgmt_ip()
        result += self._set_hostname_property()
        result += self._set_key_content_property()
        result += self._set_password_credential_property()
        result += self._set_mgmt_user_property()
        result += self._set_device_default_credentials()
        result += self._set_device_root_password()
        return result

    def _set_device_root_password(self):
        if self.device_root_password is None:
            return []
        if self.username_credential != 'root':
            return []

        result =[dict(
            id='DeviceRootPassword',
            provider=self.device_root_password
        )]
        return result

    def _set_initial_mgmt_ip(self):
        if self.initial_mgmt_ip is None:
            return []
        result = [dict(
            id='DeviceInitialMgmtIP',
            provider=self.initial_mgmt_ip
        )]
        return result

    def _set_password_credential_property(self):
        if self.password_credential is None:
            return []
        result = [dict(
            id='DeviceMgmtPassword',
            provider=self.password_credential
        )]
        return result

    def _set_hostname_property(self):
        if self.hostname is None:
            return []
        result = [dict(
            id='DeviceHostname',
            provider=self.hostname
        )]
        return result

    def _set_key_content_property(self):
        if self.key_content is None:
            return []
        result = [dict(
            id='KeyPrivate',
            value=self.key_content
        )]
        return result

    def _set_mgmt_user_property(self):
        if self.username_credential is None:
            return []

        # iWorkflow 2.1.0 requires that this be 'admin'. If you don't
        # set this as 'admin', you get the following error in iWorkflow
        #
        # VALIDATE_NODE stage FAILED because ... DeviceMgmtUser property
        # must be ********.  Delete and re-create Node with that property.
        #
        # I am leaving this as a function though in case that changes in
        # the future.
        result = [dict(
            id='DeviceMgmtUser',
            provider=self.username_credential
        )]
        return result

    def _set_device_default_credentials(self):
        result = []
        if self.username_credential == 'admin' and self.device_root_password is None:
            result.append(dict(
                id='BIG-IP-WITH-ADMIN-SSH',
                provider="true"
            ))
        else:
            result.append(dict(
                id='BIG-IP-WITH-ADMIN-SSH',
                provider="false"
            ))

        # This setting controls whether or not SSH auth is used.
        #
        # If it is "false" then SSH auth will be tried and the
        # `key_content` option must be set.
        if self.password_credential:
            result.append(dict(
                id='DeviceCreatedWithDefaultCredentials',
                provider="true"
            ))
        elif self.key_content:
            result.append(dict(
                id='DeviceCreatedWithDefaultCredentials',
                provider="false"
            ))
        else:
            raise F5ModuleError(
                "At least one of `password_credential` or `key_content` "
                "is required."
            )
        return result

    def _get_base_properties(self):
        result = [
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
                provider="true"
            ),
            dict(
                id='DeviceLeaveRootLoginEnabled',
                provider="false"
            )
        ]
        return result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters()
            self.changes.client = self.client
            self.changes.update(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = attr1
        if changed:
            self.changes = Parameters()
            self.changes.client = self.client
            self.changes.update(changed)
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
        connector = self.want.connector.resource
        collection = connector.nodes_s.get_collection()
        for resource in collection:
            if resource.ipAddress == self.want.device.address:
                return True
        return False

    def present(self):
        if self.exists():
            try:
                if self.have.currentConfigDeviceTaskReference['status'] == 'FAILED':
                    return self.update()
            except AttributeError:
                # We don't update things that aren't broken, and things that completed
                # successfully. iWorkflow removes this attribute if the task completed.
                return False
        else:
            return self.create()

    def create(self):
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.want.api_params()
        connector = self.want.connector.resource
        resource = connector.nodes_s.node.create(**params)
        self._wait_for_state_to_activate(resource)

    def _wait_for_state_to_activate(self, resource):
        for x in range(360):
            resource.refresh(
                requests_params=dict(
                    params='$expand=currentConfigDeviceTaskReference'
                )
            )
            if not hasattr(resource, 'currentConfigDeviceTaskReference'):
                pass
            elif 'status' not in resource.currentConfigDeviceTaskReference:
                pass
            elif resource.currentConfigDeviceTaskReference['status'] == 'FINISHED':
                return
            elif resource.currentConfigDeviceTaskReference['status'] == 'FAILED':
                raise F5ModuleError(
                    str(resource.currentConfigDeviceTaskReference['errorMessage'])
                )
            time.sleep(10)
        raise F5ModuleError(
            "Timed out waiting 30 minutes for node to finish."
        )

    def read_current_from_device(self):
        connector = self.want.connector.resource
        collection = connector.nodes_s.get_collection(
            requests_params=dict(
                params="$filter=ipAddress+eq+'{0}'".format(self.want.device.address)
            )
        )
        resource = collection.pop()
        resource.refresh(
            requests_params=dict(
                params='$expand=currentConfigDeviceTaskReference'
            )
        )
        result = resource.attrs
        return Parameters(result)

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True

        # The only way to update is to delete the existing node and re-post.
        self.remove()
        return self.create()

    def should_update(self):
        result = self._update_changed_options()
        failed = self.have.currentConfigDeviceTaskReference['status'] == 'FAILED'
        if result or failed:
            return True
        return False

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_connector_node_from_device()
        if self.exists():
            raise F5ModuleError(
                "Failed to remove the node from the connector"
            )
        return True

    def remove_from_device(self):
        connector = self.want.connector.resource
        collection = connector.nodes_s.get_collection()
        for resource in collection:
            if resource.ipAddress == self.want.device.ip_address:
                resource.delete()
                return True
        return False


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            connector=dict(
                required=True
            ),
            device=dict(
                required=True
            ),
            device_root_password=dict(
                required=False,
                default=None,
                no_log=True
            ),
            key_content=dict(
                type='str',
                required=False,
                default=None
            ),
            password_credential=dict(
                required=False,
                default=None,
                no_log=True
            ),
            username_credential=dict(
                required=False,
                default=None
            ),
            hostname=dict(
                required=False,
                default=None
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

        self.mutually_exclusive=[
            ['key_content', 'password_credential'],
        ]
        self.required_if=[
            ['state', 'present', ['interfaces']]
        ]
        self.f5_product_name = 'iworkflow'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name,
        required_if=spec.required_if,
        mutually_exclusive=spec.mutually_exclusive
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
