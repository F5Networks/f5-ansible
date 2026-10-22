# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import importlib
import os

import pytest

from ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip import F5RestClient
from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import F5ModuleError
from ansible_collections.f5networks.f5_modules.plugins.module_utils.icontrol import iControlRestSession
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import MagicMock, Mock, patch


@pytest.fixture(autouse=True)
def clean_env():
    with patch.dict(os.environ):
        os.environ.pop('F5_TIMEOUT', None)
        yield


def make_client(provider_timeout=None, **kwargs):
    provider = dict(server='localhost', server_port=443, user='admin', password='password', validate_certs=False, timeout=provider_timeout)
    return F5RestClient(provider=provider, **kwargs)


def make_result(status, body=b'{}'):
    result = Mock()
    result.getcode.return_value = status
    result.read.return_value = body
    result.geturl.return_value = 'https://localhost/mgmt/tm/sys'
    result.getheaders.return_value = []
    return result


class TestTimeoutResolution:
    def test_session_timeout_overrides_default_and_provider(self):
        client = make_client(provider_timeout=60, session_timeout=900, default_timeout=300)
        assert client.session_timeout == 900
        assert client.token_timeout == 900

    def test_default_timeout_overrides_provider_for_session(self):
        client = make_client(provider_timeout=60, default_timeout=300)
        assert client.session_timeout == 300
        assert client.token_timeout == 300

    def test_longer_provider_timeout_sets_token_lifetime(self):
        client = make_client(provider_timeout=600, default_timeout=300)
        assert client.session_timeout == 300
        assert client.token_timeout == 600

    def test_shorter_session_timeout_keeps_longer_provider_token_lifetime(self):
        client = make_client(provider_timeout=600, session_timeout=100)
        assert client.session_timeout == 100
        assert client.token_timeout == 600

    def test_provider_timeout_used_without_task_or_default(self):
        client = make_client(provider_timeout=60)
        assert client.session_timeout == 60
        assert client.token_timeout == 60

    def test_env_timeout_used_without_task_or_default(self):
        os.environ['F5_TIMEOUT'] = '45'
        client = make_client()
        assert client.session_timeout == 45
        assert client.token_timeout == 45

    def test_no_timeout_uses_120_and_no_token_timeout(self):
        client = make_client()
        assert client.session_timeout == 120
        assert client.token_timeout is None

    def test_plain_timeout_kwarg_is_not_a_task_timeout(self):
        client = make_client(timeout=900)
        assert client.session_timeout == 120
        assert client.token_timeout is None


class TestUnauthorizedRetry:
    def test_401_reauthenticates_and_retries_once(self):
        session = iControlRestSession()
        session.request = Mock(headers={})
        session.request.open.side_effect = [make_result(401), make_result(200)]
        session.on_unauthorized = Mock(return_value=True)
        response = session.get('https://localhost/mgmt/tm/sys')
        assert response.status == 200
        assert session.on_unauthorized.call_count == 1
        assert session.request.open.call_count == 2

    def test_401_returned_when_reauthentication_fails(self):
        session = iControlRestSession()
        session.request = Mock(headers={})
        session.request.open.return_value = make_result(401)
        session.on_unauthorized = Mock(return_value=False)
        response = session.get('https://localhost/mgmt/tm/sys')
        assert response.status == 401
        assert session.request.open.call_count == 1

    def test_401_returned_without_hook(self):
        session = iControlRestSession()
        session.request = Mock(headers={})
        session.request.open.return_value = make_result(401)
        response = session.get('https://localhost/mgmt/tm/sys')
        assert response.status == 401
        assert session.request.open.call_count == 1

    def test_retry_resends_json_body(self):
        session = iControlRestSession()
        session.request = Mock(headers={})
        session.request.open.side_effect = [make_result(401), make_result(200)]
        session.on_unauthorized = Mock(return_value=True)
        session.patch('https://localhost/mgmt/tm/sys', json={'a': 1})
        first, second = session.request.open.call_args_list
        assert first[1]['data'] == second[1]['data']

    def test_reauthenticate_copies_new_token(self):
        client = make_client(provider_timeout=60)
        old = MagicMock()
        old.request.headers = {'X-F5-Auth-Token': 'old'}
        new = MagicMock()
        new.request.headers = {'X-F5-Auth-Token': 'new'}
        with patch.object(client, 'connect_via_token_auth', return_value=(new, None)):
            assert client.reauthenticate(old) is True
        assert old.request.headers['X-F5-Auth-Token'] == 'new'

    def test_reauthenticate_returns_false_when_login_fails(self):
        client = make_client(provider_timeout=60)
        with patch.object(client, 'connect_via_token_auth', return_value=(None, b'denied')):
            assert client.reauthenticate(MagicMock()) is False

    def test_token_login_wires_reauthenticate_hook(self):
        client = make_client(provider_timeout=60)
        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip.iControlRestSession') as session_cls:
            session = session_cls.return_value
            session.post.return_value = Mock(status=200, json=Mock(return_value={'token': {'token': 'abc'}}))
            session.patch.return_value = Mock(status=200)
            client.connect_via_token_auth()
        assert session.on_unauthorized == client.reauthenticate


class TestTimeoutPropagation:
    def test_module_default_reaches_http_session(self):
        client = make_client(provider_timeout=60, default_timeout=300)
        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip.iControlRestSession') as session_cls:
            session_cls.return_value.get.return_value = Mock(status=200)
            client.connect_via_basic_auth()
        assert session_cls.call_args[1]['timeout'] == 300

    def test_token_patch_uses_longer_of_default_and_provider(self):
        client = make_client(provider_timeout=600, default_timeout=300)
        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip.iControlRestSession') as session_cls:
            session = session_cls.return_value
            session.post.return_value = Mock(status=200, json=Mock(return_value={'token': {'token': 'abc'}}))
            session.patch.return_value = Mock(status=200)
            client.connect_via_token_auth()
        assert session.patch.call_args[1]['json']['timeout'] == 600

    def test_provider_timeout_beats_env(self):
        os.environ['F5_TIMEOUT'] = '600'
        client = make_client(provider_timeout=60)
        assert client.session_timeout == 60
        assert client.token_timeout == 60

    def test_invalid_env_timeout_raises(self):
        os.environ['F5_TIMEOUT'] = 'abc'
        with pytest.raises(F5ModuleError):
            make_client()


class TestUnauthorizedEndToEnd:
    def test_401_relogin_retries_with_new_token(self):
        client = make_client(provider_timeout=60)
        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.icontrol.Request.open') as open_mock:
            open_mock.side_effect = [
                make_result(200, b'{"token": {"token": "old"}}'),
                make_result(200),
                make_result(401),
                make_result(200, b'{"token": {"token": "new"}}'),
                make_result(200),
                make_result(200),
            ]
            session, err = client.connect_via_token_auth()
            response = session.get('https://localhost/mgmt/tm/sys')
            token = session.request.headers['X-F5-Auth-Token']
            session.request.headers.clear()
        assert response.status == 200
        assert token == 'new'
        assert open_mock.call_count == 6


class TestSessionTimeoutArgument:
    @pytest.mark.parametrize('module_name', ['bigip_pool', 'bigip_wait', 'bigip_command', 'bigip_ucs_fetch'])
    def test_argument_spec_declares_session_timeout(self, module_name):
        module = importlib.import_module('ansible_collections.f5networks.f5_modules.plugins.modules.' + module_name)
        assert module.ArgumentSpec().argument_spec['session_timeout'] == dict(type='int')
