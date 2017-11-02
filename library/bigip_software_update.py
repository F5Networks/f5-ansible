#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_software_update
short_description: Manage the software update settings of a BIG-IP
description:
  - Manage the software update settings of a BIG-IP.
version_added: "2.4"
options:
  auto_check:
    description:
      - Specifies whether to automatically check for updates on the F5
        Networks downloads server.
    required: False
    default: None
    choices:
      - yes
      - no
  frequency:
    description:
      - Specifies the schedule for the automatic update check.
    required: False
    default: None
    choices:
      - daily
      - monthly
      - weekly
notes:
  - Requires the f5-sdk Python package on the host This is as easy as pip
    install f5-sdk
extends_documentation_fragment: f5
requirements:
  - f5-sdk >= 2.2.3
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''

'''

RETURN = r'''
# only common fields returned
'''

from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError

try:
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    api_map = {
        'autoCheck': 'auto_check'
    }

    updatables = [
        'auto_check', 'frequency'
    ]

    returnables = [
        'auto_check', 'frequency'
    ]

    @property
    def auto_check(self):
        if self._values['auto_check'] is None:
            return None
        elif self._values['auto_check'] in [True, 'enabled']:
            return 'enabled'
        else:
            return 'disabled'

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.network == 'default':
                result['network'] = None
            elif self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def exec_module(self):
        result = dict()

        try:
            changed = self.update()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

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

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def update_on_device(self):
        params = self.want.api_params()
        result = self.client.api.tm.sys.software.update.load()
        result.modify(**params)

    def read_current_from_device(self):
        resource = self.client.api.tm.sys.software.update.load()
        result = resource.attrs
        return Parameters(result)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            auto_check=dict(
                type='bool'
            ),
            frequency=dict(
                choices=['daily', 'monthly', 'weekly']
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

    mm = ModuleManager(client)
    results = mm.exec_module()
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
