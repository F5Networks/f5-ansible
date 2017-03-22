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
module: bigip_dns_zone
short_description: Manages DNS zones on a BIG-IP
description:
  - This module manages DNS zones described in the iControl Management
    documentation
version_added: "2.2"
options:
  server:
    description:
      - BIG-IP host
    required: true
  user:
    description:
      - BIG-IP username
    required: true
    aliases:
      - username
  password:
    description:
      - BIG-IP password
    required: true
  zone:
    description:
      - The name of the zone
    required: true
  options:
    description:
      - A sequence of options for the view
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
  - https://devcentral.f5.com/wiki/iControl.Management__Zone.ashx
requirements:
  - bigsuds
  - distutils
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

from distutils.version import StrictVersion
import re

VERSION_PATTERN = 'BIG-IP_v(?P<version>\d+\.\d+\.\d+)'


class ViewZoneException(Exception):
    pass


class ViewZone(object):
    REQUIRED_BIGIP_VERSION = '9.0.3'

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

        self.client = bigsuds.BIGIP(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            debug=True
        )

        # Do some checking of things
        self.check_version()

    def get_zone_type(self):
        zone_type_maps = dict(
            unset='UNSET',      # Not yet initialized
            master='MASTER',    # A master zone
            slave='SLAVE',      # A slave zone
            stub='STUB',        # A stub zone
            forward='FORWARD',  # A forward zone
            hint='HINT'         # A hint zone, "."
        )

        if self.zone_type in zone_type_maps:
            return zone_type_maps[self.zone_type]
        else:
            raise ViewZoneException('Specified zone_type does not exist')

    def check_version(self):
        response = self.client.System.SystemInfo.get_version()
        match = re.search(VERSION_PATTERN, response)
        version = match.group('version')

        v1 = StrictVersion(version)
        v2 = StrictVersion(self.REQUIRED_BIGIP_VERSION)

        if v1 < v2:
            raise ViewException('The BIG-IP version %s does not support this feature' % version)

    def zone_exists(self):
        view_zone = dict(
            view_name=self.view_name,
            zone_name=self.zone_name,
        )

        response = self.client.Management.Zone.zone_exist(
            view_zones=[view_zone]
        )

        return response

    def create_zone(self):
        view_zone = dict(
            view_name=self.view_name,
            zone_name=self.zone_name,
            zone_type=self.get_zone_type(),
            zone_file=self.zone_file,
            option_seq=self.options
        )

        self.client.Management.Zone.add_zone_text(
            zone_records=[view_zone],
            text=[[self.text]],
            sync_ptrs=[1]
        )

    def delete_zone(self):
        view_zone = dict(
            view_name=self.view_name,
            zone_name=self.zone_name
        )

        self.client.Management.Zone.delete_zone(
            view_zones=[view_zone]
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            username=dict(default='admin'),
            password=dict(default='admin'),
            hostname=dict(default='localhost'),
            view_name=dict(default='external'),
            zone_name=dict(required=True),
            zone_type=dict(default='master'),
            options=dict(required=False, type='list'),
            zone_file=dict(default=None),
            text=dict(default=None),
            state=dict(default="present", choices=["absent", "present"]),
        )
    )

    state = module.params["state"]
    zone_file = module.params['zone_file']

    if not bigsuds_found:
        module.fail_json(msg="The python bigsuds module is required")

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
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
