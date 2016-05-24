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
module: bigip_selfip
short_description: Manage Self-IPs on a BIG-IP system
description:
  - Manage Self-IPs on a BIG-IP system
version_added: "2.2"
options:
  address:
    description:
      - The IP addresses for the new self IP
    required: true
  floating_state:
    description:
      - The floating attributes of the self IPs.
    default: disabled
    required: false
    choices:
      - enabled
      - disabled
  name:
    description:
      - The self IP to create
    required: false
    default: Value of C(address)
  netmask:
    description:
      - The netmasks for the self IP
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  server:
    description:
      - BIG-IP host
    required: true
  state:
    description:
      - The state of the variable on the system. When C(present), guarantees
        that the Self-IP exists with the provided attributes. When C(absent),
        removes the floating IP from the system.
    required: false
    default: present
    choices:
      - absent
      - present
  traffic_group:
    description:
      - The traffic group for the self IP addresses in an active-active,
        redundant load balancer configuration
    required: false
  user:
    description:
      - BIG-IP username
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
  vlan:
    description:
      - The VLAN that the new self IPs will be on
    required: true
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk
  - Requires the netaddr Python package on the host
requirements:
  - netaddr
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

# import netaddr
# TODO(Add verification of IP addrs)


class F5ModuleError(Exception):
    pass


class BigIpSelfIp(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def absent(self):
        if not self.exists():
            return False

        if self.params['check_mode']:
            return True

        self.delete()

        if self.exists():
            raise F5ModuleError("Failed to delete the self IP")
        else:
            return True

    def present(self):
        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True
            return self.create()

    def create(self):
        pass

    def delete(self):
        return self.api.net.selfips.selfip.delete(
            name=self.params['name']
        )

    def exists(self):
        return self.api.net.selfips.selfip.exists(
            name=self.params['name']
        )

    def flush(self):
        current = self.read()

        if self.params['check_mode']:
            if value == current:
                changed = False
            else:
                changed = True
        else:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
            current = self.read()
            result.update(current)

        result.update(dict(changed=changed))
        return result


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        address=dict(required=True, default=None),
        floating_state=dict(required=False, default='disabled'),
        name=dict(required=False, default=None),
        netmask=dict(required=True),
        traffic_group=dict(required=True),
        vlan=dict(required=True)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpSelfIp(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
