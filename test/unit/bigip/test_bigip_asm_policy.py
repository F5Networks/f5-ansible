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
from ansible.compat.tests.mock import patch, Mock, DEFAULT, PropertyMock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client

try:
    from library.bigip_asm_policy import Parameters
    from library.bigip_asm_policy import ModuleManager
    from library.bigip_asm_policy import ArgumentSpec
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_asm_policy import Parameters
        from ansible.modules.network.f5.bigip_asm_policy import ModuleManager
        from ansible.modules.network.f5.bigip_asm_policy import ArgumentSpec
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}
policy_path = os.path.join(os.path.dirname(__file__), 'fixtures/extra_files')


def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def load_fixture(name):
    path = os.path.join(fixture_path, name)
    with open(path) as f:
        data = f.read()
    try:
        data = json.loads(data)
    except Exception:
        pass
    return data


class BigIpObj(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.attrs = self.__dict__

    def refresh(self):
        pass

    @property
    def status(self):
        return

    @property
    def active(self):
        return


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='fake_policy',
            state='present',
            file='/var/fake/fake.xml'
        )

        p = Parameters(args)
        assert p.name == 'fake_policy'
        assert p.state == 'present'
        assert p.file == '/var/fake/fake.xml'

    def test_module_parameters_template(self):
        args = dict(
            name='fake_policy',
            state='present',
            template='fake_template_builtin'
        )

        # Override methods to force specific logic in the module to happen
        with patch.object(Parameters, '_template_exists_on_device') as obj:
            obj.return_value = True

        p = Parameters(args)
        assert p.name == 'fake_policy'
        assert p.state == 'present'
        assert p.template == 'fake_template_builtin'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestLocalManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.policy = os.path.join(policy_path, 'fake_policy.xml')
        self.policy_absent = []
        self.policy_present = []
        self.policy_templates = []
        self.templates = load_fixture('list_asm_policy_templates.json')
        self.policies = load_fixture('list_asm_policies_policy_not_present.json')
        self.policies2 = load_fixture('list_asm_policies_policy_present.json')
        self.import_start = BigIpObj(**load_fixture('import_policy_task_started.json'))
        self.apply_start = BigIpObj(**load_fixture('apply_asm_policy_started.json'))
        self.import_from_template_start = BigIpObj(**load_fixture('import_policy_from_template_task_started.json'))
        for item in self.templates:
            self.policy_templates.append(BigIpObj(**item))
        for item in self.policies:
            self.policy_absent.append(BigIpObj(**item))
        for item in self.policies2:
            self.policy_present.append(BigIpObj(**item))

    def test_activate_import_from_file(self, *args):
        set_module_args(dict(
            name='fake_policy',
            file=self.policy,
            state='activate',
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
        with patch.object(BigIpObj, 'status', new_callable=PropertyMock, return_value='COMPLETED'):
            mm = ModuleManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.policies_on_device = Mock(return_value=self.policy_absent)
            mm.import_policy_to_device = Mock(return_value=self.import_start)
            mm.apply_policy_on_device = Mock(return_value=self.apply_start)
            results = mm.exec_module()

        assert results['changed'] is True
        assert results['name'] == 'fake_policy'
        assert results['file'] == self.policy
        assert results['active'] is True

    def test_activate_import_from_template(self, *args):
        set_module_args(dict(
            name='fake_policy',
            template='POLICY_TEMPLATE_SHAREPOINT_2007_HTTP',
            state='activate',
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
        with patch.object(BigIpObj, 'status', new_callable=PropertyMock, return_value='COMPLETED'):
            mm = ModuleManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.policies_on_device = Mock(return_value=self.policy_absent)
            mm.create_policy_from_template_on_device = Mock(return_value=self.import_from_template_start)
            mm.apply_policy_on_device = Mock(return_value=self.apply_start)
            results = mm.exec_module()

        assert results['changed'] is True
        assert results['name'] == 'fake_policy'
        assert results['template'] == 'POLICY_TEMPLATE_SHAREPOINT_2007_HTTP'
        assert results['active'] is True

    def test_activate_create_by_name(self, *args):
        set_module_args(dict(
            name='fake_policy',
            state='activate',
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
        with patch.object(BigIpObj, 'status', new_callable=PropertyMock, return_value='COMPLETED'):
            mm = ModuleManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.policies_on_device = Mock(side_effect=[self.policy_absent, self.policy_present])
            mm.create_policy_on_device = Mock(return_value=True)
            mm.apply_policy_on_device = Mock(return_value=self.apply_start)
            results = mm.exec_module()

        assert results['changed'] is True
        assert results['name'] == 'fake_policy'
        assert results['active'] is True

    def test_activate_policy_exists_inactive(self, *args):
        set_module_args(dict(
            name='fake_policy',
            state='activate',
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
        with patch.object(BigIpObj, 'status', new_callable=PropertyMock, return_value='COMPLETED'):
            mm = ModuleManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.policies_on_device = Mock(return_value=self.policy_present)
            mm.apply_policy_on_device = Mock(return_value=self.apply_start)
            results = mm.exec_module()

        assert results['changed'] is True
        assert results['name'] == 'fake_policy'
        assert results['active'] is True

    def test_activate_policy_exists_active(self, *args):
        set_module_args(dict(
            name='fake_policy',
            state='activate',
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
        with patch.object(BigIpObj, 'active', new_callable=PropertyMock, return_value=True):
            mm = ModuleManager(client)
            mm.exit_json = Mock(return_value=False)
            mm.policies_on_device = Mock(return_value=self.policy_present)
            results = mm.exec_module()

        assert results['changed'] is False
