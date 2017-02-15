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
module: bigip_provision
short_description: Manage BIG-IP module provisioning
description:
  - Manage BIG-IP module provisioning. This module will only provision at the
    standard levels of Dedicated, Nominal, and Minimum. While iControl SOAP
    additionally supports a Custom level, this level is not supported by this
    module.
version_added: "2.3"
options:
  module:
    description:
      - The module to provision in BIG-IP.
    required: true
    choices:
      - afm
      - am
      - sam
      - asm
      - avr
      - fps
      - gtm
      - lc
      - ltm
      - pem
      - swg
  level:
    description:
      - Sets the provisioning level for the requested modules. Changing the
        level for one module may require modifying the level of another module.
        For example, changing one module to C(dedicated) requires setting all
        others to C(none). Setting the level of a module to C(none) means that
        the module is not run.
    required: false
    default: nominal
    choices:
      - dedicated
      - nominal
      - minimum
  state:
    description:
      - The state of the provisioned module on the system. When C(present),
        guarantees that the specified module is provisioned at the requested
        level provided that there are sufficient resources on the device (such
        as physical RAM) to support the provisioned module. When C(absent),
        unprovisions the module.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
requirements:
  - f5-sdk
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Provision PEM at "nominal" level
  bigip_provision:
      server: "lb.mydomain.com"
      module: "pem"
      level: "nominal"
      password: "secret"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost

- name: Provision a dedicated SWG. This will unprovision every other module
  bigip_provision:
      server: "lb.mydomain.com"
      module: "swg"
      password: "secret"
      level: "dedicated"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost
'''

try:
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


class BigIpRest():
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/sys/db/%s' % (self._hostname, self._key)
        self._headers = {
            'Content-Type': 'application/json'
        }

    def read(self):
        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return {}
        else:
            return resp.json()

    def present(self):
        changed = False
        current = self.read()

        if current and current['name'] == self._key:
            if current['value'] != self._value:
                resp = requests.put(self._uri,
                                    auth=(self._username, self._password),
                                    data=json.dumps(self._payload),
                                    verify=self._validate_certs)
                if resp.status_code == 200:
                    changed = True
                else:
                    raise Exception('Failed to set the provided key')

        return changed


def main():
    changed = False

    module_choices = [
        'afm', 'am', 'sam', 'asm', 'avr', 'fps',
        'gtm', 'lc', 'ltm', 'pem', 'swg'
    ]

    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True),
            module=dict(required=True, choices=module_choices),
            level=dict(default='nominal', choices=['nominal', 'dedicated', 'minimal']),
            password=dict(default='admin'),
            state=dict(default='present', choices=['present', 'reset']),
            user=dict(default='admin'),
            validate_certs=dict(default='yes', type='bool', choices=['yes', 'no']),
        )
    )

    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')

    try:
        if connection == 'icontrol':
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            icontrol = test_icontrol(username, password, hostname)
            if icontrol:
                obj = BigIpIControl(module)
        elif connection == 'rest':
            if not requests_found:
                raise Exception("The python requests module is required")

            obj = BigIpRest(module)

        if state == "present":
            if obj.present():
                changed = True
        elif state == "absent":
            if obj.absent():
                changed = True
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except socket.timeout:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except bigsuds.ConnectionError as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
