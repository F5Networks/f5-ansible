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
module: bigip_license
short_description: Manage license installation and activation on BIG-IP devices
description:
   - Manage license installation and activation on BIG-IP devices
version_added: "2.0"
options:
  dossier_file:
    description:
      - Path to file containing kernel dossier for your system
    required: false
  server:
    description:
      - BIG-IP host to connect to
    required: true
  key:
    description:
      - The registration key to use to license the BIG-IP
    required: true
  license_file:
    description:
      - Path to file containing the license to use
    required: false
  license_options:
    description:
      - Dictionary of options to use when creating the license
    required: false
  password:
    description:
      - The password of the user used to authenticate to the BIG-IP
    required: true
  state:
    description:
      - The state of the license on the system. When C(present), only guarantees
        that a license is there. When C(latest) ensures that the license is always
        valid. C(latest) is most useful internally.
    required: false
    default: present
    choices:
      - present
      - latest
  wsdl:
    description:
      - WSDL file to use if you're receiving errors when downloading the WSDL
        file at run-time from the licensing servers
    required: false
    default: None
  user:
    description:
      - The username used when connecting to the BIG-IP
    required: true
    aliases:
      - username
notes:
  - Requires the suds Python package on the host. This is as easy as
    pip install suds
  - Requires the bigsuds Python package on the host. This is as easy as
    pip install bigsuds
requirements:
  - bigsuds
  - suds
