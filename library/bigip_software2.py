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

import io
from ansible.module_utils.f5_utils import *
import isoparser
from lxml import etree

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class Parameters(AnsibleF5Parameters):
    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        if params:
            self.update(params=params)

    def update(self, params=None):
        if params:
            for k, v in iteritems(params):
                if self.api_map is not None and k in self.api_map:
                    map_key = self.api_map[k]
                else:
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have
                        # an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    updatables = [
        'software', 'volume', 'hotfix'
    ]

    returnables = [
        'force', 'hotfix', 'state',
        'software', 'volume', 'reuse_inactive_volume', 'remote_src'
    ]

    api_attributes = [
        'volume', 'options'
    ]

    api_map = {}

    @property
    def software(self):
        link = self._values['software']
        remote = self._values['remote_src']

        if link is None:
            return None

        if remote:
            software = self.handle_remote_source(link)
            self._values['software_name'] = software
        else:
            software = os.path.split(link)[1]
            self._values['software_name'] = software

        return self._values['software']

    @property
    def hotfix(self):
        link = self._values['hotfix']
        remote = self._values['remote_src']

        if link is None:
            return None

        if remote:
            hotfix = self.handle_remote_source(link)
            self._values['hotfix_name'] = hotfix
        else:
            hotfix = os.path.split(link)[1]
            self._values['hotfix_name'] = hotfix

        return self._values['hotfix']

    @property
    def options(self):
        state = self._values['state']
        create = self._values['create_volume']
        opt = list()

        if state == 'activated' or state == 'installed':
            if create:
                opt.append({'create-volume': True})

        if state == 'activated':
            opt.append({'reboot': True})
        return opt

    @property
    def volume(self):
        state = self._values['state']
        volume = self._values['volume']
        reuse = self._values['reuse_inactive_volume']

        if state == 'activated' or state == 'installed':
            if volume is None:
                if reuse:
                    volume = self._get_next_available_volume(True)
                else:
                    err = "You must specify a volume."
                    raise F5ModuleError(err)

            if self._is_volume_active(volume):
                err = "Cannot install software or " \
                      "hotfixes to active volumes."
                raise F5ModuleError(err)

            self._values['create_volume'] = True

        return volume

    @property
    def version(self):
        psoftware = self.software
        photfix = self.hotfix
        software = self.software_name
        hotfix = self.hotfix_name
        remote = self._values['remote_src']

        if remote:
            if hotfix:
                self.set_info(hotfix, hotfix=True)
            else:
                self.set_info(software)
        else:
            if hotfix:
                self.use_iso(photfix)
            else:
                self.use_iso(psoftware)

        return self._values['version']

    @property
    def build(self):
        psoftware = self.software
        photfix = self.hotfix
        software = self.software_name
        hotfix = self.hotfix_name
        remote = self._values['remote_src']

        if remote:
            if hotfix:
                self.set_info(hotfix, hotfix=True)
            else:
                self.set_info(software)
        else:
            if hotfix:
                self.use_iso(photfix)
            else:
                self.use_iso(psoftware)

        return self._values['build']

    def handle_remote_source(self, link):
        source = urlparse.urlparse(link)
        name = source.path.split('/')[-1]
        if source.scheme:
            if source.scheme == 'http':
                return name
            elif source.scheme == 'https':
                self._values['secure'] = True
                return name
            else:
                err = 'Only remote HTTP sources are supported.'
                raise F5ModuleError(err)

    def set_info(self, name, hotfix=False):
        if hotfix:
            info = self._load_hotfix(name)
        else:
            info = self._load_image(name)

        self._values['version'] = info.version
        self._values['product'] = info.product
        self._values['build'] = info.build

    def use_iso(self, iso):
        iso = isoparser.parse(iso)
        content = self._find_iso_content(iso)
        content = io.BytesIO(content)
        context = etree.iterparse(content)

        for action, elem in context:
            if elem.text:
                text = elem.text
            if elem.tag == 'productName':
                self._values['product'] = text
            elif elem.tag == 'version':
                self._values['version'] = text
            elif elem.tag == 'buildNumber':
                self._values['build'] = text

    def _find_iso_content(self, iso):
        paths = ['/METADATA.XML', 'metadata.xml']

        for path in paths:
            try:
                content = iso.record(path).content
                return content
            except KeyError:
                pass
        raise Exception(
            "Unable to find metadata file in ISO. Please file a bug."
        )

    def _list_volumes(self):
        volumes = self.client.api.tm.sys.software.volumes.get_collection()
        return volumes

    def _load_volume(self, volume):
        vol = self.client.api.tm.sys.software.volumes.volume.load(
            name=volume)
        return vol

    def _volume_exists(self, volume):
        return self.self.client.api.tm.sys.software.volumes.volume.exists(
            name=volume)

    def _load_hotfix(self, hotfix_name):
        info = self.client.api.tm.sys.software.hotfix_s.hotfix.load(
            name=hotfix_name)
        return info

    def _load_image(self, software_name):
        info = self.client.api.tm.sys.software.images.image.load(
            name=software_name)
        return info

    def _is_volume_active(self, volume):
        if self._volume_exists(volume):
            vol = self._load_volume(volume)
            if hasattr(vol, 'active') and vol.active is True:
                return True
        else:
            return False

    def _get_next_available_volume(self, delete_target=False):
        target_volume = None
        active_volume = None
        volumes = self._list_volumes()

        for vol in volumes:
            if hasattr(vol, 'active') and vol.active is True:
                active_volume = vol
            else:
                target_volume = vol
                break

        if target_volume is None:
            try:
                _active_volume = str(active_volume.name).split('.')
                _active_volume[-1] = str(int(_active_volume[-1]) + 1)
                target_volume_name = '.'.join(_active_volume)
            except Exception:
                target_volume_name = str(active_volume.name) + '.1'
        else:
            target_volume_name = str(target_volume.name)

        if delete_target:
            self._delete_volume_on_device(target_volume)

        return target_volume_name

    def _delete_volume_on_device(self, volume):
        sleep_interval = 0.25
        volume_name = volume.name

        if self._is_volume_active(volume.name):
            return False

        volume.delete()

        while True:
            time.sleep(sleep_interval)
            for v in self._list_volumes():
                if v.name == volume_name:
                    break
            break
        return True

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self,
                                                self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)
        self.changes = Parameters()

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "activated":
                changed = self.activated()
            elif state == "installed":
                changed = self.installed()
            elif state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = attr1
        if changed:
            self.changes = Parameters(changed)
            return True
        return False

    def activated(self):
        if self.is_activated():
            return False
        elif self.is_installed():
            return self.activate()
        else:
            self.install_volume()
            self.wait_for_device_reboot()
            return True

    def installed(self):
        if self.is_installed():
            return False
        else:
            self.install_volume()
            return True

    def present(self):
        if self.exists():
            return False
        else:
            self._set_changed_options()
            if self.client.check_mode:
                return True
            self.upload()
            return True

    def absent(self):
        if not self.exists():
            return False
        else:
            if self.client.check_mode:
                return True
            self.remove()
            return True

    def install_volume(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        if not self.exists():
            self.upload()
        if self.want.hotfix:
            version = self.want.version
            if self.base_image_exists():
                self.install_hotfix_on_device()
            else:
                err = 'Base image of version: {0} must exist to install ' \
                      'this hotfix.'.format(version)
                raise F5ModuleError(err)
        else:
            self.install_image_on_device()

        self.wait_for_software_install_on_device()

    def upload(self):
        software_path = self.want.software
        hotfix_path = self.want.hotfix
        image_list = self.list_images_on_device()
        hotfix_list = self.list_hotfixes_on_device()

        if self.want.forced:
            self.remove()

        if software_path:
            if self.want.remote_src:
                self.download_iso_on_device()
            else:
                self.upload_to_device(software_path)
            self.wait_for_images(image_list)

        if hotfix_path:
            if self.want.remote_src:
                self.download_iso_on_device(True)
            else:
                self.upload_to_device(hotfix_path)
            self.wait_for_images(hotfix_list, True)

    def remove(self):
        image_list = self.list_images_on_device()
        hotfix_list = self.list_hotfixes_on_device()

        if self.want.hotfix_name:
            self.delete_hotfix_on_device()
            self.wait_for_images(hotfix_list, True)

        if self.want.software_name:
            self.delete_image_on_device()
            self.wait_for_images(image_list)

    def exists(self):
        result = False
        forced = self.want.forced
        software_path = self.want.software
        hotfix_path = self.want.hotfix

        if software_path and hotfix_path:
            if self.image_exists_on_device() and \
             self.hotfix_exists_on_device():
                result = True
        if hotfix_path:
            if self.hotfix_exists_on_device():
                result = True
        if software_path:
            if self.image_exists_on_device():
                result = True
        if forced:
            result = False
        return result

    def activate(self):
        self._update_changed_options()
        if self.client.check_mode:
            return True
        self.reboot_volume_on_device()
        self.wait_for_device_reboot()
        return True

    def is_installed(self):
        result = self.software_on_volume()
        if result:
            self.have, volume = result
            if not hasattr(volume, 'active') or volume.active is not True:
                return True

    def is_activated(self):
        result = self.software_on_volume()
        if result:
            self.have, volume = result
            if hasattr(volume, 'active') and volume.active is True:
                return True

    def wait_for_images(self, list, hotfix=False):
        current = len(list)
        if hotfix:
            while True:
                if len(self.list_hotfixes_on_device()) != current:
                    break
            time.sleep(1)
        else:
            while True:
                if len(self.list_images_on_device()) != current:
                    break
            time.sleep(1)

    def prepare_command(self, url, name):
        # We will add file download resume, multiple file download,
        # ftp/ftps and authentication here in next iterations. We need to
        # test this simple solution first

        secure = self.want.secure
        if secure:
            cmd = '-c curl {0} -k -o /shared/images/{1}'.format(url, name)
        else:
            cmd = '-c curl {0} -o /shared/images/{1}'.format(url, name)

        return cmd

    def base_image_exists(self):
        version = self.want.version
        images = self.list_images_on_device()
        for image in images:
            if image.version == version:
                return True
        else:
            return False

    def install_image_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.sys.software.images.exec_cmd(
            'install', name=self.want.software_name, **params
        )

    def install_hotfix_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.sys.software.hotfix_s.exec_cmd(
            'install', name=self.want.hotfix_name, **params
        )

    def upload_to_device(self, filepath):
        self.client.api.cm.autodeploy.software_image_uploads.upload_image(
            filepath
        )

    def download_iso_on_device(self, hotfix=False):
        # Might need to implement some delay here to avoid false positives
        # when checking for downloaded images
        if hotfix:
            url = self.want.hotfix
            name = self.want.hotfix_name
            cmd = self.prepare_command(url, name)
            self.run_command_on_device(cmd)
            if not self.hotfix_exists_on_device():
                err = 'ISO download failed from remote host.'
                raise F5ModuleError(err)
        else:
            url = self.want.software
            name = self.want.software_name
            cmd = self.prepare_command(url, name)
            self.run_command_on_device(cmd)
            if not self.image_exists_on_device():
                err = 'ISO download failed from remote host.'
                raise F5ModuleError(err)

    def list_images_on_device(self):
        images = self.client.api.tm.sys.software.images.get_collection()
        return images

    def list_hotfixes_on_device(self):
        hotfixes = self.client.api.tm.sys.software.hotfix_s.get_collection()
        return hotfixes

    def delete_image_on_device(self):
        img = self.client.api.tm.sys.software.images.image.load(
            name=self.want.software_name)
        img.delete()

    def delete_hotfix_on_device(self):
        hf = self.client.api.tm.sys.software.hotfix_s.hotfix.load(
            name=self.want.hotfix_name)
        hf.delete()

    def list_volumes_on_device(self):
        volumes = self.client.api.tm.sys.software.volumes.get_collection()
        return volumes

    def image_exists_on_device(self):
        result = self.client.api.tm.sys.software.images.image.exists(
            name=self.want.software_name
        )
        return result

    def hotfix_exists_on_device(self):
        result = self.client.api.tm.sys.software.hotfix_s.hotfix.exists(
            name=self.want.hotfix_name
        )
        return result

    def reboot_volume_on_device(self):
        cmd = [{'volume': self.want.volume}]
        self.client.api.tm.software.volumes.exec_cmd('reboot', options=cmd)

    def load_volume_on_device(self):
        volume = self.client.api.tm.sys.software.volumes.volume.load(
            name=self.want.volume)
        return volume

    def run_command_on_device(self, cmd):
        self.client.api.tm.util.bash.exec_cmd('run', utilCmdArgs=cmd)

    def software_on_volume(self):
        volumes = self.list_volumes_on_device()
        version = self.want.version
        build = self.want.build
        for volume in volumes:
            if volume.version == version and volume.build == build:
                tmp_res = volume.attrs
                return Parameters(tmp_res), volume

    def wait_for_device_reboot(self):
        volume = self.want.volume
        while True:
            time.sleep(5)
            try:
                status = self.list_volumes_on_device()
                volumes = [str(x.name) for x in status if x.active is True]
                if volume in volumes:
                    break
            except Exception:
                # Handle all exceptions because if the system is offline (for a
                # reboot) the REST client will raise exceptions about
                # connections
                pass

    def wait_for_software_install_on_device(self):
        while True:
            time.sleep(5)
            status = self.load_volume_on_device()
            progress = status.refresh()
            if 'complete' in progress.status:
                break
            elif 'failed' in progress.status:
                raise F5ModuleError(progress)


class ArgumentSpec(object):
    def __init__(self):
        self.states = ['absent', 'activated', 'installed', 'present']
        self.supports_check_mode = True
        self.argument_spec = dict(
            state=dict(
                default='activated',
                choices=self.states
            ),
            force=dict(
                required=False,
                type='bool',
                default='no'
            ),
            hotfix=dict(
                required=False,
                aliases=['hotfix_image'],
                default=None
            ),
            software=dict(
                required=False,
                aliases=['base_image']
            ),
            volume=dict(
                required=False
            ),
            reuse_inactive_volume=dict(
                required=False,
                type='bool',
                default='no'
            ),
            remote_src=dict(
                required=False,
                type='bool',
                default='no'
            )
        )
        self.f5_product_name = 'bigip'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
