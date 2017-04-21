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
module: bigip_device_group
short_description: Manage device groups on a BIG-IP.
description:
  - Managing device groups allows you to create HA pairs and clusters
    of BIG-IP devices. Usage of this module should be done in conjunction
    with the C(bigip_configsync_actions) to sync configuration across
    the pair or cluster if auto-sync is disabled.
version_added: "2.4"
options:
  name:
    description:
      - Specifies the name of the device group.
    required: True
  type:
    description:
      - Specifies that the type of group. A C(sync-failover) device group
        contains devices that synchronize their configuration data and fail
        over to one another when a device becomes unavailable. A C(sync-only)
        device group has no such failover. When creating a new device group,
        this option will default to C(sync-only). This setting cannot be
        changed once it has been set.
    required: False
    default: None
    choices:
      - sync-failover
      - sync-only
  description:
    description:
      - Description of the device group.
    required: False
    default: None
  auto_sync:
    description:
      - Indicates whether configuration synchronization occurs manually or
        automatically. When creating a new device group, this option will
        default to C(false). 
    required: False
    default: None
    choices:
      - true
      - false
  save_on_auto_sync:
    description:
      - When performing an auto-sync, specifies whether the configuration
        will be saved or not. If C(false), only the running configuration
        will be changed on the device(s) being synced to. When creating a
        new device group, this option will default to C(false).
    required: False
    default: None
    choices:
      - true
      - false
  full_sync:
    description:
      - Specifies whether the system synchronizes the entire configuration
        during synchronization operations. When C(false), the system performs
        incremental synchronization operations, based on the cache size
        specified in C(max_incremental_sync_size). Incremental configuration
        synchronization is a mechanism for synchronizing a device-group's
        configuration among its members, without requiring a full configuration
        load for each configuration change. In order for this to work, all
        devices in the device-group must initially agree on the configuration.
        Typically this requires at least one full configuration load to each
        device. When creating a new device group, this option will default
        to C(false).
    required: False
    default: None
    choices:
      - true
      - false
  max_incremental_sync_size:
    description:
      - Specifies the size of the changes cache for incremental sync. For example,
        using the default, if you make more than 1024 KB worth of incremental
        changes, the system performs a full synchronization operation. Using 
        incremental synchronization operations can reduce the per-device sync/load
        time for configuration changes. This setting is relevant only when
        C(full_sync) is C(false).
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
- name: Create a sync-only device group
  bigip_device_group:
      name: "foo-group"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost

- name: Create a sync-only device group with auto-sync enabled
  bigip_device_group:
      name: "foo-group"
      auto_sync: "yes"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
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
        'saveOnAutoSync': 'save_on_auto_sync',
        'fullLoadOnSync': 'full_sync',
        'autoSync': 'auto_sync',
        'incrementalConfigSyncSizeMax': 'max_incremental_sync_size'
    }
    api_attributes = [
        'saveOnAutoSync', 'fullLoadOnSync', 'description', 'type', 'autoSync',
        'incrementalConfigSyncSizeMax'
    ]
    returnables = [
        'save_on_auto_sync', 'full_sync', 'description', 'type', 'auto_sync'
    ]
    updatables = [
        'save_on_auto_sync', 'full_sync', 'description', 'auto_sync',
        'max_incremental_sync_size'
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
