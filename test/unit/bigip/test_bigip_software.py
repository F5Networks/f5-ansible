#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.compat.tests.mock import DEFAULT
from ansible.compat.tests.mock import Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    F5ModuleError
)

from library.bigip_software import (
    Parameters,
    LocalManager,
    RemoteManager,
    ArgumentSpec
)

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}
iso_path = os.path.join(os.path.dirname(__file__), 'fixtures/extra_files')


def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


def cmd_side_effect_md5_ok(*args):
    soft = 'cat /shared/images/BIGIP'
    hf = 'cat /shared/images/Hotfix'
    md5_soft = 'cd /shared/images; md5sum -c /shared/images/BIGIP'
    md5_hf = 'cd /shared/images; md5sum -c /shared/images/Hotfix'
    curl = '-o /shared/images'
    if soft in args[0]:
        return BigIpObj(**load_fixture('cat_md5_software.json'))
    if hf in args[0]:
        return BigIpObj(**load_fixture('cat_md5_hotfix.json'))
    if md5_soft in args[0]:
        return BigIpObj(**load_fixture('md5_sum_ok_software.json'))
    if md5_hf in args[0]:
        return BigIpObj(**load_fixture('md5_sum_ok_hf.json'))
    if curl in args[0]:
        return True


def cmd_side_effect_md5_fail(*args):
    soft = 'cat /shared/images/BIGIP'
    hf = 'cat /shared/images/Hotfix'
    md5_soft = 'cd /shared/images; md5sum -c /shared/images/BIGIP'
    md5_hf = 'cd /shared/images; md5sum -c /shared/images/Hotfix'
    curl = '-o /shared/images'
    if soft in args[0]:
        return BigIpObj(**load_fixture('cat_md5_software.json'))
    if hf in args[0]:
        return BigIpObj(**load_fixture('cat_md5_hotfix.json'))
    if md5_soft in args[0]:
        return BigIpObj(**load_fixture('md5_sum_failed_software.json'))
    if md5_hf in args[0]:
        return BigIpObj(**load_fixture('md5_sum_failed_hf.json'))
    if curl in args[0]:
        return True


def cmd_side_effect_md5_fail_hotfix(*args):
    soft = 'cat /shared/images/BIGIP'
    hf = 'cat /shared/images/Hotfix'
    md5_soft = 'cd /shared/images; md5sum -c /shared/images/BIGIP'
    md5_hf = 'cd /shared/images; md5sum -c /shared/images/Hotfix'
    curl = '-o /shared/images'
    if soft in args[0]:
        return BigIpObj(**load_fixture('cat_md5_software.json'))
    if hf in args[0]:
        return BigIpObj(**load_fixture('cat_md5_hotfix.json'))
    if md5_soft in args[0]:
        return BigIpObj(**load_fixture('md5_sum_ok_software.json'))
    if md5_hf in args[0]:
        return BigIpObj(**load_fixture('md5_sum_failed_hf.json'))
    if curl in args[0]:
        return True


