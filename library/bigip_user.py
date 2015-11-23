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
module: bigip_user
short_description: Manage user accounts and user attributes on a BIG-IP
description:
   - Manage user accounts and user attributes on a BIG-IP
version_added: "2.0"
options:
  append:
    description:
      - If C(yes), will only add groups, not set them to just the list
        in groups.
    choices:
      - yes
      - no
    default: no
  comment:
    description:
      - Optionally sets the description (aka GECOS) of user account.
    required: false
  login_host:
    description:
      - BIG-IP host
    required: true
  login_password:
    description:
      - BIG-IP password
    required: true
  login_user:
    description:
      - BIG-IP username
    required: true
  name:
    description:
      - Name of the user to create, remove or modify.
    required: true
    aliases:
      - user
  password:
    description:
      - Optionally set the user's password to this crypted value. The password
        should be encrypted using crypt(3).
    required: false
  shell:
    description:
      - Optionally set the user's shell.
    required: false
    default: None
    choices:
      - bash
      - none
      - tmsh
  partition_access:
    description:
      - Specifies the administrative partition to which the user has access.
        The module will correctly adjust the specified partition if you specify
        a role that is required to be in the "all" partition.
    required: false
    default: Common
    choices:
      - all
      - Common
      - [name]
    aliases:
      - partition
  role:
    description:
      - Specifies the user role that you want to assign to the user account. For
        the given partition. Use the value C(no-access) to indicate that you do
        not want to assign a user role to the user account.
    required: false
    default: None
    choices:
      - acceleration-policy-editor
      - admin
      - application-editor
      - auditor
      - certificate-manager
      - guest
      - irule-manager
      - manager
      - no-access
      - operator
      - resource-admin
      - user-manager
      - web-application-security-administrator
      - web-application-security-editor
  state:
    description:
      - Whether the account should exist or not, taking action if the state is
        different from what is stated.
    required: false
    default: present
    choices:
      - present
      - absent
      - reset-login
  update_password:
    description:
      - C(always) will update passwords if they differ. C(on_create) will only
        set the password for newly created users.
    required: false
    default: always
    choices:
      - always
      - on_create
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
- name: Add the user 'johnd' with a specific role on the provided partition
  bigip_user:
      login_host: "big-ip"
      login_user: "admin"
      login_password: "my_password"
      name: "johnd"
      comment: "John Doe"
      role: "admin"
      state: "present"
  delegate_to: localhost

- name: Change the user "johnd's" role and shell
  bigip_user:
      login_host: "big-ip"
      login_user: "admin"
      login_password: "my_password"
      name: "johnd"
      comment: "John Doe"
      role: "manager"
      shell: "tmsh"
      state: "present"
  delegate_to: localhost

- name: Make the user 'johnd' an admin and set to advanced shell
  bigip_user:
      login_host: "big-ip"
      login_user: "admin"
      login_password: "my_password"
      name: "johnd"
      comment: "John Doe"
      role: "admin"
      shell: "bash"
      state: "present"
  delegate_to: localhost

- name: Remove the user 'johnd'
  bigip_user:
      login_host: "big-ip"
      login_user: "admin"
      login_password: "my_password"
      name: "johnd"
      state: "absent"
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


class AdminRoleNoModifyError(Exception):
    pass

class CurrentUserNoRoleModifyError(Exception):
    pass

class CreateUserError(Exception):
    pass

class DeleteUserError(Exception):
    pass

class CustomShellError(Exception):
    pass

class UnlicensedError(Exception):
    pass

class BigIpCommon(object):
    def __init__(self, module):
        self._login_user = module.params.get('login_user')
        self._login_password = module.params.get('login_password')
        self._login_host = module.params.get('login_host')

        self._comment = module.params.get('comment')
        self._name = module.params.get('name')
        self._password = module.params.get('password')
        self._shell = module.params.get('shell')
        self._partition_access = module.params.get('partition_access')

        self._append = module.params.get('append')
        self._current = {}
        self._role_default = 'no-access'

        self._role = module.params.get('role')
        self._update_password = module.params.get('update_password')
        self._validate_certs = module.params.get('validate_certs')

        self._required_all_partitions = [
            'resource-admin', 'auditor', 'admin',
            'web-application-security-administrator', 'no-access'
        ]
        self._can_have_advanced_shell = ['admin', 'resource-admin']

        # The system requires that certain roles be listed in the 'all'
        # partition. So this conditional changes the specified partition
        # to be accurate in case the user does not know of this constraint
        if self._role in self._required_all_partitions:
            self._partition_access = 'all'

        # Check if we can connect to the device
        sock = socket.create_connection((self._login_host,443), 60)
        sock.close()

    def can_have_advanced_shell(self):
        roles = []
        can_have_advanced = ['resource-admin', 'admin']

        pa = self._current['partitionAccess']
        if self._role:
            roles.append(self._role)
        roles = set([ p['role'] for p in pa ])

        found = [ x for x in roles if x in can_have_advanced ]
        if len(found) > 0:
            return True
        else:
            return False

    def _determine_updates(self):
        result = {
            'comment': False,
            'password': False,
            'shell': False
        }
        current = self.read()

        if self._comment:
            if current['description'] != self._comment:
                result['comment'] = True

        if self._password and self._update_password == 'always':
            if current['password'] != self._password:
                result['password'] = True

        if self._shell:
            if self._shell == 'bash':
                if not self.can_have_advanced_shell():
                    raise CustomShellError()

            if 'shell' not in current:
                result['shell'] = True
            elif self._shell == current['shell']:
                result['shell'] = False
            else:
                result['shell'] = True

        return result

    def _determine_user_permissions(self, role):
        changed = False
        result = []

        pa = self._current['partitionAccess']
        roles = set([ p['role'] for p in pa ])

        # These roles affect all partitions. There can be no other roles
        # assigned to any other partitions if they are set.
        #
        # Likewise, if the specified role is being placed in the 'all' partition
        # then existing permissions must be cleared
        if role in self._required_all_partitions or self._partition_access == 'all':
            result.append({'name': 'all-partitions', 'role': role})
            if role in roles:
                changed = False
            else:
                changed = True
        elif self._append:
            found = False
            for part in pa:
                if (part['name'] == self._partition_access and
                    part['role'] == role):
                        found = True

            if not found:
                result = pa
                result.append({'name': self._partition_access, 'role': role})
                changed = True
        else:
            result.append({'name': self._partition_access, 'role': role})
            orole = pa[0]['role']
            oname = pa[0]['name']
            if orole == role and oname == self._partition_access:
                changed = False
            else:
                changed = True

        return { 'changed': changed, 'permissions': result }

