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
module: bigip_gtm_datacenter
short_description: Manage Datacenter configuration in BIG-IP
description:
   - Manage BIG-IP data center configuration. A data center defines the location
     where the physical network components reside, such as the server and link
     objects that share the same subnet on the network. This module is able to
     manipulate the data center definitions in a BIG-IP
version_added: "2.0"
options:
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: rest
    choices: [ "rest", "icontrol" ]
  contact:
    description:
      - The name of the contact for the data center
    required: false
    default: None
  description:
    description:
      - The description of the data center
    required: false
    default: None
  enabled:
    description:
      - Whether the data center should be enabled. At least one of state and enabled are required.
    required: false
    default: None
  location:
    description:
      - The location of the data center
    required: false
    default: None
  name:
    description:
      - The name of the data center
    required: true
  password:
    description:
      - BIG-IP password
    required: false
    default: admin
  server:
    description:
      - BIG-IP host
    required: true
  user:
    description:
      - BIG-IP username
    required: false
    default: admin
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: yes
    choices: [ "yes", "no" ]
  state:
    description:
      - The state of the datacenter on the BIG-IP. When C(present), guarantees
        that the data center exists. When C(absent) removes the data center
        from the BIG-IP. C(enabled) will enable the data center and C(disabled)
        will ensure the data center is disabled. At least one of state and enabled are required.
    required: false
    default: None
    choices: [ "present", "absent" ]

notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds

