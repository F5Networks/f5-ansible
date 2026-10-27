# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import time

from .common import (
    F5BaseClient, F5ModuleError
)
from .constants import (
    LOGIN, BASE_HEADERS
)
from .icontrol import iControlRestSession


class F5RestClient(F5BaseClient):
    def __init__(self, *args, **kwargs):
        self.task_timeout = kwargs.pop('session_timeout', None)
        self.default_timeout = kwargs.pop('default_timeout', None)
        super(F5RestClient, self).__init__(*args, **kwargs)
        self.provider = self.merge_provider_params()
        self.session_timeout, self.token_timeout = self.resolve_timeouts()
        self.headers = BASE_HEADERS
        self.retries = 0

    def resolve_timeouts(self):
        explicit = self.task_timeout if self.task_timeout is not None else self.default_timeout
        provider_timeout = self.provider.get('timeout')
        session_timeout = explicit if explicit is not None else (provider_timeout or 120)
        candidates = [t for t in (explicit, provider_timeout) if t is not None]
        token_timeout = max(candidates) if candidates else None
        return session_timeout, token_timeout

    @property
    def api(self):
        if self._client:
            return self._client
        session, err = self.connect_via_token_auth()
        if err or session is None:
            session, err = self.connect_via_basic_auth()
            if err or session is None:
                raise F5ModuleError(err)
        self._client = session
        return session

    def connect_via_token_auth(self):
        url = "https://{0}:{1}{2}".format(
            self.provider['server'], self.provider['server_port'], LOGIN
        )
        payload = {
            'username': self.provider['user'],
            'password': self.provider['password'],
            'loginProviderName': self.provider['auth_provider'] or 'tmos'
        }
        session = iControlRestSession(
            validate_certs=self.provider['validate_certs'],
            timeout=self.session_timeout
        )

        response = session.post(
            url,
            json=payload,
            headers=self.headers
        )

        if response.status not in [200]:
            if b'Configuration Utility restarting...' in response.content and self.retries < 3:
                time.sleep(30)
                self.retries += 1
                return self.connect_via_token_auth()
            else:
                self.retries = 0
                return None, response.content

        self.retries = 0
        session.request.headers['X-F5-Auth-Token'] = response.json()['token']['token']
        session.on_unauthorized = self.reauthenticate
        if self.token_timeout is not None:
            token_value = response.json()['token']['token']
            self.modify_token_timeout(session, token_value, self.token_timeout)
        return session, None

    def reauthenticate(self, session):
        new_session, err = self.connect_via_token_auth()
        if err or new_session is None:
            return False
        # Pop so the temporary session's destructor does not log out the token handed over.
        session.request.headers['X-F5-Auth-Token'] = new_session.request.headers.pop('X-F5-Auth-Token')
        return True

    def connect_via_basic_auth(self):
        url = "https://{0}:{1}/mgmt/tm/sys".format(
            self.provider['server'], self.provider['server_port']
        )
        session = iControlRestSession(
            url_username=self.provider['user'],
            url_password=self.provider['password'],
            validate_certs=self.provider['validate_certs'],
            timeout=self.session_timeout
        )

        response = session.get(
            url,
            headers=self.headers
        )

        if response.status not in [200]:
            if b'Configuration Utility restarting...' in response.content and self.retries < 3:
                time.sleep(30)
                self.retries += 1
                return self.connect_via_basic_auth()
            else:
                self.retries = 0
                return None, response.content
        self.retries = 0
        return session, None

    def modify_token_timeout(self, client_session, token_value, token_timeout):
        url = "https://{0}:{1}/mgmt/shared/authz/tokens/{2}".format(
            self.provider['server'], self.provider['server_port'], token_value
        )
        payload = {
            'timeout': token_timeout
        }
        response = client_session.patch(
            url,
            json=payload
        )
        if response.status not in [200]:
            raise F5ModuleError(response.content)
        return None
