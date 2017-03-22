#!/usr/bin/python
# -*- coding: utf-8 -*-
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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
---
module: bigip_software_update
short_description: Manage the software update settings of a BIG-IP
description:
  - Manage the software update settings of a BIG-IP
version_added: "2.2"
options:
  auto_check:
    description:
      - Specifies whether to automatically check for updates on the F5
        Networks downloads server
    required: false
    default: None
  frequency:
    description:
      - Specifies the schedule for the automatic update check
    required: false
    default: None
    choices:
      - daily
      - monthly
      - weekly
  password:
    description:
      - BIG-IP password
    required: true
  server:
    description:
      - BIG-IP host
    required: true
  server_port:
    description:
      - BIG-IP server port
    required: false
    default: 443
  user:
    description:
      - BIG-IP username
    required: true
    aliases:
      - username
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
  - Requires the f5-sdk Python package on the host This is as easy as pip
    install f5-sdk
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

try:
    from f5.bigip import ManagementRoot
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


AUTOCHECK = ['disabled', 'enabled']
FREQ = ['daily', 'monthly', 'weekly']


class BigIpSoftwareUpdate(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def update(self):
        changed = False
        current = self.read()

        if self.params['auto_check']:
            if self.params['auto_check'] != current['autoCheck']:
                changed = True
        else:
            del self.params['auto_check']

        if self.params['frequency']:
            if self.params['frequency'] != current['frequency']:
                changed = True
        else:
            del self.params['frequency']

        if self.params['check_mode']:
            return changed

        r = self.api.tm.sys.software.update.load()
        r.update(**self.params)

        return True

    def read(self):
        r = self.api.tm.sys.software.update.load()
        return r

    def flush(self):
        changed = self.update()
        current = self.read()
        result.update(**current)

        result.update(dict(changed=changed))
        return result


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        auto_check=dict(required=False, default=None, choices=AUTOCHECK),
        frequency=dict(required=False, default=None, choices=FREQ),
        state=dict(default='present', choices=['present'])
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpSoftwareUpdate(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
