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
---
module: bigip_configsync_actions
short_description: Perform different actions related to config-sync.
description:
  - Allows one to run different config-sync actions. These actions allow
    you to manually sync your configuration across multiple BIG-IPs when
    those devices are in an HA pair.
version_added: "2.4"
options:
  device_group:
    description:
      - The device group that you want to perform config-sync actions on.
    required: True
  sync_device_to_group:
    description:
      - Specifies that the system synchronizes configuration data from this
        device to other members of the device group. This option is mutually
        exclusive with the C(sync_group_to_device) option.
    required: False
    default: False
    choices:
      - yes
      - no
  sync_group_to_device:
    description:
      - Specifies that the system synchronizes configuration data from the
        group to this device. This option is mutually exclusive with the
        C(sync_device_to_group) options.
    required: False
    default: False
    choices:
      - yes
      - no
  overwrite_config:
    description:
      - Indicates that the sync operation overwrites the configuration on
        the target.
    required: False
    default: False
    choices:
      - yes
      - no
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Requires Ansible >= 2.3.
requirements:
  - f5-sdk >= 2.2.3
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Sync configuration from device to group
  bigip_configsync_actions:
      device_group: "foo-group"
      sync_device_to_group: yes
      server: "lb01.mydomain.com"
      user: "admin"
      password: "secret"
      validate_certs: no
  delegate_to: localhost
  
- name: Sync configuration from group to devices in group
  bigip_configsync_actions:
      device_group: "foo-group"
      sync_group_to_device: yes
      server: "lb01.mydomain.com"
      user: "admin"
      password: "secret"
      validate_certs: no
  delegate_to: localhost

- name: Perform an initial sync of a device to a new device group
  bigip_configsync_actions:
      device_group: "new-device-group"
      sync_device_to_group: yes
      server: "lb01.mydomain.com"
      user: "admin"
      password: "secret"
      validate_certs: no
  delegate_to: localhost
'''

RETURN = '''

'''

import time

from ansible.module_utils.basic import BOOLEANS
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    HAS_F5SDK,
    F5ModuleError,
    iControlUnexpectedHTTPError
)


class Parameters(AnsibleF5Parameters):
    api_attributes = []
    returnables = []

    @property
    def direction(self):
        if self.sync_device_to_group:
            return 'to-group'
        else:
            return 'from-group'

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
        self.want = Parameters(self.client.module.params)

    def exec_module(self):
        result = dict()

        try:
            self.present()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(dict(changed=True))
        return result

    def present(self):
        if not self._device_group_exists():
            raise F5ModuleError(
                "The specified 'device_group' not not exist."
            )
        if not self._validate_sync_to_group_required():
            raise F5ModuleError(
                "This device group needs an initial sync. Please use "
                "'sync_device_to_group'"
            )
        self.execute()

    def _validate_sync_to_group_required(self):
        resource = self.client.api.tm.cm.sync_status.load()
        k,v = resource.entries.popitem()
        status = v['nestedStats']['entries']['status']['description']
        if status == 'Awaiting Initial Sync' and self.want.sync_group_to_device:
            return False
        return True

    def _device_group_exists(self):
        result = self.client.api.tm.cm.device_groups.device_group.exists(
            name=self.want.device_group
        )
        return result

    def execute(self):
        self.execute_on_device()
        self._wait_for_sync()

    def execute_on_device(self):
        sync_cmd = 'config-sync {0} {1}'.format(
            self.want.direction,
            self.want.device_group
        )
        self.client.api.tm.cm.exec_cmd(
            'run',
            utilCmdArgs=sync_cmd
        )

    def _wait_for_sync(self):
        # Wait no more than half an hour
        resource = self.client.api.tm.cm.sync_status.load()
        for x in range(1, 180):
            resource.refresh()
            k,v = resource.entries.popitem()
            status = v['nestedStats']['entries']['status']['description']

            # Changes Pending:
            #     The existing device has changes made to it that
            #     need to be sync'd to the group.
            #
            # Awaiting Initial Sync:
            #     This is a new device group and has not had any sync
            #     done yet. You _must_ `sync_device_to_group` in this
            #     case.
            #
            if status in ['Changes Pending', 'Awaiting Initial Sync']:
                pass
            elif status == 'In Sync':
                return
            else:
                raise F5ModuleError(status)
            time.sleep(3)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            sync_device_to_group=dict(
                required=False,
                default=False,
                type='bool',
                choices=BOOLEANS
            ),
            sync_group_to_device=dict(
                required=False,
                default=False,
                type='bool',
                choices=BOOLEANS
            ),
            overwrite_config=dict(
                required=False,
                default=False,
                type='bool',
                choices=BOOLEANS
            ),
            device_group=dict(
                required=True
            )
        )
        self.f5_product_name = 'bigip'


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

