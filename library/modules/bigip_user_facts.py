#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
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
  - Facts are placed in the C(bigip) variable
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Gather facts about user 'johnd'
  bigip_user_facts:
    name: johnd
    password: secret
    server: lb.mydomain.com
    user: admin
    validate_certs: no
  delegate_to: localhost

- name: Display the user facts
  debug:
    var: bigip
'''

RETURN = r'''
description:
  description: The description of the user
  returned: changed
  type: string
  sample: John Doe
username_credential:
  description: The username beign searched for
  returned: changed
  type: string
  sample: jdoe
encrypted_password:
  description: The encrypted value of the password
  returned: changed
  type: string
  sample: $6$/cgtFz0....yzv465uAJ/
partition_access:
  description: Access permissions for the account
  returned: changed
  type: list
  sample:
    - name: all-partitions
      role: admin
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


def cleanup_tokens(client):
    try:
        resource = client.api.shared.authz.tokens_s.token.load(
            name=client.api.icrs.token
        )
        resource.delete()
    except Exception:
        pass


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
