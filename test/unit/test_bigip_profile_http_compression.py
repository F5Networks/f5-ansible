# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
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
from ansible.module_utils.basic import AnsibleModule

try:
    from library.modules.bigip_profile_http_compression import ApiParameters
    from library.modules.bigip_profile_http_compression import ModuleParameters
    from library.modules.bigip_profile_http_compression import ModuleManager
    from library.modules.bigip_profile_http_compression import ArgumentSpec
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    from test.unit.modules.utils import set_module_args
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_profile_http_compression import ApiParameters
        from ansible.modules.network.f5.bigip_profile_http_compression import ModuleParameters
        from ansible.modules.network.f5.bigip_profile_http_compression import ModuleManager
        from ansible.modules.network.f5.bigip_profile_http_compression import ArgumentSpec
        from ansible.module_utils.network.f5.common import F5ModuleError
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
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
            parent='bar',
            description='description1',
            buffer_size=1024,
            gzip_memory_level=64,
            gzip_level=2,
            gzip_window_size=128
        )

        p = ModuleParameters(params=args)
        assert p.name == 'foo'
        assert p.parent == '/Common/bar'
        assert p.description == 'description1'
        assert p.buffer_size == 1024
        assert p.gzip_memory_level == 64
        assert p.gzip_level == 2
        assert p.gzip_window_size == 128

    def test_api_parameters(self):
        p = ApiParameters(params=load_fixture('load_ltm_profile_http_compression_1.json'))
        assert p.description == 'my profile'
        assert p.buffer_size == 4096
        assert p.gzip_memory_level == 8
        assert p.gzip_level == 1
        assert p.gzip_window_size == 16


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create(self, *args):
        # Configure the arguments that would be sent to the Ansible module
        set_module_args(dict(
            name='foo',
            parent='bar',
            description='description1',
            buffer_size=1024,
            gzip_memory_level=64,
            gzip_level=2,
            gzip_window_size=128,
            password='password',
            server='localhost',
            user='admin'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(return_value=False)
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
