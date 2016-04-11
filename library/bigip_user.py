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
version_added: "2.1"
options:
  append:
    description:
      - If C(yes), will only add groups, not set them to just the list
        in groups.
    choices: ['yes', 'no']
    default: no
  full_name:
    description:
      - Full name of the user
    required: false
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: soap
    choices: ['rest', 'soap']
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
  username_credential:
    description:
      - Name of the user to create, remove or modify.
    required: true
    aliases:
      - user
  password_credential:
    description:
      - Optionally set the user's password to this unencrypted value. One of
        either C(password_credential) or C(encrypted_credential) is required
        when creating a new account.
    default: None
    required: false
  encrypted_credential:
    description:
      - Optionally set the user's password to this crypted value. One of either
        C(password_credential) or C(encrypted_credential) is required when
        creating a new account. The password should be encrypted using crypt(3).
    default: None
    required: false
  shell:
    description:
      - Optionally set the user's shell.
    required: false
    default: None
    choices: ['bash', 'none', 'tmsh']
  partition:
    description:
      - Partition to create user. Ignored during updates.
    required: false
    default: 'Common'
  partition_access:
    description:
      - Specifies the administrative partition to which the user has access.
        Should be in the form "partition:role". Valid roles include
        C(acceleration-policy-editor), C(admin), C(application-editor), C(auditor)
        C(certificate-manager), C(guest), C(irule-manager), C(manager), C(no-access)
        C(operator), C(resource-admin), C(user-manager), C(web-application-security-administrator),
        and C(web-application-security-editor). Partition portion of tuple should
        be an existing partition or the value 'all'.
    required: false
    default: "all:no-access"
    choices: []
  state:
    description:
      - Whether the account should exist or not, taking action if the state is
        different from what is stated.
    required: false
    default: present
    choices:
      - present
      - absent
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
   - Requires the requests Python package on the host. This is as easy as
     pip install requests
   - For BIG-IP versions < 11.6.0, multiple roles on different partitions
     is not supported. Instead, the last specified role wins.
   - Specifying a C(partition) to create the account on is only supported
     via the C(soap) connection type (the default) due to missing
     functionality in BIG-IP versions <= 12.1.0

requirements: [ "bigsuds", "requests" ]
author:
  - Matt Hite <mhite@hotmail.com> (@mhite)
  - Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = '''
- name: Add the user 'johnd' as an admin
  bigip_user:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      username_credential: "johnd"
      password_credential: "password"
      full_name: "John Doe"
      partition_access: "all:admin"
      state: "present"
  delegate_to: localhost

- name: Change the user "johnd's" role and shell
  bigip_user:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      username_credential: "johnd"
      partition_access: "NewPartition:manager"
      shell: "tmsh"
      state: "present"
  delegate_to: localhost

- name: Make the user 'johnd' an admin and set to advanced shell
  bigip_user:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      name: "johnd"
      partition_access: "all:admin"
      shell: "bash"
      state: "present"
  delegate_to: localhost

- name: Remove the user 'johnd'
  bigip_user:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      name: "johnd"
      state: "absent"
  delegate_to: localhost

- name: Update password
  bigip_user:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "present"
      username_credential: "johnd"
      password_credential: "newsupersecretpassword"
'''

RETURN = '''
full_name:
    description: Full name of the user
    returned: changed and success
    type: string
    sample: "John Doe"
partition_access:
    description:
      - List of strings containing the user's roles and which partitions they
        are applied to. They are specified in the form "partition:role".
    returned: changed and success
    type: list
    sample: "['all:admin']"
shell:
    description: The shell assigned to the user account
    returned: changed and success
    type: string
    sample: "tmsh"
'''

import json

try:
    import bigsuds
    BIGSUDS_AVAILABLE = True
except ImportError:
    BIGSUDS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

TRANSPORTS = ['rest', 'soap']

# These are the roles that are available to be set in the BIG-IP
ROLES = [
    'acceleration-policy-editor', 'application-editor', 'auditor',
    'certificate-manager', 'guest', 'irule-manager', 'manager',
    'no-access', 'operator', 'resource-admin', 'user-manager',
    'web-application-security-administrator', 'web-application-security-editor',
    'admin'
]

SHELLS = ['bash', 'none', 'tmsh']
STATES = ['absent', 'present']


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