author: Tim Rupp <t.rupp@f5.com>
'''

EXAMPLES = """
- name: License BIG-IP using iControl delegated to localhost
  bigip_license:
      server: "big-ip"
      username: "admin"
      password: "MyPassword123"
      key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
  delegate_to: localhost

- name: License BIG-IP using iControl specifying license options
  bigip_license:
      server: big-ip
      key: XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX
      username: "admin"
      password: "MyPassword123"
      license_options:
          email: 'joe.user@myplace.com'
          firstname: 'Joe'
          lastname: 'User'
          company: 'My Place'
          phone: '630-555-1212'
          jobtitle: 'Systems Administrator'
          address: '207 N Rodeo Dr'
          city: 'Beverly Hills'
          state: 'CA'
          postalcode: '90210'
          country: 'US'
  delegate_to: localhost
"""

import base64
import socket
import suds
import re

from xml.sax._exceptions import SAXParseException

try:
    import bigsuds
except ImportError:
    bigsuds_found = False
else:
    bigsuds_found = True

def is_production_key(key):
    m = re.search("\d", key[1:-1])
    if m:
        return False
    else:
        return True

def test_license_server(server, wsdl=None):
    if wsdl:
        url = 'file://%s' % wsdl
    else:
        url = 'https://%s/license/services/urn:com.f5.license.v5b.ActivationService?wsdl' % server

    try:
        # Specifying the location here is required because the URLs in the
        # WSDL for activate specify http but the URL we are querying for
        # here is https. Something is weird in suds and causes the following
        # to be returned
        #
        #     <h1>/license/services/urn:com.f5.license.v5b.ActivationService</h1>
        #     <p>Hi there, this is an AXIS service!</p>
        #     <i>Perhaps there will be a form for invoking the service here...</i>
        #
        client = suds.client.Client(url=url, location=url)

        result = client.service.ping()
        if result:
            return True
        else:
            return False
    except SAXParseException:
        return False


class BigIpLicenseCommon(object):
    def __init__(self, regkey, username, password, hostname):
        self.eula_file = 'LICENSE.F5'
        self.license = None
        self.dossier = None
        self.regkey = regkey
        self.username = username
        self.password = password
        self.hostname = hostname
        self.license_options = {
            'eula': '',
            'email': '',
            'firstname': '',
            'lastname': '',
            'company': '',
            'phone': '',
            'jobtitle': '',
            'address': '',
            'city': '',
            'state': '',
            'postalcode': '',
            'country': ''
        }
        self.license_server = None

        # Check if we can connect to the device
        sock = socket.create_connection((hostname,443), 60)
        sock.close()

        self.client = bigsuds.BIGIP(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            debug=True
        )

    def get_license(self, wsdl=None):
        if wsdl:
            url = 'file://%s' % wsdl
        else:
            url = 'https://%s/license/services/urn:com.f5.license.v5b.ActivationService?wsdl' % self.license_server

        client = suds.client.Client(url=url, location=url)
        resp = client.service.getLicense(
            self.dossier,
            self.license_options['eula'],
            self.license_options['email'],
            self.license_options['firstname'],
            self.license_options['lastname'],
            self.license_options['company'],
            self.license_options['phone'],
            self.license_options['jobtitle'],
            self.license_options['address'],
            self.license_options['city'],
            self.license_options['state'],
            self.license_options['postalcode'],
            self.license_options['country'],
        )

        return resp

    def get_license_activation_status(self):
        '''Returns the license status

        This method will return the license activation status of a BIG-IP. The
        following status may be returned from this method.

            STATE_DISABLED when it is not licensed
            STATE_ENABLED when it is licensed
        '''

        response = self.client.Management.LicenseAdministration.get_license_activation_status()
        return response


class BigIpLicenseIControl(BigIpLicenseCommon):
    def get_dossier(self, key):
        response = self.client.Management.LicenseAdministration.get_system_dossier(
            registration_keys=[key]
        )
        self.dossier = response
        return response

    def install_license(self, license):
        license = base64.b64encode(license)
        self.client.Management.LicenseAdministration.install_license(
            license_file_data=license
        )

        status = self.get_license_activation_status()
        if status == 'STATE_ENABLED':
            return True
        else:
            return False

    def upload_eula(self, eula):
        file_name = '/%s' % self.eula_file

        self.client.System.ConfigSync.upload_file(
            file_name = file_name,
            file_context = {
                'file_data': base64.b64encode(eula),
                'chain_type': 'FILE_FIRST_AND_LAST'
            }
        )


def main():
    changed = False

    module = AnsibleModule(
        argument_spec = dict(
            dossier_file=dict(),
            server=dict(required=True),
            key=dict(required=True),
            license_file=dict(),
            license_options=dict(type='dict'),
            password=dict(required=True),
            state=dict(default='present', choices=['present', 'latest']),
            user=dict(required=True, aliases=['username']),
            wsdl=dict(default=None)
        )
    )

    dossier_file = module.params.get('dossier_file')
    hostname = module.params.get('server')
    key = module.params.get('key')
    license_file = module.params.get('license_file')
    license_options = module.params.get('license_options')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')
    wsdl = module.params.get('wsdl')

    try:
        if not bigsuds_found:
            raise Exception("The python bigsuds module is required")

        obj = BigIpLicenseIControl(key, username, password, hostname)

        if license_options:
            tmp = dict(obj.license_options.items() + license_options.items())
            obj.license_options = tmp

        if is_production_key(key):
            license_server = 'activate.f5.com'
        else:
            license_server = 'authem.f5net.com'

        obj.license_server = license_server

        if license_file:
            fh = open(license_file)
            obj.license = fh.read()
            fh.close()

        if dossier_file:
            fh = open(dossier_file)
            obj.dossier = fh.read()
            fh.close()

        if state == "present":
            lic_status = obj.get_license_activation_status()

            if lic_status == 'STATE_ENABLED':
                module.exit_json(changed=False)

            lic_server = test_license_server(license_server, wsdl)
            if not lic_server and lic_status == 'STATE_DISABLED':
                module.fail_json(changed=False, msg="Could not reach the specified activation server to license BIG-IP")

            if not obj.dossier:
                obj.get_dossier(key)
                if not obj.dossier:
                    raise Exception('Dossier not generated')

            resp = obj.get_license(wsdl)

            if resp.state == "EULA_REQUIRED":
                # Extract the eula offered from first try
                eula_string = resp.eula
                obj.license_options['eula'] = eula_string
                resp = obj.get_license(wsdl)

            # Try again, this time with eula populated
            if resp.state == 'LICENSE_RETURNED':
                big_license = resp.license
                if big_license:
                    obj.upload_eula(resp.eula)
            else:
                module.fail_json(msg=resp.fault.faultText)

            if obj.install_license(big_license):
                changed = True
            else:
                module.fail_json(msg="License not installed")
    except bigsuds.ConnectionError, e:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except socket.timeout:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except Exception, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
