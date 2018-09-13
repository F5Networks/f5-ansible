#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_user
short_description: Manage user accounts and user attributes on a BIG-IP
description:
  - Manage user accounts and user attributes on a BIG-IP. Typically this
    module operates only on the REST API users and not the CLI users.
    When specifying C(root), you may only change the password.
    Your other parameters will be ignored in this case. Changing the C(root)
    password is not an idempotent operation. Therefore, it will change it
    every time this module attempts to change it.
version_added: 2.4
options:
  full_name:
    description:
      - Full name of the user.
  username_credential:
    description:
      - Name of the user to create, remove or modify.
      - The C(root) user may not be removed.
    required: True
    aliases:
      - name
  password_credential:
    description:
      - Set the users password to this unencrypted value.
        C(password_credential) is required when creating a new account.
  shell:
    description:
      - Optionally set the users shell.
    choices:
      - bash
      - none
      - tmsh
  partition_access:
    description:
      - Specifies the administrative partition to which the user has access.
        C(partition_access) is required when creating a new account.
        Should be in the form "partition:role". Valid roles include
        C(acceleration-policy-editor), C(admin), C(application-editor), C(auditor)
        C(certificate-manager), C(guest), C(irule-manager), C(manager), C(no-access)
        C(operator), C(resource-admin), C(user-manager), C(web-application-security-administrator),
        and C(web-application-security-editor). Partition portion of tuple should
        be an existing partition or the value 'all'.
  state:
    description:
      - Whether the account should exist or not, taking action if the state is
        different from what is stated.
    default: present
    choices:
      - present
      - absent
  update_password:
    description:
      - C(always) will allow to update passwords if the user chooses to do so.
        C(on_create) will only set the password for newly created users. When
        C(username_credential) is C(root), this value will be forced to C(always).
    default: always
    choices:
      - always
      - on_create
  partition:
    description:
      - Device partition to manage resources on.
    default: Common
    version_added: 2.5
notes:
   - Requires BIG-IP versions >= 12.0.0
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
  - Wojciech Wypior (@wojtek0806)
'''

EXAMPLES = r'''
- name: Add the user 'johnd' as an admin
  bigip_user:
    server: lb.mydomain.com
    user: admin
    password: secret
    username_credential: johnd
    password_credential: password
    full_name: John Doe
    partition_access: all:admin
    update_password: on_create
    state: present
  delegate_to: localhost

- name: Change the user "johnd's" role and shell
  bigip_user:
    server: lb.mydomain.com
    user: admin
    password: secret
    username_credential: johnd
    partition_access: NewPartition:manager
    shell: tmsh
    state: present
  delegate_to: localhost

- name: Make the user 'johnd' an admin and set to advanced shell
  bigip_user:
    server: lb.mydomain.com
    user: admin
    password: secret
    name: johnd
    partition_access: all:admin
    shell: bash
    state: present
  delegate_to: localhost

- name: Remove the user 'johnd'
  bigip_user:
    server: lb.mydomain.com
    user: admin
    password: secret
    name: johnd
    state: absent
  delegate_to: localhost

- name: Update password
  bigip_user:
    server: lb.mydomain.com
    user: admin
    password: secret
    state: present
    username_credential: johnd
    password_credential: newsupersecretpassword
  delegate_to: localhost

# Note that the second time this task runs, it would fail because
# The password has been changed. Therefore, it is recommended that
# you either,
#
#   * Put this in its own playbook that you run when you need to
#   * Put this task in a `block`
#   * Include `ignore_errors` on this task
- name: Change the Admin password
  bigip_user:
    server: lb.mydomain.com
    user: admin
    password: secret
    state: present
    username_credential: admin
    password_credential: NewSecretPassword
  delegate_to: localhost

- name: Change the root user's password
  bigip_user:
    server: lb.mydomain.com
    user: admin
    password: secret
    username_credential: root
    password_credential: secret
    state: present
  delegate_to: localhost
'''

RETURN = r'''
full_name:
  description: Full name of the user
  returned: changed and success
  type: string
  sample: John Doe
partition_access:
  description:
    - List of strings containing the user's roles and which partitions they
      are applied to. They are specified in the form "partition:role".
  returned: changed and success
  type: list
  sample: ['all:admin']
shell:
  description: The shell assigned to the user account
  returned: changed and success
  type: string
  sample: tmsh