class BigIpObj(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.attrs = self.__dict__


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            volume='HD1.1',
            state='present',
            software='/var/fake/software_iso.iso',
            hotfix='/var/fake/hotfix_iso.iso',
            force='yes',
            reuse_inactive_volume='yes'
        )

        p = Parameters(args)
        assert p.volume == 'HD1.1'
        assert p.software == '/var/fake/software_iso.iso'
        assert p.hotfix == '/var/fake/hotfix_iso.iso'
        assert p.force == 'yes'
        assert p.reuse_inactive_volume == 'yes'

    def test_module_parameters_remote_src(self):
        args = dict(
            volume='HD1.1',
            state='present',
            software='http://somesite/software_iso.iso',
            hotfix='http://somesite/hotfix_iso.iso',
            force='yes',
            reuse_inactive_volume='yes',
            remote_src='yes',
            software_md5sum='http://somesite/software_iso.iso.md5',
            hotfix_md5sum='https://somesite/hotfix_iso.iso.md5'
        )

        p = Parameters(args)
        assert p.volume == 'HD1.1'
        assert p.force == 'yes'
        assert p.reuse_inactive_volume == 'yes'
        assert p.remote_src == 'yes'
        assert p.software_md5sum == 'http://somesite/software_iso.iso.md5'
        assert p.hotfix_md5sum == 'https://somesite/hotfix_iso.iso.md5'
        assert p.software == 'http://somesite/software_iso.iso'
        assert p.hotfix == 'http://somesite/hotfix_iso.iso'

    def test_api_parameters(self):
        args = dict(
            volume='HD1.1',
            state='activated',
            software='/var/fake/software_iso.iso'
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = False

            tmp = [{'create-volume': True}, {'reboot': True}]
            p = Parameters(args)
            assert p.volume == 'HD1.1'
            assert p.options == tmp


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestLocalManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.iso = os.path.join(iso_path, 'BIGIP-12.1.2.iso')
        self.iso2 = os.path.join(iso_path, 'BIGIP-12.0.0.0.0.606.iso')
        self.iso_hf1 = os.path.join(
            iso_path, 'Hotfix-BIGIP-12.0.0.2.0.644-HF2.iso'
        )
        self.iso_hf2 = os.path.join(
            iso_path, 'Hotfix-BIGIP-12.1.0.1.0.1447-HF1.iso'
        )
        self.iso_hf3 = os.path.join(
            iso_path, 'Hotfix-BIGIP-12.1.1.1.0.196-HF1.iso'
        )
        self.loaded_volumes = []
        self.loaded_volumes_2 = []
        self.loaded_volumes_trimmed = []
        self.loaded_images = []
        self.loaded_images_after_upload = []
        self.loaded_hotfixes = []
        vols = load_fixture('list_of_volumes_12_1_2_installed.json')
        vols2 = load_fixture('list_of_volumes_only_active_volume.json')
        vols3 = load_fixture('list_of_volumes_12_1_2_not_installed.json')
        images = load_fixture('list_images_local.json')
        images2 = load_fixture('list_images_after_upload_local.json')
        hotfixes = load_fixture('list_hotfixes_local.json')
        self.active_volume = BigIpObj(**load_fixture(
            'load_active_volume.json'))
        for item in vols:
            self.loaded_volumes.append(BigIpObj(**item))
        for item in vols2:
            self.loaded_volumes_trimmed.append(BigIpObj(**item))
        for item in vols3:
            self.loaded_volumes_2.append(BigIpObj(**item))
        for item in images:
            self.loaded_images.append(BigIpObj(**item))
        for item in images2:
            self.loaded_images_after_upload.append(BigIpObj(**item))
        for item in hotfixes:
            self.loaded_hotfixes.append(BigIpObj(**item))

    def test_activate_installed_volume(self, *args):
        set_module_args(dict(
            volume='HD1.3',
            software=self.iso,
            state='activated',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.reboot_volume_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['software'] == self.iso
            assert results['volume'] == 'HD1.3'

    def test_activate_installed_volume_using_hotfix(self, *args):
        set_module_args(dict(
            volume='HD1.2',
            hotfix=self.iso_hf3,
            state='activated',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.reboot_volume_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['hotfix'] == self.iso_hf3
            assert results['volume'] == 'HD1.2'

    def test_install_and_activate_software_new_volume(self, *args):
        set_module_args(dict(
            software=self.iso2,
            volume='HD1.2',
            state='activated',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = False

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=True)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is False
            assert results['state'] == 'activated'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso2

    def test_install_and_activate_software_reuse_volume(self, *args):
        set_module_args(dict(
            software=self.iso,
            state='activated',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_2
            patched['_volume_exists_on_device'].return_value = True

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['state'] == 'activated'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso

    def test_install_and_activate_software_create_volume_name(
            self, *args
    ):
        set_module_args(dict(
            software=self.iso,
            state='activated',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed
            patched['_volume_exists_on_device'].return_value = False

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_trimmed
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['volume'] == 'HD1.active.1'
            assert results['state'] == 'activated'
            assert results['software'] == self.iso

    def test_install_and_activate_hotfix_new_volume(self, *args):
        set_module_args(dict(
            volume='HD1.2',
            software=self.iso2,
            hotfix=self.iso_hf1,
            state='activated',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        with patch.object(Parameters, '_check_active_volume') as obj:
            obj.return_value = False

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.list_images_on_device = Mock(
                return_value=self.loaded_images_after_upload
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is False
            assert results['state'] == 'activated'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso2
            assert results['hotfix'] == self.iso_hf1

    def test_install_and_activate_hotfix_reuse_volume(self, *args):
        set_module_args(dict(
            software=self.iso2,
            hotfix=self.iso_hf1,
            state='activated',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes
            patched['_volume_exists_on_device'].return_value = True
            

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.list_images_on_device = Mock(
                return_value=self.loaded_images_after_upload
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['state'] == 'activated'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso2
            assert results['hotfix'] == self.iso_hf1

    def test_install_and_activate_hotfix_create_volume_name(self, *args):
        set_module_args(dict(
            software=self.iso2,
            hotfix=self.iso_hf1,
            state='activated',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed
            patched['_volume_exists_on_device'].return_value = False

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_trimmed
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(
                return_value=self.loaded_images_after_upload
            )

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['volume'] == 'HD1.active.1'
            assert results['state'] == 'activated'
            assert results['software'] == self.iso2
            assert results['hotfix'] == self.iso_hf1

    def test_install_and_activate_hotfix_base_image_missing(self, *args):
        set_module_args(dict(
            volume='HD1.2',
            hotfix=self.iso_hf1,
            state='activated',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

        with pytest.raises(F5ModuleError) as err:
            msg = 'Base image of version: 12.0.0 must exist to install this ' \
                  'hotfix.'
            mm.exec_module()
            assert err.value.message == msg

    def test_install_software_new_volume(self, *args):
        set_module_args(dict(
            volume='HD1.2',
            software=self.iso,
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is False
            assert results['state'] == 'installed'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso

    def test_install_software_reuse_volume(self, *args):
        set_module_args(dict(
            software=self.iso,
            state='installed',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_2

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.image_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['state'] == 'installed'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso

    def test_install_software_create_volume_name(self, *args):
        set_module_args(dict(
            software=self.iso,
            state='installed',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_volume_exists_on_device'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_trimmed
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['volume'] == 'HD1.active.1'
            assert results['state'] == 'installed'
            assert results['software'] == self.iso

    def test_install_hotfix_new_volume(self, *args):
        set_module_args(dict(
            volume='HD1.2',
            software=self.iso2,
            hotfix=self.iso_hf1,
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.list_images_on_device = Mock(
                return_value=self.loaded_images_after_upload
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is False
            assert results['state'] == 'installed'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso2
            assert results['hotfix'] == self.iso_hf1

    def test_install_hotfix_reuse_volume(self, *args):
        set_module_args(dict(
            software=self.iso2,
            hotfix=self.iso_hf1,
            state='installed',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.list_images_on_device = Mock(
                return_value=self.loaded_images_after_upload
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['state'] == 'installed'
            assert results['volume'] == 'HD1.2'
            assert results['software'] == self.iso2
            assert results['hotfix'] == self.iso_hf1

    def test_install_hotfix_create_volume_name(self, *args):
        set_module_args(dict(
            software=self.iso2,
            hotfix=self.iso_hf1,
            state='installed',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed
            

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_trimmed)
            mm.list_images_on_device = Mock(
                return_value=self.loaded_images_after_upload)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['volume'] == 'HD1.active.1'
            assert results['state'] == 'installed'
            assert results['software'] == self.iso2
            assert results['hotfix'] == self.iso_hf1

    def test_install_hotfix_base_image_missing(self, *args):
        set_module_args(dict(
            volume='HD1.2',
            hotfix=self.iso_hf1,
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.upload_to_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

        with pytest.raises(F5ModuleError) as err:
            msg = 'Base image of version: 12.0.0 must exist to install this ' \
                  'hotfix.'
            mm.exec_module()
            assert err.value.message == msg

    def test_install_to_active_volume_raises(self, *args):
        set_module_args(dict(
            volume='HD1.1',
            software=self.iso,
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_volume_exists_on_device=DEFAULT, _load_volume_from_device=DEFAULT)

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_volume_exists_on_device'].return_value = True
            patched['_load_volume_from_device'].return_value = self.active_volume

            mm = LocalManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )

            with pytest.raises(F5ModuleError) as err:
                msg = 'Cannot install software or hotfixes to active volumes.'
                mm.exec_module()

        assert err.value.message == msg

    def test_volume_missing_raises(self, *args):
        set_module_args(dict(
            software=self.iso,
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = LocalManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes_2)

        with pytest.raises(F5ModuleError) as err:
            msg = 'You must specify a volume.'
            mm.exec_module()

        assert err.value.message == msg

    def test_upload_software(self, *args):
        set_module_args(dict(
            software=self.iso,
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = LocalManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.image_exists_on_device = Mock(return_value=False)
        mm.upload_to_device = Mock(return_value=True)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.wait_for_images = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['force'] is False
        assert results['remote_src'] is False
        assert results['reuse_inactive_volume'] is False
        assert results['state'] == 'present'
        assert results['software'] == self.iso

    def test_upload_hotfix(self, *args):
        set_module_args(dict(
            hotfix=self.iso_hf1,
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = LocalManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.image_exists_on_device = Mock(return_value=False)
        mm.hotfix_exists_on_device = Mock(return_value=False)
        mm.upload_to_device = Mock(return_value=True)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.wait_for_images = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['force'] is False
        assert results['remote_src'] is False
        assert results['reuse_inactive_volume'] is False
        assert results['state'] == 'present'
        assert results['hotfix'] == self.iso_hf1

    def test_upload_software_hotfix(self, *args):
        set_module_args(dict(
            software=self.iso2,
            hotfix=self.iso_hf1,
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = LocalManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.image_exists_on_device = Mock(return_value=False)
        mm.hotfix_exists_on_device = Mock(return_value=False)
        mm.upload_to_device = Mock(return_value=True)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.wait_for_images = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['force'] is False
        assert results['remote_src'] is False
        assert results['reuse_inactive_volume'] is False
        assert results['state'] == 'present'
        assert results['hotfix'] == self.iso_hf1
        assert results['software'] == self.iso2


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestRemoteManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.loaded_volumes = []
        self.loaded_volumes_2 = []
        self.loaded_volumes_trimmed = []
        self.loaded_images = []
        self.loaded_images_after_upload = []
        self.loaded_hotfixes = []
        self.loaded_hotfixes_after_upload = []
        vols = load_fixture('list_of_volumes_12_1_2_installed.json')
        vols2 = load_fixture('list_of_volumes_only_active_volume.json')
        vols3 = load_fixture('list_of_volumes_12_1_2_not_installed.json')
        images = load_fixture('list_images_remote.json')
        images2 = load_fixture('list_images_after_upload_remote.json')
        hotfixes = load_fixture('list_hotfixes_remote.json')
        hotfixes2 = load_fixture('list_hotfixes_after_upload_remote.json')
        self.active_volume = BigIpObj(**load_fixture(
            'load_active_volume.json'))
        for item in vols:
            self.loaded_volumes.append(BigIpObj(**item))
        for item in vols2:
            self.loaded_volumes_trimmed.append(BigIpObj(**item))
        for item in vols3:
            self.loaded_volumes_2.append(BigIpObj(**item))
        for item in images:
            self.loaded_images.append(BigIpObj(**item))
        for item in images2:
            self.loaded_images_after_upload.append(BigIpObj(**item))
        for item in hotfixes:
            self.loaded_hotfixes.append(BigIpObj(**item))
        for item in hotfixes2:
            self.loaded_hotfixes_after_upload.append(BigIpObj(**item))

    def test_activate_installed_volume(self, *args):
        set_module_args(dict(
            volume='HD1.3',
            software='http://fake.com/BIGIP-12.1.2.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.iso.md5',
            build='0.0.249',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.reboot_volume_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['software'] == 'http://fake.com/BIGIP-12.1.2.iso'
            assert results['volume'] == 'HD1.3'

    def test_activate_installed_volume_using_hotfix(self, *args):
        set_module_args(dict(
            volume='HD1.4',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes)
            mm.reboot_volume_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['hotfix'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
            assert results['volume'] == 'HD1.4'

    def test_install_and_activate_software_new_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            volume='HD1.4',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=True)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is False
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['state'] == 'activated'
            assert results['version'] == '12.1.2'
            assert results['build'] == '0.0.249'
            assert results['volume'] == 'HD1.4'

    def test_install_and_activate_software_reuse_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_2
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['state'] == 'activated'
            assert results['version'] == '12.1.2'
            assert results['build'] == '0.0.249'
            assert results['volume'] == 'HD1.2'

    def test_install_and_activate_software_create_volume_name(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed
            patched['_volume_exists_on_device'].return_value = False

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['state'] == 'activated'
            assert results['version'] == '12.1.2'
            assert results['build'] == '0.0.249'
            assert results['volume'] == 'HD1.active.1'

    def test_install_and_activate_hotfix_new_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            volume='HD1.4',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(side_effect=[
                self.loaded_images, self.loaded_images_after_upload
            ]
                                            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['hotfix'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
            assert results['hotfix_md5sum'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
            assert results['state'] == 'activated'
            assert results['version'] == '12.1.2'
            assert results['build'] == '1.0.271'
            assert results['volume'] == 'HD1.4'

    def test_install_and_activate_hotfix_reuse_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            reuse_inactive_volume='yes',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_2
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(side_effect=[
                self.loaded_images, self.loaded_images_after_upload
            ]
                                            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['hotfix'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
            assert results['hotfix_md5sum'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
            assert results['state'] == 'activated'
            assert results['version'] == '12.1.2'
            assert results['build'] == '1.0.271'
            assert results['reuse_inactive_volume'] is True
            assert results['volume'] == 'HD1.2'

    def test_install_and_activate_hotfix_create_volume_name(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed
            patched['_volume_exists_on_device'].return_value = False

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(side_effect=[
                self.loaded_images, self.loaded_images_after_upload
                ]
            )
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.wait_for_device_reboot = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['hotfix'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
            assert results['hotfix_md5sum'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
            assert results['state'] == 'activated'
            assert results['version'] == '12.1.2'
            assert results['build'] == '1.0.271'
            assert results['volume'] == 'HD1.active.1'

    def test_install_and_activate_hotfix_base_image_missing(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='activated',
            remote_src='yes',
            volume='HD1.4',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.exists = Mock(return_value=False)
            mm.upload = Mock(return_value=True)

            msg = 'Base image of version: 12.1.2 ' \
                  'must exist to install this hotfix.'

            with pytest.raises(F5ModuleError) as err:
                mm.exec_module()

            assert err.value.message == msg

    def test_install_software_new_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            state='installed',
            remote_src='yes',
            volume='HD1.4',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=True)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is False
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['state'] == 'installed'
            assert results['version'] == '12.1.2'
            assert results['build'] == '0.0.249'
            assert results['volume'] == 'HD1.4'

    def test_install_software_reuse_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            state='installed',
            remote_src='yes',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_2
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['state'] == 'installed'
            assert results['version'] == '12.1.2'
            assert results['build'] == '0.0.249'
            assert results['volume'] == 'HD1.2'

    def test_install_software_create_volume_name(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            state='installed',
            remote_src='yes',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed
            patched['_volume_exists_on_device'].return_value = False

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['state'] == 'installed'
            assert results['version'] == '12.1.2'
            assert results['build'] == '0.0.249'
            assert results['volume'] == 'HD1.active.1'

    def test_install_hotfix_new_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='installed',
            remote_src='yes',
            volume='HD1.4',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(side_effect=[
                self.loaded_images, self.loaded_images_after_upload
            ]
                                            )
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['hotfix'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
            assert results['hotfix_md5sum'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
            assert results['state'] == 'installed'
            assert results['version'] == '12.1.2'
            assert results['build'] == '1.0.271'
            assert results['volume'] == 'HD1.4'

    def test_install_hotfix_reuse_volume(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='installed',
            remote_src='yes',
            reuse_inactive_volume='yes',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_2
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(side_effect=[
                self.loaded_images, self.loaded_images_after_upload
            ]
                                            )
            mm.delete_volume_on_device = Mock(return_value=True)
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['hotfix'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
            assert results['hotfix_md5sum'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
            assert results['state'] == 'installed'
            assert results['version'] == '12.1.2'
            assert results['build'] == '1.0.271'
            assert results['reuse_inactive_volume'] is True
            assert results['volume'] == 'HD1.2'

    def test_install_hotfix_create_volume_name(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='installed',
            remote_src='yes',
            server='localhost',
            password='password',
            reuse_inactive_volume='yes',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _list_volumes_on_device=DEFAULT,
                        _volume_exists_on_device=DEFAULT
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = False
            patched['_list_volumes_on_device'].return_value = self.loaded_volumes_trimmed
            patched['_volume_exists_on_device'].return_value = False

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.image_exists_on_device = Mock(return_value=False)
            mm.hotfix_exists_on_device = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(side_effect=[
                self.loaded_images, self.loaded_images_after_upload
                ]
            )
            mm.wait_for_software_install_on_device = Mock(return_value=True)
            mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
            mm.install_image_on_device = Mock(return_value=True)
            mm.install_hotfix_on_device = Mock(return_value=True)
            mm.wait_for_images = Mock(return_value=True)

            results = mm.exec_module()
            assert results['changed'] is True
            assert results['force'] is False
            assert results['reuse_inactive_volume'] is True
            assert results['remote_src'] is True
            assert results['software'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
            assert results['software_md5sum'] == \
                'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
            assert results['hotfix'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
            assert results['hotfix_md5sum'] == \
                'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
            assert results['state'] == 'installed'
            assert results['version'] == '12.1.2'
            assert results['build'] == '1.0.271'
            assert results['volume'] == 'HD1.active.1'

    def test_install_hotfix_base_image_missing(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            state='installed',
            remote_src='yes',
            volume='HD1.4',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_check_active_volume=DEFAULT,
                        _volume_exists_on_device=DEFAULT,
                        )

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_check_active_volume'].return_value = True
            patched['_volume_exists_on_device'].return_value = True

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )
            mm.list_hotfixes_on_device = Mock(
                return_value=self.loaded_hotfixes
            )
            mm.list_images_on_device = Mock(return_value=self.loaded_images)
            mm.exists = Mock(return_value=False)
            mm.upload = Mock(return_value=True)

            msg = 'Base image of version: 12.1.2 ' \
                  'must exist to install this hotfix.'

            with pytest.raises(F5ModuleError) as err:
                mm.exec_module()

            assert err.value.message == msg

    def test_install_to_active_volume_raises(self, *args):
        set_module_args(dict(
            volume='HD1.1',
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        to_patch = dict(_volume_exists_on_device=DEFAULT, _load_volume_from_device=DEFAULT)

        # Override methods to force specific logic in the module to happen
        with patch.multiple(Parameters, **to_patch) as patched:
            patched['_volume_exists_on_device'].return_value = True
            patched['_load_volume_from_device'].return_value = self.active_volume

            mm = RemoteManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.list_volumes_on_device = Mock(
                return_value=self.loaded_volumes_2
            )

            with pytest.raises(F5ModuleError) as err:
                msg = 'Cannot install software or hotfixes to active volumes.'
                mm.exec_module()

        assert err.value.message == msg

    def test_volume_missing_raises(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.list_volumes_on_device = Mock(return_value=self.loaded_volumes_2)

        with pytest.raises(F5ModuleError) as err:
            msg = 'You must specify a volume.'
            mm.exec_module()

        assert err.value.message == msg

    def test_version_and_build_missing_raises_software(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            volume='HD1.4',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.load_image_by_name_from_device = Mock(return_value=None)

        msg = 'Unable to set ISO information based on ISO name, ' \
              'please specify version and build.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    def test_version_and_build_missing_raises_hotfix(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            volume='HD1.4',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.load_hotfix_by_name_from_device = Mock(return_value=None)

        msg = 'Unable to set ISO information based on ISO name, ' \
              'please specify version and build.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    def test_version_missing_raises_software(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            volume='HD1.4',
            build='1.0.271',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.load_image_by_name_from_device = Mock(return_value=None)

        msg = 'Unable to set ISO information based on ISO name, ' \
              'please specify version and build.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    def test_version_missing_raises_hotfix(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            volume='HD1.4',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.load_hotfix_by_name_from_device = Mock(return_value=None)

        msg = 'Unable to set ISO information based on ISO name, ' \
              'please specify version and build.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    def test_build_missing_raises_software(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            volume='HD1.4',
            version='12.1.2',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.load_image_by_name_from_device = Mock(return_value=None)

        msg = 'Unable to set ISO information based on ISO name, ' \
              'please specify version and build.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    def test_build_missing_raises_hotfix(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            version='12.1.2',
            volume='HD1.4',
            remote_src='yes',
            state='installed',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.load_hotfix_by_name_from_device = Mock(return_value=None)

        msg = 'Unable to set ISO information based on ISO name, ' \
              'please specify version and build.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    def test_missing_md5_file_raises(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            build='0.0.249',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        msg = 'You must provide md5sum file links if using remote source.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()

        assert err.value.message == msg

    def test_software_download_fail_raises(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_fail)
        mm.exists = Mock(return_value=False)
        msg = 'ISO download failed from remote host.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()

        assert err.value.message == msg

    def test_hotfix_download_fail_raises(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_fail)
        mm.exists = Mock(return_value=False)
        msg = 'ISO download failed from remote host.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()

        assert err.value.message == msg

    def test_software_ok_hotfix_download_fail_raises(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.run_command_on_device = Mock(
            side_effect=cmd_side_effect_md5_fail_hotfix
        )
        mm.exists = Mock(return_value=False)
        mm.wait_for_images = Mock(return_value=True)
        msg = 'ISO download failed from remote host.'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()

        assert err.value.message == msg

    def test_device_download_fallback_to_filename(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.run_command_on_device = Mock(
            side_effect=cmd_side_effect_md5_fail_hotfix
        )
        mm.hotfix_exists_by_name_on_device = Mock(return_value=False)
        mm.image_exists_by_name_on_device = Mock(return_value=True)
        mm.wait_for_images = Mock(return_value=True)
        mm.list_hotfixes_on_device = Mock(
            return_value=self.loaded_hotfixes
        )
        mm.list_images_on_device = Mock(
            return_value=self.loaded_images_after_upload
        )
        mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)

        result = mm.exec_module()

        assert result['changed'] is True
        assert result['force'] is False
        assert result['hotfix'] == \
            'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
        assert result['hotfix_md5sum'] == \
            'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
        assert result['software'] == 'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
        assert result['software_md5sum'] == \
            'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
        assert result['reuse_inactive_volume'] is False
        assert result['remote_src'] is True
        assert result['state'] == 'present'

    def test_device_download_software(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.image_exists_on_device = Mock(return_value=False)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
        mm.wait_for_images = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['force'] is False
        assert results['reuse_inactive_volume'] is False
        assert results['remote_src'] is True
        assert results['software'] == \
            'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
        assert results['software_md5sum'] == \
            'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
        assert results['state'] == 'present'
        assert results['version'] == '12.1.2'
        assert results['build'] == '0.0.249'

    def test_device_download_hotfix(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.hotfix_exists_on_device = Mock(return_value=False)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.wait_for_images = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['force'] is False
        assert results['remote_src'] is True
        assert results['reuse_inactive_volume'] is False
        assert results['state'] == 'present'
        assert results['hotfix'] == \
            'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
        assert results['hotfix_md5sum'] == \
            'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'

    def test_device_download_software_hotfix(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            hotfix_md5sum='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5',
            build='1.0.271',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.list_hotfixes_on_device = Mock(return_value=self.loaded_hotfixes)
        mm.list_images_on_device = Mock(return_value=self.loaded_images)
        mm.run_command_on_device = Mock(side_effect=cmd_side_effect_md5_ok)
        mm.exists = Mock(return_value=False)
        mm.wait_for_images = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['force'] is False
        assert results['remote_src'] is True
        assert results['reuse_inactive_volume'] is False
        assert results['state'] == 'present'
        assert results['software'] == \
            'http://fake.com/BIGIP-12.1.2.0.0.249.iso'
        assert results['software_md5sum'] == \
            'http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5'
        assert results['hotfix'] == \
            'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso'
        assert results['hotfix_md5sum'] == \
            'http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5'
        assert results['build'] == '1.0.271'
        assert results['version'] == '12.1.2'

    def test_delete_software_image_no_md5sum(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            build='0.0.249',
            version='12.1.2',
            remote_src='yes',
            state='absent',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.exists = Mock(return_value=True)
        mm.remove = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True

    def test_delete_hotfix_image_no_md5sum(self, *args):
        set_module_args(dict(
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            build='1.0.271',
            version='12.1.2',
            remote_src='yes',
            state='absent',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.exists = Mock(return_value=True)
        mm.remove = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True

    def test_delete_software_hotfix_image_no_md5sum(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            hotfix='http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso',
            build='1.0.271',
            version='12.1.2',
            remote_src='yes',
            state='absent',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        mm.exists = Mock(return_value=True)
        mm.remove = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True

    def test_device_download_invalid_link(self, *args):
        set_module_args(dict(
            software='http://fake.com/BIGIP-12.1.2.0.0.249.iso',
            software_md5sum='/root/path/to/md5/BIGIP-12.1.2.0.0.249.iso.md5',
            build='0.0.249',
            version='12.1.2',
            remote_src='yes',
            state='present',
            server='localhost',
            password='password',
            user='admin',
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = RemoteManager(client)
        mm.exit_json = Mock(return_value=False)
        msg = '/root/path/to/md5/BIGIP-12.1.2.0.0.249.iso.md5 is not a valid URL, please provide a valid link'

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()

        assert err.value.message == msg