class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._login_host,
            username=self._login_user,
            password=self._login_password,
            debug=True
        )

    def is_locked(self):
        response = self.api.Management.UserManagement.is_locked_out([self._name])
        if response[0] == 'True':
            return True
        else:
            return False

    def reset_login(self):
        changed = False

        if not is_locked():
            return changed

        self.api.Management.UserManagement.reset_locked_out([self._name])
        return True


class BigIpRest(BigIpCommon):
    """Manipulate user accounts via REST

    This class uses calls to the REST API to manage user accounts. The account
    is a JSON structure that can resemble the following

    {
      "kind": "tm:auth:user:userstate",
      "name": "asdf",
      "fullPath": "asdf",
      "generation": 93,
      "selfLink": "https://localhost/mgmt/tm/auth/user/asdf?ver=12.0.0",
      "description": "asdf",
      "encryptedPassword": "$6$gracUaZR$S...EuV6eGSBdPQ57OUiAs/VRXHbrRn1",
      "shell": "tmsh",
      "partitionAccess": [
        {
          "name": "Common",
          "role": "operator",
          "nameReference": {
            "link": "https://localhost/mgmt/tm/auth/partition/Common?ver=12.0.0"
          }
        },
        {
          "name": "test1",
          "role": "application-editor",
          "nameReference": {
            "link": "https://localhost/mgmt/tm/auth/partition/test1?ver=12.0.0"
          }
        },
        {
          "name": "test2",
          "role": "user-manager",
          "nameReference": {
            "link": "https://localhost/mgmt/tm/auth/partition/test2?ver=12.0.0"
          }
        }
      ]
    }

    Values in this structure can be updated by sending a PUT request to the
    endpoint of the user. For example

      https://bigip.internal/mgmt/tm/auth/user/admin

    The above URL would manipulate the admin user.

    The partitionAccess field is always populated. If no access parameters are
    specified at the time the account is created, a value of "no-access" is
    granted to all partitions. For example

      "partitionAccess": [
        {
          "name": "all-partitions",
          "role": "no-access"
        }

    Users can have different roles for each partition, however there are some
    roles that require they be applied to All partitions. These roles are

      - admin
      - auditor
      - no-access
      - resource-admin
      - web-application-security-administrator

    For users who specify these roles, this module will override the existing
    partitionAccess values with the new global value even if "append" is
    specified      

    """

    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/auth/user' % (self._login_host)
        self._headers = {
            'Content-Type': 'application/json'
        }

    def read(self):
        url = "%s/%s" % (self._uri, self._name)
        resp = requests.get(url,
                            auth=(self._login_user, self._login_password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            result = {}
        else:
            result = resp.json()

        self._current = result
        return result

    def exists(self):
        url = "%s/%s" % (self._uri, self._name)
        resp = requests.get(url,
                            auth=(self._login_user, self._login_password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return False
        else:
            return True

    def present(self):
        if not self.exists():
            return self.create()
        else:
            return self.update()

    def update(self):
        payload = {}

        updates = self._determine_updates()

        if updates['comment']:
            payload['description'] = self._comment

        if updates['password']:
            payload['encryptedPassword'] = self._password

        if updates['shell']:
            payload['shell'] = self._shell

        if self._role:
            permissions = self._determine_user_permissions(self._role)
            if self._name == 'admin':
                # The admin user is a system account that cannot have its
                # role changed.
                raise AdminRoleNoModifyError()
            elif self._login_user == self._name:
                # You cannot adjust the permissions of the account talking
                # to the interface because you might set them to lower than
                # they are currently and this would lock you out.
                raise CurrentUserNoRoleModifyError()

            if permissions['changed']:
                payload['partitionAccess'] = permissions['permissions']

                # If the user is specifying a role that doesn't allow the advanced
                # shell, but the user already has an advanced shell set (for
                # instance you are downgrading their permissions) then set the
                # shell to tmsh
                if self._role not in ['resource-admin', 'admin']:
                    payload['shell'] = 'tmsh'

        if payload:
            uri = "%s/%s" % (self._uri, self._name)
            resp = requests.put(uri,
                                auth=(self._login_user, self._login_password),
                                data=json.dumps(payload),
                                verify=self._validate_certs,
                                headers=self._headers)
            if resp.status_code == 200:
                return True
            else:
                res = resp.json()
                if '01070825' in res['message']:
                    # Exception: 01070825:3: Access denied - Administrators only:
                    # Custom shells are only available to administrators not asdf
                    raise CustomShellError()
                else:
                    raise Exception(res['message'])

    def create(self):
        can_have_advanced = ['resource-admin', 'admin']
        if self._role is None:
            self._role = 'no-access'

        if self._partition_access is None:
            self._partition_access = 'all-partitions'

        if self._role in self._required_all_partitions:
            self._partition_access = 'all-partitions'

        payload = {
            'name': self._name,
            'encryptedPassword': self._password
        }

        if self._shell == 'bash' and not self._role in can_have_advanced:
            raise CustomShellError()
        else:
            payload['shell'] = self._shell

        payload['partitionAccess'] = [{
            'name': self._partition_access,
            'role': self._role
        }]

        resp = requests.post(self._uri,
                             auth=(self._login_user, self._login_password),
                             data=json.dumps(payload),
                             verify=self._validate_certs,
                             headers=self._headers)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def absent(self):
        if not self.exists():
            return True

        uri = "%s/%s" % (self._uri, self._name)
        resp = requests.delete(uri,
                               auth=(self._login_user, self._login_password),
                               verify=self._validate_certs)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])


def main():
    changed = False
    icontrol = False
    connection = 'rest'

    # Forces use of iControl SOAP for certain states.
    #
    # There are some things that cannot be done via iControl REST. For those
    # actions we deliberately override the connection that is used.
    force_icontrol_states = [
        'reset-login'
    ]

    # These are the roles that are available to be set in the BIG-IP
    role_choices = [
        'acceleration-policy-editor', 'admin', 'application-editor', 'auditor',
        'certificate-manager', 'guest', 'irule-manager', 'manager',
        'no-access', 'operator', 'resource-admin', 'user-manager',
        'web-application-security-administrator', 'web-application-security-editor'
    ]

    module = AnsibleModule(
        argument_spec = dict(
            append=dict(default='no', type='bool', choices=BOOLEANS),
            comment=dict(),
            login_host=dict(required=True),
            login_password=dict(require=True),
            partition_access=dict(default='Common', aliases=['partition']),
            password=dict(),
            role=dict(default=None, choices=role_choices),
            shell=dict(default=None, choices=['bash', 'none', 'tmsh']),
            state=dict(default='present', choices=['absent', 'present', 'reset-login']),
            login_user=dict(required=True),
            name=dict(required=True, aliases=['user']),
            update_password=dict(required=False, default='always', choices=['always', 'on_create']),
            validate_certs=dict(default='yes', type='bool', choices=BOOLEANS)
        )
    )

    hostname = module.params.get('login_host')
    password = module.params.get('login_password')
    username = module.params.get('login_user')
    state = module.params.get('state')
    role = module.params.get('role')

    try:
        if not bigsuds_found:
            raise Exception("The python bigsuds module is required")
        if not requests_found:
            raise Exception("The python requests module is required")

        if state in force_icontrol_states:
            connection = 'icontrol'
        
        if connection == 'icontrol':
            icontrol = test_icontrol(username, password, hostname)
            if icontrol:
                obj = BigIpIControl(module)
            else:
                raise UnlicensedError()
        else:
            obj = BigIpRest(module)

        if state == "present":
            if obj.present():
                changed = True
        elif state == "absent":
            if role == 'admin':
                raise Exception('The specified user cannot be removed because it is a system account')
            elif username == role:
                raise Exception('The current user cannot remove themselves')

            if obj.absent():
                changed = True
        elif state == 'reset-login':
            # You can only unlock accounts via the SOAP API
            obj = BigIpIControl(module)
            if obj.reset_login():
                changed = True
    except bigsuds.ConnectionError, e:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except AdminRoleNoModifyError:
        module.fail_json(msg="The admin user's role cannot be changed")
    except CurrentUserNoRoleModifyError:
        module.fail_json(msg='The login_user user cannot change their own role')
    except CreateUserError:
        module.fail_json(msg='Failed to create the user!')
    except DeleteUserError:
        module.fail_json(msg='Failed to delete the user!')
    except CustomShellError:
        module.fail_json(msg='Custom shells are only available to administrators')
    except UnlicensedError:
        module.fail_json(msg='The BIG-IP is not licensed')
    except socket.timeout, e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except bigsuds.ConnectionError, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
