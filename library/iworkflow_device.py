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
module: iworkflow_managed_device
short_description: Manipulate cloud managed devices in iWorkflow.
description:
  - Manipulate cloud managed devices in iWorkflow.
version_added: 2.4
options:
  device:
    description:
      - Hostname or IP address of the device to manage in iWorkflow.
    required: True
  username_credential:
    description:
      - Username credential used to log in to the remote device's REST
        interface. Note that this is usually different from the credential
        used to log into the CLI of the device.
    required: True
  password_credential:
    description:
      - Password of the user provided in C(username_credential).
    required: True
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
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 1.5.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Discover a BIG-IP device with hostname lb.mydomain.com
  iworkflow_device:
      device: "lb.mydomain.com
      username_credential: "admin"
      password_credential: "admin"
      password: "secret"
      server: "mgmt.mydomain.com"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

import time
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    F5ModuleError,
    HAS_F5SDK,
    iControlUnexpectedHTTPError
)


class Parameters(AnsibleF5Parameters):
    api_map = {
        'restFrameworkVersion': 'rest_framework_version',
        'managementAddress': 'management_address',
        'httpsPort': 'https_port',
        'address': 'device',
        'machineId': 'machine_id',
        'deviceUri': 'device_uri'
    }
    returnables = []

    api_attributes = []

    updatables = []

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
    def hostname(self):
        if self._values['hostname'] is None:
            return None
        return str(self._values['hostname'])


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
            elif state == "rediscover":
                changed = self.update()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        dg = self.client.api.shared.resolver.device_groups
        devices = dg.cm_cloud_managed_devices.devices_s.get_collection(
            requests_params=dict(
                params="$filter=address+eq+'{0}'".format(self.want.device)
            )
        )

        if len(devices) == 1:
            return True
        elif len(devices) == 0:
            return False
        else:
            raise F5ModuleError(
                "Multiple managed devices with the provided device address were found!"
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

    def update(self):
        self.have = self.read_current_from_device()
        if self.have.errors:
            if 'not upgrade rest' in str(self.have.errors).lower():
                return self.rediscover()
        return False

    def rediscover(self):
        self.have = self.read_current_from_device()
        dg = self.client.api.shared.resolver.device_groups
        collection = dg.cm_cloud_managed_devices.devices_s.get_collection(
            requests_params=dict(
                params="$filter=address+eq+'{0}'".format(self.want.device)
            )
        )
        resource = collection.pop()
        self.resource = resource
        self.rediscover_on_device()
        self._wait_for_state_to_activate(resource)
        return True

    def rediscover_on_device(self):
        self.resource.modify(
            userName=self.want.username_credential,
            password=self.want.password_credential,
            automaticallyUpdateFramework=True
        )

    def read_current_from_device(self):
        dg = self.client.api.shared.resolver.device_groups
        collection = dg.cm_cloud_managed_devices.devices_s.get_collection(
            requests_params=dict(
                params="$filter=address+eq+'{0}'".format(self.want.device)
            )
        )
        resource = collection.pop()
        result = resource.attrs
        return Parameters(result)

    def create_on_device(self):
        dg = self.client.api.shared.resolver.device_groups
        resource = dg.cm_cloud_managed_devices.devices_s.device.create(
            address=self.want.device,
            userName=self.want.username_credential,
            password=self.want.password_credential,
            automaticallyUpdateFramework=True
        )
        self._wait_for_state_to_activate(resource)

    def _wait_for_state_to_activate(self, resource):
        error_values = ['POST_FAILED', 'VALIDATION_FAILED']
        # Wait no more than half an hour
        for x in range(1, 180):
            resource.refresh()
            if resource.state == 'ACTIVE':
                break
            elif resource.state in error_values:
                raise F5ModuleError(resource.errors)
            time.sleep(10)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the managed device")
        return True

    def remove_from_device(self):
        dg = self.client.api.shared.resolver.device_groups
        devices = dg.cm_cloud_managed_devices.devices_s.get_collection(
            requests_params=dict(
                params="$filter=address+eq+'{0}'".format(self.want.device)
            )
        )
        device = devices.pop()
        device.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            device=dict(default=None),
            username_credential=dict(default=None),
            password_credential=dict(default=None, no_log=True),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present', 'rediscover']
            )
        )
        self.required_if = [
            ['state', 'present', ['device', 'username_credential', 'password_credential']],
            ['state', 'rediscover', ['device', 'username_credential', 'password_credential']]
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
        required_if=spec.required_if
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
