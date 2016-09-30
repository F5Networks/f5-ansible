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
short_description: Manage user accounts and user attributes on a BIG-IP.
description:
  - Manage user accounts and user attributes on a BIG-IP.
version_added: "2.1"
options:
  append:
    description:
      - If C(yes), will only add groups, not set them to just the list
        in groups.
    choices:
      - yes
      - no
    default: no
  full_name:
    description:
      - Full name of the user
    required: false
  username_credential:
    description:
      - Name of the user to create, remove or modify.
    required: true
    aliases:
      - user
  password_credential:
    description:
      - Optionally set the users password to this unencrypted value.
        C(password_credential) is required when creating a new account.
    default: None
    required: false
  shell:
    description:
      - Optionally set the users shell.
    required: false
    default: None
    choices:
      - bash
      - none
      - tmsh
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
    type: list
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
notes:
   - Requires the requests Python package on the host. This is as easy as
     pip install requests
   - Requires BIG-IP versions >= 13.0.0
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
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
  delegate_to: localhost
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

try:
    from distutils.version import LooseVersion
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


# These are the roles that are available to be set in the BIG-IP
ROLES = [
    'acceleration-policy-editor', 'application-editor', 'auditor',
    'certificate-manager', 'guest', 'irule-manager', 'manager',
    'no-access', 'operator', 'resource-admin', 'user-manager',
    'web-application-security-administrator',
    'web-application-security-editor', 'admin'
]


