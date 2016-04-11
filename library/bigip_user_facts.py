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
module: bigip_user_facts
short_description: Retrieve user account attributes from a BIG-IP
description:
   - Retrieve user account attributes from a BIG-IP
version_added: "2.0"
options:
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: rest
    choices:
      - rest
      - icontrol
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
  name:
    description:
      - Name of the user to retrieve facts for
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true

notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds
   - Facts are placed in the C(bigip) variable

requirements: [ "bigsuds", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = '''
- name: Gather facts about user 'johnd'
  bigip_user_facts:
      server: "big-ip"
      user: "admin"
      password: "my_password"
      name: "johnd"
  delegate_to: localhost
- debug: var=bigip
'''

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


class BigIpCommon(object):
    def __init__(self, module):
        self._user = module.params.get('user')
        self._password = module.params.get('password')
        self._server = module.params.get('server')

        self._name = module.params.get('name')

        self._validate_certs = module.params.get('validate_certs')


class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._server,
            username=self._user,
            password=self._password,
            debug=True
        )
        self._all_partition = '[All]'
        self._admin_role = 'USER_ROLE_ADMINISTRATOR'

        self._role_map = {
            'USER_ROLE_ACCELERATION_POLICY_EDITOR': 'acceleration-policy-editor',
            'USER_ROLE_ADMINISTRATOR': 'admin',
            'USER_ROLE_APPLICATION_EDITOR': 'application-editor',
            'USER_ROLE_AUDITOR': 'auditor',
            'USER_ROLE_CERTIFICATE_MANAGER': 'certificate-manager',
            'USER_ROLE_GUEST': 'guest',
            'USER_ROLE_IRULE_MANAGER': 'irule-manager',
            'USER_ROLE_MANAGER': 'manager',
            'USER_ROLE_INVALID': 'no-access',
            'USER_ROLE_TRAFFIC_MANAGER': 'operator',
            'USER_ROLE_RESOURCE_ADMINISTRATOR': 'resource-admin',
            'USER_ROLE_USER_MANAGER': 'user-manager',
            'USER_ROLE_ASM_POLICY_EDITOR': 'web-application-security-administrator',
            'USER_ROLE_ASM_EDITOR': 'web-application-security-editor'
        }
        self._shell_map = {
            '/bin/bash': 'bash',
            '/sbin/nologin': 'none',
            '/usr/bin/tmsh': 'tmsh'
        }

    def get_description(self):
        resp = self.api.Management.UserManagement.get_description([self._name])
        return resp[0]

    def get_encrypted_password(self):
        resp = self.api.Management.UserManagement.get_encrypted_password([self._name])
        return resp[0]

    def get_login_shell(self):
        resp = self.api.Management.UserManagement.get_login_shell([self._name])

        if resp[0] in self._shell_map:
            shell = resp[0]
            return self._shell_map[shell]
        else:
            return 'none'

    def get_user_permission(self):
        result = {}
        resp = self.api.Management.UserManagement.get_user_permission([self._name])
        for part in resp[0]:
            _partition = part['partition']
            _role = part['role']

            if _partition == self._all_partition:
                _partition = 'all-partitions'

            role = self._role_map[_role]

            result[_partition] = role
        return result

    def exists(self):
        resp = self.api.Management.UserManagement.get_list()
        for user in resp:
            if user['name'] == self._name:
                return True
        return False

    def facts(self):
        result = {}

        try:
            result['user'] = self._name
            result['description'] = self.get_description()
            result['password'] = self.get_encrypted_password()
            result['partition_access'] = self.get_user_permission()
            result['shell'] = self.get_login_shell()
        except bigsuds.ServerError:
            return {}

        return result


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/auth/user' % (self._server)
        self._headers = {
            'Content-Type': 'application/json'
        }
        self._all_partition = 'all-partitions'

    def facts(self):
        result = {}
        tmp = {}
        url = "%s/%s" % (self._uri, self._name)
        resp = requests.get(url,
                            auth=(self._user, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return {}
        else:
            res = resp.json()

            result['user'] = self._name

            if 'description' in res:
                result['description'] = res['description']
            else:
                result['description'] = ''

            if 'encryptedPassword' in res:
                result['password'] = res['encryptedPassword']
            else:
                result['password'] = ''

            if 'shell' in res:
                result['shell'] = res['shell']
            else:
                result['shell'] = 'none'

            if 'partitionAccess' in res:
                for part in res['partitionAccess']:
                    partition = part['name']
                    role = part['role']
                    tmp[partition] = role

            result['partition_access'] = tmp

            return result

    def exists(self):
        url = "%s/%s" % (self._uri, self._name)
        resp = requests.get(url,
                            auth=(self._user, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return False
        else:
            return True


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(default='rest', choices=['icontrol', 'rest']),
            server=dict(required=True),
            password=dict(require=True),
            user=dict(required=True, aliases=['username']),
            name=dict(required=True),
            validate_certs=dict(default='yes', type='bool', choices=BOOLEANS)
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

            icontrol = test_icontrol(username, password, hostname)
            if icontrol:
                obj = BigIpIControl(module)
        elif connection == 'rest':
            if not requests_found:
                raise Exception("The python requests module is required")

            obj = BigIpRest(module)

        if obj.exists():
            uservars = dict(bigip=obj.facts())
            module.exit_json(changed=changed, ansible_facts=uservars)
        else:
            module.fail_json(msg='The specified username was not found')
    except bigsuds.ConnectionError, e:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except socket.timeout, e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except bigsuds.ConnectionError, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
