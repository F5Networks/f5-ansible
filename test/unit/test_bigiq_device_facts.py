# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
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
from ansible.compat.tests.mock import Mock
from ansible.module_utils.basic import AnsibleModule

try:
    from library.modules.bigiq_device_facts import Parameters
    from library.modules.bigiq_device_facts import SystemInfoFactManager
    from library.modules.bigiq_device_facts import ModuleManager
    from library.modules.bigiq_device_facts import ArgumentSpec
    from library.module_utils.network.f5.common import F5ModuleError
    from test.unit.modules.utils import set_module_args
except ImportError:
    try:
        from ansible.modules.network.f5.bigiq_device_facts import Parameters
        from ansible.modules.network.f5.bigiq_device_facts import SystemInfoFactManager
        from ansible.modules.network.f5.bigiq_device_facts import ModuleManager
        from ansible.modules.network.f5.bigiq_device_facts import ArgumentSpec
        from ansible.module_utils.network.f5.common import F5ModuleError
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
            gather_subset=['system-info'],
        )
        p = Parameters(params=args)
        assert p.gather_subset == ['system-info']


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_get_facts(self, *args):
        set_module_args(dict(
            gather_subset=['system-info'],
            password='password',
            server='localhost',
            user='admin'
        ))

        fixture1 = load_fixture('load_shared_system_setup_1.json')

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        tm = SystemInfoFactManager(module=module)
        tm.read_collection_from_device = Mock(return_value=fixture1)

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['changed'] is True
        assert 'system_info' in results
