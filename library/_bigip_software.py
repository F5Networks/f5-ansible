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
module: bigip_software
short_description: Manage BIG-IP software versions and hotfixes
description:
   - Manage BIG-IP software versions and hotfixes
version_added: "2.4"
options:
  force:
    description:
      - If C(yes) will upload the file every time and replace the file on the
        device. If C(no), the file will only be uploaded if it does not already
        exist. Generally should be C(yes) only in cases where you have reason
        to believe that the image was corrupted during upload.
      - If C(yes) with C(reuse_inactive_volume) is specified and C(volume) is
        not specified, Software will be installed / activated regardless of
        current running version to a new or an existing volume.
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
  reuse_inactive_volume:
    description:
      - Automatically chooses the first inactive volume in alphanumeric order. If there
        is no inactive volume, new volume with incremented volume name will be created.
        For example, if HD1.1 is currently active and no other volume exists, then the
        module will create HD1.2 and install the software. If volume name does not end with
        numeric character, then add .1 to the current active volume name. When C(volume)
        is specified, this option will be ignored.
    required: false
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
  volume:
    description:
      - The volume to install the software and, optionally, the hotfix to. This
        parameter is only required when the C(state) is either C(activated) or
        C(installed).
    required: false
notes:
  - Requires the bigsuds Python package on the host if using the iControl
    interface. This is as easy as pip install bigsuds
  - Requires the isoparser Python package on the host. This can be installed
    with pip install isoparser
  - Requires the lxml Python package on the host. This can be installed
    with pip install lxml
extends_documentation_fragment: f5
requirements:
  - bigsuds
  - isoparser
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
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

- name: Activate (upload, install, reboot) base image and hotfix. Reuse inactive volume in volumes with prefix.
  bigip_software:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      software: "/root/BIGIP-11.6.0.0.0.401.iso"
      hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
      reuse_inactive_volume: yes
      state: "activated"
