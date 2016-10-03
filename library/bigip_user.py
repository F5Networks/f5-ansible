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
module: bigip_user
short_description: Manage user accounts and user attributes on a BIG-IP.
description:
  - Manage user accounts and user attributes on a BIG-IP.
version_added: "2.2"
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
      - Full name of the user.
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


class BigIpUserManager(object):
    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = None

    def apply_changes(self):
        result = dict()
        changed = False

        try:
            self.api = self.connect_to_bigip(**self.params)

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
        if self.user_exists():
            return self.update_user()
        else:
            return self.ensure_user_is_present()

    def absent(self):
        changed = False
        if self.user_exists():
            changed = self.ensure_user_is_absent()
        return changed

    def connect_to_bigip(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

    def can_not_login_with_new_credentials(self):
        try:
            kwargs = dict(
                server=self.params['server'],
                user=self.params['username_credential'],
                password=self.params['password_credential'],
                port=self.params['server_port']
            )
            self.connect_to_bigip(**kwargs)
            return False
        except Exception:
            return True

    def read_user_information(self):
        user = self.load_user()
        return self.format_user_information(user)

    def format_user_information(self, user):
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
            result['partition_access'] = self.format_current_partition_access(user)
        return result

    def format_current_partition_access(self, user):
        result = set()
        for acl in user.partitionAccess:
            access = '%s:%s' % (acl['name'], acl['role'])
            result.update(access)
        return list(result)

    def load_user(self):
        if self.is_version_less_than_13():
            return self.load_user_without_partition()
        else:
            return self.load_user_with_partition()

    def load_user_with_partition(self):
        return self.api.tm.auth.users.user.load(
            name=self.params['username_credential'],
            partition=self.params['partition']
        )

    def load_user_without_partition(self):
        return self.api.tm.auth.users.user.load(
            name=self.params['username_credential']
        )

    def is_version_less_than_13(self):
        """Checks to see if the TMOS version is less than 13

        Anything less than BIG-IP 13.x does not support users
        on different partitions.

        :return:
        """
        version = self.api.tmos_version
        if LooseVersion(version) < LooseVersion('13.0.0'):
            return True
        else:
            return False

    def user_exists(self):
        if self.is_version_less_than_13():
            return self.does_user_exist_without_partition()
        else:
            return self.does_user_exist_with_partition()

    def does_user_exist_with_partition(self):
        return self.api.tm.auth.users.user.exists(
            name=self.params['username_credential'],
            partition=self.params['partition']
        )

    def does_user_exist_without_partition(self):
        return self.api.tm.auth.users.user.exists(
            name=self.params['username_credential']
        )

    def update_user(self):
        params = self.get_changed_parameters()
        if params:
            self.changed_params = camel_dict_to_snake_dict(params)
            if self.params['check_mode']:
                return True
        else:
            return False
        params['name'] = self.params['username_credential']
        params['partition'] = self.params['partition']
        self.update_user_on_device(params)
        return True

    def update_user_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            if self.is_version_less_than_13():
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

    def get_changed_parameters(self):
        result = dict()
        current = self.read_user_information()
        if self.is_description_changed(current):
            result['description'] = self.params['full_name']
        if self.is_password_changed():
            result['password'] = self.params['password_credential']
        if self.is_shell_changed(current):
            result['shell'] = self.params['shell']
        if self.is_partition_access_changed(current):
            result['partitionAccess'] = self.getChangedPartitionAccess()
        return result

    def is_partition_access_changed(self, current):
        if self.params['partition_access'] is None:
            return False
        if 'partitionAccess' not in current:
            return True
        if self.params['partition_access'] == current['partition_access']:
            return False
        else:
            return True

    def is_shell_changed(self, current):
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

    def is_password_changed(self):
        username_credential = self.params['username_credential']
        password_credential = self.params['password_credential']
        if password_credential is None:
            return False
        if not password_credential and not username_credential:
            return False
        if self.params['update_password'] == 'on_create':
            return False
        if self.can_not_login_with_new_credentials():
            return True
        else:
            return False

    def is_description_changed(self, current):
        full_name = self.params['full_name']
        if full_name is None:
            return False
        if 'full_name' not in current:
            return True
        if full_name != current['full_name']:
            return True
        else:
            return False

    def ensure_user_is_present(self):
        if not self.params['password_credential']:
            raise F5ModuleError(
                "A password_credential must be specified"
            )
        params = self.get_user_creation_parameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.create_user_on_device(params)
        if self.user_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the user")

    def get_user_creation_parameters(self):
        result = dict(
            name=self.params['username_credential'],
            partition=self.params['partition'],
            partitionAccess=self.determine_partition_access_to_create()
        )
        if self.params['full_name']:
            result['description'] = self.params['full_name']
        elif self.params['password_credential']:
            result['password'] = self.params['password_credential']
        if not self.params['shell']:
            return result
        if self.params['shell'] == 'none':
            return result
        if self.can_have_advanced_shell_upon_creation():
            result['shell'] = self.params['shell']
        if self.params['shell'] == 'bash':
            raise F5ModuleError(
                "Custom shells are only available to administrators"
            )

    def can_have_advanced_shell_upon_creation(self):
        roles_with_advanced_shell = [
            'admin', 'resource-admin'
        ]
        for x in self.params['partitionAccess']:
            if x['role'] in roles_with_advanced_shell:
                return True
        return False

    def create_user_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            api.tm.auth.users.user.create(**params)

    def determine_partition_access_to_create(self):
        default_partition_access = dict(
            name='all-partitions',
            role='no-access'
        )
        if self.params['partition_access'] is None:
            return [default_partition_access]
        else:
            return self.get_partition_access_from_input()

    def get_partition_access_from_input(self):
        result = []
        partition_access = self.params['partition_access']
        for access in partition_access:
            acl = access.split(':')
            result.append({acl[0], acl[1]})
        return result

    def ensure_user_is_absent(self):
        if self.params['check_mode']:
            return True
        self.delete_user_from_device()
        if self.user_exists():
            raise F5ModuleError("Failed to delete the user")
        return True

    def delete_user_from_device(self):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            if self.is_version_less_than_13():
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


class BigIpUserModuleConfig(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.shells = ['bash', 'none', 'tmsh']
        self.states = ['absent', 'present']
        self.update_password_states = ['always', 'on_create']

        self.initialize_meta_args()
        self.initialize_argument_spec()

    def initialize_meta_args(self):
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

    def initialize_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)

    def create(self):
        return AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    config = BigIpUserModuleConfig()
    module = config.create()

    try:
        obj = BigIpUserManager(check_mode=module.check_mode, **module.params)
        result = obj.apply_changes()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import camel_dict_to_snake_dict
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
