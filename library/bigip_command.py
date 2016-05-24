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
    exist on the remote BIG-IP. Additionally, this module can detect the presence
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
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
  - Requires the paramiko Python package on the ansible host. This is as easy
    as pip install paramiko
requirements:
  - paramiko
  - requests
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Load the default system configuration
  bigip_command:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      command: "tmsh load sys config default"
      validate_certs: "no"
  delegate_to: localhost
'''

RETURN = '''
stdout:
    description: The stdout output from running the given command
    returned: changed
    type: string
    sample: ""
stderr:
    description: The stderr output from running the given command
    returned: changed
    type: string
command:
    description: The command specified by the user
    returned: changed
    type: string
    sample: "tmsh list auth user"
app_mode:
    description: Whether or not Appliance mode was detected for the user
    returned: changed
    type: boolean
    sample: True
app_mode_cmd:
    description: The command as it would have been run in Appliance mode
    returned: changed
    type: string
    sample: "list auth user"
'''

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
    def __init__(self, *args, **kwargs):
        self.result = dict(changed=False, changes=dict())
        self.params = kwargs

    def appliance_mode(self):
        user = self.params['user']
        server = self.params['server']
        password = self.params['password']
        validate_certs = self.params['validate_certs']

        uri = 'https://%s/mgmt/tm/auth/user/%s' % (server, user)
        headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.get(uri,
                            auth=(user, password),
                            verify=validate_certs,
                            headers=headers)

        if resp.status_code != 200:
            raise Exception('Failed to query the REST API to check appliance mode')
        else:
            result = resp.json()
            if 'shell' in result and result['shell'] == 'tmsh':
                return True
            else:
                return False


class BigIpSsh(BigIpCommon):
    def __init__(self, *args, **kwargs):
        super(BigIpSsh, self).__init__(*args, **kwargs)

        self.result = {}
        self.api = paramiko.SSHClient()

        user = self.params['user']
        password = self.params['password']
        server = self.params['server']
        validate_certs = self.params['validate_certs']

        if not validate_certs:
            self.api.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.api.connect(server, username=user, password=password)

    def flush(self):
        result = {}

        command = self.params['command']

        # Appliance mode drops the user directly into tmsh, so any leading tmsh
        # syntax can be removed from the provided command
        if self.appliance_mode():
            result['app_mode'] = True

            if command[0:4] == 'tmsh':
                cmd = command[4:].strip()
                result['app_mode_cmd'] = cmd
            else:
                cmd = command
        else:
            # If the user has some BIG-IPs that are in Appliance Mode and some
            # that are not, then it may be necessary to add the non-app mode
            # syntax to the command before it is executed.
            result['app_mode'] = False

            if command[0:4] != 'tmsh':
                cmd = 'tmsh ' + command
            else:
                cmd = command

        stdin, stdout, stderr = self.api.exec_command(cmd)

        result['stdout'] = ''.join(stdout.readlines())
        result['stderr'] = ''.join(stderr.readlines())
        result['command'] = command
        result['changed'] = True

        return result


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        command=dict(required=True)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    try:
        if not paramiko_found:
            raise Exception("The python paramiko module is required")

        if not requests_found:
            raise Exception("The python requests module is required")

        obj = BigIpSsh(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except socket.timeout:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except socket.gaierror:
        module.fail_json(msg="Unable to contact the BIG-IP")
    except paramiko.ssh_exception.SSHException as e:
        if 'No existing session' in str(e):
            module.fail_json(msg='Could not log in with provided credentials')
        else:
            module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
