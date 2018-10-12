# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


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
    def __init__(self, *args, **kwargs):
        super(F5Client, self).__init__(*args, **kwargs)
        self.provider = self.merge_provider_params()

    @property
    def api(self):
        if self._client:
            return self._client

        try:
            result = ManagementRoot(
                self.provider['server'],
                self.provider['user'],
                self.provider['password'],
                port=self.provider['server_port'],
                verify=self.provider['validate_certs'],
                token='tmos'
            )
            self._client = result
            return self._client
        except Exception as ex:
            error = 'Unable to connect to {0} on port {1}. The reported error was "{0}".'.format(
                self.provider['server'], self.provider['server_port'], str(ex)
            )
            raise F5ModuleError(error)


class F5RestClient(F5BaseClient):
    def __init__(self, *args, **kwargs):
        super(F5RestClient, self).__init__(*args, **kwargs)
        self.provider = self.merge_provider_params()
        self.headers = {
            'Content-Type': 'application/json'
        }

    @property
    def api(self):
        if self._client:
            return self._client
        session = self.connect_via_token_auth()
        if session:
            self._client = session
            return session
        session = self.connect_via_basic_auth()
        if session:
            self._client = session
            return session
        error = 'Unable to connect to {0} on port {1}.'.format(
            self.provider['server'], self.provider['server_port']
        )
        raise F5ModuleError(error)

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
            return None

        session.request.headers['X-F5-Auth-Token'] = response.json()['token']['token']
        return session

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
            return None
        return session







    def get_identifier(mgmt, proxy_to):
        if proxy_to is None:
            raise F5SDKError(
                "An identifier to a device to proxy to must be provided."
            )

        if re.search(r'([0-9-a-z]+\-){4}[0-9-a-z]+', proxy_to, re.I):
            return proxy_to
        return ManagementProxy._get_device_uuid(mgmt, proxy_to)

    def get_device_uuid(mgmt, proxy_to):
        dg = mgmt.shared.resolver.device_groups
        collection = dg.cm_cloud_managed_devices.devices_s.get_collection(
            requests_params=dict(
                params="$filter=hostname+eq+'{0}'&$select=uuid".format(
                    proxy_to
                )
            )
        )
        if len(collection) > 1:
            raise F5SDKError(
                "More that one managed device was found with this hostname. "
                "Proxied devices must be unique."
            )
        elif len(collection) == 0:
            raise F5SDKError(
                "No device was found with that hostname"
            )
        else:
            resource = collection.pop()
            return resource.pop('uuid', None)
