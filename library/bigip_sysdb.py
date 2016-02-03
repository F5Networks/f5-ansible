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
module: bigip_sysdb
short_description: Manage BIG-IP system database variables
description:
   - Manage BIG-IP system database variables
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
  key:
    description:
      - The database variable to manipulate
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  state:
    description:
      - The state of the variable on the system. When C(present), guarantees
        that an existing variable is set to C(value). When C(reset) sets the
        variable back to the default value. At least one of value and state
        C(reset) are required.
    required: false
    default: present
    choices: [ "present", "reset" ]
  user:
    description:
      - BIG-IP username
    required: true
    aliases:
      - username
  value:
    description:
      - The value to set the key to. At least one of value and state C(reset) are required.
    required: false
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true

notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds

requirements: [ "bigsuds", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
- name: Set the boot.quiet DB variable on the BIG-IP
  bigip_sysdb:
      server: "big-ip"
      key: "boot.quiet"
      value: "disable"
  delegate_to: localhost

- name: Disable the initial setup screen
  bigip_sysdb:
      server: "big-ip"
      key: "setup.run"
      value: "false"
  delegate_to: localhost

- name: Reset the initial setup screen
  bigip_sysdb:
      server: "big-ip"
      key: "setup.run"
      state: "reset"
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
    api = bigsuds.BIGIP(
        hostname=hostname,
        username=username,
        password=password,
        debug=True
    )

    try:
        response = api.Management.LicenseAdministration.get_license_activation_status()
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

        self._key = module.params.get('key')
        self._value = module.params.get('value')
        self._validate_certs = module.params.get('validate_certs')


class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )

    def read(self):
        try:
            response = self.api.Management.DBVariable.query(
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
                    self.api.Management.DBVariable.modify(
                        variables=[params]
                    )
                    changed = True
                except Exception, err:
                    raise Exception(err)

        return changed

    def reset(self):
        changed = False

        try:
            self.api.Management.DBVariable.reset(
                variables=[self._key]
            )
            changed = True
        except Exception, err:
            raise Exception(err)

        return changed


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/sys/db/%s' % (self._hostname, self._key)
        self._headers = {
            'Content-Type': 'application/json'
        }
        self._payload = {
            'value': self._value
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
                    res = resp.json()
                    raise Exception(res['message'])

        return changed

    def reset(self):
        changed = False
        current = self.read()

        if current and current['name'] == self._key:
            default = current['defaultValue']
            if current['value'] != default:
                payload = {
                    'value': default
                }
                resp = requests.put(self._uri,
                                    auth=(self._username, self._password),
                                    data=json.dumps(payload),
                                    verify=self._validate_certs)
                if resp.status_code == 200:
                    changed = True
                else:
                    res = resp.json()
                    raise Exception(res['message'])
        else:
            raise Exception('The given key does not exist to reset')

        return changed


def main():
    changed = False
    icontrol = False

    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(default='rest', choices=['icontrol', 'rest']),
            server=dict(required=True),
            key=dict(required=True),
            password=dict(required=True),
            state=dict(default='present', choices=['present', 'reset']),
            user=dict(required=True, aliases=['username']),
            validate_certs=dict(default='yes', type='bool'),
            value=dict(required=False, default=None)
        )
    )

    connection = module.params.get('connection')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')
    value = module.params.get('value')

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

        if not state == 'reset' and not value:
            module.fail_json(msg="Neither 'state' equal to 'reset' nor 'value' set")

        if state == "present":
            if obj.present():
                changed = True
        elif state == "reset":
            if obj.reset():
                changed = True
    except bigsuds.ConnectionError, e:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except socket.timeout, e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except Exception, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
