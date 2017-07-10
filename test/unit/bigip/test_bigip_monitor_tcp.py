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
    from library.bigip_monitor_tcp import Parameters
    from library.bigip_monitor_tcp import ModuleManager
    from library.bigip_monitor_tcp import ArgumentSpec
    from library.bigip_monitor_tcp import TcpManager
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_monitor_tcp import Parameters
        from ansible.modules.network.f5.bigip_monitor_tcp import ModuleManager
        from ansible.modules.network.f5.bigip_monitor_tcp import ArgumentSpec
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

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


'''
  name:
    description:
      - Monitor name.
    required: True
    aliases:
      - monitor
  parent:
    description:
      - The parent template of this monitor template. Once this value has
        been set, it cannot be changed. By default, this value is the C(tcp)
        parent on the C(Common) partition.
    default: "/Common/tcp"
  send:
    description:
      - The send string for the monitor call.
  receive:
    description:
      - The receive string for the monitor call.
  ip:
    description:
      - IP address part of the ip/port definition. If this parameter is not
        provided when creating a new monitor, then the default value will be
        '*'.
  type:
    description:
      - The template type of this monitor template.
      - Deprecated in 2.4. Use one of the C(bigip_monitor_tcp_echo) or
        C(migip_monitor_tcp_half_open) instead.
    default: 'TTYPE_TCP'
    choices:
      - TTYPE_TCP
      - TTYPE_TCP_ECHO
      - TTYPE_TCP_HALF_OPEN
  port:
    description:
      - Port address part op the ipport definition. If this parameter is not
        provided when creating a new monitor, then the default value will be
        '0'.
  interval:
    description:
      - The interval specifying how frequently the monitor instance of this
        template will run. If this parameter is not provided when creating
        a new monitor, then the default value will be 5.
  timeout:
    description:
      - The number of seconds in which the node or service must respond to
        the monitor request. If the target responds within the set time
        period, it is considered up. If the target does not respond within
        the set time period, it is considered down. You can change this
        number to any number you want, however, it should be 3 times the
        interval number of seconds plus 1 second. If this parameter is not
        provided when creating a new monitor, then the default value will be 16.
  time_until_up:
    description:
      - Specifies the amount of time in seconds after the first successful
        response before a node will be marked up. A value of 0 will cause a
        node to be marked up immediately after a valid response is received
        from the node. If this parameter is not provided when creating
        a new monitor, then the default value will be 0.
'''


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='foo',
            parent='parent',
            send='this is a send string',
            receive='this is a receive string',
            ip='10.10.10.10',
            type='TTYPE_TCP',
            port=80,
            interval=20,
            timeout=30,
            time_until_up=60,
            partition='Common'
        )

        p = Parameters(args)
        assert p.name == 'foo'
        assert p.parent == '/Common/parent'
        assert p.send == 'this is a send string'
        assert p.receive == 'this is a receive string'
        assert p.ip == '10.10.10.10'
        assert p.type == 'tcp'
        assert p.port == 80
        assert p.destination == '10.10.10.10:80'
        assert p.interval == 20
        assert p.timeout == 30
        assert p.time_until_up == 60

    def test_api_parameters(self):
        args = dict(
            name='foo',
            defaultsFrom='/Common/parent',
            send='this is a send string',
            recv='this is a receive string',
            destination='10.10.10.10:80',
            interval=20,
            timeout=30,
            timeUntilUp=60
        )

        p = Parameters(args)
        assert p.name == 'foo'
        assert p.parent == '/Common/parent'
        assert p.send == 'this is a send string'
        assert p.receive == 'this is a receive string'
        assert p.ip == '10.10.10.10'
        assert p.type == 'tcp'
        assert p.port == 80
        assert p.destination == '10.10.10.10:80'
        assert p.interval == 20
        assert p.timeout == 30
        assert p.time_until_up == 60


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_monitor(self, *args):
        set_module_args(dict(
            name='foo',
            parent='parent',
            send='this is a send string',
            receive='this is a receive string',
            ip='10.10.10.10',
            port=80,
            interval=20,
            timeout=30,
            time_until_up=60,
            partition='Common',
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
        tm = TcpManager(client)
        tm.exists = Mock(side_effect=[False, True])
        tm.create_on_device = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['parent'] == '/Common/parent'

    def test_create_monitor_idempotent(self, *args):
        set_module_args(dict(
            name='foo',
            parent='tcp',
            send='this is a send string',
            receive='this is a receive string',
            ip='10.10.10.10',
            port=80,
            interval=20,
            timeout=30,
            time_until_up=60,
            partition='Common',
            server='localhost',
            password='password',
            user='admin'
        ))

        current = Parameters(load_fixture('load_ltm_monitor_tcp.json'))
        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods in the specific type of manager
        tm = TcpManager(client)
        tm.exists = Mock(return_value=True)
        tm.read_current_from_device = Mock(return_value=current)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is False
