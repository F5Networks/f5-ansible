# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, F5 Networks Inc.
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

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ltm_global import (
    ApiParameters, ModuleParameters, ModuleManager, ArgumentSpec
)
from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import F5ModuleError
from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import (
    Mock, patch
)


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
            connection=dict(
                default_vs_syn_challenge_tresh=123456,
                global_syn_challenge_tresh=0
            )
        )
        p = ModuleParameters(params=args)
        assert p.default_vs_syn_challenge_tresh == '123456'
        assert p.global_syn_challenge_tresh == 'infinite'

    def test_invalid_vs_syn_value(self):
        args = dict(
            connection=dict(
                default_vs_syn_challenge_tresh=999999999
            )
        )
        p = ModuleParameters(params=args)
        with self.assertRaises(F5ModuleError) as res:
            assert p.default_vs_syn_challenge_tresh is None

        assert str(res.exception) == 'Specified number is out of valid range, correct range is ' \
                                     'between 128 and 1048576, or 0 for infinite.'

    def test_invalid_global_syn_value(self):
        args = dict(
            connection=dict(
                global_syn_challenge_tresh=999999999
            )
        )
        p = ModuleParameters(params=args)
        with self.assertRaises(F5ModuleError) as res:
            assert p.global_syn_challenge_tresh is None

        assert str(res.exception) == 'Specified number is out of valid range, correct range is ' \
                                     'between 2048 and 4194304, or 0 for infinite.'


class TestManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ltm_global.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ltm_global.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p2.stop()
        self.p3.stop()

    def test_update_parameters(self, *args):
        set_module_args(dict(
            connection=dict(
                default_vs_syn_challenge_tresh=123456,
                global_syn_challenge_tresh=1244
            ),
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        current = ApiParameters(params=load_fixture('load_ltm_global_settings_general.json'))
        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.update_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['default_vs_syn_challenge_tresh'] == 123456
        assert results['global_syn_challenge_tresh'] == 1244
