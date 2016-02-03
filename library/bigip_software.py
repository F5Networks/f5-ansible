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
module: bigip_software
short_description: Manage BIG-IP software versions and hotfixes
description:
   - Manage BIG-IP software versions and hotfixes
version_added: "2.0"
options:
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: icontrol
    choices: [ "rest", "icontrol" ]
  force:
    description:
      - If C(yes) will upload the file every time and replace the file on the
        device. If C(no), the file will only be uploaded if it does not already
        exist. Generally should be C(yes) only in cases where you have reason
        to believe that the image was corrupted during upload.
    required: false
    default: no
    choices:
      - yes
      - no
  hotfix:
    description:
      - The path to an optional Hotfix to install. This parameter requires that
        the C(software) parameter be specified.
    required: false
    default: None
    aliases:
      - hotfix_image
  password:
    description:
      - BIG-IP password
    required: true
  server:
    description:
      - BIG-IP host
    required: true
  state:
    description:
      - When C(installed), ensures that the software is uploaded and installed,
        on the system. The device is not, however, rebooted into the new software.
        When C(activated), ensures that the software is uploaded, installed, and
        the system is rebooted to the new software. When C(present), ensures
        that the software is uploaded. When C(absent), only the uploaded image
        will be removed from the system
    required: false
    default: activated
    choices:
      - absent
      - activated
      - installed
      - present
  software:
    description:
      - The path to the software (base image) to install. The parameter must be
        provided if the C(state) is either C(installed) or C(activated).
    required: false
    aliases:
      - base_image
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
  volume:
    description:
      - The volume to install the software and, optionally, the hotfix to. This
        parameter is only required when the C(state) is either C(activated) or
        C(installed).
    required: false

notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds
   - https://devcentral.f5.com/articles/icontrol-101-06-file-transfer-apis

