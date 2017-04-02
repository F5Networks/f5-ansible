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
from library.iworkflow_license_pool import (
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
        args = dict(
            name='lic-pool',
            base_key='00000-11111-22222-33333-4444444',
            state='present',
            accept_eula='yes'
        )
        p = Parameters(args)
        assert p.name == 'lic-pool'
        assert p.base_key == '00000-11111-22222-33333-4444444'
        assert p.state == 'present'
        assert p.accept_eula == 'yes'

    def test_module_parameters_empty_name(self):
        args = dict(
            name="",
        )
        p = Parameters(args)
        with pytest.raises(F5ModuleError) as e:
            assert p.name
        assert 'You must specify a name for this module' in str(e)

    def test_api_parameters(self):
        args = load_fixture('load_license_pool.json')
        p = Parameters(args)
        assert p.name == 'asdf'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_license_pool(self, *args):
        set_module_args(dict(
            name='lic-pool',
            base_key='00000-11111-22222-33333-4444444',
            state='present',
            accept_eula='yes',
            password='passsword',
            server='localhost',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: True
        mm.exists = lambda: False
        mm.create_on_device = lambda: True

        results = mm.exec_module()
        assert results['changed'] is True
