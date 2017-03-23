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
module: iworkflow_local_connector_device
short_description: Manipulate cloud local connector devices in iWorkflow.
description:
  - Manipulate cloud local connector devices in iWorkflow.
version_added: 2.4
options:
  connector:
    description:
      - Name of the local connector to add the device(s) to.
    required: True
  device:
    description:
      - The Hostname, Self-IP address, or Management Address of the device
        to associated with the connector. This parameter is required when
        C(state) is C(present).
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
    - f5-sdk >= 2.3.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

import re
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    defaultdict,
    F5ModuleError,
    HAS_F5SDK,
    iteritems
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
        self._values['selfLink'] = resource.selfLink

    def _get_device_collection(self):
        dg = self.client.api.shared.resolver.device_groups
        return dg.cm_cloud_managed_devices.devices_s.get_collection()

    @property
    def selfLink(self):
        return str(self._values['selfLink'])


class Connector(object):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        self._values = defaultdict(lambda: None)
        self.devices = []

    def update(self, params=None):
        # Handle the case where the Ansible user provides a name as string
        if isinstance(params, basestring):
            self._values['name'] = params
            resource = self._load_resource_by_name()
            try:
                for reference in resource.deviceReferences:
                    device = Device()
                    device.client = self.client
                    device.update(reference['link'])
                    self.devices.append(device)
            except AttributeError:
                pass
        else:
            # Handle the case where the REST API provides a dict
            self._values['name'] = params['name']
            try:
                for reference in params['deviceReferences']:
                    device = Device()
                    device.client = self.client
                    device.update(reference['link'])
                    self.devices.append(device)
            except AttributeError:
                pass

    def _load_resource_by_name(self):
        collection = self.client.api.cm.cloud.connectors.locals.get_collection()
        for connector in collection:
            if str(connector.displayName) != "BIG-IP":
                continue
            if str(connector.name) != self.name:
                continue
            return connector
        return None

    @property
    def name(self):
        return str(self._values['name'])


class Parameters(AnsibleF5Parameters):
    returnables = []
    api_attributes = []

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
        return result

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
        return self._values['devices']

    @device.setter
    def device(self, value):
        result = []
        device = Device()
        device.client = self.client
        device.update(value)
        result.append(device)
        self._values['devices'] = result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None

        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)

        self.changes = Parameters()
        self.changes.client = self.client

    def _set_changed_options(self):
        changed = {}
        want = set([x.selfLink for x in self.want.connector.devices])
        changed['devices'] = want
        self.changes = Parameters()
        self.changes.client = self.client
        self.changes.update(changed)
        return True

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except IOError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        if not self.want.connector.devices:
            return False

        # Getting new sets of parameters here ensures that nothing is
        # cached when, for example, delete is used.
        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)

        tcr = set([x.selfLink for x in self.want.connector.devices])
        cr = set([x.selfLink for x in self.want.devices])
        if cr.issubset(tcr):
            return True
        return False

    def present(self):
        if self.exists():
            return False
        else:
            return self.create()

    def create(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        resource = None
        device_refs = self.to_add()
        collection = self.client.api.cm.cloud.connectors.locals.get_collection()
        for connector in collection:
            if str(connector.displayName) != "BIG-IP":
                continue
            if str(connector.name) != self.want.connector.name:
                continue
            resource = connector
            break
        if not resource:
            raise F5ModuleError(
                "Resource disappeared during device reference updating"
            )
        resource.update(
            deviceReferences=device_refs
        )
        return True

    def to_add(self):
        want = [x.selfLink for x in self.want.devices]
        have = [x.selfLink for x in self.want.connector.devices]
        references = set(want + have)
        return [dict(link=x) for x in references]

    def read_current_from_device(self):
        result = dict()
        collection = self.client.api.cm.cloud.connectors.locals.get_collection()
        for connector in collection:
            if str(connector.displayName) != "BIG-IP":
                continue
            if str(connector.name) != self.want.connector.name:
                continue
            resource = connector
            break
        if not resource:
            raise F5ModuleError(
                "The specified connector was not found"
            )
        result['connector'] = resource.attrs
        params = Parameters()
        params.client = self.client
        params.update(result)
        return params

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        self.have = self.read_current_from_device()
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the connector device reference")
        return True

    def remove_from_device(self):
        resource = None
        references = self.to_remove()
        collection = self.client.api.cm.cloud.connectors.locals.get_collection()
        for connector in collection:
            if str(connector.displayName) != "BIG-IP":
                continue
            if str(connector.name) != self.want.connector.name:
                continue
            resource = connector
            break
        if not resource:
            raise F5ModuleError(
                "The specified connector was not found"
            )
        resource.update(deviceReferences=references)
        return True

    def to_remove(self):
        want = set([x.selfLink for x in self.want.devices])
        have = set([x.selfLink for x in self.want.connector.devices])
        references = set(have - want)
        return [dict(link=x) for x in references]


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            connector=dict(
                required=True
            ),
            devices=dict(
                type='str',
                required=True,
                aliases=['device']
            ),
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