requirements: [ "bigsuds", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
- name: Remove uploaded hotfix
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
      state: "absent"
  delegate_to: localhost

- name: Upload hotfix
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
      state: "present"
  delegate_to: localhost

- name: Remove uploaded base image
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      state: "absent"
  delegate_to: localhost

- name: Upload base image
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      state: "present"
  delegate_to: localhost

- name: Upload base image and hotfix
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
      state: "present"
  delegate_to: localhost

- name: Remove uploaded base image and hotfix
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
      state: "absent"
  delegate_to: localhost

- name: Install (upload, install) base image. Create volume if not exists
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      volume: "HD1.1"
      state: "installed"
  delegate_to: localhost

- name: Install (upload, install) base image and hotfix. Create volume if not exists
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
      volume: "HD1.1"
      state: "installed"

- name: Activate (upload, install, reboot) base image. Create volume if not exists
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      volume: "HD1.1"
      state: "activated"
  delegate_to: localhost

- name: Activate (upload, install, reboot) base image and hotfix. Create volume if not exists
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
      volume: "HD1.1"
      state: "activated"
"""

import base64
import socket
import os
import re
import time

try:
    import bigsuds
except ImportError:
    bigsuds_found = False
else:
    bigsuds_found = True


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
    def __init__(self, user, password, server, software=None, hotfix=None,
                 volume=None, force=False, validate_certs=True):

        # This regex supports filenames like the following
        #
        # - BIGIP-11.6.0.0.0.401.iso"
        # - Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
        # - BIGIP-tmos-core-tunnel-geneve-12.1.0.0.0.144.iso"
        #
        self._regex = '^(Hotfix-)?(?P<product>[^-]+).*-(?P<version>\d+\.\d+\.\d+)\.(?P<build>\d+\.\d+\.\d+).*'

        # Size of chunks of data to read and send via the iControl API
        self.chunk_size = 512 * 1024

        self._username = user
        self._password = password
        self._hostname = server
        self._software = software
        self._hotfix = hotfix
        self._volume = volume
        self._force = force
        self._validate_certs = validate_certs

        if self._hotfix:
            self._pvb_hotfix = self._parse_pvb(self._hotfix)
            self._basename_hotfix = os.path.basename(self._hotfix)

        if self._software:
            self._pvb_software = self._parse_pvb(self._software)
            self._basename_software = os.path.basename(self._software)


class BigIpIControl(BigIpCommon):
    def __init__(self, user, password, server, software=None, hotfix=None,
                 volume=None, force=False, validate_certs=True):

        super(BigIpIControl, self).__init__(user, password, server, software,
                                            hotfix, volume, force, validate_certs)

        self.api = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )

    def read(self):
        result = {
            'software': [],
            'hotfix': []
        }

        try:
            images = self.api.System.SoftwareManagement.get_software_image_list()
            for image in images:
                info = self.api.System.SoftwareManagement.get_software_image(imageIDs=[image])
                result['software'].append(info[0])

            hotfixes = self.api.System.SoftwareManagement.get_software_hotfix_list()
            for hf in hotfixes:
                info = self.api.System.SoftwareManagement.get_software_hotfix(imageIDs=[hf])
                result['hotfix'].append(info[0])
        except bigsuds.ServerError:
            pass

        return result

    def _parse_pvb(self, filename):
        """Parse the product, version and build from the filename

        Filenames should be the original name of the hotfix to best
        derive the product, version, and build values

        Example:

            software: "/root/BIGIP-11.6.0.0.0.401.iso"
            hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
        """

        if filename is None:
            return None

        filename = os.path.basename(filename)
        match = re.match(self._regex, filename)

        # The product in the filename is not necessarily what is stored in
        # the F5 products. So we have to map those here
        product = match.group('product')
        if product == 'BIGIP':
            product = 'BIG-IP'

        result = {
            'product': product,
            'version': match.group('version'),
            'build': match.group('build')
        }

        return result

    def _get_active_volume(self):
        softwares = self.api.System.SoftwareManagement.get_all_software_status()
        for software in softwares:
            if software['active']:
                return software['installation_id']['install_volume']
        return None

    def _upload(self, filename):
        fileobj = open(filename, 'rb')
        done = False
        first = True

        remote_path = "/shared/images/%s" % os.path.basename(filename)

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

            self.api.System.ConfigSync.upload_file(
                file_name=remote_path,
                file_context=dict(
                    file_data=text,
                    chain_type=chain_type
                )
            )

    def _is_hotfix_available(self):
        images = self.api.System.SoftwareManagement.get_software_hotfix_list()
        for image in images:
            if image['filename'] == self._basename_hotfix:
                return True
        return False

    def _is_software_available(self):
        images = self.api.System.SoftwareManagement.get_software_image_list()
        for image in images:
            if image['filename'] == self._basename_software:
                return True
        return False

    def _delete(self):
        filenames = []

        if self._software:
            filenames.append(self._basename_software)

        if self._hotfix:
            filenames.append(self._basename_hotfix)

        self.api.System.SoftwareManagement.delete_software_image(image_filenames=filenames)

    def _is_activated(self):
        return self._software_active(True)

    def _is_installed(self):
        result = self._software_active(False)
        if result:
            softwares = self.api.System.SoftwareManagement.get_all_software_status()
            for software in softwares:
                if software['installation_id']['install_volume'] == self._volume:
                    return True
        return False

    def _software_active(self, activity):
        result = False
        softwares = self.api.System.SoftwareManagement.get_all_software_status()

        for software in softwares:
            if software['active'] == activity:
                if self._hotfix:
                    pvb = self._pvb_hotfix
                    if pvb['build'] == software['build'] and \
                       pvb['version'] == software['version'] and \
                       pvb['product'] == software['product']:
                            result = True

                if self._software:
                    pvb = self._pvb_software
                    if pvb['build'] == software['base_build'] and \
                       pvb['version'] == software['version'] and \
                       pvb['product'] == software['product']:
                            result = True

        return result

    def _wait_for_software_install(self):
        while True:
            time.sleep(5)
            status = self.api.System.SoftwareManagement.get_all_software_status()
            progress = [x['status'] for x in status if not x['active']]
            if 'complete' in progress:
                break

    def _wait_for_system_reboot(self):
        while True:
            time.sleep(5)

            try:
                status = self.api.System.SoftwareManagement.get_all_software_status()
                volumes = [x['installation_id']['install_volume'] for x in status if x['active']]
                if self._volume in volumes:
                    break
            except:
                # Handle all exceptions because if the system is offline (for a
                # reboot) the SOAP client will raise exceptions about connections
                pass

    def _install_software(self, pvb, reboot=False, create=False):
        self.api.System.SoftwareManagement.install_software_image_v2(
            volume=self._volume,
            product=pvb['product'],
            version=pvb['version'],
            build=pvb['build'],
            create_volume=create,
            reboot=reboot,
            retry=False
        )

    def activated(self):
        """Ensures a base image and optionally a hotfix are activated

        Activated means that the current active boot location contains
        the base image + hotfix(optional).

        If the image is uploaded to the "Available Images" list but has not yet
        been made active, this method will activate it.

        If the image is not uploaded to the "Available Images" list, but is
        listed as activated, this method will return true

        If the image is not uploaded to the "Available Images" list, and is not
        in the active list, this method will upload the image and activate it.
        """
        if self._is_activated() and self._volume == self._get_active_volume():
            return False
        elif self._is_installed() and self._volume != self._get_active_volume():
            self.api.System.SoftwareManagement.set_cluster_boot_location(self._volume)
            self.api.System.Services.reboot_system(seconds_to_reboot=1)
            self._wait_for_system_reboot()
            return True
        elif self._volume == self._get_active_volume():
            raise Exception('Cannot install software or hotfixes to active volumes')

        if self._force:
            self._delete()

        if self._hotfix:
            if not self._is_hotfix_available():
                self._upload(self._hotfix)

        if not self._is_software_available():
            self._upload(self._software)

        status = self.api.System.SoftwareManagement.get_all_software_status()
        volumes = [x['installation_id']['install_volume'] for x in status]

        if self._volume in volumes:
            create_volume = False
        else:
            create_volume = True

        if self._hotfix:
            # We do not want to reboot after installation of the base image
            # because we can install the hotfix image right away and reboot
            # the system after that happens instead
            self._install_software(self._pvb_software, reboot=False, create=create_volume)
            self._wait_for_software_install()
            self._install_software(self._pvb_hotfix, reboot=True, create=False)
        else:
            self._install_software(self._pvb_software, reboot=True, create=create_volume)

        self._wait_for_software_install()

        # We need to wait for the system to reboot so that we can check the
        # active volume to ensure it is the volume that was specified to the
        # module
        self._wait_for_system_reboot()
        return True

    def installed(self):
        """Ensures a base image and optionally a hotfix are installed

        """
        if self._is_installed():
            return False
        elif self._volume == self._get_active_volume():
            raise Exception('Cannot install software or hotfixes to active volumes')

        if self._force:
            self._delete()

        if self._hotfix:
            if not self._is_hotfix_available():
                self._upload(self._hotfix)

        if not self._is_software_available():
            self._upload(self._software)

        status = self.api.System.SoftwareManagement.get_all_software_status()
        volumes = [x['installation_id']['install_volume'] for x in status]

        if self._volume in volumes:
            self._install_software(self._pvb_software, reboot=False, create=False)
            self._wait_for_software_install()
        else:
            self._install_software(self._pvb_software, reboot=False, create=True)
            self._wait_for_software_install()

        if self._hotfix:
            self._install_software(self._pvb_hotfix, reboot=False, create=False)

        self._wait_for_software_install()

        return True

    def present(self):
        changed = False

        if self._force:
            self._delete()
            changed = True

        if self._hotfix:
            if not self._is_hotfix_available():
                self._upload(self._hotfix)
                changed = True

        if self._software:
            if not self._is_software_available():
                self._upload(self._software)
                changed = True

        # Sleep a moment for the system to settle
        time.sleep(1)
        return changed

    def absent(self):
        """Ensures software images are deleted from the system

        """
        changed = False
        softwares = self.read()

        if self._hotfix:
            for software in softwares['hotfix']:
                if self._basename_hotfix == software['filename']:
                    changed = True

        if self._software:
            for software in softwares['software']:
                if self._basename_software == software['filename']:
                    changed = True

        if changed:
            self._delete()

        # Sleep a moment for the system to settle
        time.sleep(1)
        return changed


def main():
    changed = False
    icontrol = False

    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(default='icontrol', choices=['icontrol', 'rest']),
            force=dict(required=False, type='bool', default='no'),
            hotfix=dict(required=False, aliases=['hotfix_image'], default=None),
            password=dict(required=True),
            server=dict(required=True),
            software=dict(required=False, aliases=['base_image']),
            state=dict(default='activated', choices=['absent', 'activated', 'installed', 'present']),
            user=dict(required=True),
            validate_certs=dict(default='yes', type='bool'),
            volume=dict(required=False)
        )
    )

    connection = module.params.get('connection')
    force = module.params.get('force')
    hotfix = module.params.get('hotfix')
    password = module.params.get('password')
    server = module.params.get('server')
    software = module.params.get('software')
    state = module.params.get('state')
    user = module.params.get('user')
    validate_certs = module.params.get('validate_certs')
    volume = module.params.get('volume')

    try:
        if connection == 'icontrol':
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            icontrol = test_icontrol(user, password, server)
            if icontrol:
                obj = BigIpIControl(user, password, server, software, hotfix,
                                    volume, force, validate_certs)
        elif connection == 'rest':
            module.fail_json(msg='The REST connection is currently not supported')

        if state == 'activated' or state == 'installed':
            if not volume:
                module.fail_json(msg='You must specify a volume')
            elif not software:
                module.fail_json(msg='You must specify a base image')

        if state == "activated":
            if obj.activated():
                changed = True
        elif state == "installed":
            if obj.installed():
                changed = True
        elif state == "present":
            if obj.present():
                changed = True
        elif state == "absent":
            if obj.absent():
                changed = True
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % server)
    except socket.timeout:
        module.fail_json(msg="Timed out connecting to the BIG-IP")

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
