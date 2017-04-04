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
module: bigip_partition
short_description: Manage BIG-IP partitions
description:
  - Manage BIG-IP partitions
version_added: "2.3"
options:
  description:
    description:
      - The description to attach to the Partition
    required: False
    default: None
  route_domain:
    description:
      - The default Route Domain to assign to the Partition. If no route domain
        is specified, then the default route domain for the system (typically
        zero) will be used only when creating a new partition. C(route_domain)
        and C(route_domain_id) are mutually exclusive.
    required: False
    default: None
  state:
    description:
      - Whether the partition should exist or not
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the bigsuds Python package on the host if using the iControl
    interface. This is as easy as pip install bigsuds
requirements:
  - bigsuds
  - requests
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Create partition "foo" using the default route domain
  bigip_partition:
      name: "foo"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"

- name: Delete the foo partition
  bigip_partition:
      name: "foo"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
      state: "absent"
'''

RETURN = '''
route_domain:
    description: Name of the route domain associated with the partition
    returned: changed and success
    type: string
    sample: "0"
description:
    description: The description of the partition
    returned: changed and success
    type: string
    sample: "Example partition"
name:
    description: The name of the partition
    returned: changed and success
    type: string
    sample: "/foo"
'''

try:
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

def connect_to_bigip(**kwargs):
    return ManagementRoot(kwargs['server'],
                          kwargs['user'],
                          kwargs['password'],
                          port=kwargs['server_port'],
                          token=True)


class BigIpPartitionManager(object):
    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = None

    def apply_changes(self):
        result = dict()
        changed = False

        try:
            self.api = connect_to_bigip(**self.params)

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
        if self.partition_exists():
            return False
        else:
            return self.ensure_partition_is_present()

    def absent(self):
        changed = False
        if self.partition_exists():
            changed = self.ensure_partition_is_absent()
        return changed

    def partition_exists(self):
        return self.api.tm.sys.folder.exists(
            name=self.params['name']
        )






    def get_route_domain_id(self, route_domain):
        resp = self.api.Networking.RouteDomainV2.get_identifier(
            route_domains=[route_domain]
        )
        return resp[0]

    def create(self):
        name = self.params['name']
        folder = self.params['folder']
        # description = self.params['description']
        route_domain = self.params['route_domain']

        if route_domain:
            # When setting the default route domain, you need to use the ID
            # instead of the string name. So if the name was specified, we
            # need to translate it
            self.params['route_domain_id'] = self.get_route_domain_id(route_domain)

        route_domain_id = self.params['route_domain_id']

        self.api.System.Session.start_transaction()
        self.api.Management.Folder.create(
            folders=[folder]
        )

        # A valid route domain is zero, so I need to specifically check
        # for None
        if route_domain_id is not None:
            self.api.Management.Partition.set_default_route_domain(
                partitions=[name],
                route_domains=[route_domain_id]
            )

        self.api.System.Session.submit_transaction()

        return True

    def update(self):
        changed = dict()

        name = self.params['name']
        folder = self.params['folder']
        description = self.params['description']
        route_domain = self.params['route_domain']
        route_domain_id = self.params['route_domain_id']

        current = self.read()

        if route_domain:
            if '/' + route_domain not in current['route_domain']:
                changed['route_domain'] = True

        if route_domain_id is not None:
            if route_domain_id != current['route_domain_id']:
                changed['route_domain_id'] = True

        if description:
            if description != current['description']:
                changed['description'] = True

        if changed:
            if 'route_domain' in changed:
                # This is a special case because the route domain name needs
                # to be translated to an ID
                route_domain_id = self.get_route_domain_id(route_domain)
                changed['route_domain_id'] = True

            self.api.System.Session.start_transaction()

            if 'route_domain_id' in changed:
                self.api.Management.Partition.set_default_route_domain(
                    partitions=[name],
                    route_domains=[route_domain_id]
                )

            if 'description' in changed:
                self.api.Management.Folder.set_description(
                    folders=[folder],
                    descriptions=[description]
                )

                try:
                    # This method is only available on BIG-IP >= 11.0.0
                    self.api.Management.Folder.set_description(
                        folders=[folder],
                        descriptions=[description]
                    )
                except Exception:
                    self.api.Management.Partition.set_description(
                        partitions=[name],
                        descriptions=[description]
                    )

            self.api.System.Session.submit_transaction()
            return True
        return False

    def absent(self):
        folder = self.params['folder']

        if not self.exists():
            return False

        if self.params['check_mode']:
            return True

        self.api.Management.Folder.delete_folder(
            folders=[folder]
        )

        if self.exists():
            raise DeleteFolderError()
        else:
            return True

    def read(self):
        result = dict()
        name = self.params['name']
        folder = self.params['folder']

        try:
            # This method is only available on BIG-IP >= 11.0.0
            resp = self.api.Management.Folder.get_description(
                folders=[folder]
            )
            result['description'] = resp[0]
        except Exception:
            resp = self.api.Management.Partition.get_description(
                partitions=[name]
            )
            result['description'] = resp[0]

        resp = self.api.Management.Partition.get_default_route_domain(
            partitions=[name]
        )
        result['route_domain_id'] = resp[0]

        resp = self.api.Networking.RouteDomainV2.get_list()
        for route_domain in resp:
            id = self.get_route_domain_id(route_domain)
            if id == result['route_domain_id']:
                result['route_domain'] = route_domain

        result['name'] = folder
        return result


class BigIpPartitionModuleConfig(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.states = ['present', 'absent']

        self.initialize_meta_args()
        self.initialize_argument_spec()

    def initialize_meta_args(self):
        args = dict(
            name=dict(required=True),
            description=dict(required=False, default=None),
            route_domain=dict(required=False, default=None)
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

    config = BigIpPartitionModuleConfig()
    module = config.create()

    try:
        obj = BigIpPartitionManager(
            check_mode=module.check_mode, **module.params
        )
        result = obj.apply_changes()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
