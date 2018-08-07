# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import os
import socket
import sys

from ansible.module_utils.urls import open_url, fetch_url
from ansible.module_utils.parsing.convert_bool import BOOLEANS
from ansible.module_utils.six import string_types
from ansible.module_utils.six import iteritems
from ansible.module_utils.urls import urllib_error
from ansible.module_utils._text import to_native
from ansible.module_utils.six import PY3

try:
    import json as _json
except ImportError:
    import simplejson as _json

try:
    from library.module_utils.network.f5.common import F5ModuleError
except ImportError:
    from ansible.module_utils.network.f5.common import F5ModuleError


"""An F5 REST API URI handler.

Use this module to make calls to an F5 REST server. It is influenced by the same
API that the Python ``requests`` tool uses, but the two are not the same, as the
library here is **much** more simple and targeted specifically to F5's needs.

The ``requests`` design was chosen due to familiarity with the tool. Internally,
the classes contained herein use Ansible native libraries.

The means by which you should use it are similar to ``requests`` basic usage.

Authentication is not handled for you automatically by this library, however it *is*
handled automatically for you in the supporting F5 module_utils code; specifically the
different product module_util files (bigip.py, bigiq.py, etc).

Internal (non-module) usage of this library looks like this.

```
# Create a session instance
mgmt = iControlRestSession()
mgmt.verify = False

server = '1.1.1.1'
port = 443

# Payload used for getting an initial authentication token
payload = {
  'username': 'admin',
  'password': 'secret',
  'loginProviderName': 'tmos'
}

# Create URL to call, injecting server and port
url = f"https://{server}:{port}/mgmt/shared/authn/login"

# Call the API
resp = session.post(url, json=payload)

# View the response
print(resp.json())

# Update the session with the authentication token
session.headers['X-F5-Auth-Token'] = resp.json()['token']['token']

# Create another URL to call, injecting server and port
url = f"https://{server}:{port}/mgmt/tm/ltm/virtual/~Common~virtual1"

# Call the API
resp = session.get(url)

# View the details of a virtual payload
print(resp.json())
```
"""


