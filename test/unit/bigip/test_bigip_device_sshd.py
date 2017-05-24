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

import sys

if sys.version_info < (2, 7):
    from nose.plugins.skip import SkipTest
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

import os
import json

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client

try:
    from library.bigip_device_sshd import Parameters
    from library.bigip_device_sshd import ModuleManager
    from library.bigip_device_sshd import ArgumentSpec
except ImportError:
    from ansible.modules.network.f5.bigip_device_sshd import Parameters
    from ansible.modules.network.f5.bigip_device_sshd import ModuleManager
    from ansible.modules.network.f5.bigip_device_sshd import ArgumentSpec

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
    def test_module_parameters(self):
        args = dict(
            allow=['all'],
            banner='enabled',
            banner_text='asdf',
            inactivity_timeout='100',
            log_level='debug',
            login='enabled',
            port=1010,
            server='localhost',
            user='admin',
            password='password'
        )
        p = Parameters(args)
        assert p.allow == ['all']
        assert p.banner == 'enabled'
        assert p.banner_text == 'asdf'
        assert p.inactivity_timeout == 100
        assert p.log_level == 'debug'
        assert p.login == 'enabled'
        assert p.port == 1010


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_update_settings(self, *args):
        set_module_args(dict(
            allow=['all'],
            banner='enabled',
            banner_text='asdf',
            inactivity_timeout='100',
            log_level='debug',
            login='enabled',
            port=1010,
            server='localhost',
            user='admin',
            password='password'
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(
            dict(
                allow=['172.27.1.1']
            )
        )

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.update_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['allow'] == ['all']
