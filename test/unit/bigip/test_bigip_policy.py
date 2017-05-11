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

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    AnsibleF5Client
)

try:
    from library.bigip_policy import (
        Parameters,
        ModuleManager,
        ArgumentSpec
    )
except ImportError:
    from ansible.modules.network.f5.bigip_policy import (
        Parameters,
        ModuleManager,
        ArgumentSpec
    )

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
    def test_module_parameters_none_strategy(self):
        args = dict(
            name='foo',
            description='asdf asdf asdf',
            password='password',
            server='localhost',
            user='admin'
        )
        p = Parameters(args)
        assert p.name == 'foo'
        assert p.description == 'asdf asdf asdf'
        assert p.strategy is None

    def test_module_parameters_with_strategy_no_partition(self):
        args = dict(
            name='foo',
            description='asdf asdf asdf',
            password='password',
            server='localhost',
            strategy='foo',
            user='admin',
            partition='Common'
        )
        p = Parameters(args)
        assert p.name == 'foo'
        assert p.description == 'asdf asdf asdf'
        assert p.strategy == '/Common/foo'

    def test_module_parameters_with_strategy_partition(self):
        args = dict(
            name='foo',
            description='asdf asdf asdf',
            password='password',
            server='localhost',
            strategy='/Common/foo',
            user='admin',
            partition='Common'
        )
        p = Parameters(args)
        assert p.name == 'foo'
        assert p.description == 'asdf asdf asdf'
        assert p.strategy == '/Common/foo'

    def test_module_parameters_with_strategy_different_partition(self):
        args = dict(
            name='foo',
            description='asdf asdf asdf',
            password='password',
            server='localhost',
            strategy='/Foo/bar',
            user='admin',
            partition='Common'
        )
        p = Parameters(args)
        assert p.name == 'foo'
        assert p.description == 'asdf asdf asdf'
        assert p.strategy == '/Foo/bar'

    def test_api_parameters(self):
        args = dict(
            name='foo',
            description='asdf asdf asdf',
            strategy='/Common/asdf'
        )
        p = Parameters(args)
        assert p.name == 'foo'
        assert p.description == 'asdf asdf asdf'
        assert p.strategy == '/Common/asdf'

#@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
#       return_value=True)
#class TestManager(unittest.TestCase):
#
#    def setUp(self):
#        self.spec = ArgumentSpec()
#
#    def test_create_trap(self, *args):
#        set_module_args(dict(
#            name='foo',
#            snmp_version='1',
#            community='public',
#            destination='10.10.10.10',
#            port=1000,
#            network='other',
#            password='password',
#            server='localhost',
#            user='admin'
#        ))
#
#        client = AnsibleF5Client(
#            argument_spec=self.spec.argument_spec,
#            supports_check_mode=self.spec.supports_check_mode,
#            f5_product_name=self.spec.f5_product_name
#        )
#        mm = ModuleManager(client)
#
#        # Override methods to force specific logic in the module to happen
#        mm.exit_json = lambda x: False
#        mm.create_on_device = lambda: True
#        mm.exists = lambda: False
#
#        results = mm.exec_module()
#
#        assert results['changed'] is True
