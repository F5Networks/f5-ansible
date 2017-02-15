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
from library.bigip_snmp import (
    Parameters,
    SnmpManager
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


class TestSnmpParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            agent_status_traps='enabled',
            agent_authentication_traps='enabled',
            device_warning_traps='enabled',
            location='Lunar orbit',
            contact='Alice@foo.org'
        )
        p = Parameters(args)
        self.assertEqual(p.agent_status_traps, 'enabled')
        self.assertEqual(p.agent_authentication_traps, 'enabled')
        self.assertEqual(p.device_warning_traps, 'enabled')
        self.assertEqual(p.location, 'Lunar orbit')
        self.assertEqual(p.contact, 'Alice@foo.org')

    def test_module_parameters_disabled(self):
        args = dict(
            agent_status_traps='disabled',
            agent_authentication_traps='disabled',
            device_warning_traps='disabled',
        )
        p = Parameters(args)
        self.assertEqual(p.agent_status_traps, 'disabled')
        self.assertEqual(p.agent_authentication_traps, 'disabled')
        self.assertEqual(p.device_warning_traps, 'disabled')

    def test_api_parameters(self):
        args = dict(
            agentTrap="enabled",
            authTrap="enabled",
            bigipTraps="enabled",
            sysLocation="Lunar orbit",
            sysContact="Alice@foo.org"
        )
        p = Parameters.from_api(args)
        self.assertEqual(p.agent_status_traps, 'enabled')
        self.assertEqual(p.agent_authentication_traps, 'enabled')
        self.assertEqual(p.device_warning_traps, 'enabled')
        self.assertEqual(p.location, 'Lunar orbit')
        self.assertEqual(p.contact, 'Alice@foo.org')

    def test_api_parameters_disabled(self):
        args = dict(
            agentTrap="disabled",
            authTrap="disabled",
            bigipTraps="disabled",
        )
        p = Parameters.from_api(args)
        self.assertEqual(p.agent_status_traps, 'disabled')
        self.assertEqual(p.agent_authentication_traps, 'disabled')
        self.assertEqual(p.device_warning_traps, 'disabled')


class TestSnmpManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_blackhole(self, foo):
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
        mm = SnmpManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: True

        results = mm.exec_module()

        assert results['changed'] is True