class BigIpUserManager(object):
    ADMIN_ROLE = 'admin'

    RESERVED_ROLES = [
        'admin'
    ]
    RESERVED_NAMES = [
        'admin'
    ]
    ALL_PARTITIONS = [
        'resource-admin', 'auditor', 'admin',
        'web-application-security-administrator', 'no-access'
    ]

    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = self.connectToApi(**kwargs)

    def applyChanges(self):
        result = dict()
        changed = False

        try:
            if self.params['state'] == "present":
                changed = self.present()
            elif self.params['state'] == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.changed_params)
        result.update(dict(changed=changed))
        return result

    def present(self):
        if self.userExists():
            return self.updateUser()
        else:
            return self.ensureUserIsPresent()

    def absent(self):
        changed = False
        if self.userExists():
            changed = self.ensureUserIsAbsent()
        return changed

    def connectToApi(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

    def canNotLoginWithNewCredentials(self):
        try:
            kwargs = dict(
                server=self.params['server'],
                user=self.params['username_credential'],
                password=self.params['password_credential'],
                port=self.params['server_port']
            )
            self.connectToApi(**kwargs)
            return False
        except Exception:
            return True

    def readUserInformation(self):
        user = self.loadUser()
        return self.formatUserInformation(user)

    def formatUserInformation(self, user):
        """Ensure that the user information is in a standard format

        The SDK provides information back in a format that may change with
        the version of BIG-IP being worked with. Therefore, we need to make
        sure that the data is formatted in a way that our module expects it.

        Additionally, this takes care of minor variations between Python 2
        and Python 3.

        :param user:
        :return:
        """
        result = dict()
        result['name'] = str(user.name)
        if hasattr(user, 'description'):
            result['full_name'] = str(user.description)
        if hasattr(user, 'shell'):
            result['shell'] = str(user.shell)
        if hasattr(user, 'partitionAccess'):
            result['partition_access'] = self.formatCurrentPartitionAccess(user)
        return result

    def formatCurrentPartitionAccess(self, user):
        result = set()
        for acl in user.partitionAccess:
            access = '%s:%s' % (acl['name'], acl['role'])
            result.update(access)
        return list(result)

    def loadUser(self):
        if self.isVersionLessThan13():
            return self.loadUserWithoutPartition()
        else:
            return self.loadUserWithPartition()

    def loadUserWithPartition(self):
        return self.api.tm.auth.users.user.load(
            name=self.params['username_credential'],
            partition=self.params['partition']
        )

    def loadUserWithoutPartition(self):
        return self.api.tm.auth.users.user.load(
            name=self.params['username_credential']
        )

    def isVersionLessThan13(self):
        """Checks to see if the TMOS version is less than 13

        Anything less than BIG-IP 13.x does not support user
        on different partitions.

        :return:
        """
        version = self.api.tmos_version
        if LooseVersion(version) < LooseVersion('13.0.0'):
            return True
        else:
            return False

    def userExists(self):
        if self.isVersionLessThan13():
            return self.checkIfUserExistsWithoutPartition()
        else:
            return self.checkIfUserExistsWithPartition()

    def checkIfUserExistsWithPartition(self):
        return self.api.tm.auth.users.user.exists(
            name=self.params['username_credential'],
            partition=self.params['partition']
        )

    def checkIfUserExistsWithoutPartition(self):
        return self.api.tm.auth.users.user.exists(
            name=self.params['username_credential']
        )

    def updateUser(self):
        params = self.getChangedParameters()
        if params:
            self.changed_params = camel_dict_to_snake_dict(params)
            if self.params['check_mode']:
                return True
        else:
            return False
        params['name'] = self.params['username_credential']
        params['partition'] = self.params['partition']
        self.updateUserOnDevice(params)
        return True

    def updateUserOnDevice(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            if self.isVersionLessThan13():
                r = api.tm.auth.users.user.load(
                    name=self.params['username_credential']
                )
                r.modify(**params)
            else:
                r = api.tm.auth.users.user.load(
                    name=self.params['username_credential'],
                    partition=self.params['partition']
                )
                r.modify(**params)

    def getChangedParameters(self):
        result = dict()
        current = self.readUserInformation()
        if self.isDescriptionChanged(current):
            result['description'] = self.params['full_name']
        if self.isPasswordChanged():
            result['password'] = self.params['password_credential']
        if self.isShellChanged(current):
            result['shell'] = self.params['shell']
        if self.isPartitionAccessChanged(current):
            result['partitionAccess'] = self.getChangedPartitionAccess()
        return result

    def isPartitionAccessChanged(self, current):
        if self.params['partition_access'] is None:
            return False
        if 'partitionAccess' not in current:
            return True
        if self.params['partition_access'] == current['partition_access']:
            return False
        else:
            return True

    def isShellChanged(self, current):
        shell = self.params['shell']
        if shell is None:
            return False
        if shell == 'none' and 'shell' not in current:
            return False
        if 'shell' not in current:
            return True
        if shell == current['shell']:
            return False
        else:
            return True

    def isPasswordChanged(self):
        username_credential = self.params['username_credential']
        password_credential = self.params['password_credential']
        if password_credential is None:
            return False
        if not password_credential and not username_credential:
            return False
        if self.params['update_password'] == 'on_create':
            return False
        if self.canNotLoginWithNewCredentials():
            return True
        else:
            return False

    def isDescriptionChanged(self, current):
        full_name = self.params['full_name']
        if full_name is None:
            return False
        if 'full_name' not in current:
            return True
        if full_name != current['full_name']:
            return True
        else:
            return False

    def ensureUserIsPresent(self):
        if not self.params['password_credential']:
            raise F5ModuleError(
                "A password_credential must be specified"
            )
        params = self.getUserCreationParameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.createUserOnDevice(params)
        if self.userExists():
            return True
        else:
            raise F5ModuleError("Failed to create the user")

    def getUserCreationParameters(self):
        result = dict()
        result['name'] = self.params['username_credential']
        result['partition'] = self.params['partition']
        result['partitionAccess'] = self.determinePartitionAccessToCreate()
        if self.params['full_name']:
            result['description'] = self.params['full_name']
        elif self.params['password_credential']:
            result['password'] = self.params['password_credential']
        if not self.params['shell']:
            return result
        if self.params['shell'] == 'none':
            return result
        if self.canHaveAdvancedShellUponCreation():
            result['shell'] = self.params['shell']
        if self.params['shell'] == 'bash':
            raise F5ModuleError(
                "Custom shells are only available to administrators"
            )

    def canHaveAdvancedShellUponCreation(self):
        roles_with_advanced_shell = [
            'admin', 'resource-admin'
        ]
        for x in self.params['partitionAccess']:
            if x['role'] in roles_with_advanced_shell:
                return True
        return False

    def createUserOnDevice(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            api.tm.auth.users.user.create(**params)

    def determinePartitionAccessToCreate(self):
        default_partition_access = dict(
            name='all-partitions',
            role='no-access'
        )
        if self.params['partition_access'] is None:
            return [default_partition_access]
        else:
            return self.getPartitionAccessFromInput()

    def getPartitionAccessFromInput(self):
        result = []
        partition_access = self.params['partition_access']
        for access in partition_access:
            acl = access.split(':')
            result.append({acl[0], acl[1]})
        return result

    def ensureUserIsAbsent(self):
        if self.params['check_mode']:
            return True
        self.deleteUserFromDevice()
        if self.userExists():
            raise F5ModuleError("Failed to delete the user")
        return True

    def deleteUserFromDevice(self):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            if self.isVersionLessThan13():
                user = api.tm.auth.users.user.load(
                    name=self.params['username_credential']
                )
                user.delete()
            else:
                user = api.tm.auth.users.user.load(
                    name=self.params['username_credential'],
                    partition=self.params['partition']
                )
                user.delete()


class BigIpUserModuleCreator(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.shells = ['bash', 'none', 'tmsh']
        self.states = ['absent', 'present']
        self.update_password_states = ['always', 'on_create']

        self.initializeMetaArgs()
        self.initializeArgumentSpec()

    def initializeArgumentSpec(self):
        """Ensure the argument spec is updated for this module

        The argument spec combines the values provided in the F5 common
        arguments as well as the arguments that are specific to this module.

        :return:
        """
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)

    def initializeMetaArgs(self):
        """Ensure meta arguments are set

        The meta arguments are arguments that are specific to this module.
        These arguments are combined with the common F5 arguments to form
        the complete argument spec.

        Arguments defined in this method will override the F5 common
        arguments.

        :return:
        """
        args = dict(
            append=dict(
                default=False,
                type='bool',
                choices=BOOLEANS
            ),
            full_name=dict(),
            partition_access=dict(
                required=False,
                default=None,
                type='list'
            ),
            password_credential=dict(
                required=False,
                default=None,
                no_log=True
            ),
            shell=dict(
                default=None,
                choices=self.shells
            ),
            state=dict(
                default='present',
                choices=self.states
            ),
            username_credential=dict(
                required=True,
                aliases=['name']
            ),
            update_password=dict(
                required=False,
                default='always',
                choices=self.update_password_states
            )
        )
        self.meta_args = args

    def create(self):
        return AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module_creator = BigIpUserModuleCreator()
    module = module_creator.create()

    try:
        obj = BigIpUserManager(check_mode=module.check_mode, **module.params)
        result = obj.applyChanges()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import camel_dict_to_snake_dict
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
