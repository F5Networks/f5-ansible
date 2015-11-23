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
module: bigip_command
short_description: Run commands on a BIG-IP via tmsh
description:
   - Run commands on a BIG-IP via tmsh. This module is similar to the ansible
     C(command) module, but specifically supports all BIG-IPs via the paramiko
     python extension. For some operations on the BIG-IP, there is not a SOAP
     or REST endpoint that is available and the operation can only be accomplished
     via C(tmsh). The Ansible C(command) module should be able to perform this,
     however, older releases of BIG-IP do not have sufficient python versions
     to support Ansible. By using this module, there is no need for python to
     exist on the remote BIG-IP. Additionally, this module can detect the prescence
     of Appliance Mode on a BIG-IP and adjust the provided command to take this
     feature into account. Finally, the output of this module provides more
     Ansible-friendly data formats than could be accomplished by the C(command)
     module alone.
version_added: "2.0"
options:
  server:
    description:
      - BIG-IP host
    required: true
  command:
    description:
      - tmsh command to run on the remote host
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  user:
    description:
      - BIG-IP username
    required: false
    aliases:
      - username
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true

notes:
   - Requires the paramiko Python package on the ansible host. This is as easy
     as pip install paramiko

requirements: [ "paramiko", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
- name: Set the hostname of the BIG-IP
  bigip_command:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      command: "tmsh load sys config default"
  delegate_to: localhost
"""

import socket

try:
    import paramiko
except ImportError:
    paramiko_found = False
else:
    paramiko_found = True

try:
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True

class BigIpCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._hostname = module.params.get('server')
        self._command = module.params.get('command').strip()
        self._validate_certs = module.params.get('validate_certs')

        # Check if we can connect to the device
        sock = socket.create_connection((self._hostname,443), 60)
        sock.close()

    def appliance_mode(self):
        self._uri = 'https://%s/mgmt/tm/auth/user/%s' % (self._hostname, self._username)
        self._headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            raise Exception('Failed to query the REST API to check appliance mode')
        else:
            result = resp.json()
            if result['shell'] == 'tmsh':
                return True
            else:
                return False


class BigIpSsh(BigIpCommon):
    def __init__(self, module):
        super(BigIpSsh, self).__init__(module)

        self.result = {}
        self.api = paramiko.SSHClient()

        if not self._validate_certs:
            self.api.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.api.connect(self._hostname, username=self._username, password=self._password)

    def run(self):
        result = {}

        # Appliance mode drops the user directly into tmsh, so any leading tmsh
        # syntax can be removed from the provided command
        if self.appliance_mode():
            result['app_mode'] = True

            if self._command[0:4] == 'tmsh':
                cmd = self._command[4:].strip()
                result['app_mode_cmd'] = cmd
            else:
                cmd = self._command
        else:
            # If the user has some BIG-IPs that are in Appliance Mode and some
            # that are not, then it may be necessary to add the non-app mode
            # syntax to the command before it is executed.
            result['app_mode'] = False

            if self._command[0:4] != 'tmsh':
                cmd = 'tmsh ' + self._command
            else:
                cmd = self._command

        stdin, stdout, stderr = self.api.exec_command(cmd)

        result['stdout'] = stdout.readlines()
        result['stderr'] = stderr.readlines()
        result['command'] = self._command
        result['changed'] = True

        self.result = result
        return True


def main():
    changed = False

    module = AnsibleModule(
        argument_spec = dict(
            server=dict(required=True),
            command=dict(required=True),
            password=dict(required=True),
            user=dict(required=True, aliases=['username']),
            validate_certs=dict(default='yes', type='bool')
        )
    )

    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')

    try:
        if not paramiko_found:
            raise Exception("The python paramiko module is required")

        if not requests_found:
            raise Exception("The python requests module is required")

        obj = BigIpSsh(module)
        if obj.run():
            result = obj.result
            module.exit_json(**result)
    except socket.timeout, e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except paramiko.ssh_exception.SSHException, e:
        if 'No existing session' in str(e):
            module.fail_json(msg='Could not log in with provided credentials')
        else:
            module.fail_json(msg=str(e))
    except Exception, e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
