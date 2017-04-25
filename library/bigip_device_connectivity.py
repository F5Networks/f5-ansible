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
module: bigip_device_mirroring
short_description: Manage device mirroring settings on a BIG-IP.
description:
  - Manages device mirroring settings on a BIG-IP. These settings are
    related to the IP address configuration of the devices to mirror to.
version_added: "2.4"
options:
  config_sync_ip:
    description:
      - Local IP address that the system uses for ConfigSync operations.
    default: None
    required: False
  primary_mirror_address:
    description:
      - Specifies the primary IP address for the system to use to mirror
        connections.
    required: False
    default: None
  secondary_mirror_address:
    description:
      - Specifies the secondary IP address for the system to use to mirror
        connections.
    required: False
    default: None
  unicast_failover:
    description:
      - Desired addresses to use for failover operations. Options C(address)
        and C(port) are supported with dictionary structure where C(address) is the
        local IP address that the system uses for failover operations. Port
        specifies the port that the system uses for failover operations.
    required: False
    default: None
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - This module is primarily used as a component of configuring HA pairs of
    BIG-IP devices.
  - Requires BIG-IP >= 12.1.x.
  - Requires Ansible >= 2.3.
requirements:
  - f5-sdk >= 2.2.3
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Set mirroring settings for HA
  bigip_device_mirroring:
      primary_mirror_address: 10.0.2.15
      secondary_mirror_address: 10.2.2.3
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
  delegate_to: localhost

- name: Remove mirroring setting for secondary address
  bigip_device_mirroring:
      secondary_mirror_address: "none"
      name: "foo-group"
      auto_sync: "yes"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

from ansible.module_utils.basic import BOOLEANS
from ansible.module_utils.basic import BOOLEANS_TRUE
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    HAS_F5SDK,
    F5ModuleError,
    iControlUnexpectedHTTPError
)


class Parameters(AnsibleF5Parameters):
    api_map = {
        'mirrorIp': 'mirror_ip',
        'mirrorSecondaryIp': 'mirror_secondary_ip'
    }
    api_attributes = [
        'saveOnAutoSync', 'fullLoadOnSync', 'description', 'type', 'autoSync',
        'incrementalConfigSyncSizeMax'
    ]
    returnables = [
        'mirror_ip', 'mirror_secondary_ip'
    ]
    updatables = [
        'mirror_ip', 'mirror_secondary_ip'
    ]

    @property
    def save_on_auto_sync(self):
        if self._values['save_on_auto_sync'] is None:
            return None
        elif self._values['save_on_auto_sync'] in BOOLEANS_TRUE:
            return True
        else:
            return False

    @property
    def auto_sync(self):
        if self._values['auto_sync'] is None:
            return None
        elif self._values['auto_sync'] in [True, 'enabled']:
            return 'enabled'
        else:
            return 'disabled'

    @property
    def full_sync(self):
        if self._values['full_sync'] is None:
            return None
        elif self._values['full_sync'] in BOOLEANS_TRUE:
            return True
        else:
            return False

    @property
    def max_incremental_sync_size(self):
        if not self.full_sync and self._values['max_incremental_sync_size'] is not None:
            if self._values['__warnings'] is None:
                self._values['__warnings'] = []
            self._values['__warnings'].append(
                [
                    dict(
                        msg='"max_incremental_sync_size has no effect if "full_sync" is not true',
                        version='2.4'
                    )
                ]
            )
        if self._values['max_incremental_sync_size'] is None:
            return None
        return int(self._values['max_incremental_sync_size'])

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

    def should_update(self):
        result = self._update_changed_options()
        if result:
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
        self._announce_deprecations(result)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def exists(self):
        result = self.client.api.tm.cm.device_groups.device_group.exists(
            name=self.want.name,
            partition=self.want.partition
        )
        return result

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the device group")
        return True

    def create(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.cm.device_groups.device_group.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def update_on_device(self):
        params = self.want.api_params()
        resource = self.client.api.tm.cm.device_groups.device_group.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.modify(**params)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove_from_device(self):
        resource = self.client.api.tm.cm.device_groups.device_group.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if resource:
            resource.delete()

    def read_current_from_device(self):
        resource = self.client.api.tm.cm.device_groups.device_group.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result = resource.attrs
        return Parameters(result)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            type=dict(
                required=False,
                default=None,
                choices=['sync-failover', 'sync-only']
            ),
            description=dict(
                required=False,
                default=None
            ),
            auto_sync=dict(
                required=False,
                default=None,
                type='bool',
                choices=BOOLEANS
            ),
            save_on_auto_sync=dict(
                required=False,
                default=None,
                type='bool',
                choices=BOOLEANS
            ),
            full_sync=dict(
                required=False,
                default=None,
                type='bool',
                choices=BOOLEANS
            ),
            name=dict(
                required=True
            ),
            max_incremental_sync_size=dict(
                required=False,
                default=None
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
