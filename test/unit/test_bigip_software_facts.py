# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
from ansible.compat.tests.mock import Mock
from ansible.compat.tests.mock import patch
from ansible.module_utils.basic import AnsibleModule

try:
    from library.bigip_software_facts import Parameters
    from library.bigip_software_facts import ModuleManager
    from library.bigip_software_facts import ArgumentSpec
    from library.bigip_software_facts import F5ModuleError
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    from test.unit.modules.utils import set_module_args
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_software_facts import Parameters
        from ansible.modules.network.f5.bigip_software_facts import ModuleManager
        from ansible.modules.network.f5.bigip_software_facts import ArgumentSpec
        from ansible.modules.network.f5.bigip_software_facts import F5ModuleError
        from ansible.module_utils.network.f5.common import F5ModuleError
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
        from units.modules.utils import set_module_args
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


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

        p = Parameters(params=args)

        assert p.filter == ('version', '12.1.1')
        assert p.include == ['image', 'hotfix', 'volume']


@patch('library.bigip_software_facts.ImageFactManager.get_facts_from_device', return_value=loaded_images)
@patch('library.bigip_software_facts.HotfixFactManager.get_facts_from_device', return_value=loaded_hotfixes)
@patch('library.bigip_software_facts.VolumeFactManager.get_facts_from_device', return_value=loaded_volumes)
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

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        mm = ModuleManager(module=module)
        mm.exit_json = Mock(return_value=False)
        results = mm.exec_module()

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

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        mm = ModuleManager(module=module)
        mm.exit_json = Mock(return_value=False)
        results = mm.exec_module()

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

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        mm = ModuleManager(module=module)
        mm.exit_json = Mock(return_value=False)
        results = mm.exec_module()

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

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        mm = ModuleManager(module=module)
        mm.exit_json = Mock(return_value=False)
        results = mm.exec_module()

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

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        mm = ModuleManager(module=module)
        mm.exit_json = Mock(return_value=False)
        results = mm.exec_module()

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

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        mm = ModuleManager(module=module)
        mm.exit_json = Mock(return_value=False)
        results = mm.exec_module()
        images = results['images'][0]
        volumes = results['volumes'][0]

        assert results['changed'] is True
        assert len(results['hotfixes']) == 0
        assert len(results['images']) == 1
        assert len(results['volumes']) == 1
        assert 'product' in images.keys()
        assert 'name' in images.keys()
        assert 'product' in volumes.keys()
        assert 'name' in volumes.keys()
        assert images['product'] == 'BIG-IP'
        assert images['name'] == 'BIGIP-12.1.1.0.0.184.iso'
        assert volumes['product'] == 'BIG-IP'
        assert volumes['name'] == 'HD1.2'

    def test_get_volume_filter_on_active(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include='volume',
            filter='active:true'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        mm = ModuleManager(module=module)
        mm.exit_json = Mock(return_value=False)
        results = mm.exec_module()
        volumes = results['volumes'][0]

        assert results['changed'] is True
        assert 'images' not in results.keys()
        assert 'hotfixes' not in results.keys()
        assert len(results['volumes']) == 1
        assert 'product' in volumes.keys()
        assert 'name' in volumes.keys()
        assert volumes['product'] == 'BIG-IP'
        assert volumes['name'] == 'HD1.1'

    def test_invalid_filter_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter='foo:bar'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '"foo" is not a supported filter. Supported key values are: name, build, version, status, active'
            mm = ModuleManager(module=module)
            mm.exec_module()

        assert str(err.value) == msg

    def test_invalid_filter_format_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter='foobar'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '"foobar" is not a valid filter format. Filters must have key:value format'
            mm = ModuleManager(module=module)
            mm.exec_module()

        assert str(err.value) == msg

    def test_invalid_filter_empty_key_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter=':foobar'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '":foobar" is not a valid filter format. Filters must have key:value format'
            mm = ModuleManager(module=module)
            mm.exec_module()

        assert str(err.value) == msg

    def test_invalid_filter_empty_value_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            filter='name:'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        with pytest.raises(F5ModuleError) as err:
            msg = '"name:" is not a valid filter format. Filters must have key:value format'
            mm = ModuleManager(module=module)
            mm.exec_module()

        assert str(err.value) == msg

    def test_invalid_include_raises(self, *args):
        set_module_args(dict(
            server='localhost',
            password='password',
            user='admin',
            include=['bar', 'foo']
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        with pytest.raises(F5ModuleError) as err:
            msg = 'Include parameter may only be specified as one or more of the following: all, volume, image, hotfix'
            mm = ModuleManager(module=module)
            mm.exec_module()

        assert str(err.value) == msg
