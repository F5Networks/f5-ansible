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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
---
module: bigip_user_facts
short_description: Retrieve user account attributes from a BIG-IP
description:
   - Retrieve user account attributes from a BIG-IP
version_added: "2.2"
options:
  username_credential:
    description:
      - Name of the user to retrieve facts for
    required: true
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk
  - Facts are placed in the C(bigip) variable
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Gather facts about user 'johnd'
  bigip_user_facts:
      name: "johnd"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost

- name: Display the user facts
  debug:
    var: bigip
'''

RETURN = '''
description:
    description: The description of the user
    returned: changed
    type: string
    sample: "John Doe"
username_credential:
    description: The username beign searched for
    returned: changed
    type: string
    sample: "jdoe"
encrypted_password:
    description: The encrypted value of the password
    returned: changed
    type: string
    sample: "$6$/cgtFz0....yzv465uAJ/"
partition_access:
    description: Access permissions for the account
    returned: changed
    type: list
    sample:
        - name: "all-partitions"
          role: "admin"
'''

try:
    from f5.bigip import ManagementRoot
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


class BigIpUserFacts(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def exists(self):
        username_credential = self.params['username_credential']
        if self.api.tm.auth.users.user.exists(name=username_credential):
            return True
        else:
            return False

    def flush(self):
        if self.exists:
            result = dict(
                changed=True,
                ansible_facts=dict(
                    bigip=self.read()
                )
            )
        else:
            result = dict(
                changed=False
            )
        return result

    def read(self):
        result = {}

        username_credential = self.params['username_credential']
        user = self.api.tm.auth.users.user.load(name=username_credential)

        result['username_credential'] = username_credential

        if hasattr(user, 'description'):
            result['description'] = user.description

        if hasattr(user, 'encryptedPassword'):
            result['encrypted_password'] = user.encryptedPassword

        if hasattr(user, 'shell'):
            result['shell'] = user.shell

        if hasattr(user, 'partitionAccess'):
            result['partition_access'] = user.partitionAccess

        return result


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        username_credential=dict(required=True, aliases=['name'], no_log=False)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        result = dict()
        obj = BigIpUserFacts(check_mode=module.check_mode, **module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
