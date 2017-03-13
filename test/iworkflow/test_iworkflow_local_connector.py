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
from ansible.compat.tests.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    AnsibleF5Client
)
from library.iworkflow_local_connector import (
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

    def test_module_parameters_template(self):
        args = dict(
            name="MyCloud",
        )
        p = Parameters(args)
        assert p.name == 'MyCloud'

    def test_api_parameters_variables(self):
        args = dict(
            name="MyCloud"
        )
        p = Parameters(args)
        assert p.name == 'MyCloud'


#class TestManager(unittest.TestCase):
#
#    def setUp(self):
#        self.spec = ArgumentSpec()
#
#    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
#           return_value=True)
#    def test_create_service(self, *args):
#        parameters = load_fixture('create_iapp_service_parameters_f5_http.json')
#        set_module_args(dict(
#            name='foo',
#            template='f5.http',
#            parameters=parameters,
#            state='present',
#            password='passsword',
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
#        mm.exit_json = lambda x: True
#        mm.exists = lambda: False
#        mm.create_on_device = lambda: True
#
#        results = mm.exec_module()
#        assert results['changed'] is True
