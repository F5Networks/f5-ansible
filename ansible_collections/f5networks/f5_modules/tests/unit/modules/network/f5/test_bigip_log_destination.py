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

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_log_destination import (
    V1ApiParameters, V1ModuleParameters, ModuleManager, V1Manager, ArgumentSpec
)
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock
from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args


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


class TestV1Parameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='foo',
            syslog_settings=dict(
                forward_to='pool1',
                syslog_format='rfc5424'
            ),
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        )
        p = V1ModuleParameters(params=args)
        assert p.name == 'foo'
        assert p.forward_to == '/Common/pool1'
        assert p.syslog_format == 'rfc5424'

    def test_api_parameters(self):
        args = load_fixture('load_sys_log_config_destination_1.json')
        p = V1ApiParameters(params=args)
        assert p.name == 'foo'
        assert p.syslog_format == 'rfc5424'
        assert p.forward_to == '/Common/pool1'


class TestV1Manager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_policy(self, *args):
        set_module_args(dict(
            name="foo",
            type='remote-syslog',
            syslog_settings=dict(
                forward_to='pool1',
            ),
            state='present',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            mutually_exclusive=self.spec.mutually_exclusive
        )

        # Override methods in the specific type of manager
        tm = V1Manager(module=module, params=module.params)
        tm.exists = Mock(return_value=False)
        tm.create_on_device = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
