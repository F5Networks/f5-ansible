# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
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

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_config import (
    Parameters, ModuleManager, ArgumentSpec
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


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            save='yes',
            reset='yes',
            merge_content='asdasd',
            verify='no',
        )
        p = Parameters(params=args)
        assert p.save == 'yes'
        assert p.reset == 'yes'
        assert p.merge_content == 'asdasd'


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_run_single_command(self, *args):
        set_module_args(dict(
            save='yes',
            reset='yes',
            merge_content='asdasd',
            verify='no',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = Mock(return_value=True)
        mm.reset_device = Mock(return_value='reset output')
        mm.upload_to_device = Mock(return_value=True)
        mm.move_on_device = Mock(return_value=True)
        mm.merge_on_device = Mock(return_value='merge output')
        mm.remove_temporary_file = Mock(return_value=True)
        mm.save_on_device = Mock(return_value='save output')

        results = mm.exec_module()

        assert results['changed'] is True
