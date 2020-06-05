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
from .icontrol import iControlRestSession


class F5RestClient(F5BaseClient):
    def __init__(self, *args, **kwargs):
        super(F5RestClient, self).__init__(*args, **kwargs)
        self.provider = self.merge_provider_params()
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.retries = 0

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
        url = "https://{0}:{1}/mgmt/shared/authn/login".format(
            self.provider['server'], self.provider['server_port']
        )
        payload = {
            'username': self.provider['user'],
            'password': self.provider['password'],
            'loginProviderName': self.provider['auth_provider'] or 'tmos'
        }
        session = iControlRestSession(
            validate_certs=self.provider['validate_certs']
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
        return session, None

    def connect_via_basic_auth(self):
        url = "https://{0}:{1}/mgmt/tm/sys".format(
            self.provider['server'], self.provider['server_port']
        )
        session = iControlRestSession(
            url_username=self.provider['user'],
            url_password=self.provider['password'],
            validate_certs=self.provider['validate_certs'],
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
