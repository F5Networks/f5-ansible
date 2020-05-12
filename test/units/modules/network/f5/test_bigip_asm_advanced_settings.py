# -*- coding: utf-8 -*-
#
# Copyright: (c) 2019, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible.module_utils.basic import AnsibleModule

try:
    from library.modules.bigip_asm_advanced_settings import ApiParameters
    from library.modules.bigip_asm_advanced_settings import ModuleParameters
    from library.modules.bigip_asm_advanced_settings import ModuleManager
    from library.modules.bigip_asm_advanced_settings import ArgumentSpec
    from test.units.compat import unittest
    from test.units.compat.mock import Mock
    from test.units.compat.mock import patch
    from test.units.compat.utils import set_module_args
except ImportError:
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_asm_advanced_settings import ApiParameters
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_asm_advanced_settings import ModuleParameters
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_asm_advanced_settings import ModuleManager
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_asm_advanced_settings import ArgumentSpec
    from ansible_collections.f5networks.f5_modules.tests.units.compat import unittest
    from ansible_collections.f5networks.f5_modules.tests.units.compat import Mock
    from ansible_collections.f5networks.f5_modules.tests.units.compat import patch
    from ansible_collections.f5networks.f5_modules.tests.units.utils import set_module_args


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


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='foo',
            value='5',
        )
        p = ModuleParameters(params=args)
        assert p.name == 'foo'
        assert p.value == 5

    def test_api_parameters(self):
        args = dict(
            name='foo',
            value='bar',
            defaultValue='baz',

        )
        p = ApiParameters(params=args)
        assert p.name == 'foo'
        assert p.value == 'bar'
        assert p.default_value == 'baz'


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()
        try:
            self.p1 = patch('library.modules.bigip_asm_advanced_settings.module_provisioned')
            self.m1 = self.p1.start()
            self.m1.return_value = True
        except Exception:
            self.p1 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_asm_advanced_settings.module_provisioned')
            self.m1 = self.p1.start()
            self.m1.return_value = True

    def tearDown(self):
        self.p1.stop()

    def test_set_asm_setting(self, *args):
        set_module_args(dict(
            name='long_request_buffer_size',
            value='30',
            state='present',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = ApiParameters(params=load_fixture('load_asm_settings.json'))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(return_value=False)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
