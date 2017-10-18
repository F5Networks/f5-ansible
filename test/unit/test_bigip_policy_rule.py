# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import sys

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client

try:
    from library.bigip_policy_rule import Parameters
    from library.bigip_policy_rule import ModuleParameters
    from library.bigip_policy_rule import ApiParameters
    from library.bigip_policy_rule import ModuleManager
    from library.bigip_policy_rule import ArgumentSpec
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_policy_rule import Parameters
        from ansible.modules.network.f5.bigip_policy_rule import ModuleParameters
        from ansible.modules.network.f5.bigip_policy_rule import ApiParameters
        from ansible.modules.network.f5.bigip_policy_rule import ModuleManager
        from ansible.modules.network.f5.bigip_policy_rule import ArgumentSpec
        from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
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


class TestParameters(unittest.TestCase):
    def test_module_parameters_policy(self):
        args = dict(
            policy='Policy - Foo'
        )
        p = ModuleParameters(params=args)
        assert p.policy == 'Policy - Foo'

    def test_module_parameters_actions(self):
        args = dict(
            actions=[
                dict(
                    type='forward',
                    pool='pool-svrs'
                )
            ]
        )
        p = ModuleParameters(params=args)
        assert len(p.actions) == 1

    def test_module_parameters_conditions(self):
        args = dict(
            conditions=[
                dict(
                    type='http_uri',
                    path_starts_with='/ABC'
                )
            ]
        )
        p = ModuleParameters(params=args)
        assert len(p.conditions) == 1

    def test_module_parameters_name(self):
        args = dict(
            name='rule1'
        )
        p = ModuleParameters(params=args)
        assert p.name == 'rule1'

    def test_module_parameters_none_strategy(self):
        args = dict()
        p = ModuleParameters(params=args)
        assert p.strategy is None

    def test_module_parameters_relative_strategy(self):
        args = dict(
            strategy='asdf'
        )
        p = ModuleParameters(params=args)
        assert p.strategy == '/Common/asdf'

    def test_module_parameters_absolute_strategy(self):
        args = dict(
            strategy='/MyPartition/asdf'
        )
        p = ModuleParameters(params=args)
        assert p.strategy == '/MyPartition/asdf'

    def test_api_parameters(self):
        args = load_fixture('load_ltm_policy_draft_rule_http-uri_forward.json')
        p = ApiParameters(params=args)
        assert p.strategy == '/Common/asdf'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestSimpleTrafficPolicyManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_policy_rule(self, *args):
        set_module_args(dict(
            name="Policy-Foo",
            state='present',
            strategy='best',
            password='password',
            server='localhost',
            user='admin'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods in the specific type of manager
        tm = SimpleManager(client)
        tm.exists = Mock(return_value=False)
        tm.create_on_device = Mock(return_value=True)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(client)
        mm.version_is_less_than_12 = Mock(return_value=True)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
