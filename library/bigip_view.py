#!/usr/bin/python

# Ansible module to manage BIG-IP devices
#
# This module covers the ResourceRecord interfaces described in the iControl
# Management documentation.
#
# More information can be found here
#
#    https://devcentral.f5.com/wiki/iControl.Management.ashx
#

DOCUMENTATION = '''
---
module: bigip_view
short_description: Manage resource records on a BIG-IP
description:
   - Manage resource records on a BIG-IP
version_added: "1.8"
options:
  username:
    description:
      - The username used to authenticate with
    required: true
    default: admin
  password:
    description:
      - The password used to authenticate with
    required: true
    default: admin
  hostname:
    description:
      - BIG-IP host to connect to
    required: true
    default: localhost
  view_name:
    description:
      - The name of the view
    required: true
  view_order:
    description:
      - The order of the view within the named.conf file. 0 = first in zone.
      0xffffffff means to move the view to last. Any other number will move the
      view to that position, and bump up any view(s) by one (if necessary).
    default: 0
  options:
    description:
      - A sequence of options for the view
  zone_names:
    description:
      - A sequence of zones in this view
    required: true
  state:
    description:
      - Whether the record should exist.  When C(absent), removes
        the record.
    required: false
    default: present
    choices: [ "present", "absent" ]
notes:
   - Requires the bigsuds Python package on the remote host. This is as easy as
     pip install bigsuds

requirements: [ "bigsuds", "distutils" ]
author: Tim Rupp <t.rupp@f5.com>
'''

EXAMPLES = """

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
"""

import sys
import re
from distutils.version import StrictVersion

try:
    import bigsuds
except ImportError:
	bigsuds_found = False
else:
	bigsuds_found = True

VERSION_PATTERN='BIG-IP_v(?P<version>\d+\.\d+\.\d+)'

class ViewInfoException(Exception):
	  pass

class ViewInfo(object):
    REQUIRED_BIGIP_VERSION='9.0.3'

    def __init__(self, module):
        new_zones = []

        self.module = module

        self.username = module.params['username']
        self.password = module.params['password']
        self.hostname = module.params['hostname']
        self.view = module.params['view_name']
        self.order = module.params['view_order']
        self.options = module.params['options']
        self.zones = module.params['zone_names']

        # Ensure that the zone names are correctly formatted. Note that they
        # need to have a dot at the end of the name
        for zone in self.zone_names:
            if not zone.endswith('.'):
                zone += '.'
            new_zones.append(zone)
        self.zones = new_zones

        self.client = bigsuds.BIGIP(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            debug=True
        )

        # Do some checking of things
        self.check_version()
       
    def check_version(self):
        response = self.client.System.SystemInfo.get_version()
        match = re.search(VERSION_PATTERN, response)
        version = match.group('version')

        v1 = StrictVersion(version)
        v2 = StrictVersion(self.REQUIRED_BIGIP_VERSION)

        if v1 < v2:
            raise ViewException('The BIG-IP version %s does not support this feature' % version)

    def create_view(self):
        view_info = [{
            'view_name': self.view,
            'view_order': self.view_order,
            'option_seq': self.options,
            'zone_names': self.zone_names
        }]

        #try:
        response = self.client.Management.View.add_view(
            views=view_info
        )
        #except Exception, e:
        #    raise ViewException(str(e))

def main():
    module = AnsibleModule(
        argument_spec = dict(
            username=dict(default='admin'),
            password=dict(default='admin'),
            hostname=dict(default='localhost'),
            view_name=dict(default='external'),
            view_order=dict(default=0),
            options=dict(required=False, type='list'),
            zone_names=dict(required=True, type='list'),
            state=dict(default="present", choices=["absent", "present"]),
        )
    )

    state = module.params["state"]

    if not bigsuds_found:
        module.fail_json(msg="The python bigsuds module is required")

    #try:
    view_info = ViewInfo(module)

    if state == "present":
        view_info.create_view()
        changed = True
    elif state == "absent":
        record.delete_record()
    #except Exception, e:
    #    module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
main()