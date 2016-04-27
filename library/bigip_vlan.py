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
module: bigip_vlan
short_description: Manage VLANs on a BIG-IP system
description:
   - Manage VLANs on a BIG-IP system
version_added: "2.2"
options:
  description:
    description:
      - The description to give to the VLAN
    required: false
    default: None
  interface:
    description:
      - The interface to create the VLAN on when C(state) is C(present)
  interfaces:
    description:
      - Specifies a list of tagged or untagged interfaces and trunks that you
        want to configure for the VLAN. Use tagged interfaces or trunks when
        you want to assign a single interface or trunk to multiple VLANs.
    required: false
    dfault: None
  name:
    description:
      - The VLAN to manage. If the special VLAN C(ALL) is specified with
        the C(state) value of C(absent) then all VLANs will be removed.
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  route_domain:
    description:
      - The route domain that the VLAN is associated with if something other
        than Common
    required: false
    default: None
  server:
    description:
      - BIG-IP host
    required: true
  state:
    description:
      - The state of the VLAN on the system. When C(present), guarantees
        that the VLAN exists with the provided attributes. When C(absent),
        removes the VLAN from the system.
    required: false
    default: present
    choices:
      - absent
      - present
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
  vlan_id:
    description:
      - The ID (tag) of the VLAN
    required: true
    aliases:
      - tag
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk
  - Requires BIG-IP versions >= 11.6.0
requirements:
  - f5-sdk
author:
  - Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = '''
'''

from f5.bigip import BigIP


class F5ModuleError(Exception):
    pass


class BigIpVlan(BigIpCommon):
    def __init__(self, *args, **kwargs):
        if not f5sdk_found:
            raise F5ModuleError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = BigIP(kwargs['server'],
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
        self.api.net.vlans.vlan.delete(
            name=self.params['name']
        )

    def exists(self):
        return self.api.net.vlans.vlan.exists(
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
        description=dict(required=False, default=None),
        interface=dict(required=False, default=None),
        interfaces=dict(required=False, default=None),
        name=dict(required=True, default=None),
        route_domain=dict(required=False, default=None),
        vlan_id=dict(required=False, default=None, aliases=['tag'])
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ['interface', 'interfaces']
        ]
    )

    try:
        obj = BigIpVlan(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError, e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
