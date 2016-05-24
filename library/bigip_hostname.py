#!/usr/bin/python
# -*- coding: utf-8 -*-
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
version_added: "2.2"
options:
  hostname:
    description:
      - Hostname of the BIG-IP host
    required: true
  server:
    description:
      - BIG-IP host
    required: true
  password:
    description:
      - BIG-IP password
    required: true
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
- name: Set the hostname of the BIG-IP
  bigip_hostname:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      name: "bigip.localhost.localdomain"
  delegate_to: localhost
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
        if not self.exists():
            return False

        r = self.api.tm.sys.global_settings.load()
        r.update(hostname=self.params['hostname'])

        if self.exists():
            return True
        else:
            raise F5SDKError("Failed to set the hostname")

    def exists(self):
        current = self.read()
        if self.params['hostname'] == current:
            return True
        else:
            return False

    def present(self):
        return self.update()

    def read(self):
        r = self.api.sys.global_settings.load()
        return r['hostname']

    def flush(self):
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

        result.update(dict(changed=changed))
        return result


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
        obj = BigIpHostname(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