class InvalidRoleError(Exception):
    pass


class PartitionAccessMalformedError(Exception):
    pass


class RestrictiveAclForShellError(Exception):
    pass


class PasswordRequiredError(Exception):
    pass


class RestrictedToSinglePartitionError(Exception):
    pass


class BigIpApiFactory(object):
    def factory(module):
        connection = module.params.get('connection')
        pa = module.params.get('partition_access')

        if pa is None or 'Common:' in pa:
            connection = 'soap'

        if connection == 'rest':
            if not REQUESTS_AVAILABLE:
                raise Exception("The python requests module is required")
            return BigIpRestApi(check_mode=module.check_mode, **module.params)
        elif connection == 'soap':
            if not BIGSUDS_AVAILABLE:
                raise Exception("The python bigsuds module is required")
            # iControl REST does not support creating users on different
            # partitions, so we need to use SOAP
            return BigIpSoapApi(check_mode=module.check_mode, **module.params)

    factory = staticmethod(factory)


class BigIpCommon(object):
    ALL_PARTITIONS = [
        'resource-admin', 'auditor', 'admin',
        'web-application-security-administrator', 'no-access',
        'USER_ROLE_ADMINISTRATOR', 'USER_ROLE_INVALID'
    ]

    RESERVED_NAMES = [
        'admin'
    ]

    RESERVED_ROLES = [
        'admin', 'USER_ROLE_ADMINISTRATOR'
    ]

    ADVANCED_SHELL = [
        'admin', 'resource-admin',
        'USER_ROLE_ADMINISTRATOR', 'USER_ROLE_RESOURCE_ADMINISTRATOR'
    ]

    SHELL_BASH = 'bash'
    SHELL_NONE = 'none'

    def __init__(self, *args, **kwargs):
        self.result = dict(changed=False, changes=dict())

        self.params = kwargs

        if self.params['partition_access'] is None:
            pass
        elif not isinstance(self.params['partition_access'], list):
            self.params['partition_access'] = [kwargs['partition_access']]

        self.current = dict()

    def can_have_advanced_shell(self):
        current = self.read()

        for acl in current['partition_access']:
            permission = acl.split(':')
            if permission[0] in self.ADVANCED_SHELL:
                return True

        return False

    def _determine_updates(self):
        result = dict(
            full_name=False,
            password=False,
            shell=False,
            partition_access=False
        )
        current = self.read()

        full_name = self.params['full_name']
        password_credential = self.params['password_credential']
        username_credential = self.params['username_credential']
        shell = self.params['shell']
        partition_access = self.params['partition_access']
        update_password = self.params['update_password']
        encrypted_credential = self.params['encrypted_credential']

        if full_name:
            if current['full_name'] != full_name:
                result['full_name'] = True

        if encrypted_credential and username_credential:
            if update_password == 'always':
                result['password'] = True
        elif password_credential and username_credential:
            if update_password == 'always' and self.did_password_change():
                result['password'] = True

        if shell:
            if shell == 'bash':
                if not self.can_have_advanced_shell():
                    raise CustomShellError()

            if shell == current['shell']:
                result['shell'] = False
            else:
                result['shell'] = True

        if partition_access:
            if partition_access == current['partition_access']:
                result['partition_access'] = False
            else:
                result['partition_access'] = True

        return result

    def _determine_partition_access(self):
        result = []
        has_all = False

        if self.params['partition_access'] is None:
            return result

        for permission in self.params['partition_access']:
            acl = permission.split(':')
            if len(acl) != 2:
                raise PartitionAccessMalformedError
            elif acl[1] not in ROLES:
                raise InvalidRoleError

            partition = acl[0]
            role = acl[1]

            # These roles affect all partitions. There can be no other roles
            # assigned to any other partitions if they are set.
            #
            # Likewise, if the specified role is being placed in the 'all' partition
            # then existing permissions must be cleared
            if role in self.ALL_PARTITIONS or partition == 'all':
                result = []
                has_all = True
            elif self.params['append']:
                if permission in self._current['partition_access']:
                    continue

            permissions = dict(
                role=role,
                partition=partition
            )
            result.append(permissions)
            if has_all:
                break

        for permission in result:
            role = permission['role']
            partition = permission['partition']

            if role in self.ALL_PARTITIONS and partition != 'all':
                raise RestrictedToSinglePartitionError

        return result

    def flush(self):
        result = dict()
        encrypted_credential = self.params['encrypted_credential']
        password_credential = self.params['password_credential']
        state = self.params['state']
        user = self.params['user']
        username_credential = self.params['username_credential']

        if password_credential:
            self.params['is_encrypted'] = False
        else:
            self.params['is_encrypted'] = True
            self.params['password_credential'] = encrypted_credential

        if state == "present":
            changed = self.present()

            if not self.params['check_mode']:
                current = self.read()
                result.update(current)
        else:
            if username_credential in self.RESERVED_NAMES:
                raise Exception('The specified user cannot be removed because it is a system account')
            elif user == username_credential:
                raise Exception('The current user cannot remove themselves')
            changed = self.absent()

        result.update(dict(changed=changed))
        return result