'''

import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
from distutils.version import LooseVersion

try:
    from library.module_utils.network.f5.bigip import HAS_F5SDK
    from library.module_utils.network.f5.bigip import F5Client
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import cleanup_tokens
    from library.module_utils.network.f5.common import f5_argument_spec
    try:
        from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False
except ImportError:
    from ansible.module_utils.network.f5.bigip import HAS_F5SDK
    from ansible.module_utils.network.f5.bigip import F5Client
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import AnsibleF5Parameters
    from ansible.module_utils.network.f5.common import cleanup_tokens
    from ansible.module_utils.network.f5.common import f5_argument_spec
    try:
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    api_map = {
        'partitionAccess': 'partition_access',
        'description': 'full_name',
    }

    updatables = [
        'partition_access', 'full_name', 'shell', 'password_credential'
    ]

    returnables = [
        'shell', 'partition_access', 'full_name', 'username_credential'
    ]

    api_attributes = [
        'shell', 'partitionAccess', 'description', 'name', 'password'
    ]

    @property
    def partition_access(self):
        """Partition access values will require some transformation.


        This operates on both user and device returned values.

        Check if the element is a string from user input in the format of
        name:role, if it is split  it and create dictionary out of it.

        If the access value is a dictionary (returned from device,
        or already processed) and contains nameReference
        key, delete it and append the remaining dictionary element into
        a list.
        If the nameReference key is removed just append the dictionary
        into the list.

        :returns list of dictionaries

        """
        if self._values['partition_access'] is None:
            return
        result = []
        part_access = self._values['partition_access']
        for access in part_access:
            if isinstance(access, dict):
                if 'nameReference' in access:
                    del access['nameReference']

                    result.append(access)
                else:
                    result.append(access)
            if isinstance(access, str):
                acl = access.split(':')
                if acl[0].lower() == 'all':
                    acl[0] = 'all-partitions'
                value = dict(
                    name=acl[0],
                    role=acl[1]
                )

                result.append(value)
        return result

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if api_attribute in self.api_map:
                result[api_attribute] = getattr(
                    self, self.api_map[api_attribute])
            elif api_attribute == 'password':
                result[api_attribute] = self._values['password_credential']
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = kwargs.get('client', None)
        self.kwargs = kwargs

    def exec_module(self):
        if self.is_root_username_credential():
            manager = self.get_manager('root')
        elif self.is_version_less_than_13():
            manager = self.get_manager('v1')
        else:
            manager = self.get_manager('v2')
        return manager.exec_module()

    def get_manager(self, type):
        if type == 'root':
            return RootUserManager(**self.kwargs)
        elif type == 'v1':
            return UnparitionedManager(**self.kwargs)
        elif type == 'v2':
            return PartitionedManager(**self.kwargs)

    def is_version_less_than_13(self):
        """Checks to see if the TMOS version is less than 13

        Anything less than BIG-IP 13.x does not support users
        on different partitions.

        :return: Bool
        """
        version = self.client.api.tmos_version
        if LooseVersion(version) < LooseVersion('13.0.0'):
            return True
        else:
            return False

    def is_root_username_credential(self):
        user = self.module.params.get('username_credential', None)
        if user == 'root':
            return True
        return False


class BaseManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = kwargs.get('client', None)
        self.have = None
        self.want = Parameters(params=self.module.params)
        self.changes = Parameters()

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(params=changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                if key == 'password_credential':
                    new_pass = getattr(self.want, key)
                    if self.want.update_password == 'always':
                        changed[key] = new_pass
                else:
                    # We set the shell parameter to 'none' when bigip does
                    # not return it.
                    if self.want.shell == 'bash':
                        self.validate_shell_parameter()
                    if self.want.shell == 'none' and self.have.shell is None:
                        self.have.shell = 'none'
                    attr1 = getattr(self.want, key)
                    attr2 = getattr(self.have, key)
                    if attr1 != attr2:
                        changed[key] = attr1

        if changed:
            self.changes = Parameters(params=changed)
            return True
        return False

    def validate_shell_parameter(self):
        """Method to validate shell parameters.

        Raise when shell attribute is set to 'bash' with roles set to
        either 'admin' or 'resource-admin'.

        NOTE: Admin and Resource-Admin roles automatically enable access to
        all partitions, removing any other roles that the user might have
        had. There are few other roles which do that but those roles,
        do not allow bash.
        """

        err = "Shell access is only available to " \
              "'admin' or 'resource-admin' roles"
        permit = ['admin', 'resource-admin']

        if self.have is not None:
            have = self.have.partition_access
            if not any(r['role'] for r in have if r['role'] in permit):
                raise F5ModuleError(err)

        # This check is needed if we want to modify shell AND
        # partition_access attribute.
        # This check will also trigger on create.
        if self.want.partition_access is not None:
            want = self.want.partition_access
            if not any(r['role'] for r in want if r['role'] in permit):
                raise F5ModuleError(err)

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def validate_create_parameters(self):
        """Password credentials and partition access are mandatory,

        when creating a user resource.
        """
        if self.want.password_credential and \
                self.want.update_password != 'on_create':
            err = "The 'update_password' option " \
                  "needs to be set to 'on_create' when creating " \
                  "a resource with a password."
            raise F5ModuleError(err)
        if self.want.partition_access is None:
            err = "The 'partition_access' option " \
                  "is required when creating a resource."
            raise F5ModuleError(err)

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the user")
        return True

    def create(self):
        self.validate_create_parameters()
        if self.want.shell == 'bash':
            self.validate_shell_parameter()
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True


class UnparitionedManager(BaseManager):
    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.auth.users.user.create(**params)

    def update_on_device(self):
        params = self.want.api_params()
        result = self.client.api.tm.auth.users.user.load(name=self.want.name)
        result.modify(**params)

    def read_current_from_device(self):
        tmp_res = self.client.api.tm.auth.users.user.load(name=self.want.name)
        result = tmp_res.attrs
        return Parameters(params=result)

    def exists(self):
        return self.client.api.tm.auth.users.user.exists(name=self.want.name)

    def remove_from_device(self):
        result = self.client.api.tm.auth.users.user.load(name=self.want.name)
        if result:
            result.delete()


class PartitionedManager(BaseManager):
    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.auth.users.user.create(
            partition=self.want.partition, **params
        )

    def _read_one_resource_from_collection(self):
        collection = self.client.api.tm.auth.users.get_collection(
            requests_params=dict(
                params="$filter=partition+eq+'{0}'".format(self.want.partition)
            )
        )
        collection = [x for x in collection if x.name == self.want.name]
        if len(collection) == 1:
            resource = collection.pop()
            return resource
        elif len(collection) == 0:
            raise F5ModuleError(
                "No accounts with the provided name were found"
            )
        else:
            raise F5ModuleError(
                "Multiple users with the provided name were found!"
            )

    def update_on_device(self):
        params = self.want.api_params()
        try:
            resource = self._read_one_resource_from_collection()
            resource.modify(**params)
        except iControlUnexpectedHTTPError as ex:
            # TODO: Patch this in the F5 SDK so that I dont need this check
            if 'updated successfully' not in str(ex):
                raise F5ModuleError(
                    "Failed to update the specified user"
                )

    def read_current_from_device(self):
        resource = self._read_one_resource_from_collection()
        result = resource.attrs
        return Parameters(params=result)

    def exists(self):
        collection = self.client.api.tm.auth.users.get_collection(
            requests_params=dict(
                params="$filter=partition+eq+'{0}'".format(self.want.partition)
            )
        )
        collection = [x for x in collection if x.name == self.want.name]
        if len(collection) == 1:
            result = True
        elif len(collection) == 0:
            result = False
        else:
            raise F5ModuleError(
                "Multiple users with the provided name were found!"
            )
        return result

    def remove_from_device(self):
        resource = self._read_one_resource_from_collection()
        if resource:
            resource.delete()


class RootUserManager(BaseManager):
    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                raise F5ModuleError(
                    "You may not remove the root user."
                )
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        return True

    def update(self):
        result = self.update_on_device()
        return result

    def update_on_device(self):
        escape_patterns = r'([$' + "'])"
        errors = ['Bad password', 'password change canceled', 'based on a dictionary word']
        content = "{0}\n{0}\n".format(self.want.password_credential)
        command = re.sub(escape_patterns, r'\\\1', content)
        cmd = '-c "printf \\\"{0}\\\" | tmsh modify auth password root"'.format(command)
        try:
            output = self.client.api.tm.util.bash.exec_cmd(
                'run',
                utilCmdArgs=cmd
            )
            if hasattr(output, 'commandResult'):
                result = str(output.commandResult)
                if any(x for x in errors if x in result):
                    raise F5ModuleError(result)
            return True
        except iControlUnexpectedHTTPError:
            return False


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            name=dict(
                required=True,
                aliases=['username_credential']
            ),
            password_credential=dict(
                no_log=True,
            ),
            partition_access=dict(
                type='list'
            ),
            full_name=dict(),
            shell=dict(
                choices=['none', 'bash', 'tmsh']
            ),
            update_password=dict(
                default='always',
                choices=['always', 'on_create']
            ),
            state=dict(default='present', choices=['absent', 'present']),
            partition=dict(
                default='Common',
                fallback=(env_fallback, ['F5_PARTITION'])
            )
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    if not HAS_F5SDK:
        module.fail_json(msg="The python f5-sdk module is required")

    try:
        client = F5Client(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        module.exit_json(**results)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