requirements: [ "bigsuds", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
- name: Create data center "New York"
  bigip_gtm_datacenter:
      server: "big-ip"
      name: "New York"
      location: "New York"
  delegate_to: localhost
"""

import json
import socket

try:
    import bigsuds
except ImportError:
    bigsuds_found = False
else:
    bigsuds_found = True

try:
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True


def test_icontrol(username, password, hostname):
    api = bigsuds.BIGIP(
        hostname=hostname,
        username=username,
        password=password,
        debug=True
    )

    try:
        response = api.Management.LicenseAdministration.get_license_activation_status()
        if 'STATE' in response:
            return True
        else:
            return False
    except:
        return False


class BigIpCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._hostname = module.params.get('server')

        self._name = module.params.get('name')
        self._description = module.params.get('description')
        self._location = module.params.get('location')
        self._contact = module.params.get('contact')
        self._validate_certs = module.params.get('validate_certs')


class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )

    def create(self):
        params = {
            'name': self._name,
            'location': self._location,
            'contact': self._contact
        }

        self.api.GlobalLB.DataCenter.create(params)
        self.set_description()
        return True

    def delete(self):
        self.api.GlobalLB.DataCenter.delete_data_center([self._name])

    def get_enabled(self):
        return self.api.GlobalLB.DataCenter.get_enabled_state([self._name])[0]

    def get_contact(self):
        return self.api.GlobalLB.DataCenter.get_contact_information([self._name])[0]

    def get_location(self):
        return self.api.GlobalLB.DataCenter.get_location_information([self._name])[0]

    def get_description(self):
        return self.api.GlobalLB.DataCenter.get_description([self._name])[0]

    def set_enabled(self):
        status = self.get_enabled()
        if status == 'STATE_ENABLED':
            return False
        else:
            self.api.GlobalLB.DataCenter.set_enabled_state([self._name], ['STATE_ENABLED'])
            return True

    def set_disabled(self):
        status = self.get_enabled()

        if status == 'STATE_DISABLED':
            return False
        else:
            self.api.GlobalLB.DataCenter.set_enabled_state([self._name], ['STATE_DISABLED'])
            return True

    def set_contact(self):
        current = self.get_contact()

        if current != self._contact:
            self.api.GlobalLB.DataCenter.set_contact_information([self._name], [self._contact])
            return True
        else:
            return False

    def set_location(self):
        current = self.get_location()

        if current != self._location:
            self.api.GlobalLB.DataCenter.set_location_information([self._name], [self._location])
            return True
        else:
            return False

    def set_description(self):
        current = self.get_description()

        if current != self._description:
            self.api.GlobalLB.DataCenter.set_description([self._name], [self._description])
            return True
        else:
            return False

    def exists(self):
        tmp_name = '/Common/%s' % self._name

        try:
            response = self.api.GlobalLB.DataCenter.get_list()

            if tmp_name in response:
                return True
            else:
                return False
        except bigsuds.ServerError:
            return False

    def absent(self):
        changed = False

        if self.exists():
            changed = self.delete()

        return changed

    def present(self):
        changed = False

        if self.exists():
            if self._contact is not None:
                changed = self.set_contact()

            if self._location is not None:
                changed = self.set_location()

            if self._description is not None:
                changed = self.set_description()
        else:
            changed = self.create()

        return changed

    def enable(self):
        changed = False
        current = self.get_enabled()

        if not current:
            self.set_enabled()
            changed = True

        return changed

    def disable(self):
        changed = False
        current = self.get_enabled()

        if current:
            self.set_disabled()
            changed = True

        return changed


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm/gtm/datacenter' % (self._hostname)
        self._headers = {
            'Content-Type': 'application/json'
        }
        self._full_name = '~Common~%s' % self._name

    def create(self):
        params = dict(
            name=self._name,
            location=self._location,
            contact=self._contact,
            description=self._description
        )

        resp = requests.post(self._uri,
                             auth=(self._username, self._password),
                             data=json.dumps(params),
                             verify=self._validate_certs,
                             headers=self._headers)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def read(self):
        uri = '%s/%s' % (self._uri, self._full_name)
        resp = requests.get(uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)
        if resp.status_code == 200:
            return resp.json()
        else:
            res = resp.json()
            raise Exception(res['message'])

    def update(self):
        uri = '%s/%s' % (self._uri, self._full_name)
        resp = requests.put(uri,
                            auth=(self._username, self._password),
                            data=json.dumps(self._payload),
                            verify=self._validate_certs,
                            headers=self._headers)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def delete(self):
        uri = '%s/%s' % (self._uri, self._full_name)
        resp = requests.delete(uri,
                               auth=(self._username, self._password),
                               verify=self._validate_certs)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def get_enabled(self):
        info = self.read()

        # If a data center is disabled, it will not have an enabled field.
        # Instead it will have a disabled field
        if 'enabled' in info:
            return True
        return False

    def get_contact(self):
        info = self.read()
        if 'contact' in info:
            return info['contact']
        return None

    def get_location(self):
        info = self.read()
        if 'location' in info:
            return info['location']
        return None

    def get_description(self):
        info = self.read()
        if 'description' in info:
            return info['description']
        return None

    def set_enabled(self):
        status = self.get_enabled()

        if status:
            return False
        else:
            self._payload = {
                'enabled': True
            }
            return self.update()

    def set_disabled(self):
        status = self.get_enabled()

        if not status:
            return False
        else:
            self._payload = {
                'disabled': True
            }
            return self.update()

    def set_contact(self):
        current = self.get_contact()

        if current != self._contact:
            self._payload = {
                'contact': self._contact
            }
            return self.update()
        else:
            return False

    def set_location(self):
        current = self.get_location()

        if current != self._location:
            self._payload = {
                'location': self._location
            }
            return self.update()
        else:
            return False

    def set_description(self):
        current = self.get_description()

        if current != self._description:
            self._payload = {
                'description': self._description
            }
            return self.update()
        else:
            return False

    def present(self):
        changed = False

        if self.exists():
            if self._contact is not None:
                changed = self.set_contact()

            if self._location is not None:
                changed = self.set_location()

            if self._description is not None:
                changed = self.set_description()
        else:
            changed = self.create()

        return changed

    def absent(self):
        changed = False

        if self.exists():
            changed = self.delete()

        return changed

    def enable(self):
        changed = False
        current = self.get_enabled()

        if not current:
            self.set_enabled()
            changed = True

        return changed

    def disable(self):
        changed = False
        current = self.get_enabled()

        if current:
            self.set_disabled()
            changed = True

        return changed

    def exists(self):
        uri = '%s/%s' % (self._uri, self._full_name)
        resp = requests.get(uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)
        if resp.status_code == 200:
            return True
        else:
            return False


def main():
    changed = False
    icontrol = False

    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(default='rest', choices=['icontrol', 'rest']),
            contact=dict(required=False, default=None),
            description=dict(required=False, default=None),
            enabled=dict(type='bool'),
            location=dict(required=False, default=None),
            name=dict(require=True),
            password=dict(default='admin'),
            server=dict(required=True),
            state=dict(choices=['present', 'absent']),
            user=dict(default='admin'),
            validate_certs=dict(default=True, type='bool')
        )
    )

    connection = module.params.get('connection')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')
    enabled = module.params.get('enabled')

    try:
        if connection == 'icontrol':
            if not bigsuds_found:
                pass

            icontrol = test_icontrol(username, password, hostname)
            if icontrol:
                obj = BigIpIControl(module)

        if not icontrol:
            obj = BigIpRest(module)

        if state is None and enabled is None:
            module.fail_json(msg="Neither 'state' nor 'enabled' set")

        if enabled is not None:
            if enabled:
                changed = obj.set_enabled()
            else:
                changed = obj.set_disabled()

        if state is None:
            module.exit_json(changed=changed)

        if state == "present":
            if obj.present():
                changed = True
        elif state == "absent":
            if obj.absent():
                changed = True
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except socket.timeout:
        module.fail_json(msg="Timed out connecting to the BIG-IP")

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
