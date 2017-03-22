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
module: bigip_view
short_description: Manage ZoneRunner Views on a BIG-IP
description:
  - Manage ZoneRunner Views on a BIG-IP. ZoneRunner is a feature of the GTM
    module. Therefore, this module should only be used on BIG-IP systems that
    have the GTM module enabled. The SOAP connection has a number of known
    limitations when it comes to updating Views. It is only possible to
version_added: "2.2"
options:
  user:
    description:
      - BIG-IP username
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  port:
    description:
      - BIG-IP web API port
    required: false
    default: 443
  server:
    description:
      - BIG-IP host
    required: true
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
  zones:
    description:
      - A sequence of zones in this view
    required: false
    default: None
  state:
    description:
      - When C(present), will ensure that the View exists with the correct
        zones in it. When C(absent), removes the View.
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
- name: Create a view foo.local
  local_action:
      module: "bigip_view"
      user: "admin"
      password: "admin"
      name: "foo.local"

- name: Assign zone "bar" to view "foo.local"
  local_action:
      module: "bigip_view"
      user: "admin"
      password: "admin"
      name: "foo.local"
      zones:
          - "bar"
'''


class ViewInfoException(Exception):
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
        self.params = kwargs
        self.current = dict()

        self.zones = []

    def correct_zone_name_format(self):
        new_zones = []
        # Ensure that the zone names are correctly formatted. Note that they
        # need to have a dot at the end of the name
        for zone in self.params['view_zones']:
            if not zone.endswith('.'):
                zone += '.'
            new_zones.append(zone)

        self.zones = new_zones

    def has_gtm(self):
        try:
            self.api.Management.Provision.get_level(
                modules=['TMOS_MODULE_GTM']
            )
            return True
        except bigsuds.ServerError:
            return False

    def flush(self):
        result = dict()
        state = self.params['state']

        if not self.has_gtm():
            raise Exception('This module only works with GTM enabled')

        current = self.read()

        if state == "present":
            if self.params['check_mode']:
                if current['view_name'] != self.params['view_name']:
                    changed = True
                elif current['view_zones'] != self.params['view_zones']:
                    changed = True
            else:
                changed = self.present()
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
                             kwargs['validate_certs'],
                             kwargs['port'])

    def read(self):
        try:
            response = self.api.Management.View.get_view([self.params['view_name']])[0]
        except Exception:
            response = {}

        return response

    def create(self):
        view_info = {
            'view_name': self.params['view_name']
        }

        if self.params['view_order'] == 'first':
            view_info['view_order'] = '0'
        elif self.params['view_order'] == 'last':
            view_info['view_order'] = '0xffffffff'
        elif self.params['view_order']:
            view_info['view_order'] = self.params['view_order']

        if self.params['options']:
            view_info['option_seq'] = self.params['options']
        if self.params['zones']:
            view_info['zone_names'] = self.params['zones']

        self.set_active_folder()
        self.api.Management.View.add_view(
            views=[view_info]
        )
        self.reset_active_folder()

        if self.read():
            return True
        else:
            raise Exception('Failed to add the view')

    def exists(self):
        if self.read():
            return True
        else:
            return False

    def update(self):
        """Updates a view if parameters have changed

        The SOAP View API does not support transactions, so we cannot
        guarantee that atomic operations can take place.

        There exists the possibility that if you lose connectivity to
        your BIG-IP during these operations, your configuration may be
        left in an inconsistent state.
        """
        current = self.read()

        if self.params['view_order'] != current['view_order']:
            current['view_order'] = self.params['view_order']
            self.set_active_folder()
            self.api.Management.View.move_view(
                views=[current]
            )
            self.reset_active_folder()
        if params['zones'] != current['zones']:
            current['view_order'] = self.params['view_order']
            self.set_active_folder()
            self.api.Management.View.move_view(
                views=[current]
            )
            self.reset_active_folder()

    def delete(self):
        view_info = self.read()

        self.set_active_folder()
        self.api.Management.View.delete_view(
            views=[view_info]
        )
        self.reset_active_folder()

        if self.exists():
            return True
        else:
            raise Exception('Failed to add the view')

    def set_active_folder(self):
        # need to switch to root, set recursive query state
        self.current_folder = self.api.System.Session.get_active_folder()
        if self.current_folder != '/' + self.params['partition']:
            self.api.System.Session.set_active_folder(folder='/' + self.params['partition'])

        self.current_query_state = self.api.System.Session.get_recursive_query_state()
        if self.current_query_state == 'STATE_DISABLED':
            self.api.System.Session.set_recursive_query_state('STATE_ENABLED')

    def reset_active_folder(self):
        # set everything back
        if self.current_query_state == 'STATE_DISABLED':
            self.api.System.Session.set_recursive_query_state('STATE_DISABLED')

        if self.current_folder != '/' + self.params['partition']:
            self.api.System.Session.set_active_folder(folder=self.current_folder)

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def absent(self):
        if self.exists():
            return self.delete()
        else:
            return False


class BigIpRestApi(BigIpCommon):
    def __init__(self, *args, **kwargs):
        super(BigIpRestApi, self).__init__(*args, **kwargs)

        server = self.params['server']

        self._uri = 'https://%s/mgmt/tm/auth/user' % (server)
        self._headers = {
            'Content-Type': 'application/json'
        }


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        view_name=dict(default='external'),
        view_order=dict(required=False, type='int', default=None),
        options=dict(required=False, type='list', default=None),
        zones=dict(required=False, default=None)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpApiFactory.factory(module)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))


from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
