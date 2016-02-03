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
  name:
    description:
      - Name of the host
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
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds

requirements: [ "bigsuds", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
- name: Set the hostname of the BIG-IP
  bigip_hostname:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      name: "bigip.localhost.localdomain"
  delegate_to: localhost
"""

import socket

try:
    import bigsuds
except ImportError:
    bigsuds_found = False
else:
    bigsuds_found = True

try:
    import json
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
        self._name = module.params.get('name')
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
        result = None

        try:
            result = self.api.System.Inet.get_hostname()
        except bigsuds.ServerError:
            pass

        return result

    def run(self):
        current = self.read()
        if current == self._name:
            return False

        self.api.System.Inet.set_hostname(hostname=self._name)
        return True


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/sys/global-settings' % (self._hostname)
        self._headers = {
            'Content-Type': 'application/json'
        }
        self._payload = {
            'hostname': self._name
        }

    def read(self):
        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return {}
        else:
            return resp.json()['hostname']

    def run(self):
        changed = False
        current = self.read()

        if current == self._name:
            return False

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


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(default='icontrol', choices=['icontrol', 'rest']),
            server=dict(required=True),
            name=dict(required=True),
            password=dict(required=True),
            user=dict(required=True, aliases=['username']),
            validate_certs=dict(default='yes', type='bool')
        )
    )

    connection = module.params.get('connection')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')

    try:
        if connection == 'icontrol':
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            test_icontrol(username, password, hostname)
            obj = BigIpIControl(module)
        elif connection == 'rest':
            if not requests_found:
                raise Exception("The python requests module is required")

            obj = BigIpRest(module)

        if obj.run():
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
