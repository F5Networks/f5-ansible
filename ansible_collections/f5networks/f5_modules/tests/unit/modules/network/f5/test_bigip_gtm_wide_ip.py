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

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_wide_ip import (
    ApiParameters, ModuleParameters, ModuleManager, ArgumentSpec, UntypedManager, TypedManager
)
from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import F5ModuleError
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock, patch
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
            name='foo.baz.bar',
            pool_lb_method='round-robin',
        )
        p = ModuleParameters(params=args)
        assert p.name == 'foo.baz.bar'
        assert p.pool_lb_method == 'round-robin'

    def test_module_pools(self):
        args = dict(
            pools=[
                dict(
                    name='foo',
                    ratio='100'
                )
            ]
        )
        p = ModuleParameters(params=args)
        assert len(p.pools) == 1

    def test_api_parameters(self):
        args = dict(
            name='foo.baz.bar',
            poolLbMode='round-robin'
        )
        p = ApiParameters(params=args)
        assert p.name == 'foo.baz.bar'
        assert p.pool_lb_method == 'round-robin'

    def test_api_pools(self):
        args = load_fixture('load_gtm_wide_ip_with_pools.json')
        p = ApiParameters(params=args)
        assert len(p.pools) == 3
        assert 'name' in p.pools[0]
        assert 'ratio' in p.pools[0]
        assert 'order' in p.pools[0]
        assert p.pools[0]['name'] == '/Common/baz'
        assert p.pools[0]['ratio'] == 10
        assert p.pools[0]['order'] == 0
        assert p.pools[1]['name'] == '/Common/maz'
        assert p.pools[1]['ratio'] == 10
        assert p.pools[1]['order'] == 1
        assert p.pools[2]['name'] == '/Common/vaz'
        assert p.pools[2]['ratio'] == 11
        assert p.pools[2]['order'] == 2

    def test_module_not_fqdn_name(self):
        args = dict(
            name='foo',
            lb_method='round-robin'
        )
        with pytest.raises(F5ModuleError) as excinfo:
            p = ModuleParameters(params=args)
            assert p.name == 'foo'
        assert 'The provided name must be a valid FQDN' in str(excinfo.value)


class TestUntypedManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.p1 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_wide_ip.module_provisioned')
        self.m1 = self.p1.start()
        self.m1.return_value = True
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_wide_ip.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_wide_ip.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()

    def test_create_wideip(self, *args):
        set_module_args(dict(
            name='foo.baz.bar',
            lb_method='round-robin',
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

        # Override methods in the specific type of manager
        tm = UntypedManager(module=module, params=module.params)
        tm.exists = Mock(return_value=False)
        tm.create_on_device = Mock(return_value=True)
        tm.version_is_less_than_12 = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.version_is_less_than_12 = Mock(return_value=True)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['name'] == 'foo.baz.bar'
        assert results['state'] == 'present'
        assert results['lb_method'] == 'round-robin'


class TestTypedManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.p1 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_wide_ip.module_provisioned')
        self.m1 = self.p1.start()
        self.m1.return_value = True
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_wide_ip.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_wide_ip.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()

    def test_create_wideip(self, *args):
        set_module_args(dict(
            name='foo.baz.bar',
            lb_method='round-robin',
            type='a',
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

        # Override methods in the specific type of manager
        tm = TypedManager(module=module, params=module.params)
        tm.exists = Mock(return_value=False)
        tm.create_on_device = Mock(return_value=True)
        tm.version_is_less_than_12 = Mock(return_value=False)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.version_is_less_than_12 = Mock(return_value=False)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['name'] == 'foo.baz.bar'
        assert results['state'] == 'present'
        assert results['lb_method'] == 'round-robin'

    def test_create_wideip_with_pool(self, *args):
        set_module_args(dict(
            name='foo.baz.bar',
            lb_method='round-robin',
            type='a',
            pools=[
                dict(
                    name='baz',
                    ratio=10,
                ),
                dict(
                    name='maz',
                    ratio=10,
                    order=1
                ),
                dict(
                    name='vaz',
                    ratio=11,
                    order=2
                )
            ],
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

        # Override methods in the specific type of manager
        tm = TypedManager(module=module, params=module.params)
        tm.exists = Mock(return_value=False)
        tm.create_on_device = Mock(return_value=True)
        tm.version_is_less_than_12 = Mock(return_value=False)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.version_is_less_than_12 = Mock(return_value=False)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['name'] == 'foo.baz.bar'
        assert results['state'] == 'present'
        assert results['lb_method'] == 'round-robin'

    def test_create_wideip_with_pool_idempotent(self, *args):
        set_module_args(dict(
            name='foo.bar.com',
            lb_method='round-robin',
            type='a',
            pools=[
                dict(
                    name='baz',
                    ratio=10,
                ),
                dict(
                    name='maz',
                    ratio=10,
                    order=1
                ),
                dict(
                    name='vaz',
                    ratio=11,
                    order=2
                )
            ],
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = ApiParameters(params=load_fixture('load_gtm_wide_ip_with_pools.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        tm = TypedManager(module=module, params=module.params)
        tm.exists = Mock(return_value=True)
        tm.read_current_from_device = Mock(return_value=current)
        tm.version_is_less_than_12 = Mock(return_value=False)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.version_is_less_than_12 = Mock(return_value=False)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is False

    def test_update_wideip_with_pool(self, *args):
        set_module_args(dict(
            name='foo.bar.com',
            lb_method='round-robin',
            type='a',
            pools=[
                dict(
                    name='baz',
                    ratio=10
                ),
                dict(
                    name='alec',
                    ratio=100
                )
            ],
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = ApiParameters(params=load_fixture('load_gtm_wide_ip_with_pools.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        tm = TypedManager(module=module, params=module.params)
        tm.exists = Mock(return_value=True)
        tm.read_current_from_device = Mock(return_value=current)
        tm.update_on_device = Mock(return_value=True)
        tm.version_is_less_than_12 = Mock(return_value=False)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.version_is_less_than_12 = Mock(return_value=False)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
        assert 'pools' in results
