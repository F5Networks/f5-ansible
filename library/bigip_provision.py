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
module: bigip_provision
short_description: Manage BIG-IP module provisioning
description:
   - Manage BIG-IP module provisioning. This module will only provision at the
     standard levels of Dedicated, Nominal, and Minimum. While iControl SOAP
     additionally supports a Custom level, this level is not supported by this
     module.
version_added: "2.0"
options:
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: rest
    choices: [ "rest", "icontrol" ]
  server:
    description:
      - BIG-IP host
    required: true
  module:
    description:
      - The module to provision in BIG-IP
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
  password:
    description:
      - BIG-IP password
    required: true
    default: admin
  level:
    description:
      - Sets the provisioning level for the requested modules. Changing the
        level for one module may require modifying the level of another module.
        For example, changing one module to C(dedicated) requires setting all
        others to C(none). Setting the level of a module to C(none) means that
        the module is not run.
    required: false
    default: nominal
    choices: [ "dedicated", "nominal", "minimum" ]
  user:
    description:
      - BIG-IP username
    required: false
    default: admin
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: yes
    choices: [ "yes", "no" ]
  state:
    description:
      - The state of the provisioned module on the system. When C(present),
        guarantees that the specified module is provisioned at the requested
        level provided that there are sufficient resources on the device (such
        as physical RAM) to support the provisioned module. When C(absent),
        unprovisions the module.
    required: false
    default: present
    choices: [ "present", "absent" ]

notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds

requirements: [ "bigsuds", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
- name: Provision PEM at "nominal" level
  bigip_provision:
      server: "big-ip"
      module: "pem"
      level: "nominal"
  delegate_to: localhost

- name: Provision a dedicated SWG. This will unprovision every other module
  bigip_provision:
      server: "big-ip"
      module: "swg"
      level: "dedicated"
  delegate_to: localhost
"""

import json
import socket

try:
    import bigsuds
except ImportError:
    bigsuds_found = False
else:
    bigsuds_found = True

try:
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True

def test_icontrol(username, password, hostname):
    client = bigsuds.BIGIP(
        hostname=hostname,
        username=username,
        password=password,
        debug=True
    )

    try:
        response = client.Management.LicenseAdministration.get_license_activation_status()
        if 'STATE' in response:
            return True
        else:
            return False
    except:
        return False

class BigIpCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._hostname = module.params.get('server')

        self._level = module.params.get('level')
        self._module = module.params.get('module')
        self._validate_certs = module.params.get('validate_certs')

        # Check if we can connect to the device
        sock = socket.create_connection((self._hostname,443), 60)
        sock.close()

class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self._client = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )
        module_map = {
            'afm': 'TMOS_MODULE_AFM',
            'am': 'TMOS_MODULE_AM',
            'sam': 'TMOS_MODULE_SAM',
            'asm': 'TMOS_MODULE_ASM',
            'avr': 'TMOS_MODULE_AVR',
            'fps': 'TMOS_MODULE_FPS',
            'gtm': 'TMOS_MODULE_GTM',
            'lc': 'TMOS_MODULE_LC',
            'ltm': 'TMOS_MODULE_LTM',
            'pem': 'TMOS_MODULE_PEM',
            'swg': 'TMOS_MODULE_SWG'
        }
        level_map = {
            'PROVISION_LEVEL_NONE',
            'PROVISION_LEVEL_NOMINAL',
            'PROVISION_LEVEL_MINIMAL',
            'PROVISION_LEVEL_DEDICATED'
        }

    def exists(self):
        try:
            response = self._client.Management.Provision.get_level(
                moduless=[self._module]
            )
        except bigsuds.ServerError:
            return False

    def read(self):
        try:
            response = self._client.Management.DBVariable.query(
                variables=[self._key]
            )
        except bigsuds.ServerError:
            return {}

        return response[0]

    def present(self):
        changed = False
        current = self.read()

        if current and current['name'].lower() == self._key:
            if current['value'] != self._value:
                try:
                    params = dict(
                        name=self._key,
                        value=self._value
                    )
                    self._client.Management.DBVariable.modify(
                        variables=[params]
                    )
                    changed = True
                except:
                    raise Exception('Failed to set the provided key')

        return changed


class BigIpRest(BigIpCommon):
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
    icontrol = False

    module_choices = [
        'afm', 'am', 'sam', 'asm', 'avr', 'fps',
        'gtm', 'lc', 'ltm', 'pem', 'swg'
    ]

    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(default='rest', choices=['icontrol', 'rest']),
            server=dict(required=True),
            module=dict(required=True, choices=module_choices),
            level=dict(default='nominal', choices=['nominal', 'dedicated', 'minimal']),
            password=dict(default='admin'),
            state=dict(default='present', choices=['present', 'reset']),
            user=dict(default='admin'),
            validate_certs=dict(default='yes', type='bool', choices=['yes', 'no']),
        )
    )

    connection = module.params.get('connection')
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
    except bigsuds.ConnectionError, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
