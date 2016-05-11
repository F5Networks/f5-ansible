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
module: bigip_zone
short_description: Manage ZoneRunner Zones on a BIG-IP
description:
  - Manage resource records on a BIG-IP
version_added: "2.2"
options:
  user:
    description:
      - The username used to authenticate with
    required: true
  password:
    description:
      - The password used to authenticate with
    required: true
  server:
    description:
      - BIG-IP host
    required: true
  name:
    description:
      - The name of the view
    required: true
  state:
    description:
      - Whether the record should exist.  When C(absent), removes
        the record.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the bigsuds Python package on the remote host. This is as easy as
    pip install bigsuds
requirements:
  - bigsuds
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add a view, named "internal", to organization.com zone
  local_action:
      module: bigip_view
      username: 'admin'
      password: 'admin'
      hostname: 'bigip.organization.com'
      zone_names:
          - 'organization.com'
      state: 'present'
      options:
          - domain_name: elliot.organization.com
            ip_address: 10.1.1.1
'''


class ViewZoneException(Exception):
    pass


class ViewZone(object):
    def __init__(self, module):
        self.module = module

        self.username = module.params['username']
        self.password = module.params['password']
        self.hostname = module.params['hostname']
        self.view_name = module.params['view_name']
        self.zone_name = module.params['zone_name']
        self.zone_type = module.params['zone_type'].lower()
        self.zone_file = module.params['zone_file']
        self.options = module.params['options']
        self.text = module.params['text']

        if not self.zone_name.endswith('.'):
            self.zone_name += '.'

    def get_zone_type(self):
        zone_type_maps = {
            'unset': 'UNSET',
            'master': 'MASTER',
            'slave': 'SLAVE',
            'stub': 'STUB',
            'forward': 'FORWARD',
            'hint': 'HINT'
        }

        if self.zone_type in zone_type_maps:
            return zone_type_maps[self.zone_type]
        else:
            raise ViewZoneException('Specified zone_type does not exist')

    def zone_exists(self):
        view_zone = [{
            'view_name': self.view_name,
            'zone_name': self.zone_name,
        }]

        response = self.client.Management.Zone.zone_exist(
            view_zones=view_zone
        )

        return response

    def create_zone(self):
        view_zone = [{
            'view_name': self.view_name,
            'zone_name': self.zone_name,
            'zone_type': self.get_zone_type(),
            'zone_file': self.zone_file,
            'option_seq': self.options
        }]

        self.client.Management.Zone.add_zone_text(
            zone_records=view_zone,
            text=[[self.text]],
            sync_ptrs=[1]
        )

    def delete_zone(self):
        view_zone = [{
            'view_name': self.view_name,
            'zone_name': self.zone_name
        }]

        self.client.Management.Zone.delete_zone(
            view_zones=view_zone
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            view_name=dict(default='external'),
            zone_name=dict(required=True),
            zone_type=dict(default='master'),
            options=dict(required=False, type='list'),
            zone_file=dict(default=None),
            text=dict(default=None)
        )
    )

    state = module.params["state"]
    zone_file = module.params['zone_file']

    view_zone = ViewZone(module)

    if state == "present":
        if not zone_file:
            raise ViewZoneException('A zone_file must be specified')

        if view_zone.zone_exists():
            changed = False
        else:
            view_zone.create_zone()
            changed = True
    elif state == "absent":
        view_zone.delete_zone()
        changed = True

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
