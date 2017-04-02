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
from library.iworkflow_service_template import (
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


class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestParameters(unittest.TestCase):

    def setUp(self):
        self.loaded_connectors = []
        connectors_json = load_fixture('load_connectors.json')
        for item in connectors_json:
            self.loaded_connectors.append(Namespace(**item))

    def test_module_parameters_tables_general(self):
        fixture = load_fixture('create_iworkflow_service_template_appsvcs_integration.json')
        params = dict(
            parameters=fixture
        )
        p = Parameters(params)

        assert 'tables' in p._values
        assert len(p.tables) == 9

    def test_module_parameters_tables_first_val(self):
        fixture = load_fixture('create_iworkflow_service_template_appsvcs_integration.json')
        params = dict(
            parameters=fixture
        )
        p = Parameters(params)

        assert 'columns' in p.tables[0]
        assert len(p.tables[0]['columns']) == 1
        assert p.tables[0]['columns'][0]['name'] == 'CIDRRange'

        assert 'name' in p.tables[0]
        assert p.tables[0]['name'] == 'feature__easyL4FirewallBlacklist'

        assert 'description' in p.tables[0]
        assert p.tables[0]['description'] == 'Security: Firewall: Static Blacklisted Addresses (CIDR Format)'

        assert 'rows' in p.tables[0]
        assert len(p.tables[0]['rows']) == 1
        assert len(p.tables[0]['rows'][0]) == 1

    def test_module_parameters_variables_general(self):
        fixture = load_fixture('create_iworkflow_service_template_appsvcs_integration.json')
        params = dict(
            parameters=fixture
        )
        p = Parameters(params)

        assert 'vars' in p._values
        assert len(p.vars) == 61

    def test_module_parameters_variables_first_val(self):
        fixture = load_fixture('create_iworkflow_service_template_appsvcs_integration.json')
        params = dict(
            parameters=fixture
        )
        p = Parameters(params)

        # Assert one configuration value
        assert 'name' in p.vars[0]
        assert 'description' in p.vars[0]
        assert 'displayName' in p.vars[0]
        assert 'isRequired' in p.vars[0]
        assert 'provider' in p.vars[0]
        assert p.vars[0]['name'] == 'extensions__Field1'
        assert p.vars[0]['description'] == 'Extensions: Field 1'
        assert p.vars[0]['displayName'] == 'Field1'
        assert p.vars[0]['isRequired'] == 'False'
        assert p.vars[0]['provider'] == ''

    def test_module_parameters_variables_second_val(self):
        fixture = load_fixture('create_iworkflow_service_template_appsvcs_integration.json')
        params = dict(
            parameters=fixture
        )
        p = Parameters(params)

        # Assert a second configuration value
        assert 'name' in p.vars[1]
        assert 'description' in p.vars[1]
        assert 'displayName' in p.vars[1]
        assert 'isRequired' in p.vars[1]
        assert 'provider' in p.vars[1]
        assert p.vars[1]['name'] == 'extensions__Field2'
        assert p.vars[1]['description'] == 'Extensions: Field 2'
        assert p.vars[1]['displayName'] == 'Field2'
        assert p.vars[1]['isRequired'] == 'False'
        assert p.vars[1]['provider'] == ''

    def test_module_parameters_connector(self):
        params = dict(
            connector='foo'
        )

        with patch.object(Parameters, '_get_connector_collection') as mo:
            mo.return_value = self.loaded_connectors
            p = Parameters()
            p.update(params)
            assert p.connector == 'https://localhost/mgmt/cm/cloud/connectors/local/212301e6-6d01-4509-bfe3-8e372e792fb0'

    def test_module_parameters_base_template(self):
        params = dict(
            base_template='foo'
        )
        expected = dict(
            link="https://localhost/mgmt/cm/cloud/templates/iapp/foo"
        )
        p = Parameters()
        p.update(params)
        assert p.base_template == expected

    def test_module_parameters_properties(self):
        params = dict(
            connector='foo'
        )

        with patch.object(Parameters, '_get_connector_collection') as mo:
            mo.return_value = self.loaded_connectors
            p = Parameters()
            p.update(params)
            assert len(p.properties) == 1
            assert 'id' in p.properties[0]
            assert 'isRequired' in p.properties[0]
            assert 'provider' in p.properties[0]
            assert p.properties[0]['id'] == 'cloudConnectorReference'
            assert p.properties[0]['isRequired'] == True
            assert p.properties[0]['provider'] == 'https://localhost/mgmt/cm/cloud/connectors/local/212301e6-6d01-4509-bfe3-8e372e792fb0'


#    def test_api_parameters_variables(self):
#        args = dict(
#            variables=[
#                dict(
#                    name="client__http_compression",
#                    encrypted="no",
#                    value="/#create_new#"
#                )
#            ]
#        )
#        p = Parameters(args)
#        assert p.variables[0]['name'] == 'client__http_compression'
#
#    def test_api_parameters_tables(self):
#        args = dict(
#            tables=[
#                {
#                    "name": "pool__members",
#                    "columnNames": [
#                        "addr",
#                        "port",
#                        "connection_limit"
#                    ],
#                    "rows": [
#                        {
#                            "row": [
#                                "12.12.12.12",
#                                "80",
#                                "0"
#                            ]
#                        },
#                        {
#                            "row": [
#                                "13.13.13.13",
#                                "443",
#                                10
#                            ]
#                        }
#                    ]
#                }
#            ]
#        )
#        p = Parameters(args)
#        assert p.tables[0]['name'] == 'pool__members'
#        assert p.tables[0]['columnNames'] == ['addr', 'port', 'connection_limit']
#        assert len(p.tables[0]['rows']) == 2
#        assert 'row' in p.tables[0]['rows'][0]
#        assert 'row' in p.tables[0]['rows'][1]
#        assert p.tables[0]['rows'][0]['row'] == ['12.12.12.12', '80', '0']
#        assert p.tables[0]['rows'][1]['row'] == ['13.13.13.13', '443', '10']


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
#
#    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
#           return_value=True)
#    def test_update_agent_status_traps(self, *args):
#        parameters = load_fixture('update_iapp_service_parameters_f5_http.json')
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
#        # Configure the parameters that would be returned by querying the
#        # remote device
#        parameters = load_fixture('create_iapp_service_parameters_f5_http.json')
#        current = Parameters(parameters)
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
#        mm.exists = lambda: True
#        mm.update_on_device = lambda: True
#        mm.read_current_from_device = lambda: current
#
#        results = mm.exec_module()
#        assert results['changed'] is True
#
