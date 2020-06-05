# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
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

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_monitor_tcp import (
    Parameters, ModuleManager, ArgumentSpec
)
from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import F5ModuleError
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock
from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args


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
            parent='parent',
            send='this is a send string',
            receive='this is a receive string',
            ip='10.10.10.10',
            type='TTYPE_TCP',
            port=80,
            interval=20,
            timeout=30,
            time_until_up=60,
            partition='Common'
        )

        p = Parameters(params=args)
        assert p.name == 'foo'
        assert p.parent == '/Common/parent'
        assert p.send == 'this is a send string'
        assert p.receive == 'this is a receive string'
        assert p.ip == '10.10.10.10'
        assert p.type == 'tcp'
        assert p.port == 80
        assert p.destination == '10.10.10.10:80'
        assert p.interval == 20
        assert p.timeout == 30
        assert p.time_until_up == 60

    def test_module_parameters_ints_as_strings(self):
        args = dict(
            name='foo',
            parent='parent',
            send='this is a send string',
            receive='this is a receive string',
            ip='10.10.10.10',
            type='TTYPE_TCP',
            port='80',
            interval='20',
            timeout='30',
            time_until_up='60',
            partition='Common'
        )

        p = Parameters(params=args)
        assert p.name == 'foo'
        assert p.parent == '/Common/parent'
        assert p.send == 'this is a send string'
        assert p.receive == 'this is a receive string'
        assert p.ip == '10.10.10.10'
        assert p.type == 'tcp'
        assert p.port == 80
        assert p.destination == '10.10.10.10:80'
        assert p.interval == 20
        assert p.timeout == 30
        assert p.time_until_up == 60

    def test_api_parameters(self):
        args = dict(
            name='foo',
            defaultsFrom='/Common/parent',
            send='this is a send string',
            recv='this is a receive string',
            destination='10.10.10.10:80',
            interval=20,
            timeout=30,
            timeUntilUp=60
        )

        p = Parameters(params=args)
        assert p.name == 'foo'
        assert p.parent == '/Common/parent'
        assert p.send == 'this is a send string'
        assert p.receive == 'this is a receive string'
        assert p.ip == '10.10.10.10'
        assert p.type == 'tcp'
        assert p.port == 80
        assert p.destination == '10.10.10.10:80'
        assert p.interval == 20
        assert p.timeout == 30
        assert p.time_until_up == 60


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_monitor(self, *args):
        set_module_args(dict(
            name='foo',
            parent='parent',
            send='this is a send string',
            receive='this is a receive string',
            ip='10.10.10.10',
            port=80,
            interval=20,
            timeout=30,
            time_until_up=60,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.exists = Mock(side_effect=[False, True])
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['parent'] == '/Common/parent'

    def test_create_monitor_idempotent(self, *args):
        set_module_args(dict(
            name='foo',
            parent='tcp',
            send='this is a send string',
            receive='this is a receive string',
            ip='10.10.10.10',
            port=80,
            interval=20,
            timeout=30,
            time_until_up=60,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()

        assert results['changed'] is False

    def test_update_port(self, *args):
        set_module_args(dict(
            name='foo',
            port=800,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['port'] == 800

    def test_update_interval(self, *args):
        set_module_args(dict(
            name='foo',
            interval=10,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['interval'] == 10

    def test_update_interval_larger_than_existing_timeout(self, *args):
        set_module_args(dict(
            name='foo',
            interval=30,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        with pytest.raises(F5ModuleError) as ex:
            mm.exec_module()

        assert "must be less than" in str(ex.value)

    def test_update_interval_larger_than_new_timeout(self, *args):
        set_module_args(dict(
            name='foo',
            interval=10,
            timeout=5,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        with pytest.raises(F5ModuleError) as ex:
            mm.exec_module()

        assert "must be less than" in str(ex.value)

    def test_update_send(self, *args):
        set_module_args(dict(
            name='foo',
            send='this is another send string',
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['send'] == 'this is another send string'

    def test_update_receive(self, *args):
        set_module_args(dict(
            name='foo',
            receive='this is another receive string',
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['receive'] == 'this is another receive string'

    def test_update_timeout(self, *args):
        set_module_args(dict(
            name='foo',
            timeout=300,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['timeout'] == 300

    def test_update_time_until_up(self, *args):
        set_module_args(dict(
            name='foo',
            time_until_up=300,
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = Parameters(params=load_fixture('load_ltm_monitor_tcp.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['time_until_up'] == 300
