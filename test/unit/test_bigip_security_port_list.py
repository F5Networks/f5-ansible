# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
from ansible.compat.tests.mock import Mock
from ansible.compat.tests.mock import patch
from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import F5ModuleError

try:
    from library.bigip_security_port_list import ApiParameters
    from library.bigip_security_port_list import ModuleParameters
    from library.bigip_security_port_list import ModuleManager
    from library.bigip_security_port_list import ArgumentSpec
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
    from test.unit.modules.utils import set_module_args
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_security_port_list import Parameters
        from ansible.modules.network.f5.bigip_security_port_list import ApiParameters
        from ansible.modules.network.f5.bigip_security_port_list import ModuleParameters
        from ansible.modules.network.f5.bigip_security_port_list import ModuleManager
        from ansible.modules.network.f5.bigip_security_port_list import ArgumentSpec
        from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
        from units.modules.utils import set_module_args
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


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
            name='foo',
            description='this is a description',
            ports=[1,2,3,4],
            port_ranges='10-20',
            port_lists=['/Common/foo', 'foo']
        )

        p = ModuleParameters(args)
        assert p.name == 'foo'
        assert p.description == 'this is a description'
        assert len(p.ports) == 4
        assert len(p.port_ranges) == 3
        assert len(p.port_lists) == 2

    def test_api_parameters(self):
        args = load_fixture('load_security_port_list_1.json')

        p = ApiParameters(args)
        assert len(p.ports) == 4
        assert len(p.port_ranges) == 3
        assert len(p.port_lists) == 1
        assert sorted(p.ports) == [1, 2, 3, 4]
        assert sorted(p.port_ranges) == ['10-20','30-40','50-60']
        assert p.port_lists[0] == '/Common/_sys_self_allow_tcp_defaults'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):
    def test_create(self, *args):
        raise Exception('You must write a creation test')
