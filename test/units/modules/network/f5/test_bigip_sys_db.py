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

try:
    from library.modules.bigip_sys_db import Parameters
    from library.modules.bigip_sys_db import ModuleManager
    from library.modules.bigip_sys_db import ArgumentSpec

    # In Ansible 2.8, Ansible changed import paths.
    from test.units.compat import unittest
    from test.units.compat.mock import Mock
    from test.units.compat.mock import patch

    from test.units.modules.utils import set_module_args
except ImportError:
    from ansible.modules.network.f5.bigip_sys_db import Parameters
    from ansible.modules.network.f5.bigip_sys_db import ModuleManager
    from ansible.modules.network.f5.bigip_sys_db import ArgumentSpec

    # Ansible 2.8 imports
    from units.compat import unittest
    from units.compat.mock import Mock
    from units.compat.mock import patch

    from units.modules.utils import set_module_args


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
            key='foo',
            value='bar',
            password='password',
            server='localhost',
            user='admin'
        )
        p = Parameters(params=args)
        assert p.key == 'foo'
        assert p.value == 'bar'

    def test_api_parameters(self):
        args = dict(
            key='foo',
            value='bar',
            password='password',
            server='localhost',
            defaultValue='baz',
            user='admin'

        )
        p = Parameters(params=args)
        assert p.key == 'foo'
        assert p.value == 'bar'


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_blackhole(self, *args):
        set_module_args(dict(
            key='provision.cpu.afm',
            value='1',
            password='admin',
            server='localhost',
            user='admin',
            state='present'
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(
            dict(
                kind="tm:sys:db:dbstate",
                name="provision.cpu.afm",
                fullPath="provision.cpu.afm",
                generation=1,
                selfLink="https://localhost/mgmt/tm/sys/db/provision.cpu.afm?ver=11.6.1",
                defaultValue="0",
                scfConfig="false",
                value="0",
                valueRange="integer min:0 max:100"
            )
        )

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(return_value=False)
        mm.read_current_from_device = Mock(return_value=current)
        mm.update_on_device = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
