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

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ssl_key_cert import (
    ApiParameters, ModuleParameters, ModuleManager, ArgumentSpec
)
from ansible_collections.f5networks.f5_modules.plugins.module_utils.icontrol import TransactionContextManager
from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import F5ModuleError
from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import (
    Mock, patch, MagicMock
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
    def test_module_parameters_key(self):
        key_content = load_fixture('create_insecure_key1.key')
        args = dict(
            key_content=key_content,
            key_name="cert1",
            partition="Common",
            state="present",
            password='password',
            server='localhost',
            user='admin'
        )
        p = ModuleParameters(params=args)
        assert p.key_name == 'cert1'
        assert p.key_filename == 'cert1.key'
        assert '-----BEGIN RSA PRIVATE KEY-----' in p.key_content
        assert '-----END RSA PRIVATE KEY-----' in p.key_content
        assert p.key_checksum == '91bdddcf0077e2bb2a0258aae2ae3117be392e83'
        assert p.state == 'present'

    def test_module_parameters_cert(self):
        cert_content = load_fixture('create_insecure_cert1.crt')
        args = dict(
            cert_content=cert_content,
            cert_name="cert1",
            partition="Common",
            state="present",
        )
        p = ModuleParameters(params=args)
        assert p.cert_name == 'cert1'
        assert p.cert_filename == 'cert1.crt'
        assert 'Signature Algorithm' in p.cert_content
        assert '-----BEGIN CERTIFICATE-----' in p.cert_content
        assert '-----END CERTIFICATE-----' in p.cert_content
        assert p.cert_checksum == '1e55aa57ee166a380e756b5aa4a835c5849490fe'
        assert p.state == 'present'

    def test_module_issuer_cert_key(self):
        args = dict(
            issuer_cert='foo',
            partition="Common",
        )
        p = ModuleParameters(params=args)
        assert p.issuer_cert == '/Common/foo.crt'

    def test_api_issuer_cert_key(self):
        args = load_fixture('load_sys_file_ssl_cert_with_issuer_cert.json')
        p = ApiParameters(params=args)
        assert p.issuer_cert == '/Common/intermediate.crt'


class TestModuleManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ssl_key_cert.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_ssl_key_cert.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p2.stop()
        self.p3.stop()

    def test_import_key_no_key_passphrase(self, *args):
        set_module_args(dict(
            key_name='foo',
            key_content=load_fixture('cert1.key'),
            state='present',
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

        # Override methods in the specific type of manager
        cm = ModuleManager(module=module)
        cm.exists = Mock(side_effect=[False, True])
        cm.create_on_device = Mock(return_value=True)
        cm.remove_uploaded_file_from_device = Mock(return_value=True)

        results = cm.exec_module()

        assert results['changed'] is True


class TestTransactionContextManager(unittest.TestCase):
    """Tests for TransactionContextManager error handling.

    These tests verify that meaningful error messages are raised
    instead of bare Exception when transactions fail.
    """

    def _make_mock_client(self):
        client = MagicMock()
        client.provider = {
            'server': 'localhost',
            'server_port': 443
        }
        return client

    def _make_response(self, status, body=None):
        resp = MagicMock()
        resp.status = status
        if body is not None:
            resp.json.return_value = body
            resp.content = json.dumps(body)
        else:
            resp.json.side_effect = ValueError('No JSON')
            resp.content = ''
        return resp

    def test_enter_failure_with_message(self):
        """Test that __enter__ raises F5ModuleError with BIG-IP message on failure."""
        client = self._make_mock_client()
        error_body = {'code': 400, 'message': 'Authorization failed'}
        client.api.post.return_value = self._make_response(400, error_body)

        tcm = TransactionContextManager(client)

        with self.assertRaises(F5ModuleError) as cm:
            tcm.__enter__()

        self.assertIn('Failed to create transaction', str(cm.exception))
        self.assertIn('Authorization failed', str(cm.exception))

    def test_enter_failure_without_message(self):
        """Test that __enter__ raises F5ModuleError with status on non-JSON failure."""
        client = self._make_mock_client()
        client.api.post.return_value = self._make_response(500)

        tcm = TransactionContextManager(client)

        with self.assertRaises(F5ModuleError) as cm:
            tcm.__enter__()

        self.assertIn('Failed to create transaction', str(cm.exception))
        self.assertIn('500', str(cm.exception))

    def test_exit_failure_with_message(self):
        """Test that __exit__ raises F5ModuleError with BIG-IP message on commit failure.

        This is the exact scenario from GitHub issue #2504 where updating
        an existing cert/key pair fails during transaction commit because
        of a cert/key mismatch validation error.
        """
        client = self._make_mock_client()

        # Simulate successful transaction creation
        create_resp = self._make_response(200, {'transId': 12345})
        client.api.post.return_value = create_resp
        client.api.request.headers = {}

        # Simulate failed transaction commit with BIG-IP error message
        error_body = {
            'code': 400,
            'message': "01070317:3: profile /Common/test-profile's key(/Common/test-cert) "
                       "and certificate(/Common/test-cert) do not match."
        }
        client.api.patch.return_value = self._make_response(400, error_body)

        tcm = TransactionContextManager(client)
        tcm.__enter__()

        with self.assertRaises(F5ModuleError) as cm:
            tcm.__exit__(None, None, None)

        self.assertIn('Failed to commit transaction 12345', str(cm.exception))
        self.assertIn('do not match', str(cm.exception))

    def test_exit_failure_without_message(self):
        """Test that __exit__ raises F5ModuleError with status on non-JSON commit failure."""
        client = self._make_mock_client()

        # Simulate successful transaction creation
        create_resp = self._make_response(200, {'transId': 12345})
        client.api.post.return_value = create_resp
        client.api.request.headers = {}

        # Simulate failed commit with no JSON body
        client.api.patch.return_value = self._make_response(500)

        tcm = TransactionContextManager(client)
        tcm.__enter__()

        with self.assertRaises(F5ModuleError) as cm:
            tcm.__exit__(None, None, None)

        self.assertIn('Failed to commit transaction 12345', str(cm.exception))
        self.assertIn('500', str(cm.exception))

    def test_exit_skips_commit_on_exception(self):
        """Test that __exit__ does not commit when an exception occurred in the with block."""
        client = self._make_mock_client()

        # Simulate successful transaction creation
        create_resp = self._make_response(200, {'transId': 12345})
        client.api.post.return_value = create_resp
        client.api.request.headers = {}

        tcm = TransactionContextManager(client)
        tcm.__enter__()

        # Simulate __exit__ called with an exception (exc_tb is not None)
        tcm.__exit__(ValueError, ValueError('test error'), Mock())

        # patch should NOT have been called since there was an exception
        client.api.patch.assert_not_called()

    def test_exit_success(self):
        """Test that __exit__ succeeds when commit returns 200."""
        client = self._make_mock_client()

        # Simulate successful transaction creation
        create_resp = self._make_response(200, {'transId': 12345})
        client.api.post.return_value = create_resp
        client.api.request.headers = {}

        # Simulate successful commit
        client.api.patch.return_value = self._make_response(200, {'state': 'COMPLETED'})

        tcm = TransactionContextManager(client)
        tcm.__enter__()

        # Should not raise
        tcm.__exit__(None, None, None)
