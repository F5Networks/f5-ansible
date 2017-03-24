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
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    F5ModuleError
)

from library.bigip_user import (
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
    except:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        access = [{'name': 'Common', 'role': 'guest'}]
        args = dict(
            username_credential='someuser',
            password_credential='testpass',
            full_name='Fake Person',
            partition_access=access,
            update_password='always'
        )

        p = Parameters(args)
        assert p.username_credential == 'someuser'
        assert p.password_credential == 'testpass'
        assert p.full_name == 'Fake Person'
        assert p.partition_access == access
        assert p.update_password == 'always'

    def test_api_parameters(self):
        access = [{'name': 'Common', 'role': 'guest'}]
        args = dict(
            name='someuser',
            description='Fake Person',
            password='testpass',
            partitionAccess=access,
            shell='none'
        )

        p = Parameters(args)
        assert p.name == 'someuser'
        assert p.password == 'testpass'
        assert p.full_name == 'Fake Person'
        assert p.partition_access == access
        assert p.shell == 'none'


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_user(self, *args):
        access = [{'name': 'Common', 'role': 'guest'}]
        set_module_args(dict(
            username_credential='someuser',
            password_credential='testpass',
            partition_access=access,
            server='localhost',
            password='password',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(client)
        mm.exit_json = lambda x: False
        mm.create_on_device = lambda: True
        mm.exists = lambda: False

        results = mm.exec_module()

        assert results['changed'] is True

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_user_nopassword_raises(self, *args):
        access = [{'name': 'Common', 'role': 'guest'}]
        set_module_args(dict(
            username_credential='someuser',
            partition_access=access,
            password='password',
            server='localhost',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(client)
        mm.exit_json = lambda x: False
        mm.create_on_device = lambda: True
        mm.exists = lambda: False
        msg = "The 'password_credential' option " \
              "is required when creating a resource."
        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_user_nopartition_access_raises(self, *args):
        set_module_args(dict(
            username_credential='someuser',
            password_credential='testpass',
            password='password',
            server='localhost',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(client)
        mm.exit_json = lambda x: False
        mm.create_on_device = lambda: True
        mm.exists = lambda: False
        msg = "The 'partition_access' option " \
              "is required when creating a resource."
        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_user_shell_not_permitted_raises(self, *args):
        access = [{'name': 'Common', 'role': 'guest'}]
        set_module_args(dict(
            username_credential='someuser',
            password_credential='testpass',
            partition_access=access,
            password='password',
            server='localhost',
            user='admin',
            shell='bash'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(client)
        mm.exit_json = lambda x: False
        mm.create_on_device = lambda: True
        mm.exists = lambda: False
        msg = "Shell access is only available to 'admin' or " \
              "'resource-admin' roles"
        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()
        assert err.value.message == msg

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_update_user_password(self, *args):
        set_module_args(dict(
            username_credential='someuser',
            password_credential='testpass',
            update_password='always',
            password='password',
            server='localhost',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(
            dict(
                shell='tmsh'
            )
        )

        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: False
        mm.update_on_device = lambda: True
        mm.exists = lambda: True
        mm.read_current_from_device = lambda: current

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['password_credential'] == 'testpass'

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_update_user_password_raises(self, *args):
        set_module_args(dict(
            username_credential='someuser',
            password_credential='testpass',
            password='password',
            server='localhost',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(
            dict(
                shell='tmsh'
            )
        )

        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: False
        mm.update_on_device = lambda: True
        mm.exists = lambda: True
        mm.read_current_from_device = lambda: current
        msg = "'Update_password' option must be set to " \
              "'always' to update password_credential"

        with pytest.raises(F5ModuleError) as err:
            mm.exec_module()

        assert err.value.message == msg

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_update_user_shell_to_none(self, *args):
        set_module_args(dict(
            username_credential='someuser',
            password='password',
            server='localhost',
            user='admin',
            shell='none'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(
            dict(
                user='admin',
                shell='tmsh'
            )
        )

        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: False
        mm.update_on_device = lambda: True
        mm.exists = lambda: True
        mm.read_current_from_device = lambda: current

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['shell'] == 'none'

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_update_user_shell_to_none_shell_attribute_missing(self, *args):
        set_module_args(dict(
            username_credential='someuser',
            password='password',
            server='localhost',
            user='admin',
            shell='none'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(
            dict(
                user='admin'
            )
        )

        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: False
        mm.update_on_device = lambda: True
        mm.exists = lambda: True
        mm.read_current_from_device = lambda: current

        msg = "Attribute 'bash' is already set to 'none'" \
              " on target device."
        with pytest.raises(F5ModuleError) as error:
                mm.exec_module()
        assert error.value.message == msg

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_update_user_shell_to_bash(self, *args):
        set_module_args(dict(
            username_credential='someuser',
            password='password',
            server='localhost',
            user='admin',
            shell='bash'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        access = [{'name': 'all', 'role': 'admin'}]
        current = Parameters(
            dict(
                user='admin',
                shell='tmsh',
                partition_access=access
            )
        )

        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: False
        mm.update_on_device = lambda: True
        mm.exists = lambda: True
        mm.read_current_from_device = lambda: current

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['shell'] == 'bash'

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_update_user_shell_to_bash_mutliple_roles(self, *args):
        set_module_args(dict(
            username_credential='someuser',
            password='password',
            server='localhost',
            user='admin',
            shell='bash'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        access = [
            {'name': 'Common', 'role': 'operator'},
            {'name': 'all', 'role': 'guest'}
        ]
        current = Parameters(
            dict(
                user='admin',
                shell='tmsh',
                partition_access=access
            )
        )

        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: False
        mm.update_on_device = lambda: True
        mm.exists = lambda: True
        mm.read_current_from_device = lambda: current

        msg = "Shell access is only available to 'admin' or " \
              "'resource-admin' roles"

        with pytest.raises(F5ModuleError) as error:
            mm.exec_module()
        assert error.value.message == msg
