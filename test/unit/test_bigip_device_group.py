#!/usr/bin/python
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
    from library.bigip_device_group import Parameters
    from library.bigip_device_group import ModuleManager
    from library.bigip_device_group import ArgumentSpec
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_device_group import Parameters
        from ansible.modules.network.f5.bigip_device_group import ModuleManager
        from ansible.modules.network.f5.bigip_device_group import ArgumentSpec
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
    def test_module_parameters(self):
        args = dict(
            save_on_auto_sync=True,
            full_sync=False,
            description="my description",
            type="sync-failover",
            auto_sync=True
        )

        p = Parameters(args)
        assert p.save_on_auto_sync is True
        assert p.full_sync is False
        assert p.description == "my description"
        assert p.type == "sync-failover"
        assert p.auto_sync == 'enabled'

    def test_api_parameters(self):
        args = dict(
            asmSync="disabled",
            autoSync="enabled",
            fullLoadOnSync="false",
            incrementalConfigSyncSizeMax=1024,
            networkFailover="disabled",
            saveOnAutoSync="false",
            type="sync-only"
        )

        p = Parameters(args)
        assert p.auto_sync == 'enabled'
        assert p.full_sync is False
        assert p.max_incremental_sync_size == 1024
        assert p.save_on_auto_sync is False
        assert p.type == 'sync-only'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestModuleManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_default_device_group(self, *args):
        set_module_args(
            dict(
                name="foo-group",
                state="present",
                server='localhost',
                user='admin',
                password='password'
            )
        )

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.create_on_device = Mock(return_value=True)
        mm.exists = Mock(return_value=False)

        results = mm.exec_module()
        assert results['changed'] is True

    def test_update_device_group(self, *args):
        set_module_args(
            dict(
                full_sync=True,
                name="foo-group",
                state="present",
                server='localhost',
                user='admin',
                password='password'
            )
        )

        current = Parameters(load_fixture('load_tm_cm_device_group.json'))
        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.update_on_device = Mock(return_value=True)
        mm.exists = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()
        assert results['changed'] is True

    def test_delete_device_group(self, *args):
        set_module_args(
            dict(
                name="foo-group",
                state="absent",
                server='localhost',
                user='admin',
                password='password'
            )
        )

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(side_effect=[True, False])
        mm.remove_from_device = Mock(return_value=True)

        results = mm.exec_module()
        assert results['changed'] is True
