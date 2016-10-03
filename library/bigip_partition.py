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
module: bigip_partition
short_description: Manage BIG-IP partitions
description:
  - Manage BIG-IP partitions
version_added: "2.2"
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
  route_domain_id:
    description:
      - The default Route Domain ID to assign to the Partition. If you track
        the route domains by their numeric identifier, then this argument
        can be used to supply that ID. C(route_domain) and C(route_domain_id)
        are mutually exclusive.
    required: False
    default: None
  server:
    description:
      - BIG-IP host
    required: true
  state:
    description:
      - Whether the partition should exist or not
    required: false
    default: present
    choices:
      - present
      - absent
  user:
    description:
      - BIG-IP username
    required: false
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
  - Requires the bigsuds Python package on the host if using the iControl
    interface. This is as easy as pip install bigsuds
requirements:
  - bigsuds
  - requests
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
route_domain_id:
    description: ID of the route domain associated with the partition
    returned: changed and success
    type: string
    sample: "0"
route_domain:
    description: Name of the route domain associated with the partition
    returned: changed and success
    type: string
    sample: "/Common/asdf"
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

TRANSPORTS = ['rest', 'soap']


class DeleteFolderError(Exception):
    pass


class BigIpApiFactory(object):
    def factory(module):
        connection = module.params.get('connection')

        if connection == 'rest':
            if not requests_found:
                raise Exception("The python requests module is required")
            return BigIpRestApi(check_mode=module.check_mode, **module.params)
        elif connection == 'soap':
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")
            return BigIpSoapApi(check_mode=module.check_mode, **module.params)

    factory = staticmethod(factory)


class BigIpCommon(object):
    def __init__(self, *args, **kwargs):
        self.result = dict(changed=False, changes=dict())

        if kwargs['name'][0:1] != '/':
            kwargs['folder'] = '/' + kwargs['name']
        else:
            kwargs['folder'] = kwargs['name']

        self.params = kwargs
        self.current = dict()

    def flush(self):
        result = dict()
        state = self.params['state']

        if state == "present":
            changed = self.present()

            if not self.params['check_mode']:
                current = self.read()
                result.update(current)
        else:
            changed = self.absent()

        result.update(dict(changed=changed))
        return result


class BigIpSoapApi(BigIpCommon):
    def __init__(self, *args, **kwargs):
        super(BigIpSoapApi, self).__init__(*args, **kwargs)

        self.api = bigip_api(kwargs['server'],
                             kwargs['user'],
                             kwargs['password'],
                             kwargs['validate_certs'])

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

    def exists(self):
        name = self.params['name']
        resp = self.api.Management.Partition.get_partition_list()
        for partition in resp:
            if partition['partition_name'] == name:
                return True
        return False

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

    def present(self):
        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True
            return self.create()


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        connection=dict(default='soap', choices=TRANSPORTS),
        description=dict(required=False, default=None),
        name=dict(required=True),
        route_domain=dict(required=False, default=None),
        route_domain_id=dict(required=False, default=None)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ['route_domain', 'route_domain_id']
        ]
    )

    try:
        obj = BigIpApiFactory.factory(module)
        result = obj.flush()

        module.exit_json(**result)
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host")
    except bigsuds.ServerError as e:
        module.fail_json(msg=str(e))
    except DeleteFolderError:
        module.fail_json(msg='Failed to delete the specified partition')

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
