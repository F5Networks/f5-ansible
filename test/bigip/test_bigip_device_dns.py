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
from library.bigip_device_dns import (
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
            cache='disable',
            forwarders=['12.12.12.12', '13.13.13.13'],
            ip_version=4,
            name_servers=['10.10.10.10', '11.11.11.11'],
            search=['14.14.14.14', '15.15.15.15'],
            server='localhost',
            user='admin',
            password='password'
        )
        p = Parameters(args)
        assert p.cache == 'disable'
        assert p.name_servers == ['10.10.10.10', '11.11.11.11']
        assert p.forwarders == '12.12.12.12 13.13.13.13'
        assert p.search == ['14.14.14.14', '15.15.15.15']

        # BIG-IP considers "ipv4" to be an empty value
        assert p.ip_version == ''

        print(p.api_params())

    def test_ipv6_parameter(self):
        args = dict(
            ip_version=6
        )
        p = Parameters(args)
        assert p.ip_version == 'options inet6'


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_blackhole(self, mgmt):
        set_module_args(dict(
            agent_status_traps='enabled',
            agent_authentication_traps='enabled',
            device_warning_traps='enabled',
            location='Lunar orbit',
            contact='Alice@foo.org'
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
