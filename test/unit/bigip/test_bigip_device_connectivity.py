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

# from ansible.modules.network.f5.bigip_device_connectivity import (
from library.bigip_device_connectivity import (
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
            multicast_port='1010',
            multicast_address='10.10.10.10',
            multicast_interface='eth0',
            failover_multicast=True,
            unicast_failover=[
                dict(
                    address='20.20.20.20',
                    port='1234'
                )
            ],
            mirror_primary_address='1.2.3.4',
            mirror_secondary_address='5.6.7.8',
            config_sync_ip='4.3.2.1',
            state='present',
            server='localhost',
            user='admin',
            password='password'
        )
        p = Parameters(args)
        assert p.multicast_port == 1010
        assert p.multicast_address == '10.10.10.10'
        assert p.multicast_interface == 'eth0'
        assert p.failover_multicast is True
        assert p.mirror_primary_address == '1.2.3.4'
        assert p.mirror_secondary_address == '5.6.7.8'
        assert p.config_sync_ip == '4.3.2.1'
        assert len(p.unicast_failover) == 1
        assert 'effectiveIp' in p.unicast_failover[0]
        assert 'effectivePort' in p.unicast_failover[0]
        assert 'port' in p.unicast_failover[0]
        assert 'ip' in p.unicast_failover[0]
        assert p.unicast_failover[0]['effectiveIp'] == '20.20.20.20'
        assert p.unicast_failover[0]['ip'] == '20.20.20.20'
        assert p.unicast_failover[0]['port'] == 1234
        assert p.unicast_failover[0]['effectivePort'] == 1234

    def test_api_parameters(self):
        params = load_fixture('load_tm_cm_device.json')
        p = Parameters(params)
        assert p.multicast_port == 62960
        assert p.multicast_address == '224.0.0.245'
        assert p.multicast_interface == 'eth0'
        assert p.mirror_primary_address == '10.2.2.2'
        assert p.mirror_secondary_address == '10.2.3.2'
        assert p.config_sync_ip == '10.2.2.2'
        assert len(p.unicast_failover) == 2
        assert 'effectiveIp' in p.unicast_failover[0]
        assert 'effectivePort' in p.unicast_failover[0]
        assert 'port' in p.unicast_failover[0]
        assert 'ip' in p.unicast_failover[0]
        assert p.unicast_failover[0]['effectiveIp'] == '10.0.2.15'
        assert p.unicast_failover[0]['ip'] == '10.0.2.15'
        assert p.unicast_failover[0]['port'] == 1026
        assert p.unicast_failover[0]['effectivePort'] == 1026
