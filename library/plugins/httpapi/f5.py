#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2019, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
author: Wojciech Wypior <w.wypior@f5.com>
httpapi : f5
short_description: HttpApi Plugin for F5 devices
description:
  - This HttpApi plugin provides methods to connect to F5
    devices over a HTTP(S)-based api.
version_added: "2.10"
"""
import re
from ansible.module_utils.basic import to_text
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.errors import AnsibleConnectionFailure

try:
    import json
except ImportError:
    import simplejson as json

BASE_HEADERS = {'Content-Type': 'application/json'}
TMOS = '/mgmt/shared/authn/login'


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        super(HttpApi, self).__init__(connection)
        self.connection = connection
        self.last_url = None

    def login(self, username, password, url=TMOS, provider='tmos'):
        payload = {
            'username': username,
            'password': password,
            'loginProviderName': provider
        }

        response_data = self.send_request(url, method='POST', data=payload, headers=BASE_HEADERS)

        try:
            self.connection._auth = {'X-F5-Auth-Token': response_data['contents']['token']['token']}
        except KeyError:
            self.connection._auth = None

    def logout(self):
        if not self.connection._auth:
            return
        token = self.connection._auth.get('X-F5-Auth-Token', None)
        logout_uri = '/mgmt/shared/authz/tokens/{0}'.format(token)
        self.send_request(logout_uri, method='DELETE')

    def handle_httperror(self, exc):
        err_5xx = r'^5\d{2}$'
        # We raise AnsibleConnectionFailure without passing to the module, as 50x type errors indicate a problem
        # with BigIP. If we need to handle 50x upstream for say modules that loop and reconnect after performing
        # operation on device i.e. software install we will remove this and do the handling in the module.
        # If not this should fix Github issue #1237, without having us to rewrite all of the modules exists method.

        handled_error = re.search(err_5xx, str(exc.code))
        if handled_error:
            raise AnsibleConnectionFailure('Could not connect to {0}: {1}'.format(self.last_url, exc.reason))
        return False

    def send_request(self, url, method=None, **kwargs):
        body = kwargs.pop('data', None)
        data = json.dumps(body) if body else None

        try:
            self._display_request(method=method)
            self.last_url = self.connection._url + url
            response, response_data = self.connection.send(url, data, method=method, **kwargs)

            response_value = self._get_response_value(response_data)
            return dict(code=response.getcode(), contents=self._response_to_json(response_value))

        except HTTPError as e:
            return dict(code=e.code, contents=json.loads(e.read()))

    def _display_request(self, method):
        self.connection.queue_message('vvvv', 'F5 API Call: %s %s' % (method, self.connection._url))

    def _get_response_value(self, response_data):
        return to_text(response_data.getvalue())

    def _response_to_json(self, response_text):
        try:
            return json.loads(response_text) if response_text else {}
        # JSONDecodeError only available on Python 3.5+
        except ValueError:
            raise ConnectionError('Invalid JSON response: %s' % response_text)

    def delete(self, url, **kwargs):
        return self.send_request(url, method='DELETE', **kwargs)

    def get(self, url, **kwargs):
        return self.send_request(url, method='GET', **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.send_request(url, method='PATCH', data=data, headers=BASE_HEADERS, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.send_request(url, method='POST', data=data, headers=BASE_HEADERS, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.send_request(url, method='PUT', data=data, headers=BASE_HEADERS, **kwargs)
