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

DOCUMENTATION = '''
---
module: bigip_hostname
short_description: Manage the hostname of a BIG-IP
description:
  - Manage the hostname of a BIG-IP
version_added: "2.3"
options:
  hostname:
    description:
      - Hostname of the BIG-IP host
    required: true
notes:
  - Requires the f5-sdk Python package on the host This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Set the hostname of the BIG-IP
  bigip_hostname:
      hostname: "bigip.localhost.localdomain"
      password: "admin"
      server: "bigip.localhost.localdomain"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''
hostname:
    description: The new hostname of the device
    returned: changed
    type: string
    sample: "big-ip01.internal"
'''

try:
    from f5.bigip import ManagementRoot
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


class BigIpHostname(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def update(self):
        if self.exists():
            return False

        r = self.api.tm.sys.global_settings.load()
        r.update(hostname=self.params['hostname'])

        if self.exists():
            return True
        else:
            raise F5ModuelError("Failed to set the hostname")

    def exists(self):
        current = self.read()
        if self.params['hostname'] == current:
            return True
        else:
            return False

    def present(self):
        return self.update()

    def read(self):
        r = self.api.tm.sys.global_settings.load()
        return r.hostname

    def flush(self):
        result = dict()
        current = self.read()

        if self.params['check_mode']:
            if self.params['hostname'] == current:
                changed = False
            else:
                changed = True
        else:
            changed = self.present()
            current = self.read()
            result.update(hostname=current)

        if changed:
            self.save_running_config()

        result.update(dict(changed=changed))
        return result

    def save_running_config(self):
        self.api.tm.sys.config.exec_cmd('save')


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        hostname=dict(required=True, default=None),
        state=dict(required=False, choices=['present'])
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpHostname(check_mode=module.check_mode, **module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
