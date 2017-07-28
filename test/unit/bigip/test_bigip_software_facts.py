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
import sys
import pytest

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from mock import patch
from mock import Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client

try:
    from library.bigip_software_facts import Parameters
    from library.bigip_software_facts import FactManagerBase
    from library.bigip_software_facts import ArgumentSpec
    from library.bigip_software_facts import F5ModuleError
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_software_facts import Parameters
        from ansible.modules.network.f5.bigip_software_facts import FactManagerBase
        from ansible.modules.network.f5.bigip_software_facts import ArgumentSpec
        from ansible.modules.network.f5.bigip_software_facts import F5ModuleError
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


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


class BigIpObj(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.attrs = self.__dict__

loaded_volumes = []
loaded_images = []
loaded_hotfixes = []
vols = load_fixture('list_of_volumes_12_1_2_installed.json')
images = load_fixture('list_images_after_upload_local.json')
hotfixes = load_fixture('list_hotfixes_local.json')
for item in vols:
    loaded_volumes.append(BigIpObj(**item))
for item in images:
    loaded_images.append(BigIpObj(**item))
for item in hotfixes:
    loaded_hotfixes.append(BigIpObj(**item))


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            include=['image', 'hotfix', 'volume'],
            filter='version:12.1.1'
        )

        p = Parameters(args)

        assert p.filter == ('version', '12.1.1')
        assert p.include == ['image', 'hotfix', 'volume']


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
@patch('library.bigip_software_facts.ImageFactManager.list_images_on_device', return_value=loaded_images)
@patch('library.bigip_software_facts.HotfixFactManager.list_hotfixes_on_device', return_value=loaded_hotfixes)
@patch('library.bigip_software_facts.VolumeFactManager.list_volumes_on_device', return_value=loaded_volumes)
class TestFactManagerBase(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()

    def test_get_all_facts_no_filter(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include='all'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        mm = FactManagerBase(client)
        mm.exit_json = Mock(return_value=False)
        results = mm.display_facts()

        assert results['changed'] is True
        assert len(results['images']) == 8
        assert len(results['hotfixes']) == 5
        assert len(results['volumes']) == 4

    def test_get_images_no_filter(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include='image'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        mm = FactManagerBase(client)
        mm.exit_json = Mock(return_value=False)
        results = mm.display_facts()

        assert results['changed'] is True
        assert 'hotfixes' not in results.keys()
        assert 'volumes' not in results.keys()
        assert len(results['images']) == 8

    def test_get_hotfixes_no_filter(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include='hotfix'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        mm = FactManagerBase(client)
        mm.exit_json = Mock(return_value=False)
        results = mm.display_facts()

        assert results['changed'] is True
        assert 'images' not in results.keys()
        assert 'volumes' not in results.keys()
        assert len(results['hotfixes']) == 5

    def test_get_volumes_no_filter(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include='volume'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        mm = FactManagerBase(client)
        mm.exit_json = Mock(return_value=False)
        results = mm.display_facts()

        assert results['changed'] is True
        assert 'images' not in results.keys()
        assert 'hotfixes' not in results.keys()
        assert len(results['volumes']) == 4

    def test_get_image_and_hotfixes_no_filter(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include=['image', 'hotfix']
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        mm = FactManagerBase(client)
        mm.exit_json = Mock(return_value=False)
        results = mm.display_facts()

        assert results['changed'] is True
        assert len(results['images']) == 8
        assert len(results['hotfixes']) == 5
        assert 'volumes' not in results.keys()

    def test_get_all_facts_filter_on_version(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include='all',
            filter='version:12.1.1'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        mm = FactManagerBase(client)
        mm.exit_json = Mock(return_value=False)
        results = mm.display_facts()

        assert results['changed'] is True
        assert len(results['hotfixes']) == 0
        assert results['images'] == [{'product': 'BIG-IP', 'name': 'BIGIP-12.1.1.0.0.184.iso',
                                      'lastModified': 'Sun Oct  2 20:50:04 2016', 'version': '12.1.1',
                                      'build': '0.0.184', 'fileSize': '1997 MB'}]
        assert results['volumes'] == [{'status': 'complete', 'product': 'BIG-IP', 'name': 'HD1.2',
                                       'basebuild': '0.0.184', 'version': '12.1.1', 'build': '1.0.196'}]

    def test_get_volume_filter_on_active(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include='volume',
            filter='active:true'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        mm = FactManagerBase(client)
        mm.exit_json = Mock(return_value=False)
        results = mm.display_facts()

        assert results['changed'] is True
        assert 'images' not in results.keys()
        assert 'hotfixes' not in results.keys()
        assert results['volumes'] == [{'status': 'complete', 'product': 'BIG-IP', 'name': 'HD1.1',
                                       'basebuild': '0.0.1434', 'version': '12.1.0', 'build': '1.0.1447',
                                       'active': 'True'}]

    def test_invalid_filter_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter='foo:bar'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '"foo" is not a supported filter. Supported key values are: name, build, version, status, active'
            FactManagerBase(client)

        assert err.value.message == msg

    def test_invalid_filter_format_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter='foobar'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '"foobar" is not a valid filter format. Filters must have key:value format'
            FactManagerBase(client)

        assert err.value.message == msg

    def test_invalid_filter_empty_key_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter=':foobar'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '":foobar" is not a valid filter format. Filters must have key:value format'
            FactManagerBase(client)

        assert err.value.message == msg

    def test_invalid_filter_empty_value_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter='name:'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '"name:" is not a valid filter format. Filters must have key:value format'
            FactManagerBase(client)

        assert err.value.message == msg

    def test_invalid_include_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include=['bar', 'foo']
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        with pytest.raises(F5ModuleError) as err:
            msg = 'Include parameter may only be specified as one or more of the following: all, volume, image, hotfix'
            FactManagerBase(client)

        assert err.value.message == msg

