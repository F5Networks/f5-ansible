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
from library.bigip_iapp_service import (
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
    def setUp(self):
        args = dict(
            name='foo',
            template='f5.http',
            parameters=dict(
                variables=[
                    {'afm__policy': '/#do_not_use#'},
                    {'afm__dos_security_profile': '/#do_not_use#'},
                    {'asm__use_asm': '/#do_not_use#'},
                    {'client__http_compression': '/#do_not_use#'},
                    {'client__standard_caching_without_wa': '/#do_not_use#'},
                    {'client__tcp_wan_opt': '/#create_new#'},
                    {'monitor__monitor': '/#create_new#'},
                    {'monitor__frequency': '30'},
                    {'monitor__uri': '/my/path'},
                    {'monitor__response': ''},
                    {'net__client_mode': 'wan'},
                    {'net__server_mode': 'lan'},
                    {'net__vlan_mode': 'all'},
                    {'pool__addr': '10.10.10.10'},
                    {'pool__http': '/#create_new#'},
                    {'pool__mask': ''},
                    {'pool__persist': '/#cookie#'},
                    {'pool__lb_method': 'least-connections-member'},
                    {'pool__pool_to_use': '/#create_new#'},
                    {'pool__port_secure': '443'},
                    {'pool__redirect_port': '80'},
                    {'pool__redirect_to_https': 'yes'},
                    {'pool__xff': 'yes'},
                    {'server__oneconnect': '/#create_new#'},
                    {'server__tcp_lan_opt': '/#create_new#'},
                    {'ssl__cert': '/Common/default.crt'},
                    {'ssl__client_ssl_profile': '/#create_new#'},
                    {'ssl__key': '/Common/default.key'},
                    {'ssl__mode': 'client_ssl'},
                    {'ssl__use_chain_cert': '/#do_not_use#'},
                    {'ssl_encryption_questions__advanced': 'yes'},
                    {'stats__analytics': '/#do_not_use#'},
                    {'stats__request_logging': '/#do_not_use#'}
                ],
                tables=[
                    {''}
                ]
            )
        )
        p = Parameters(args)
        self.p1 = p

    def test_module_parameters(self):
        # check that all the provided variables have a correctly
        # interpreted name and value
        for variable in self.p1.variables:
            assert 'name' in variable
            assert 'value' in variable

        assert self.p1.variables[0]['name'] == 'afm__policy'
        assert self.p1.variables[1]['name'] == 'afm__dos_security_profile'
        assert self.p1.variables[2]['name'] == 'asm__use_asm'
        assert self.p1.variables[3]['name'] == 'client__http_compression'
        assert self.p1.variables[4]['name'] == 'client__standard_caching_without_wa'
        assert self.p1.variables[5]['name'] == 'client__tcp_wan_opt'
        assert self.p1.variables[6]['name'] == 'monitor__monitor'
        assert self.p1.variables[7]['name'] == 'monitor__frequency'
        assert self.p1.variables[8]['name'] == 'monitor__uri'
        assert self.p1.variables[9]['name'] == 'monitor__response'
        assert self.p1.variables[10]['name'] == 'net__client_mode'
        assert self.p1.variables[11]['name'] == 'net__server_mode'
        assert self.p1.variables[12]['name'] == 'net__vlan_mode'
        assert self.p1.variables[13]['name'] == 'pool__addr'
        assert self.p1.variables[14]['name'] == 'pool__http'


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_blackhole(self, mgmt):
        set_module_args(dict(
            name='foo',
            template='f5.http',
            parameters_src='enabled',
            state='present'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: True

        results = mm.exec_module()

        assert results['changed'] is True
