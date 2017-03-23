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
module: bigip_license
short_description: Manage license installation and activation on BIG-IP devices
description:
  - Manage license installation and activation on BIG-IP devices
version_added: "2.2"
options:
  dossier_file:
    description:
      - Path to file containing kernel dossier for your system
    required: false
  key:
    description:
      - The registration key to use to license the BIG-IP. This is required
        if the C(state) is equal to C(present) or C(latest)
    required: false
  license_file:
    description:
      - Path to file containing the license to use
    required: false
  license_options:
    description:
      - Dictionary of options to use when creating the license
    required: false
  state:
    description:
      - The state of the license on the system. When C(present), only guarantees
        that a license is there. When C(latest) ensures that the license is always
        valid. When C(absent) removes the license on the system. C(latest) is
        most useful internally. When using C(absent), the account accessing the
        device must be configured to use the advanced shell instead of Appliance
        Mode.
    required: false
    default: present
    choices:
      - absent
      - latest
      - present
  wsdl:
    description:
      - WSDL file to use if you're receiving errors when downloading the WSDL
        file at run-time from the licensing servers
    required: false
    default: None
notes:
  - Requires the suds Python package on the host. This is as easy as
    pip install suds
  - Requires the bigsuds Python package on the host. This is as easy as
    pip install bigsuds
  - Requires the paramiko Python package on the host if using the C(state)
    C(absent). This is as easy as pip install paramiko
  - Requires the requests Python package on the host if using the C(state)
    C(absent). This is as easy as pip install paramiko
extends_documentation_fragment: f5
requirements:
  - bigsuds
  - requests
  - suds
  - paramiko
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: License BIG-IP using default license options
  bigip_license:
      server: "big-ip.domain.org"
      user: "admin"
      password: "MyPassword123"
      key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
  delegate_to: localhost

- name: License BIG-IP, specifying license options
  bigip_license:
      server: "big-ip.domain.org"
      key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
      user: "admin"
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

- name: Remove the license from the system
  bigip_license:
      server: "big-ip.domain.org"
      user: "admin"
      password: "MyPassword123"
      state: "absent"
  delegate_to: localhost

- name: Update the current license of the BIG-IP
  bigip_license:
      server: "big-ip.domain.org"
      user: "admin"
      password: "MyPassword123"
      key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
      state: "latest"
  delegate_to: localhost