class Request(object):
    def __init__(self, method=None, url=None, headers=None, data=None, params=None,
                 auth=None, json=None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.data = data or []
        self.json = json
        self.params = params or {}
        self.auth = auth

    def prepare(self):
        p = PreparedRequest()
        p.prepare(
            method=self.method,
            url=self.url,
            headers=self.headers,
            data=self.data,
            json=self.json,
            params=self.params,
        )
        return p


class PreparedRequest(object):
    def __init__(self):
        self.method = None
        self.url = None
        self.headers = None
        self.body = None

    def prepare(self, method=None, url=None, headers=None, data=None, params=None, json=None):
        self.prepare_method(method)
        self.prepare_url(url, params)
        self.prepare_headers(headers)
        self.prepare_body(data, json)

    def prepare_url(self, url, params):
        self.url = url

    def prepare_method(self, method):
        self.method = method
        if self.method:
            self.method = self.method.upper()

    def prepare_headers(self, headers):
        self.headers = {}
        if headers:
            for k, v in iteritems(headers):
                self.headers[k] = v

    def prepare_body(self, data, json=None):
        body = None
        content_type = None

        if not data and json is not None:
            self.headers['Content-Type'] = 'application/json'
            body = _json.dumps(json)
            if not isinstance(body, bytes):
                body = body.encode('utf-8')

        if data:
            body = data
            content_type = None

        if content_type and 'content-type' not in self.headers:
            self.headers['Content-Type'] = content_type

        self.body = body


class Response(object):
    def __init__(self):
        self._content = None
        self.status = None
        self.headers = dict()
        self.url = None
        self.reason = None
        self.request = None

    @property
    def content(self):
        return self._content.decode('utf-8')

    @property
    def raw_content(self):
        return self._content

    def json(self):
        return _json.loads(self._content)

    @property
    def ok(self):
        if self.status is not None and int(self.status) > 400:
            return False
        try:
            response = self.json()
            if 'code' in response and response['code'] > 400:
                return False
        except ValueError:
            pass
        return True


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
    def __init__(self):
        self.headers = self.default_headers()
        self.verify = True
        self.params = {}
        self.timeout = 30

        self.server = None
        self.user = None
        self.password = None
        self.server_port = None
        self.auth_provider = None

    def _normalize_headers(self, headers):
        result = {}
        result.update(dict((k.lower(), v) for k, v in headers))

        # Don't be lossy, append header values for duplicate headers
        # In Py2 there is nothing that needs done, py2 does this for us
        if PY3:
            temp_headers = {}
            for name, value in headers:
                # The same as above, lower case keys to match py2 behavior, and create more consistent results
                name = name.lower()
                if name in temp_headers:
                    temp_headers[name] = ', '.join((temp_headers[name], value))
                else:
                    temp_headers[name] = value
            result.update(temp_headers)
        return result

    def default_headers(self):
        return {
            'connection': 'keep-alive',
            'accept': '*/*',
        }

    def prepare_request(self, request):
        headers = self.headers.copy()
        params = self.params.copy()

        if request.headers is not None:
            headers.update(request.headers)
        if request.params is not None:
            params.update(request.params)

        prepared = PreparedRequest()
        prepared.prepare(
            method=request.method,
            url=request.url,
            data=request.data,
            json=request.json,
            headers=headers,
            params=params,
        )
        return prepared

    def request(self, method, url, params=None, data=None, headers=None, auth=None,
                timeout=None, verify=None, json=None):
        request = Request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=json,
            data=data or {},
            params=params or {},
            auth=auth
        )
        kwargs = dict(
            timeout=timeout,
            verify=verify
        )
        prepared = self.prepare_request(request)
        return self.send(prepared, **kwargs)

    def send(self, request, **kwargs):
        response = Response()

        params = dict(
            method=request.method,
            data=request.body,
            timeout=kwargs.get('timeout', None) or self.timeout,
            validate_certs=kwargs.get('verify', None) or self.verify,
            headers=request.headers
        )

        try:
            result = open_url(request.url, **params)
            response._content = result.read()
            response.status = result.getcode()
            response.url = result.geturl()
            response.msg = "OK (%s bytes)" % result.headers.get('Content-Length', 'unknown')
            response.headers = self._normalize_headers(result.headers.items())
            response.request = request
        except urllib_error.HTTPError as e:
            try:
                response._content = e.read()
            except AttributeError:
                response._content = ''

            response.reason = to_native(e)
            response.status_code = e.code
        return response

    def delete(self, url, json=None, **kwargs):
        return self.request('DELETE', url, json=json, **kwargs)

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request('PATCH', url, data=data, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request('PUT', url, data=data, **kwargs)


def debug_prepared_request(url, method, headers, data=None):
    result = "curl -k -X {0} {1}".format(method.upper(), url)
    for k, v in iteritems(headers):
        result = result + " -H '{0}: {1}'".format(k, v)
    if any(v == 'application/json' for k, v in iteritems(headers)):
        if data:
            kwargs = _json.loads(data.decode('utf-8'))
            result = result + " -d '" + _json.dumps(kwargs, sort_keys=True) + "'"
    return result


def download_file(client, url, dest):
    """Download a file from the remote device

    This method handles the chunking needed to download a file from
    a given URL on the BIG-IP.

    Arguments:
        client (object): The F5RestClient connection object.
        url (string): The URL to download.
        dest (string): The location on (Ansible controller) disk to store the file.

    Returns:
        bool: True on success. False otherwise.
    """
    with open(dest, 'wb') as fileobj:
        chunk_size = 512 * 1024
        start = 0
        end = chunk_size - 1
        size = 0
        current_bytes = 0

        while True:
            content_range = "%s-%s/%s" % (start, end, size)
            headers = {
                'Content-Range': content_range,
                'Content-Type': 'application/octet-stream'
            }
            data = {
                'headers': headers,
                'verify': False,
                'stream': False
            }
            response = client.api.get(url, headers=headers, json=data)
            if response.status == 200:
                # If the size is zero, then this is the first time through
                # the loop and we don't want to write data because we
                # haven't yet figured out the total size of the file.
                if size > 0:
                    current_bytes += chunk_size
                    fileobj.write(response.raw_content)
            # Once we've downloaded the entire file, we can break out of
            # the loop
            if end == size:
                break
            crange = response.headers['content-range']
            # Determine the total number of bytes to read.
            if size == 0:
                size = int(crange.split('/')[-1]) - 1
                # If the file is smaller than the chunk_size, the BigIP
                # will return an HTTP 400. Adjust the chunk_size down to
                # the total file size...
                if chunk_size > size:
                    end = size
                # ...and pass on the rest of the code.
                continue
            start += chunk_size
            if (current_bytes + chunk_size) > size:
                end = size
            else:
                end = start + chunk_size - 1
    return True


def upload_file(client, url, dest):
    """Upload a file to an arbitrary URL.

    This method is responsible for correctly chunking an upload request to an
    arbitrary file worker URL.

    Arguments:
        client (object): The F5RestClient connection object.
        url (string): The URL to upload a file to.
        dest (string): The file to be uploaded.

    Examples:
        The ``dest`` may be either an absolute or relative path. The basename
        of the path is used as the remote file name upon upload. For instance,
        in the example below, ``BIGIP-13.1.0.8-0.0.3.iso`` would be the name
        of the remote file.

        The specified URL should be the full URL to where you want to upload a
        file. BIG-IP has many different URLs that can be used to handle different
        types of files. This is why a full URL is required.

        >>> from ansible.module_utils.network.f5.icontrol import upload_client
        >>> url = 'https://{0}:{1}/mgmt/cm/autodeploy/software-image-uploads'.format(
        ...   self.client.provider['server'],
        ...   self.client.provider['server_port']
        ... )
        >>> dest = '/path/to/BIGIP-13.1.0.8-0.0.3.iso'
        >>> upload_file(self.client, url, dest)
        True

    Returns:
        bool: True on success. False otherwise.

    Raises:
        F5ModuleError: Raised if ``retries`` limit is exceeded.
    """
    with open(dest, 'rb') as fileobj:
        size = os.stat(dest).st_size

        # This appears to be the largest chunk size that iControlREST can handle.
        #
        # The trade-off you are making by choosing a chunk size is speed, over size of
        # transmission. A lower chunk size will be slower because a smaller amount of
        # data is read from disk and sent via HTTP. Lots of disk reads are slower and
        # There is overhead in sending the request to the BIG-IP.
        #
        # Larger chunk sizes are faster because more data is read from disk in one
        # go, and therefore more data is transmitted to the BIG-IP in one HTTP request.
        #
        # If you are transmitting over a slow link though, it may be more reliable to
        # transmit many small chunks that fewer large chunks. It will clearly take
        # longer, but it may be more robust.
        chunk_size = 1024 * 7168
        start = 0
        retries = 0
        basename = os.path.basename(dest)
        url = '{0}/{1}'.format(url.rstrip('/'), basename)

        while True:
            if retries == 3:
                # Retries are used here to allow the REST API to recover if you kill
                # an upload mid-transfer.
                #
                # There exists a case where retrying a new upload will result in the
                # API returning the POSTed payload (in bytes) with a non-200 response
                # code.
                #
                # Retrying (after seeking back to 0) seems to resolve this problem.
                raise F5ModuleError(
                    "Failed to upload file too many times."
                )
            try:
                file_slice = fileobj.read(chunk_size)
                if not file_slice:
                    break

                current_bytes = len(file_slice)
                if current_bytes < chunk_size:
                    end = size
                else:
                    end = start + current_bytes
                headers = {
                    'Content-Range': '%s-%s/%s' % (start, end - 1, size),
                    'Content-Type': 'application/octet-stream'
                }

                # Data should always be sent using the ``data`` keyword and not the
                # ``json`` keyword. This allows bytes to be sent (such as in the case
                # of uploading ISO files.
                response = client.api.post(url, headers=headers, data=file_slice)

                if response.status != 200:
                    # When this fails, the output is usually the body of whatever you
                    # POSTed. This is almost always unreadable because it is a series
                    # of bytes.
                    #
                    # Therefore, including an empty exception here.
                    raise F5ModuleError()
                start += current_bytes
            except F5ModuleError:
                # You must seek back to the beginning of the file upon exception.
                #
                # If this is not done, then you risk uploading a partial file.
                fileobj.seek(0)
                retries += 1
    return True
