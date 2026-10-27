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

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ucs_fetch import (
    Parameters, ModuleParameters, ModuleManager, V1Manager, ArgumentSpec, get_rest_client
)
from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import F5ModuleError
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import MagicMock, Mock, patch
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
            backup='yes',
            create_on_missing='yes',
            encryption_password='my-password',
            dest='/tmp/foo.ucs',
            force='yes',
            fail_on_missing='no',
            src='remote.ucs',
        )
        p = Parameters(params=args)
        assert p.backup == 'yes'

    def test_async_timeout_accepts_upper_bound_of_3600(self):
        p = ModuleParameters(params=dict(async_timeout=3600))
        delay, period = p.async_timeout
        assert delay == 36
        assert period == 100

    def test_async_timeout_rejects_values_above_3600(self):
        p = ModuleParameters(params=dict(async_timeout=3601))
        with pytest.raises(F5ModuleError) as ex:
            p.async_timeout
        assert 'Timeout value must be between 150 and 3600 seconds.' in str(ex.value)

    def test_timeout_accepts_custom_value(self):
        p = ModuleParameters(params=dict(timeout=600))
        assert p._values['timeout'] == 600


class TestV1Manager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ucs_fetch.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ucs_fetch.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p2.stop()
        self.p3.stop()

    def test_create(self, *args):
        set_module_args(dict(
            backup='yes',
            create_on_missing='yes',
            dest='/tmp/foo.ucs',
            force='yes',
            fail_on_missing='no',
            src='remote.ucs',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            add_file_common_args=self.spec.add_file_common_args
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


class TestGetRestClient(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ)
        self.env.start()
        os.environ.pop('F5_TIMEOUT', None)

    def tearDown(self):
        self.env.stop()

    def build_module(self, **kwargs):
        spec = ArgumentSpec()
        set_module_args(kwargs)
        return AnsibleModule(
            argument_spec=spec.argument_spec,
            supports_check_mode=spec.supports_check_mode,
            add_file_common_args=spec.add_file_common_args
        )

    def provider(self, **kwargs):
        provider = dict(server='localhost', password='password', user='admin')
        provider.update(kwargs)
        return provider

    def test_task_timeout_takes_precedence_over_provider(self):
        module = self.build_module(provider=self.provider(timeout=60), timeout=900)
        assert get_rest_client(module).session_timeout == 900

    def test_provider_timeout_ignored_when_task_unset(self):
        module = self.build_module(provider=self.provider(timeout=60))
        assert get_rest_client(module).session_timeout == 300

    def test_default_300_when_neither_set(self):
        module = self.build_module(provider=self.provider())
        assert get_rest_client(module).session_timeout == 300

    def test_env_timeout_ignored_when_task_unset(self):
        os.environ['F5_TIMEOUT'] = '600'
        module = self.build_module(provider=self.provider())
        assert get_rest_client(module).session_timeout == 300

    def test_task_timeout_takes_precedence_over_env(self):
        os.environ['F5_TIMEOUT'] = '600'
        module = self.build_module(provider=self.provider(), timeout=900)
        assert get_rest_client(module).session_timeout == 900

    def test_timeout_is_passed_to_http_session(self):
        module = self.build_module(provider=self.provider(), timeout=900)
        client = get_rest_client(module)
        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip.iControlRestSession') as session_cls:
            session_cls.return_value.get.return_value = Mock(status=200)
            client.connect_via_basic_auth()
        assert session_cls.call_args[1]['timeout'] == 900

    def test_token_lifetime_matches_task_timeout(self):
        module = self.build_module(provider=self.provider(timeout=60), timeout=900)
        client = get_rest_client(module)
        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip.iControlRestSession') as session_cls:
            session = session_cls.return_value
            session.request = MagicMock()
            session.post.return_value = Mock(status=200, json=Mock(return_value={'token': {'token': 'abc'}}))
            session.patch.return_value = Mock(status=200)
            client.connect_via_token_auth()
        assert session.patch.call_args[1]['json']['timeout'] == 900

    def test_token_lifetime_defaults_to_300_when_task_unset(self):
        module = self.build_module(provider=self.provider(timeout=60))
        client = get_rest_client(module)
        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip.iControlRestSession') as session_cls:
            session = session_cls.return_value
            session.post.return_value = Mock(status=200, json=Mock(return_value={'token': {'token': 'abc'}}))
            session.patch.return_value = Mock(status=200)
            client.connect_via_token_auth()
        assert session.patch.call_args[1]['json']['timeout'] == 300

    def test_session_timeout_takes_precedence_over_module_timeout(self):
        module = self.build_module(provider=self.provider(), timeout=600, session_timeout=900)
        assert get_rest_client(module).session_timeout == 900

    def test_session_timeout_used_when_module_timeout_unset(self):
        module = self.build_module(provider=self.provider(), session_timeout=900)
        assert get_rest_client(module).session_timeout == 900

    def test_session_timeout_takes_precedence_over_provider(self):
        module = self.build_module(provider=self.provider(timeout=60), session_timeout=900)
        assert get_rest_client(module).session_timeout == 900

    def test_token_lifetime_is_longer_of_session_timeout_and_provider(self):
        module = self.build_module(provider=self.provider(timeout=600), session_timeout=100)
        client = get_rest_client(module)
        assert client.session_timeout == 100
        assert client.token_timeout == 600
