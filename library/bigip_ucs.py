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
module: bigip_ucs
short_description: Manage UCS files.
description:
   - Manage UCS files.
version_added: "2.0"
options:
  include_chassis_level_config:
    description:
      - During restore of the UCS file, include chassis level configuration
        that is shared among boot volume sets. For example, cluster default
        configuration.
    required: false
    default: false
    choices: ['yes', 'no']
  ucs:
    description:
      - The path to the UCS file to install. The parameter must be
        provided if the C(state) is either C(installed) or C(activated).
    required: false
  force:
    description:
      - If C(yes) will upload the file every time and replace the file on the
        device. If C(no), the file will only be uploaded if it does not already
        exist. Generally should be C(yes) only in cases where you have reason
        to believe that the image was corrupted during upload.
    required: false
    default: false
    choices: ['yes', 'no']
  no_license:
    description:
      - Performs a full restore of the UCS file and all the files it contains,
        with the exception of the license file. The option must be used to
        restore a UCS on RMA devices (Returned Materials Authorization).
    required: false
    default: false
    choices: ['yes', 'no']
  no_platform_check:
    description:
      - Bypasses the platform check and allows a UCS that was created using a
        different platform to be installed. By default (without this option),
        a UCS created from a different platform is not allowed to be installed.
    required: false
    default: false
    choices: ['yes', 'no']
  passphrase:
    description:
      - Specifies the passphrase that is necessary to load the specified UCS file
    required: false
    default: false
    choices: ['yes', 'no']
  reset_trust:
    description:
      - When specified, the device and trust domain certs and keys are not
        loaded from the UCS. Instead, a new set is regenerated.
    required: false
    default: false
    choices: ['yes', 'no']
  state:
    description:
      - When C(installed), ensures that the UCS is uploaded and installed,
        on the system. When C(present), ensures that the UCS is uploaded.
        When C(absent), the UCS will be removed from the system.
    required: false
    default: installed
    choices:
      - absent
      - installed
      - present
notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds
   - Requires the paramiko Python package on the host for UCS load commands
     that are not available through the REST or SOAP APIs
   - Only the most basic checks are performed by this module. Other checks and
     considerations need to be taken into account. See the following URL.
     https://support.f5.com/kb/en-us/solutions/public/11000/300/sol11318.html
   - This module requires SSH access to the remote BIG-IP and will use the
     C(user) and C(password) values specified by default. The web UI
     credentials typically differ from the SSH credentials so it is
     recommended that you use the bigip_user module to enable terminal access
     for the Web UI user
   - This module does not handle devices with the FIPS 140 HSM
   - This module does not handle BIG-IPs systems on the 6400, 6800, 8400, or
     8800 hardware platform.
   - This module does not verify that the new or replaced SSH keys from the
     UCS file are synchronized between the BIG-IP system and the SCCP
   - This module does not support the 'rma' option
   - This module does not support restoring a UCS archive on a BIG-IP 1500,
     3400, 4100, 6400, 6800, or 8400 hardware platform other than the system
     from which the backup was created
   - This module does not support restoring a UCS archive using the bigpipe
     utility
   - The UCS restore operation restores the full configuration only if the
     hostname of the target system matches the hostname on which the UCS
     archive was created. If the hostname does not match, only the shared
     configuration is restored. You can ensure hostnames match by using
     the bigip_hostname Ansible module in a task before using this module.
   - This module does not support re-licensing a BIG-IP restored from a UCS
   - This module does not support restoring encrypted archives on replacement
     RMA units.
   - This module will attempt to auto-recover a failed UCS load by using the
     iControl API to load the default backup UCS file (cs_backup.ucs)
extends_documentation_fragment: f5
requirements:
  - bigsuds
  - requests
  - paramiko
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Upload UCS
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      ucs: "/root/bigip.localhost.localdomain.ucs"
      state: "present"
  delegate_to: localhost

- name: Install (upload, install) UCS.
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      ucs: "/root/bigip.localhost.localdomain.ucs"
      state: "installed"
  delegate_to: localhost