'''

import base64
import re
import socket
import ssl
import suds
import time
import urllib2

from xml.sax._exceptions import SAXParseException
from suds.transport.https import HttpAuthenticated

try:
    import paramiko
except ImportError:
    paramiko_found = False
else:
    paramiko_found = True


LIC_EXTERNAL = 'activate.f5.com'
LIC_INTERNAL = 'authem.f5net.com'


class HTTPSHandlerNoVerify(urllib2.HTTPSHandler):
    def __init__(self, *args, **kwargs):
        try:
            kwargs['context'] = ssl._create_unverified_context()
        except AttributeError:
            # Python prior to 2.7.9 doesn't have default-enabled certificate
            # verification
            pass

        urllib2.HTTPSHandler.__init__(self, *args, **kwargs)


class HTTPSTransportNoVerify(HttpAuthenticated):
    def u2handlers(self):
        handlers = HttpAuthenticated.u2handlers(self)
        handlers.append(HTTPSHandlerNoVerify())
        return handlers


def is_production_key(key):
    m = re.search("\d", key[1:-1])
    if m:
        return False
    else:
        return True


class BigIpLicenseCommon(object):
    def __init__(self, module):
        self.password = module.params.get('password')
        self.username = module.params.get('user')
        self.hostname = module.params.get('server')

        # Holds the SSH connection for paramiko if ensurign the license is absent
        self.cli = None

        self._validate_certs = module.params.get('validate_certs')

        self.client = bigsuds.BIGIP(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            debug=True
        )

    def get_license_activation_status(self):
        """Returns the license status

        This method will return the license activation status of a BIG-IP. The
        following status may be returned from this method.

            STATE_DISABLED when it is not licensed
            STATE_ENABLED when it is licensed
        """
        return self.client.Management.LicenseAdministration.get_license_activation_status()

    def read_account(self):
        self._uri = 'https://%s/mgmt/tm/auth/user/%s' % (self.hostname, self.username)
        self._headers = {
            'Content-Type': 'application/json'
        }

        try:
            resp = requests.get(self._uri,
                                auth=(self.username, self.password),
                                verify=self._validate_certs)
        except requests.exceptions.SSLError:
            raise F5ModuleError(
                "SSL certificate verification failed. Use "
                "validate_certs=no to bypass this"
            )

        if resp.status_code != 200:
            raise Exception('Failed to query the REST API')
        else:
            return resp.json()

    def appliance_mode(self):
        """Checks for appliance mode

        Appliance mode is simply having your shell set to "tmsh". This mode
        prevents you from running arbitrary system commands. For this module,
        however, we need to ensure that Appliance Mode is not enabled for
        the account used to connect to the BIG-IP device.

        If it is, we will not be able to reload the license correctly and the
        APIs will continue to report the previous status of the license even
        after we have removed it from disk
        """
        result = self.read_account()

        if 'shell' in result and result['shell'] == 'tmsh':
            return True
        else:
            return False

    def can_have_advanced_shell(self):
        """Ensure account can use an advanced shell

        Only a few types of roles are allowed to use the advanced shell.
        Since we need to use this shell when making a license 'absent'
        on the system, we need to check to see if the user is assigned a
        role that is allowed to have an advanced shell
        """
        roles = []
        can_have_advanced = ['resource-admin', 'admin']

        user_data = self.read_account()
        pa = user_data['partitionAccess']
        roles = set([p['role'] for p in pa])

        found = [x for x in roles if x in can_have_advanced]
        if len(found) > 0:
            return True
        else:
            return False

    def set_shell(self, shell):
        payload = {}
        shell = str(shell)

        if shell == '/bin/bash':
            shell = 'bash'
        elif shell == '/sbin/nologin':
            shell = 'none'
        elif shell == '/usr/bin/tmsh':
            shell = 'tmsh'

        payload['shell'] = shell

        uri = 'https://%s/mgmt/tm/auth/user/%s' % (self.hostname, self.username)
        self._headers = {
            'Content-Type': 'application/json',
            'Connection': 'close'
        }
        requests.put(uri,
                     auth=(self.username, self.password),
                     data=json.dumps(payload),
                     verify=self._validate_certs)

    def absent(self):
        """Removes a license from a device

        This method will remove a license completely from a system and reload
        the configuration so that it is reporting as removed in the APIs.

        Notes about this method:

        It detects admin-ness and changes the connecting account's shell
        temporarily.

        There is no API command that can be used to remove a license.
        Therefore, my workaround is to use the SOAP API to delete the file
        directly from the server.

        This works to remove the license, but the system will not be aware
        that the license has been removed. To make the system aware of this
        you need to run the 'reloadlic' command from the advanced shell as
        there is no way to run an equivalent command from any API.

        The advanced shell is only available to two roles.

        To negate the need to specify a special account to connect with
        in this module, we change the shell of the connecting user to be
        the advanced shell. Afterwards we set the shell back to what it
        was before we changed it.

        There is a small risk that during the time that the shell is exposed
        that someone could connect to the system and have interactive access
        to the device. Since this module is one that should be used fairly
        infrequently in practice, I think the risk to the owner of the device
        during this brief period of time is minimal.

        This behavior is only needed for the 'absent' state and in future
        versions of our products this process may be unnecessary due to
        enhancements in the APIs that correctly reload the license status
        if it changes through the API
        """
        licenses = [
            '/config/bigip.license',
            '/config/bigiq.license'
        ]

        # Because this account may need to adjust your shell to run the
        # 'reloadlic' command, you must be running this module with an
        # account that has the privileges necessary to have an advanced
        # shell.
        #
        # Usually this is the 'admin' account. If you do not have the
        # required role though, we need to stop further work
        if not self.can_have_advanced_shell():
            raise F5ModuleError(
                "You account does not have permission to reload the license."
            )

        # Start by reading in the current shell.
        #
        # This is being done so that if we need to set the shell to the
        # advanced shell, we will know what shell to set the account back
        # to after we are done.
        user_data = self.read_account()

        # There is the possibility that there will be no shell specified
        # in the account details. The REST API does not list a shell if
        # the console has been deactivated for the account
        if 'shell' in user_data:
            if user_data['shell'] != 'bash':
                self.set_shell('bash')
        else:
            self.set_shell('bash')

        self.cli = paramiko.SSHClient()

        if not self._validate_certs:
            self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.cli.connect(self.hostname, username=self.username, password=self.password)

        # I am deleting all of the BIG-IP and BIG-IQ licenses so that this
        # module can be used by both devices
        for license in licenses:
            # If the file does not exist, the SOAP client will raise an
            # exception. Handle it and move on
            try:
                self.client.System.ConfigSync.delete_file(license)
            except bigsuds.ServerError:
                pass

        # The reloadlic command is used to refresh the state that is
        # reported by the APIs. If this is not done, then the existing
        # state reported does not changed from STATE_ENABLED
        cmd = "/usr/bin/reloadlic"

        stdin, stdout, stderr = self.cli.exec_command(cmd)
        self.cli.close()

        # reloadlic doesn't actually return anything, and it also doesn't
        # correctly report back its status upon failure (for example by
        # exiting with return codes greater than zero
        #
        # So the only way to really know if the license was succesfully
        # deleted is to recheck the state of the license
        stop_time = time.time() + 60
        while True:
            status = self.get_license_activation_status()
            if status == 'STATE_DISABLED':
                break
            elif time.time() >= stop_time:
                # ensure we do not run forever
                break
            time.sleep(1)

        if 'shell' in user_data:
            shell = user_data['shell']
            if shell == 'bash':
                shell = '/bin/bash'
            elif shell == 'none':
                shell = '/sbin/nologin'
            elif shell == 'tmsh':
                shell = '/usr/bin/tmsh'

            stop_time = time.time() + 60
            while True:
                self.set_shell(shell)
                time.sleep(5)
                resp = self.client.Management.UserManagement.get_login_shell([self.username])
                if resp[0] == shell:
                    break
                elif time.time() >= stop_time:
                    # ensure we do not run forever
                    break
                time.sleep(5)

        return True


class BigIpLicenseIControl(BigIpLicenseCommon):
    def __init__(self, module):
        super(BigIpLicenseIControl, self).__init__(module)

        self.eula_file = 'LICENSE.F5'
        self.license = None
        self.dossier = None
        self.license_file = module.params.get('license_file')
        self.dossier_file = module.params.get('dossier_file')
        self.regkey = module.params.get('key')
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
        self.wsdl = module.params.get('wsdl')

        license_options = module.params.get('license_options')
        if license_options:
            tmp = dict(self.license_options.items() + license_options.items())
            self.license_options = tmp

    def get_license(self):
        if self.wsdl:
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
            file_name=file_name,
            file_context=dict(
                file_data=base64.b64encode(eula),
                chain_type='FILE_FIRST_AND_LAST'
            )
        )

    def present(self):
        if is_production_key(self.regkey):
            license_server = LIC_EXTERNAL
        else:
            license_server = LIC_INTERNAL

        self.license_server = license_server

        if self.license_file:
            fh = open(license_file)
            self.license = fh.read()
            fh.close()

        if self.dossier_file:
            fh = open(dossier_file)
            self.dossier = fh.read()
            fh.close()

        if not self.dossier:
            self.get_dossier(self.regkey)
            if not self.dossier:
                raise F5ModuleError(
                    "Dossier not generated"
                )

        resp = self.get_license()
        if resp.state == "EULA_REQUIRED":
            # Extract the eula offered from first try
            eula_string = resp.eula
            self.license_options['eula'] = eula_string
            resp = self.get_license()

        # Try again, this time with eula populated
        if resp.state == 'LICENSE_RETURNED':
            big_license = resp.license
            if big_license:
                self.upload_eula(resp.eula)
        else:
            raise F5ModuleError(resp.fault.faultText)

        if self.install_license(big_license):
            return True
        else:
            return False


def main():
    changed = False

    argument_spec = f5_argument_spec()

    meta_args = dict(
        dossier_file=dict(no_log=True),
        key=dict(required=False, no_log=True),
        license_file=dict(no_log=True),
        license_options=dict(type='dict', no_log=True),
        state=dict(default='present', choices=['absent', 'present', 'latest']),
        wsdl=dict(default=None)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    state = module.params.get('state')

    try:
        common = BigIpLicenseCommon(module)
        lic_status = common.get_license_activation_status()

        if state == "present" and lic_status == 'STATE_ENABLED':
            module.exit_json(changed=False)

        if state == "absent" and lic_status == 'STATE_DISABLED':
            module.exit_json(changed=False)

        if state == "present" or state == "latest":
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            obj = BigIpLicenseIControl(module)

            if obj.present():
                changed = True
            else:
                module.fail_json(msg="License not installed")
        elif state == 'absent':
            if not paramiko_found:
                raise Exception("The python paramiko module is required")

            result = common.absent()
            if result:
                changed = True
            else:
                module.fail_json(msg="License not removed")

        module.exit_json(changed=changed)
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host")
    except socket.timeout:
        module.fail_json(msg="Timed out connecting to the BIG-IP")

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