class BigIpSoapApi(BigIpCommon):
    """Manipulate user accounts via SOAP
    """

    ROLE_MAP = {
        'acceleration-policy-editor': 'USER_ROLE_ACCELERATION_POLICY_EDITOR',
        'admin': 'USER_ROLE_ADMINISTRATOR',
        'application-editor': 'USER_ROLE_APPLICATION_EDITOR',
        'auditor': 'USER_ROLE_AUDITOR',
        'certificate-manager': 'USER_ROLE_CERTIFICATE_MANAGER',
        'guest': 'USER_ROLE_GUEST',
        'irule-manager': 'USER_ROLE_IRULE_MANAGER',
        'manager': 'USER_ROLE_MANAGER',
        'no-access': 'USER_ROLE_INVALID',
        'operator': 'USER_ROLE_TRAFFIC_MANAGER',
        'resource-admin': 'USER_ROLE_RESOURCE_ADMINISTRATOR',
        'user-manager': 'USER_ROLE_USER_MANAGER',
        'web-application-security-administrator': 'USER_ROLE_ASM_POLICY_EDITOR',
        'web-application-security-editor': 'USER_ROLE_ASM_EDITOR'
    }

    SHELL_MAP = {
        'bash': '/bin/bash',
        'none': '/sbin/nologin',
        'tmsh': '/usr/bin/tmsh',
    }

    SHELL_RMAP = {
        '/bin/bash': 'bash',
        '/sbin/nologin': 'none',
        '/usr/bin/tmsh': 'tmsh',
        '/bin/false': 'none'
    }

    ALL_PARTITION = '[All]'
    ADMIN_ROLE = 'USER_ROLE_ADMINISTRATOR'
    ROLE_DEFAULT = 'USER_ROLE_INVALID'

    def __init__(self, *args, **kwargs):
        super(BigIpSoapApi, self).__init__(*args, **kwargs)

        self.api = bigip_api(kwargs['server'],
                             kwargs['user'],
                             kwargs['password'],
                             kwargs['validate_certs'])

    def did_password_change(self):
        server = self.params['server']
        user = self.params['username_credential']
        password = self.params['password_credential']
        validate_certs = self.params['validate_certs']

        try:
            api = bigip_api(server,
                      user,
                      password,
                      validate_certs)
            api.Management.UserManagement.get_fullname(
                user_names=[user]
            )
            return False
        except bigsuds.ConnectionError, e:
            if 'Authorization Required' in str(e):
                return False

            return True

    def get_fullname(self):
        username_credential = self.params['username_credential']

        resp = self.api.Management.UserManagement.get_fullname(
            user_names=[username_credential]
        )
        return resp[0]

    def get_login_shell(self):
        username_credential = self.params['username_credential']

        resp = self.api.Management.UserManagement.get_login_shell(
            user_names=[username_credential]
        )
        return resp[0]

    def get_user_permission(self):
        result = {}

        username_credential = self.params['username_credential']

        resp = self.api.Management.UserManagement.get_user_permission(
            user_names=[username_credential]
        )

        for part in resp[0]:
            partition = part['partition']
            role = part['role']
            result[partition] = role
        return result

    def delete_all_permissions(self):
        username_credential = self.params['username_credential']

        permissions = self.get_user_permission()
        for partition, role in permissions.iteritems():
            permission = dict(role=role, partition=partition)
            self.api.Management.UserManagement.delete_user_permission(
                user_names=[username_credential],
                permissions=[[permission]]
            )

    def set_permission(self, role, partition):
        username_credential = self.params['username_credential']

        permission = dict(role=role, partition=partition)

        self.api.Management.UserManagement.set_user_permission(
            user_names=[username_credential],
            permissions=[[permission]]
        )

    def set_fullname(self):
        username_credential = self.params['username_credential']
        full_name = self.params['full_name']

        self.api.Management.UserManagement.set_fullname(
            user_names=[username_credential],
            fullnames=[full_name]
        )

        return True

    def set_login_shell(self):
        username_credential = self.params['username_credential']
        shell = self.params['shell']
        shell = self.SHELL_MAP[shell]

        self.api.Management.UserManagement.set_login_shell(
            user_names=[username_credential],
            shells=[shell]
        )

        return True

    def start_transaction(self):
        self.api.System.Session.start_transaction()

        # need to switch to root, set recursive query state
        self.current_folder = self.api.System.Session.get_active_folder()
        if self.current_folder != '/' + self.params['partition']:
            self.api.System.Session.set_active_folder(folder='/' + self.params['partition'])

        self.current_query_state = self.api.System.Session.get_recursive_query_state()
        if self.current_query_state == 'STATE_DISABLED':
            self.api.System.Session.set_recursive_query_state('STATE_ENABLED')

    def submit_transaction(self):
        # set everything back
        if self.current_query_state == 'STATE_DISABLED':
            self.api.System.Session.set_recursive_query_state('STATE_DISABLED')

        if self.current_folder != '/' + self.params['partition']:
            self.api.System.Session.set_active_folder(folder=self.current_folder)

        self.api.System.Session.submit_transaction()

    def set_password(self):
        is_encrypted = self.params['is_encrypted']
        password_credential = self.params['password_credential']
        username_credential = self.params['username_credential']

        passwords = dict(
            is_encrypted=is_encrypted,
            password=password_credential
        )

        self.api.Management.UserManagement.change_password_2(
            user_names=[username_credential],
            passwords=[passwords]
        )

        return True

    def exists(self):
        result = False
        username_credential = self.params['username_credential']

        self.start_transaction()

        users = self.api.Management.UserManagement.get_list()
        for user in users:
            if user['name'] == username_credential:
                result = True

        self.submit_transaction()

        return result

    def read(self):
        result = {}

        ROLE_RMAP = dict((v, k) for k, v in self.ROLE_MAP.iteritems())

        result['full_name'] = self.get_fullname()
        result['partition_access'] = []
        result['shell'] = ''

        shell = self.get_login_shell()
        result['shell'] = self.SHELL_RMAP[shell]

        acls = self.get_user_permission()
        for partition, role in acls.iteritems():
            if partition == self.ALL_PARTITION:
                partition = 'all'
            role = ROLE_RMAP[role]

            partition_access = '%s:%s' % (partition, role)
            result['partition_access'].append(partition_access)

        self._current = result

        return result

    def absent(self):
        username_credential = self.params['username_credential']

        if not self.exists():
            return False

        if self.params['check_mode']:
            return True

        self.start_transaction()

        self.api.Management.UserManagement.delete_user(
            user_names=[username_credential]
        )

        self.submit_transaction()

        if self.exists():
            raise DeleteUserError()
        else:
            return True

    def update(self):
        changed = False
        updates = self._determine_updates()

        shell = self.params['shell']

        self.start_transaction()

        if updates['full_name']:
            if self.params['check_mode']:
                changed = True
            else:
                changed = self.set_fullname()

        if updates['password']:
            if self.params['check_mode']:
                changed = True
            else:
                changed = self.set_password()

        if updates['shell']:
            if shell == self.SHELL_BASH and not self.can_have_advanced_shell():
                raise CustomShellError()
            else:
                if self.params['check_mode']:
                    changed = True
                else:
                    changed = self.set_login_shell()

        if updates['partition_access']:
            permissions = self.determine_partition_access()

            if self.params['check_mode']:
                changed = True
            else:
                # Start by zeroing out the permissions
                self.delete_all_permissions()

                # Now, add all the permissions to the user account
                for permission in permissions:
                    self.set_permission(permission['role'], permission['partition'])
                changed = True

        self.submit_transaction()

        return changed

    def determine_partition_access(self):
        result = []

        access = self._determine_partition_access()
        for permission in access:
            role = permission['role']
            partition = permission['partition']

            if partition == 'all':
                partition = self.ALL_PARTITION

            permissions = dict(
                role=self.ROLE_MAP[role],
                partition=partition
            )
            result.append(permissions)
        return result

    def create(self):
        advanced_allowed = False

        is_encrypted = self.params['is_encrypted']
        password_credential = self.params['password_credential']
        shell = self.params['shell']
        username_credential = self.params['username_credential']
        partition = self.params['partition']

        user_id = dict(
            name=username_credential,
            full_name=''
        )
        password_info = dict(
            is_encrypted=is_encrypted,
            password=password_credential
        )

        users = dict(
            user=user_id,
            password=password_info,
        )

        user_permission = self.determine_partition_access()
        if user_permission:
            users['permissions'] = user_permission
        else:
            users['permissions'] = [dict(
                role=self.ROLE_DEFAULT,
                partition=self.ALL_PARTITION
            )]


        if shell and shell != self.SHELL_NONE:
            for x in user_permission:
                if x['role'] in self.ADVANCED_SHELL:
                    advanced_allowed = True

            if not advanced_allowed and shell == self.SHELL_BASH:
                raise CustomShellError()
            else:
                users['login_shell'] = self.SHELL_MAP[shell]

        self.start_transaction()

        self.api.Management.UserManagement.create_user_3(
            users=[users]
        )

        self.submit_transaction()

        if self.exists():
            return True
        else:
            raise CreateUserError()

    def present(self):
        password_credential = self.params['password_credential']

        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True
            elif password_credential is None:
                raise PasswordRequiredError
            return self.create()


