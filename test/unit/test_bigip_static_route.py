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

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client

try:
    from library.bigip_static_route import Parameters
    from library.bigip_static_route import ModuleManager
    from library.bigip_static_route import ArgumentSpec
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_static_route import Parameters
        from ansible.modules.network.f5.bigip_static_route import ModuleManager
        from ansible.modules.network.f5.bigip_static_route import ArgumentSpec
        from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
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


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            vlan="foo",
            gateway_address="10.10.10.10"
        )
        p = Parameters(args)
        assert p.vlan == '/Common/foo'
        assert p.gateway_address == '10.10.10.10'

    def test_api_parameters(self):
        args = dict(
            tmInterface="foo",
            gw="10.10.10.10"
        )
        p = Parameters(args)
        assert p.vlan == '/Common/foo'
        assert p.gateway_address == '10.10.10.10'

    def test_reject_parameter_types(self):
        # boolean true
        args = dict(reject=True)
        p = Parameters(args)
        assert p.reject is True

        # boolean false
        args = dict(reject=False)
        p = Parameters(args)
        assert p.reject is None

        # string
        args = dict(reject="yes")
        p = Parameters(args)
        assert p.reject is True

        # integer
        args = dict(reject=1)
        p = Parameters(args)
        assert p.reject is True

        # none
        args = dict(reject=None)
        p = Parameters(args)
        assert p.reject is None

    def test_destination_parameter_types(self):
        # ip address
        args = dict(destination="10.10.10.10")
        p = Parameters(args)
        assert p.destination == '10.10.10.10/32'

        # cidr address
        args = dict(destination="10.10.10.10/32")
        p = Parameters(args)
        assert p.destination == '10.10.10.10/32'

        # netmask
        args = dict(destination="10.10.10.10/255.255.255.255")
        p = Parameters(args)
        assert p.destination == '10.10.10.10/32'

    def test_vlan_with_partition(self):
        args = dict(
            vlan="/Common/foo",
            gateway_address="10.10.10.10"
        )
        p = Parameters(args)
        assert p.vlan == '/Common/foo'
        assert p.gateway_address == '10.10.10.10'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_blackhole(self, *args):
        set_module_args(dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            destination='10.10.10.10',
            reject='yes'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            mutually_exclusive=self.spec.mutually_exclusive,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(return_value=False)
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True

    def test_create_route_to_pool(self, *args):
        set_module_args(dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            destination='10.10.10.10',
            pool="test-pool"
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            mutually_exclusive=self.spec.mutually_exclusive,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(return_value=False)
        mm.create_on_device = Mock(return_value=True)
        results = mm.exec_module()

        assert results['changed'] is True
        assert results['pool'] == 'test-pool'

    def test_create_route_to_vlan(self, *args):
        set_module_args(dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            destination='10.10.10.10',
            vlan="test-vlan"
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            mutually_exclusive=self.spec.mutually_exclusive,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(return_value=False)
        mm.create_on_device = Mock(return_value=True)
        results = mm.exec_module()

        assert results['changed'] is True
        assert results['vlan'] == '/Common/test-vlan'

    def test_update_description(self, *args):
        set_module_args(dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            description='foo description'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            mutually_exclusive=self.spec.mutually_exclusive,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        current = Parameters(load_fixture('load_net_route_description.json'))
        mm.exists = Mock(return_value=True)
        mm.update_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        results = mm.exec_module()

        assert results['changed'] is True
        assert results['description'] == 'foo description'

    def test_update_description_idempotent(self, *args):
        set_module_args(dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            description='asdasd'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            mutually_exclusive=self.spec.mutually_exclusive,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        current = Parameters(load_fixture('load_net_route_description.json'))
        mm.exists = Mock(return_value=True)
        mm.update_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)
        results = mm.exec_module()

        # There is no assert for the description, because it should
        # not have changed
        assert results['changed'] is False

    def test_delete(self, *args):
        set_module_args(dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='absent'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            mutually_exclusive=self.spec.mutually_exclusive,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(side_effect=[True, False])
        mm.remove_from_device = Mock(return_value=True)
        results = mm.exec_module()

        assert results['changed'] is True
        assert 'description' not in results

    def test_invalid_unknown_params(self, *args):
        set_module_args(dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            foo="bar"
        ))
        with patch('ansible.module_utils.f5_utils.AnsibleModule.fail_json') as mo:
            mo.return_value = True
            AnsibleF5Client(
                argument_spec=self.spec.argument_spec,
                mutually_exclusive=self.spec.mutually_exclusive,
                supports_check_mode=self.spec.supports_check_mode,
                f5_product_name=self.spec.f5_product_name
            )
            assert mo.call_count == 1
