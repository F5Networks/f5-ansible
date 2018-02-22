#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible.module_utils.urls import open_url
from ansible.module_utils.parsing.convert_bool import BOOLEANS
from six import iteritems

try:
    import json
except ImportError:
    import simplejson as json

try:
    from library.module_utils.network.f5.common import F5ModuleError
except ImportError:
    from ansible.module_utils.network.f5.common import F5ModuleError


"""An F5 REST API URI handler.

Use this module to make calls to an F5 REST server. It will handle:

#. Authentication tokens
#. Exception generation -- Errors generate :class:`F5ModuleError` exceptions.

The means by which you should use it are,

```
mgmt = iControlRestSession(server='192.168.1.1', username='admin', password='secret')
>>> iCRS.get('/mgmt/tm/ltm/nat/~Common~VALIDNAME')

Available functions:

- iCRS.{get, post, put, delete, patch}: requests.Session.VERB wrappers
"""


class iControlRestSession(object):
    """Represents a session that communicates with a BigIP.

    Instantiate one of these when you want to communicate with an F5 REST
    Server, it will handle F5-specific authentication.

    Pass an existing authentication token to the ``token`` argument to re-use
    that token for authentication. Otherwise, token authentication is handled
    automatically for you.

    On BIG-IQ, it may be necessary to pass the ``auth_provider`` argument if the
    user has a different authentication handler configured. Otherwise, the system
    defaults for the different products will be used.
    """
    def __init__(self, server=None, username=None, password=None, server_port=443,
                 validate_certs=True, auth_provider=None, timeout=10, token=None,
                 **kwargs):
        """Instantiate REST session.

        Attributes:
            server (str): The server to connect to.
            username (str): The user to connect with.
            password (str): The password of the user.
            server_port (int): The port on the server running the REST API.
            validate_certs (bool): Whether to validate SSL server certs using the
                OpenSSL CA certs pre-configured on your Ansible host or not.
            auth_provider: String specifying the specific auth provider to
                authenticate the username/password against. This keyword
                implies that token based authentication is used.
                On BIG-IQ systems, the value 'local' can be used to refer to
                local user authentication.
            timeout (int): The timeout, in seconds, to wait before closing
                the session.
            token (str): String containing the token itself to use.
                This is particularly useful in situations where you want to
                mimic the behavior of a browser insofar as storing the token
                in a cookie and retrieving it for use "later". This is used
                to prevent token abuse on the F5 device. There is a limit
                that users may not go beyond when creating tokens and their
                re-use is an attempt to mitigate this scenario.
        """

        self._auth_provider = auth_provider
        self._debug_output = []
        self._debug = False
        self._default_headers = {
            'Content-Type': 'application/json'
        }
        self._parsed = {}
        self._password = password
        self._server = server
        self._server_port = server_port
        self._timeout = timeout
        self._token = token
        self._username = username
        self._validate_certs = validate_certs

    @property
    def auth_providers(self):
        """BIG-IQ specific query for auth providers.

        BIG-IP doesn't really need this because BIG-IP's multiple auth providers
        seem to handle fallthrough just fine. BIG-IQ on the other hand, needs to
        have its auth provider specified if you're using one of the non-default
        ones.
        """
        url = "https://{0}:{1}/info/system?null".format(self._server, self._server_port)
        response = open_url(
            url, method='GET', validate_certs=self._validate_certs,
            timeout=self._timeout, headers=self._default_headers
        )
        if response.code != 200:
            raise F5ModuleError('{0} Unexpected Error: {1} for uri: {2}\nText: {3}'.format(
                response.status_code, response.reason, response.url, response.text
            ))
        resp = json.loads(response)
        return resp['providers']

    @property
    def auth_provider(self):
        if self._auth_provider == 'local':
            return 'local'
        elif self._auth_provider == 'tmos':
            return 'tmos'
        elif self._auth_provider not in ['none', 'default']:
            for provider in self.auth_providers:
                if self._auth_provider in provider['link'] or self._auth_provider == provider['name']:
                    return provider['name']
        return None

    @property
    def token(self):
        """Get a new token from BIG-IP and store it internally.

        This method will be called automatically if a request is attempted
        but there is no authentication token, or the authentication token
        is expired. It is usually not necessary for users to call it, but
        it can be called if it is known that the authentication token has
        been invalidated by other means.
        """
        if self._token:
            return self._token
        login_body = {
            'username': self._username,
            'password': self._password,
        }
        if self._auth_provider:
            login_body['loginProviderName'] = self.auth_provider

        url = "https://{0}:{1}/mgmt/shared/authn/login".format(self._server, self._server_port)
        response = open_url(
            url, method='POST', data=json.dumps(login_body),
            validate_certs=self._validate_certs
        )
        if not response.code in [200]:
            raise F5ModuleError('{0} Unexpected Error: {1} for uri: {2}\nText: {3}'.format(
                response.status_code, response.reason, response.url, response.text
            ))
        resp = json.loads(response.read())
        self._token = resp.get('token', None)
        return self._token.get('name', None)

        # request.headers['X-F5-Auth-Token'] = self.token

    def get_headers(self, *args, **kwargs):
        result = {}
        result.update(self._default_headers)
        result['X-F5-Auth-Token'] = self.token
        if 'headers' in kwargs:
            result.update(kwargs['headers'])
        return result

    def get_full_url(self, url):
        if url.startswith('/'):
            url = url[1:]
        result = 'https://{0}:{1}/{2}'.format(self._server, self._server_port, url)
        return result

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        if value in BOOLEANS:
            self._debug = value

    @property
    def debug_output(self):
        return self._debug_output

    def delete(self, url):
        """Sends a HTTP DELETE command to an F5 REST Server.

        Use this method to send a DELETE command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        try:
            response = open_url(
                url, method='DELETE', headers=headers, validate_certs=self._validate_certs
            )
            try:
                return json.loads(response.read())
            except ValueError:
                return response.read()
        except Exception as ex:
            raise F5ModuleError(str(ex))

    def get(self, url):
        """Sends a HTTP GET command to an F5 REST Server.

        Use this method to send a GET command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        try:
            response = open_url(
                url, method='GET', headers=headers, validate_certs=self._validate_certs
            )
            try:
                return json.loads(response.read())
            except ValueError:
                return response.read()
        except Exception as ex:
            raise F5ModuleError(str(ex))

    def patch(self, url, data=None):
        """Sends a HTTP PATCH command to an F5 REST Server.

        Use this method to send a PATCH command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
            data (bytes): An object specifying additional data to send to the server,
                or ``None`` if no such data is needed. Currently HTTP requests are the
                only ones that use data. The supported object types include bytes,
                file-like objects, and iterables.
                See https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        try:
            response = open_url(
                url, method='PATCH', data=data, headers=headers,
                validate_certs=self._validate_certs
            )
            try:
                return json.loads(response.read())
            except ValueError:
                return response.read()
        except Exception as ex:
            raise F5ModuleError(str(ex))

    def post(self, url, data=None):
        """Sends a HTTP POST command to an F5 REST Server.

        Use this method to send a POST command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
            data (bytes): An object specifying additional data to send to the server,
                or ``None`` if no such data is needed. Currently HTTP requests are the
                only ones that use data. The supported object types include bytes,
                file-like objects, and iterables.
                See https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        try:
            response = open_url(
                url, method='POST', data=data, headers=headers,
                validate_certs=self._validate_certs
            )
            try:
                return json.loads(response.read())
            except ValueError:
                return response.read()
        except Exception as ex:
            raise F5ModuleError(str(ex))

    def put(self, url, data=None):
        """Sends a HTTP PUT command to an F5 REST Server.

        Use this method to send a PUT command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
            data (bytes): An object specifying additional data to send to the server,
                or ``None`` if no such data is needed. Currently HTTP requests are the
                only ones that use data. The supported object types include bytes,
                file-like objects, and iterables.
                See https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        try:
            response = open_url(
                url, method='PUT', data=data, headers=headers,
                validate_certs=self._validate_certs
            )
            try:
                return json.loads(response.read())
            except ValueError:
                return response.read()
        except Exception as ex:
            raise F5ModuleError(str(ex))


def debug_prepared_request(request):
    result = "curl -k -X {0} {1}".format(request.method.upper(), request.url)
    for k, v in iteritems(request.headers):
        result = result + " -H '{0}: {1}'".format(k, v)
    if any(v == 'application/json' for k, v in iteritems(request.headers)):
        if request.body:
            kwargs = json.loads(request.body.decode('utf-8'))
            result = result + " -d '" + json.dumps(kwargs, sort_keys=True) + "'"
    return result