class BigIpRestApi(BigIpCommon):
    """Manipulate user accounts via REST
    """

    ALL_PARTITION = 'all-partitions'
    ADMIN_ROLE = 'admin'
    ROLE_DEFAULT = 'no-access'

    def __init__(self, *args, **kwargs):
        super(BigIpRestApi, self).__init__(*args, **kwargs)

        server = self.params['server']

        self._uri = 'https://%s/mgmt/tm/auth/user' % (server)
        self._headers = {
            'Content-Type': 'application/json'
        }

    def did_password_change(self):
        server = self.params['server']
        user = self.params['username_credential']
        password = self.params['password_credential']
        validate_certs = self.params['validate_certs']

        try:
            url = "%s/%s" % (self._uri, user)
            resp = requests.get(url,
                                auth=(user, password),
                                verify=validate_certs)

            if resp.status_code == 200:
                return False
        except:
            return True

    def read(self):
        result = {}
        tmp = []

        user = self.params['user']
        username_credential = self.params['username_credential']
        password = self.params['password']
        validate_certs = self.params['validate_certs']

        url = "%s/%s" % (self._uri, username_credential)
        resp = requests.get(url,
                            auth=(user, password),
                            verify=validate_certs)

        if resp.status_code == 200:
            res = resp.json()

            if 'description' in res:
                result['full_name'] = res['description']
            else:
                result['full_name'] = ''

            if 'shell' in res:
                result['shell'] = res['shell']
            else:
                result['shell'] = self.SHELL_NONE

            if 'partitionAccess' in res:
                for part in res['partitionAccess']:
                    if part['name'] == self.ALL_PARTITION:
                        part['name'] = 'all'

                    partition = '%s:%s' % (part['name'], part['role'])
                    tmp.append(partition)

            result['partition_access'] = tmp

        return result

    def exists(self):
        user = self.params['user']
        username_credential = self.params['username_credential']
        password = self.params['password']
        validate_certs = self.params['validate_certs']

        url = "%s/%s" % (self._uri, username_credential)
        resp = requests.get(url,
                            auth=(user, password),
                            verify=validate_certs)

        if resp.status_code != 200:
            return False
        else:
            return True

    def present(self):
        password_credential = self.params['password_credential']

        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True
            elif password_credential is None:
                raise PasswordRequiredError
            return self.create()

    def update(self):
        payload = {}

        updates = self._determine_updates()

        is_encrypted = self.params['is_encrypted']
        user = self.params['user']
        username_credential = self.params['username_credential']
        password = self.params['password']
        password_credential = self.params['password_credential']
        shell = self.params['shell']
        validate_certs = self.params['validate_certs']

        if updates['full_name']:
            payload['description'] = self.params['full_name']

        if updates['password']:
            if is_encrypted:
                payload['encryptedPassword'] = password_credential
            else:
                payload['password'] = password_credential

        if updates['shell']:
            if shell == self.SHELL_BASH and not self.can_have_advanced_shell():
                raise CustomShellError()
            else:
                payload['shell'] = shell

        if updates['partition_access']:
            payload['partitionAccess'] = self.determine_partition_access()

        if payload:
            if self.params['check_mode']:
                return True

            uri = "%s/%s" % (self._uri, username_credential)
            resp = requests.patch(uri,
                                  auth=(user, password),
                                  data=json.dumps(payload),
                                  verify=validate_certs,
                                  headers=self._headers)
            if resp.status_code == 200:
                return True
            else:
                res = resp.json()
                raise Exception(res['message'])
        else:
            return False

    def determine_partition_access(self):
        result = []

        access = self._determine_partition_access()
        for permission in access:
            role = permission['role']
            partition = permission['partition']

            if partition == 'all':
                partition = self.ALL_PARTITION

            permissions = dict(
                role=role,
                name=partition
            )
            result.append(permissions)
        return result

    def create(self):
        full_name = self.params['full_name']
        user = self.params['user']
        username_credential = self.params['username_credential']
        password = self.params['password']
        password_credential = self.params['password_credential']
        validate_certs = self.params['validate_certs']
        is_encrypted = self.params['is_encrypted']
        partition_access = self.params['partition_access']
        shell = self.params['shell']

        payload = dict(
            name=username_credential
        )

        if partition_access is None:
            paccess = dict(
                name=self.ALL_PARTITION,
                role=self.ROLE_DEFAULT
            )
            payload['partitionAccess'] = [paccess]
        else:
            payload['partitionAccess'] = self.determine_partition_access()

        if full_name:
            payload['description'] = full_name

        if is_encrypted:
            payload['encryptedPassword'] = password_credential
        else:
            payload['password'] = password_credential

        if shell and shell != self.SHELL_NONE:
            for x in payload['partitionAccess']:
                if x['role'] in self.ADVANCED_SHELL:
                    advanced_allowed = True

            if not advanced_allowed and shell == self.SHELL_BASH:
                raise CustomShellError()
            else:
                payload['shell'] = shell

        resp = requests.post(self._uri,
                             auth=(user, password),
                             data=json.dumps(payload),
                             verify=validate_certs,
                             headers=self._headers)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def absent(self):
        user = self.params['user']
        username_credential = self.params['username_credential']
        password = self.params['password']
        validate_certs = self.params['validate_certs']

        if not self.exists():
            return False

        if self.params['check_mode']:
            return True

        uri = "%s/%s" % (self._uri, username_credential)
        resp = requests.delete(uri,
                               auth=(user, password),
                               verify=validate_certs)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        append=dict(default=False, type='bool', choices=BOOLEANS),
        full_name=dict(),
        connection=dict(default='soap', choices=TRANSPORTS),
        encrypted_credential=dict(required=False, default=None, no_log=True),
        partition_access=dict(required=False, default=None),
        password_credential=dict(required=False, default=None, no_log=True),
        shell=dict(default=None, choices=SHELLS),
        state=dict(default='present', choices=STATES),
        username_credential=dict(required=True, aliases=['name']),
        update_password=dict(required=False, default='always', choices=['always', 'on_create'])
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ['password_credential', 'encrypted_credential']
        ]
    )

    try:
        obj = BigIpApiFactory.factory(module)
        result = obj.flush()

        module.exit_json(**result)
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host")
    except bigsuds.ServerError, e:
        if 'folder not found' in str(e):
            module.fail_json(msg="Partition not found")
        else:
            module.fail_json(msg=str(e))
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
    except PasswordRequiredError:
        module.fail_json(msg='At least one of password_credential or encrypted_credential must be specified')
    except PartitionAccessMalformedError:
        module.fail_json(msg='partition_access must be one or more role:partition tuples')
    except InvalidRoleError:
        module.fail_json(msg='Value of role must be one of: %s' % ','.join(ROLES))
    except RestrictedToSinglePartitionError:
        module.fail_json(msg='The specified role may not be restricted to a single partition')
    except requests.exceptions.SSLError:
        module.fail_json(msg='Certificate verification failed. Consider using validate_certs=no')

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
