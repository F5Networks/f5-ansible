# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import os
import time

try:
    from f5.bigip import ManagementRoot
    from icontrol.exceptions import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

try:
    from library.module_utils.network.f5.common import F5BaseClient
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.icontrol import iControlRestSession
except ImportError:
    from ansible.module_utils.network.f5.common import F5BaseClient
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.icontrol import iControlRestSession


class F5Client(F5BaseClient):
    @property
    def api(self):
        exc = None
        if self._client:
            return self._client
        for x in range(0, 60):
            try:
                server = self.params['provider']['server'] or self.params['server']
                user = self.params['provider']['user'] or self.params['user']
                password = self.params['provider']['password'] or self.params['password']
                server_port = self.params['provider']['server_port'] or self.params['server_port'] or 443
                validate_certs = self.params['provider']['validate_certs'] or self.params['validate_certs']

                result = ManagementRoot(
                    server,
                    user,
                    password,
                    port=server_port,
                    verify=validate_certs,
                    token='tmos'
                )
                self._client = result
                return self._client
            except Exception as ex:
                exc = ex
                time.sleep(1)
        error = 'Unable to connect to {0} on port {1}.'.format(server, server_port)
        if exc is not None:
            error += ' The reported error was "{0}".'.format(str(exc))
        raise F5ModuleError(error)


class F5RestClient(F5BaseClient):
    def __init__(self, *args, **kwargs):
        super(F5RestClient, self).__init__(*args, **kwargs)
        self.provider = self.merge_provider_params()

    @property
    def api(self):
        exc = None
        if self._client:
            return self._client

        for x in range(0, 10):
            try:
                url = "https://{0}:{1}/mgmt/shared/authn/login".format(
                    self.provider['server'], self.provider['server_port']
                )
                payload = {
                    'username': self.provider['user'],
                    'password': self.provider['password'],
                    'loginProviderName': self.provider['auth_provider']
                }
                session = iControlRestSession()
                session.verify = self.params['validate_certs']
                response = session.post(url, json=payload)

                if response.status_code not in [200]:
                    raise F5ModuleError('{0} Unexpected Error: {1} for uri: {2}\nText: {3}'.format(
                        response.status_code, response.reason, response.url, response._content
                    ))

                session.headers['X-F5-Auth-Token'] = response.json()['token']['token']
                self._client = session
                return self._client
            except Exception as ex:
                exc = ex
                time.sleep(1)
        error = 'Unable to connect to {0} on port {1}.'.format(
            self.params['server'], self.params['server_port']
        )
        if exc is not None:
            error += ' The reported error was "{0}".'.format(str(exc))
        raise F5ModuleError(error)

    def merge_provider_params(self):
        result = dict()

        provider = self.params.get('provider', {})

        if provider.get('server', None):
            result['server'] = provider.get('server', None)
        elif self.params.get('server', None):
            result['server'] = self.params.get('server', None)
        elif os.environ.get('F5_SERVER', None):
            result['server'] = os.environ.get('F5_SERVER', None)

        if provider.get('server_port', None):
            result['server_port'] = provider.get('server_port', None)
        elif self.params.get('server_port', None):
            result['server_port'] = self.params.get('server_port', None)
        elif os.environ.get('F5_SERVER_PORT', None):
            result['server_port'] = os.environ.get('F5_SERVER_PORT', None)
        else:
            result['server_port'] = 443

        if provider.get('validate_certs', None):
            result['validate_certs'] = provider.get('validate_certs', None)
        elif self.params.get('validate_certs', None):
            result['validate_certs'] = self.params.get('validate_certs', None)
        elif os.environ.get('F5_VALIDATE_CERTS', None):
            result['validate_certs'] = os.environ.get('F5_VALIDATE_CERTS', None)
        else:
            result['validate_certs'] = True

        if provider.get('auth_provider', None):
            result['auth_provider'] = provider.get('auth_provider', None)
        elif self.params.get('auth_provider', None):
            result['auth_provider'] = self.params.get('auth_provider', None)
        else:
            result['auth_provider'] = 'tmos'

        if provider.get('user', None):
            result['user'] = provider.get('user', None)
        elif self.params.get('user', None):
            result['user'] = self.params.get('user', None)
        elif os.environ.get('F5_USER', None):
            result['user'] = os.environ.get('F5_USER', None)
        elif os.environ.get('ANSIBLE_NET_USERNAME', None):
            result['user'] = os.environ.get('ANSIBLE_NET_USERNAME', None)
        else:
            result['user'] = True

        if provider.get('password', None):
            result['password'] = provider.get('password', None)
        elif self.params.get('user', None):
            result['password'] = self.params.get('password', None)
        elif os.environ.get('F5_PASSWORD', None):
            result['password'] = os.environ.get('F5_PASSWORD', None)
        elif os.environ.get('ANSIBLE_NET_PASSWORD', None):
            result['password'] = os.environ.get('ANSIBLE_NET_PASSWORD', None)
        else:
            result['password'] = True

        return result
