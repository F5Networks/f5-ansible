# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import Mock
from ansible.compat.tests.mock import patch
from ansible.module_utils.basic import AnsibleModule

try:
    from library.bigip_data_group import ExternalModuleParameters
    from library.bigip_data_group import InternalModuleParameters
    from library.bigip_data_group import ModuleManager
    from library.bigip_data_group import ExternalManager
    from library.bigip_data_group import InternalManager
    from library.bigip_data_group import ArgumentSpec
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    from test.unit.modules.utils import set_module_args
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_data_group import ExternalModuleParameters
        from ansible.modules.network.f5.bigip_data_group import InternalModuleParameters
        from ansible.modules.network.f5.bigip_data_group import ModuleManager
        from ansible.modules.network.f5.bigip_data_group import ExternalManager
        from ansible.modules.network.f5.bigip_data_group import InternalManager
        from ansible.modules.network.f5.bigip_data_group import ArgumentSpec
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


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='foo',
            type='address',
            delete_data_group_file=False,
            internal=False,
            records=[
                dict(
                    key='foo',
                    value='bar'
                )
            ],
            separator=':=',
            state='present',
            partition='Common'
        )

        p = InternalModuleParameters(params=args)
        assert p.name == 'foo'
        assert p.type == 'address'
        assert p.delete_data_group_file is False
        assert len(p.records) == 1
        assert 'key' in p.records[0]
        assert 'value' in p.records[0]
        assert p.records[0]['key'] == 'foo'
        assert p.records[0]['value'] == 'bar'
        assert p.separator == ':='
        assert p.state == 'present'
        assert p.partition == 'Common'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_external_datagroup_type_string(self, *args):
        set_module_args(dict(
            name='foo',
            delete_data_group_file=False,
            internal=False,
            records_content="""
            a := alpha
            b := bravo
            c := charlie
            x := x-ray
            y := yankee
            z := zulu
            """,
            separator=':=',
            state='present',
            partition='Common',
            server='localhost',
            password='password',
            user='admin'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            mutually_exclusive=self.spec.mutually_exclusive,
        )

        # Override methods in the specific type of manager
        mm1 = ExternalManager(module=module, params=module.params)
        mm1.exists = Mock(side_effect=[False, True])
        mm1.create_on_device = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm0 = ModuleManager(module=module)
        mm0.get_manager = Mock(return_value=mm1)

        results = mm0.exec_module()

        assert results['changed'] is True

    def test_create_external_incorrect_address_data(self, *args):
        set_module_args(dict(
            name='foo',
            delete_data_group_file=False,
            internal=False,
            type='address',
            records_content="""
            a := alpha
            b := bravo
            c := charlie
            x := x-ray
            y := yankee
            z := zulu
            """,
            separator=':=',
            state='present',
            partition='Common',
            server='localhost',
            password='password',
            user='admin'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            mutually_exclusive=self.spec.mutually_exclusive,
        )

        # Override methods in the specific type of manager
        mm1 = ExternalManager(module=module, params=module.params)
        mm1.exists = Mock(side_effect=[False, True])
        mm1.create_on_device = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm0 = ModuleManager(module=module)
        mm0.get_manager = Mock(return_value=mm1)

        with pytest.raises(F5ModuleError) as ex:
            mm0.exec_module()

        assert "The value on line '1' does not match the type 'address'" == str(ex.value)

    def test_create_external_incorrect_integer_data(self, *args):
        set_module_args(dict(
            name='foo',
            delete_data_group_file=False,
            internal=False,
            type='integer',
            records_content="""
            a := alpha
            b := bravo
            c := charlie
            x := x-ray
            y := yankee
            z := zulu
            """,
            separator=':=',
            state='present',
            partition='Common',
            server='localhost',
            password='password',
            user='admin'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            mutually_exclusive=self.spec.mutually_exclusive,
        )

        # Override methods in the specific type of manager
        mm1 = ExternalManager(module=module, params=module.params)
        mm1.exists = Mock(side_effect=[False, True])
        mm1.create_on_device = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm0 = ModuleManager(module=module)
        mm0.get_manager = Mock(return_value=mm1)

        with pytest.raises(F5ModuleError) as ex:
            mm0.exec_module()

        assert "The value on line '1' does not match the type 'integer'" == str(ex.value)

    def test_update_external_string_data(self, *args):
        set_module_args(dict(
            name='foo',
            delete_data_group_file=False,
            internal=False,
            type='integer',
            records_content="""
            a := alpha,
            b := bravo,
            c := charlie,
            x := x-ray,
            y := yankee,
            z := zulu
            """,
            separator=':=',
            state='present',
            partition='Common',
            server='localhost',
            password='password',
            user='admin'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            mutually_exclusive=self.spec.mutually_exclusive,
        )

        # Override methods in the specific type of manager
        mm1 = ExternalManager(module=module, params=module.params)
        mm1.exists = Mock(side_effect=[False, True])
        mm1.create_on_device = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm0 = ModuleManager(module=module)
        mm0.get_manager = Mock(return_value=mm1)

        with pytest.raises(F5ModuleError) as ex:
            mm0.exec_module()

        assert "The value on line '1' does not match the type 'integer'" == str(ex.value)
