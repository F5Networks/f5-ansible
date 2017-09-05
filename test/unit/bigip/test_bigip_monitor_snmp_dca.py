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
# GNU General Public Liccense for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import F5ModuleError

try:
    from library.bigip_monitor_snmp_dca import Parameters
    from library.bigip_monitor_snmp_dca import ModuleManager
    from library.bigip_monitor_snmp_dca import ArgumentSpec
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_monitor_snmp_dca import Parameters
        from ansible.modules.network.f5.bigip_monitor_snmp_dca import ModuleManager
        from ansible.modules.network.f5.bigip_monitor_snmp_dca import ArgumentSpec
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = { }


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
            agent_type='UCD',
            community='public',
            cpu_coefficient='1.5',
            cpu_threshold='80',
            parent='/Common/snmp_dca',
            disk_coefficient='2.0',
            disk_threshold='90',
            interval=10,
            memory_coefficient='1.0',
            memory_threshold='70',
            time_until_up=0,
            timeout=30,
            version='v1'
        )

        p = Parameters(args)
        assert p.agent_type == 'UCD'
        assert p.community == 'public'
        assert p.cpu_coefficient == 1.5
        assert p.cpu_threshold == 80
        assert p.parent == '/Common/snmp_dca'
        assert p.disk_coefficient == 2.0
        assert p.disk_threshold == 90
        assert p.interval == 10
        assert p.memory_coefficient == 1.0
        assert p.memory_threshold == 70
        assert p.time_until_up == 0
        assert p.timeout == 30
        assert p.version == 'v1'

    def test_api_parameters(self):
        args = dict(
            agentType='UCD',
            community='public',
            cpuCoefficient='1.5',
            cpuThreshold='80',
            defaultsFrom='/Common/snmp_dca',
            diskCoefficient='2.0',
            diskThreshold='90',
            interval=10,
            memoryCoefficient='1.0',
            memoryThreshold='70',
            timeUntilUp=0,
            timeout=30,
            apiRawValues={
                "userDefined asdasd": "{ foo }",
                "userDefined bar": "tim rupp",
                "user-defined baz-": "nia",
                "userDefined userDefined": "23234"
            },
            version='v1'
        )

        p = Parameters(args)
        assert p.agent_type == 'UCD'
        assert p.community == 'public'
        assert p.cpu_coefficient == 1.5
        assert p.cpu_threshold == 80
        assert p.parent == '/Common/snmp_dca'
        assert p.disk_coefficient == 2.0
        assert p.disk_threshold == 90
        assert p.interval == 10
        assert p.memory_coefficient == 1.0
        assert p.memory_threshold == 70
        assert p.time_until_up == 0
        assert p.timeout == 30
        assert p.version == 'v1'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create(self, *args):
        set_module_args(dict(
            name='foo',
            agent_type='UCD',
            community='public',
            cpu_coefficient='1.5',
            cpu_threshold='80',
            parent='/Common/snmp_dca',
            disk_coefficient='2.0',
            disk_threshold='90',
            memory_coefficient='1.0',
            memory_threshold='70',
            version='v1',
            interval=20,
            timeout=30,
            time_until_up=60,
            server='localhost',
            password='password',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(client)
        mm.exists = Mock(side_effect=[False, True])
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