- name: Install (upload, install) UCS without installing the license portion
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      ucs: "/root/bigip.localhost.localdomain.ucs"
      state: "installed"
      no_license: "yes"
  delegate_to: localhost

- name: Install (upload, install) UCS except the license, and bypassing the platform check
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      ucs: "/root/bigip.localhost.localdomain.ucs"
      state: "installed"
      no_license: "yes"
      no_platform_check: "yes"
  delegate_to: localhost

- name: Install (upload, install) UCS using a passphrase necessary to load the UCS
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      ucs: "/root/bigip.localhost.localdomain.ucs"
      state: "installed"
      passphrase: "MyPassphrase1234"
  delegate_to: localhost

- name: Remove uploaded UCS file
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      ucs: "/root/bigip.localhost.localdomain.ucs"
      state: "absent"
  delegate_to: localhost
'''

import base64
import os
import socket

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False


class BigIpCommon(object):
    def __init__(self, module):
        self.result = {}

        # Size of chunks of data to read and send via the iControl API
        self.chunk_size = 512 * 1024

        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._hostname = module.params.get('server')
        self._ucs = module.params.get('ucs')
        self._basename = os.path.basename(self._ucs)
        self._force = module.params.get('force')
        self._validate_certs = module.params.get('validate_certs')

        # Options available when loading a UCS
        self._include_clc = module.params.get('include_chassis_level_config')
        self._no_license = module.params.get('no_license')
        self._no_platform = module.params.get('no_platform_check')
        self._no_passphrase = module.params.get('no_passphrase')
        self._reset_trust = module.params.get('reset_trust')

        self.options = {
            'include-chassis-level-config': self._include_clc,
            'no-license': self._no_license,
            'no-platform-check': self._no_platform,
            'passphrase': self._no_passphrase,
            'reset-trust': self._reset_trust
        }
        self._command = "tmsh load sys ucs /var/local/ucs/%s" % (self._basename)
        self._command100x = "tmsh run bigpipe config install"
        self._backup = 'cs_backup.ucs'

    def appliance_mode(self):
        self._uri = 'https://%s/mgmt/tm/auth/user/%s' % (self._hostname, self._username)
        self._headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            raise Exception('Failed to query the REST API')
        else:
            result = resp.json()
            if 'shell' in result and result['shell'] == 'tmsh':
                return True
            else:
                return False


class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )

    def version(self):
        """Check the BIG-IP version

        Different versions of BIG-IP support different arguments to the load
        command. This method will return the version of the system for
        comparison.
        """
        version = self.api.System.SystemInfo.get_version()
        return version

    def read(self):
        result = []

        try:
            resp = self.api.System.ConfigSync.get_configuration_list()
            for ucs in resp:
                result.append(ucs['file_name'])
        except bigsuds.ServerError:
            pass

        return result

    def _upload(self, filename):
        fileobj = open(filename, 'rb')
        done = False
        first = True

        while not done:
            text = base64.b64encode(fileobj.read(self.chunk_size))

            if first:
                if len(text) < self.chunk_size:
                    chain_type = 'FILE_FIRST_AND_LAST'
                else:
                    chain_type = 'FILE_FIRST'
                first = False
            else:
                if len(text) < self.chunk_size:
                    chain_type = 'FILE_LAST'
                    done = True
                else:
                    chain_type = 'FILE_MIDDLE'

            self.api.System.ConfigSync.upload_configuration(
                config_name=self._basename,
                file_context=dict(
                    file_data=text,
                    chain_type=chain_type
                )
            )

    def _is_ucs_available(self):
        ucss = self.read()
        if self._basename in ucss:
            return True
        else:
            return False

    def _delete(self):
        self.api.System.ConfigSync.delete_configuration(self._basename)

    def _rollback_ucs(self):
        self.api.System.ConfigSync.install_configuration(self._backup)

    def _has_error(self, stdout, stderr):
        if stdout.channel.recv_exit_status() > 0 or stderr.channel.recv_exit_status() > 0:
            return True

        if 'UCS installation failed' in self.result['stdout']:
            return True

        if 'UCS installation failed' in self.result['stderr']:
            return True

        return False

    def _install_ucs(self):
        """Installs a UCS file

        This method will install a UCS file that is already present on the
        system. Note that I am specifically using an SSH connection here to
        load the UCS because neither the REST nor SOAP APIs expose the ability
        to send options to the load command.

        This method, since it runs the tmsh commands natively, allows for these
        options to be specified.

        Additionally, this method detects and corrects for Appliance Mode
        """
        api = paramiko.SSHClient()

        if not self._validate_certs:
            api.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        api.connect(self._hostname, username=self._username, password=self._password)

        # Appliance mode drops the user directly into tmsh, so any leading tmsh
        # syntax can be removed from the provided command
        if self.appliance_mode():
            if self._command[0:4] == 'tmsh':
                cmd = self._command[4:].strip()
            else:
                cmd = self._command
        else:
            # If the user has some BIG-IPs that are in Appliance Mode and some
            # that are not, then it may be necessary to add the non-app mode
            # syntax to the command before it is executed.
            if self._command[0:4] != 'tmsh':
                cmd = 'tmsh ' + self._command
            else:
                cmd = self._command

        # Append any options that might be specified
        for k, v in self.options.iteritems():
            if v is False or v is None:
                continue
            elif k == 'passphrase':
                cmd += ' %s %s' % (k, v)
            else:
                cmd += ' %s' % (k)

        stdin, stdout, stderr = api.exec_command(cmd)
        self.result['stdout'] = stdout.read()
        self.result['stderr'] = stderr.read()
        self.result['command'] = cmd

        if self._has_error(stdout, stderr):
            self._rollback_ucs()
            self.result['changed'] = False
            self.result['return'] = 1
            self.result['rollback'] = True
        else:
            self.result['changed'] = True
            self.result['return'] = 0
            self.result['rollback'] = False

        return True

    def installed(self):
        """Ensures a UCS file is installed

        """
        version = self.version()
        if '11.4.0' in version:
            # This version does not support this option
            del self.options['reset-trust']

        if self._force:
            self._delete()

        if not self._is_ucs_available():
            self._upload(self._ucs)

        self._install_ucs()

        return True

    def present(self):
        changed = False

        if self._force:
            self._delete()
            changed = True

        if not self._is_ucs_available():
            self._upload(self._ucs)
            changed = True

        self.result['changed'] = changed

    def absent(self):
        """Ensures UCS files are deleted from the system

        """
        changed = False
        ucss = self.read()

        if self._basename in ucss:
            changed = True

        if changed:
            self._delete()

        self.result['changed'] = changed


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        force=dict(required=False, type='bool', default='no'),
        include_chassis_level_config=dict(required=False, type='bool', default=False),
        no_license=dict(required=False, type='bool', default=False),
        no_platform_check=dict(required=False, type='bool', default=False),
        passphrase=dict(required=False, default=False),
        reset_trust=dict(required=False, type='bool', default=False),
        server=dict(required=True),
        state=dict(default='installed', choices=['absent', 'installed', 'present']),
        ucs=dict(required=True)
    )

    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    connection = module.params.get('connection')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')

    try:
        if connection == 'icontrol':
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            icontrol = test_icontrol(username, password, hostname)
            if icontrol:
                obj = BigIpIControl(module)
        elif connection == 'rest':
            module.fail_json(msg='The REST connection is currently not supported')

        if state == "installed":
            if not paramiko_found:
                raise Exception("The python paramiko module is required")

            obj.installed()
        elif state == "present":
            obj.present()
        elif state == "absent":
            obj.absent()
    except (bigsuds.ConnectionError, bigsuds.ParseError) as e:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except paramiko.ssh_exception.SSHException as e:
        if 'No existing session' in str(e):
            module.fail_json(msg='Could not log in with provided credentials')
        else:
            module.fail_json(msg=str(e))
    except socket.timeout as e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(**obj.result)

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
