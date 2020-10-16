#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bigip_software_update
short_description: Manage the software update settings of a BIG-IP
description:
  - Manage the software update settings of a BIG-IP.
version_added: "1.0.0"
options:
  auto_check:
    description:
      - Specifies whether to automatically check for updates on the F5
        Networks downloads server.
    type: bool
  auto_phone_home:
    description:
      - Specifies whether to automatically send phone home data to the
        F5 Networks PhoneHome server.
    type: bool
  frequency:
    description:
      - Specifies the schedule for the automatic update check.
    type: str
    choices:
      - daily
      - monthly
      - weekly
extends_documentation_fragment: f5networks.f5_modules.f5
author:
  - Tim Rupp (@caphrim007)
  - Wojciech Wypior (@wojtek0806)
'''

EXAMPLES = r'''
- name: Enable automatic update checking
  bigip_software_update:
    auto_check: yes
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost

- name: Disable automatic update checking and phoning home
  bigip_software_update:
    auto_check: no
    auto_phone_home: no
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost
'''

RETURN = r'''
auto_check:
  description: Whether the system automatically checks for updates.
  returned: changed
  type: bool
  sample: True
auto_phone_home:
  description: Whether the system automatically sends phone home data.
  returned: changed
  type: bool
  sample: True
frequency:
  description: Frequency of auto update checks.
  returned: changed
  type: str
  sample: weekly
'''
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.bigip import F5RestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, f5_argument_spec
)
from ..module_utils.icontrol import tmos_version
from ..module_utils.teem import send_teem


class Parameters(AnsibleF5Parameters):
    api_map = {
        'autoCheck': 'auto_check',
        'autoPhonehome': 'auto_phone_home'
    }

    api_attributes = [
        'autoCheck', 'autoPhonehome', 'frequency',
    ]

    updatables = [
        'auto_check', 'auto_phone_home', 'frequency',
    ]

    returnables = [
        'auto_check', 'auto_phone_home', 'frequency',
    ]


class ApiParameters(Parameters):
    @property
    def auto_check(self):
        if self._values['auto_check'] is None:
            return None
        return self._values['auto_check']


class ModuleParameters(Parameters):
    @property
    def auto_check(self):
        if self._values['auto_check'] is None:
            return None
        elif self._values['auto_check'] is True:
            return 'enabled'
        else:
            return 'disabled'

    @property
    def auto_phone_home(self):
        if self._values['auto_phone_home'] is None:
            return None
        elif self._values['auto_phone_home'] is True:
            return 'enabled'
        else:
            return 'disabled'


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class UsableChanges(Changes):
    pass


class ReportableChanges(Changes):
    @property
    def auto_check(self):
        if self._values['auto_check'] == 'enabled':
            return True
        elif self._values['auto_check'] == 'disabled':
            return False

    @property
    def auto_phone_home(self):
        if self._values['auto_phone_home'] == 'enabled':
            return True
        elif self._values['auto_phone_home'] == 'disabled':
            return False


class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            return self.__default(param)

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.have = None
        self.want = ModuleParameters(params=self.module.params)
        self.changes = UsableChanges()

    def exec_module(self):
        start = datetime.now().isoformat()
        version = tmos_version(self.client)
        result = dict()

        changed = self.update()

        reportable = ReportableChanges(params=self.changes.to_return())
        changes = reportable.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        send_teem(start, self.module, version)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = UsableChanges(params=changed)
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
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def read_current_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/sys/software/update/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        return ApiParameters(params=response)

    def update_on_device(self):
        params = self.changes.api_params()
        uri = "https://{0}:{1}/mgmt/tm/sys/software/update/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            auto_check=dict(
                type='bool'
            ),
            auto_phone_home=dict(
                type='bool'
            ),
            frequency=dict(
                choices=['daily', 'monthly', 'weekly']
            )
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )

    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
