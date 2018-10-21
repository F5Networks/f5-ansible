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
from ansible.compat.tests.mock import Mock
from ansible.compat.tests.mock import patch
from ansible.module_utils.basic import AnsibleModule

try:
    from library.modules.bigip_ucs_fetch import Parameters
    from library.modules.bigip_ucs_fetch import ModuleManager
    from library.modules.bigip_ucs_fetch import V1Manager
    from library.modules.bigip_ucs_fetch import V2Manager
    from library.modules.bigip_ucs_fetch import ArgumentSpec
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    from test.unit.modules.utils import set_module_args
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_ucs_fetch import Parameters
        from ansible.modules.network.f5.bigip_ucs_fetch import ModuleManager
        from ansible.modules.network.f5.bigip_ucs_fetch import V1Manager
        from ansible.modules.network.f5.bigip_ucs_fetch import V2Manager
        from ansible.modules.network.f5.bigip_ucs_fetch import ArgumentSpec
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
            backup='yes',
            create_on_missing='yes',
            encryption_password='my-password',
            dest='/tmp/foo.ucs',
            force='yes',
            fail_on_missing='no',
            src='remote.ucs',
            password='password',
            server='localhost',
            user='admin'
        )
        p = Parameters(params=args)
        assert p.backup == 'yes'


class TestV1Manager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create(self, *args):
        set_module_args(dict(
            backup='yes',
            create_on_missing='yes',
            dest='/tmp/foo.ucs',
            force='yes',
            fail_on_missing='no',
            src='remote.ucs',
            password='password',
            server='localhost',
            user='admin'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods to force specific logic in the module to happen
        m1 = V1Manager(module=module)
        m1.exists = Mock(return_value=False)
        m1.create_on_device = Mock(return_value=True)
        m1._get_backup_file = Mock(return_value='/tmp/foo.backup')
        m1.download_from_device = Mock(return_value=True)
        m1._set_checksum = Mock(return_value=12345)
        m1._set_md5sum = Mock(return_value=54321)

        mm = ModuleManager(module=module)
        mm.get_manager = Mock(return_value=m1)
        mm.is_version_v1 = Mock(return_value=True)

        p1 = patch('os.path.exists', return_value=True)
        p1.start()
        p2 = patch('os.path.isdir', return_value=False)
        p2.start()

        results = mm.exec_module()

        p1.stop()
        p2.stop()

        assert results['changed'] is True