'''

import base64
import os
import time
import io
from lxml import etree

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import bigsuds
except ImportError:
    BIGSUDS_AVAILABLE = False
else:
    BIGSUDS_AVAILABLE = True

try:
    import isoparser
except ImportError:
    ISOPARSER_AVAILABLE = False
else:
    ISOPARSER_AVAILABLE = True

SECTOR_SIZE = 2048
TRANSPORTS = ['rest', 'soap']
STATES = ['absent', 'activated', 'installed', 'present']

# Size of chunks of data to read and send via the iControl API
CHUNK_SIZE = 512 * 1024


class BigIpApiFactory(object):
    def factory(module):
        type = module.params.get('connection')

        if type == "rest":
            module.fail_json(msg='The REST connection is currently not supported')
        elif type == "soap":
            if not BIGSUDS_AVAILABLE:
                raise Exception("The python bigsuds module is required")
            return BigIpSoapApi(check_mode=module.check_mode, **module.params)

    factory = staticmethod(factory)


class BigIpCommon(object):
    def __init__(self, *args, **kwargs):
        self.result = dict(changed=False, changes=dict())

        self.current = dict()

        if kwargs['hotfix']:
            kwargs['photfix'] = self.iso_info(kwargs['hotfix'])

        if kwargs['software']:
            kwargs['psoftware'] = self.iso_info(kwargs['software'])

        self.params = kwargs

    def _find_iso_content(self, iso):
        paths = ['/METADATA.XML', 'metadata.xml']

        for path in paths:
            try:
                content = iso.record(path).content
                return content
            except KeyError:
                pass
        raise Exception(
            "Unable to find metadata file in ISO. Please file a bug"
        )

    def iso_info(self, iso):
        result = dict(
            product=None,
            version=None,
            build=None
        )

        iso = isoparser.parse(iso)
        content = self._find_iso_content(iso)
        content = io.BytesIO(content)

        context = etree.iterparse(content)
        for action, elem in context:
            if elem.text:
                text = elem.text

            if elem.tag == 'productName':
                result['product'] = text
            elif elem.tag == 'version':
                result['version'] = text
            elif elem.tag == 'buildNumber':
                result['build'] = text

        return result

    def flush(self):
        result = dict()
        state = self.params['state']
        volume = self.params['volume']
        software = self.params['software']
        reuse_inactive_volume = self.params['reuse_inactive_volume']

        if state == 'activated' or state == 'installed':
            if not volume:
                if not reuse_inactive_volume:
                    raise F5ModuleError("You must specify a volume")
            elif not software:
                raise F5ModuleError("You must specify a base image")

        if state == "activated":
            changed = self.activated()
        elif state == "installed":
            changed = self.installed()
        elif state == "present":
            changed = self.present()
        elif state == "absent":
            changed = self.absent()

        if state in ['activated', 'installed', 'present']:
            if not self.params['check_mode']:
                current = self.read()
                result.update(current)

        changed = True
        result.update(dict(changed=changed))
        return result


class BigIpSoapApi(BigIpCommon):
    def __init__(self, *args, **kwargs):
        super(BigIpSoapApi, self).__init__(*args, **kwargs)

        self.api = bigip_api(kwargs['server'],
                             kwargs['user'],
                             kwargs['password'],
                             kwargs['validate_certs'])

    def read(self):
        result = dict(
            software=[],
            hotfix=[]
        )

        try:
            images = self.api.System.SoftwareManagement.get_software_image_list()
            for image in images:
                info = self.api.System.SoftwareManagement.get_software_image(
                    imageIDs=[image]
                )
                result['software'].append(info[0])

            hotfixes = self.api.System.SoftwareManagement.get_software_hotfix_list()
            for hotfix in hotfixes:
                info = self.api.System.SoftwareManagement.get_software_hotfix(
                    imageIDs=[hotfix]
                )
                result['hotfix'].append(info[0])
        except bigsuds.ServerError:
            pass

        return result

    def get_active_volume(self):
        softwares = self.api.System.SoftwareManagement.get_all_software_status()
        for software in softwares:
            if software['active']:
                return software['installation_id']['install_volume']
        return None

    def get_inactive_volumes(self):
        status = self.api.System.SoftwareManagement.get_all_software_status()
        volumes = [x['installation_id']['install_volume'] for x in status if not x['active']]
        volumes.sort()
        return volumes

    def get_next_available_volume(self, delete_target=False):
        target_volume = None
        active_volume = self.get_active_volume()

        for volume in self.get_inactive_volumes():
            if volume == active_volume:
                continue
            else:
                target_volume = volume
                break

        if target_volume is None:
            try:
                _active_volume = active_volume.split('.')
                _active_volume[-1] = str(int(_active_volume[-1]) + 1)
                target_volume = '.'.join(_active_volume)
            except Exception:
                target_volume = active_volume + '.1'

        if delete_target:
            self.delete_volume(target_volume)

        return target_volume

    def delete_volume(self, volume):
        sleep_interval = 0.25

        # Check the target volume exists and inactive
        if volume not in self.get_inactive_volumes():
            return False

        self.api.System.SoftwareManagement.delete_volume(volume)

        while True:
            time.sleep(sleep_interval)
            if volume not in self.get_inactive_volumes():
                break

        return True

    def upload(self, filename):
        done = False
        first = True

        with open(filename, 'rb') as fh:
            remote_path = "/shared/images/%s" % os.path.basename(filename)

            while not done:
                text = base64.b64encode(fh.read(CHUNK_SIZE))

                if first:
                    if len(text) < CHUNK_SIZE:
                        chain_type = 'FILE_FIRST_AND_LAST'
                    else:
                        chain_type = 'FILE_FIRST'
                    first = False
                else:
                    if len(text) < CHUNK_SIZE:
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

    def is_hotfix_available(self, hotfix):
        hotfix = os.path.basename(hotfix)
        images = self.api.System.SoftwareManagement.get_software_hotfix_list()
        for image in images:
            if image['filename'] == hotfix:
                return True
        return False

    def is_software_available(self, software):
        software = os.path.basename(software)
        images = self.api.System.SoftwareManagement.get_software_image_list()
        for image in images:
            if image['filename'] == software:
                return True
        return False

    def delete(self, software):
        software = os.path.basename(software)
        self.api.System.SoftwareManagement.delete_software_image(
            image_filenames=[software]
        )

    def is_activated(self):
        return self.software_active(True)

    def is_installed(self):
        volume = self.params['volume']
        result = self.software_active(False)
        if result:
            softwares = self.api.System.SoftwareManagement.get_all_software_status()
            for software in softwares:
                if software['installation_id']['install_volume'] == volume:
                    return True
        return False

    def software_active(self, activity):
        result = False
        images = self.api.System.SoftwareManagement.get_all_software_status()

        hotfix = self.params['hotfix']
        software = self.params['software']

        if hotfix:
            photfix = self.params['photfix']

        if software:
            psoftware = self.params['psoftware']

        for image in images:
            ibuild = image['base_build']
            iver = image['version']
            iprod = image['product']

            if image['active'] == activity:
                if hotfix:
                    pbuild = photfix['build']
                    pver = photfix['version']
                    pprod = photfix['product']

                    if pbuild == ibuild and pver == iver and pprod == iprod:
                        result = True

                if software:
                    pbuild = psoftware['build']
                    pver = psoftware['version']
                    pprod = psoftware['product']

                    if pbuild == ibuild and pver == iver and pprod == iprod:
                        result = True

        return result

    def wait_for_software_install(self):
        while True:
            time.sleep(5)
            status = self.api.System.SoftwareManagement.get_all_software_status()
            progress = [x['status'] for x in status if not x['active']]
            if 'complete' in progress:
                break
            elif 'failed' in progress:
                raise F5ModuleError(progress)

    def wait_for_reboot(self):
        volume = self.params['volume']

        while True:
            time.sleep(5)

            try:
                status = self.api.System.SoftwareManagement.get_all_software_status()
                volumes = [x['installation_id']['install_volume'] for x in status if x['active']]
                if volume in volumes:
                    break
            except Exception:
                # Handle all exceptions because if the system is offline (for a
                # reboot) the SOAP client will raise exceptions about connections
                pass

    def wait_for_images(self, count):
        while True:
            # Waits for the system to settle
            images = self.read()
            ntotal = sum(len(v) for v in images.itervalues())
            if ntotal == count:
                break
            time.sleep(1)

    def install_software(self, pvb, reboot=False, create=False):
        volume = self.params['volume']

        self.api.System.SoftwareManagement.install_software_image_v2(
            volume=volume,
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

        changed = False
        force = self.params['force']
        software = self.params['software']
        hotfix = self.params['hotfix']
        psoftware = self.params['psoftware']
        volume = self.params['volume']
        reuse_inactive_volume = self.params['reuse_inactive_volume']

        if reuse_inactive_volume:
            if volume is None:
                self.params['volume'] = self.get_next_available_volume(True)

            if self.is_activated() and not force:
                volume = self.get_active_volume()

        if self.is_activated() and volume == self.get_active_volume():
            return False
        elif self.is_installed() and volume != self.get_active_volume():
            self.api.System.SoftwareManagement.set_cluster_boot_location(volume)
            self.api.System.Services.reboot_system(seconds_to_reboot=1)
            self.wait_for_reboot()
            return True
        elif volume == self.get_active_volume():
            raise F5ModuleError(
                "Cannot install software or hotfixes to active volumes"
            )

        images = self.read()
        total = sum(len(v) for v in images.itervalues())

        if force:
            if hotfix:
                self.delete(hotfix)
                total -= 1
                changed = True

            if software:
                self.delete(software)
                total -= 1
                changed = True

        if changed:
            self.wait_for_images(total)
            changed = False

        if hotfix:
            if not self.is_hotfix_available(hotfix):
                self.upload(hotfix)
                total += 1
                changed = True

        if not self.is_software_available(software):
            self.upload(software)
            total += 1
            changed = True

        if changed:
            self.wait_for_images(total)

        status = self.api.System.SoftwareManagement.get_all_software_status()
        volumes = [x['installation_id']['install_volume'] for x in status if x['active']]

        if volume in volumes:
            create_volume = False
        else:
            create_volume = True

        if hotfix:
            photfix = self.params['photfix']
            # We do not want to reboot after installation of the base image
            # because we can install the hotfix image right away and reboot
            # the system after that happens instead
            self.install_software(psoftware, reboot=False, create=create_volume)
            self.wait_for_software_install()
            self.install_software(photfix, reboot=True, create=False)
        else:
            self.install_software(psoftware, reboot=True, create=create_volume)

        self.wait_for_software_install()

        # We need to wait for the system to reboot so that we can check the
        # active volume to ensure it is the volume that was specified to the
        # module
        self.wait_for_reboot()
        return True

    def installed(self):
        """Ensures a base image and optionally a hotfix are installed

        """

        changed = False
        force = self.params['force']
        hotfix = self.params['hotfix']
        psoftware = self.params['psoftware']
        software = self.params['software']
        volume = self.params['volume']
        reuse_inactive_volume = self.params['reuse_inactive_volume']

        if volume is None and reuse_inactive_volume:
            self.params['volume'] = self.get_next_available_volume(True)

        if self.is_installed():
            return False
        elif volume == self.get_active_volume():
            raise F5ModuleError(
                "Cannot install software or hotfixes to active volumes"
            )

        images = self.read()
        total = sum(len(v) for v in images.itervalues())

        if force:
            if hotfix:
                self.delete(hotfix)
                total -= 1
                changed = True

            if software:
                self.delete(software)
                total -= 1
                changed = True

            if changed:
                self.wait_for_images(total)
                changed = False

        images = self.read()
        total = sum(len(v) for v in images.itervalues())

        if hotfix:
            if not self.is_hotfix_available(hotfix):
                self.upload(hotfix)
                total += 1
                changed = True

        if not self.is_software_available(software):
            self.upload(software)
            total += 1
            changed = True

        if changed:
            self.wait_for_images(total)

        status = self.api.System.SoftwareManagement.get_all_software_status()
        volumes = [x['installation_id']['install_volume'] for x in status]

        if volume in volumes:
            self.install_software(psoftware, reboot=False, create=False)
            self.wait_for_software_install()
        else:
            self.install_software(psoftware, reboot=False, create=True)
            self.wait_for_software_install()

        if hotfix:
            photfix = self.params['photfix']
            self.install_software(photfix, reboot=False, create=False)

        self.wait_for_software_install()

        return True

    def present(self):
        changed = False

        force = self.params['force']
        hotfix = self.params['hotfix']
        software = self.params['software']

        images = self.read()
        total = sum(len(v) for v in images.itervalues())

        if force:
            if hotfix:
                self.delete(hotfix)
                total -= 1
                changed = True

            if software:
                self.delete(software)
                total -= 1
                changed = True

            if changed:
                self.wait_for_images(total)

        # I check for existence after the 'force' check because an image can
        # be incompletely uploaded and broken, but would be listed as "present"
        # so forcing the deletion beforehand allows you to handle those cases.
        #
        # Note though that in the forced re-upload, the uploading could again
        # fail (for some reason) and this module would still report success if
        # it found the "broken" image.
        #
        # A better approach would be to compare checksums, however the checksum
        # stored by the BIG-IP is not the actual checksum of the ISO, but
        # instead is the checksum of the files _inside_ the ISO.
        if hotfix and software:
            if self.is_software_available(software) and self.is_hotfix_available(hotfix):
                return False
        elif hotfix:
            if self.is_hotfix_available(hotfix):
                return False
        elif software:
            if self.is_software_available(software):
                return False

        if hotfix:
            self.upload(hotfix)
            total += 1

        if software:
            self.upload(software)
            total += 1

        self.wait_for_images(total)

        return True

    def absent(self):
        hotfix = self.params['hotfix']
        software = self.params['software']

        images = self.read()
        total = sum(len(v) for v in images.itervalues())

        if hotfix and software:
            if not self.is_software_available(software) and not self.is_hotfix_available(hotfix):
                return False
        elif hotfix:
            if not self.is_hotfix_available(hotfix):
                return False
        elif software:
            if not self.is_software_available(software):
                return False

        if hotfix:
            self.delete(hotfix)
            total -= 1

        if software:
            self.delete(software)
            total -= 1

        self.wait_for_images(total)

        return True


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        connection=dict(default='soap', choices=TRANSPORTS),
        state=dict(default='activated', choices=STATES),
        force=dict(required=False, type='bool', default='no'),
        hotfix=dict(required=False, aliases=['hotfix_image'], default=None),
        software=dict(required=False, aliases=['base_image']),
        volume=dict(required=False),
        reuse_inactive_volume=dict(reqiored=False, type='bool', default='no')
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
    except bigsuds.ConnectionError:
        module.fail_json(msg='Could not connect to BIG-IP host')

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
