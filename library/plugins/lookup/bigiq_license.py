# (c) 2013, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: Select a random license key from a file and remove it from future lookups
    author: Tim Rupp <caphrim007@gmail.com>
    version_added: "2.5"
    short_description: Return random license from list
    description:
      - Select a random license key from a file and remove it from future lookups
      - Can optionally remove the key if C(remove=True) is specified
"""

EXAMPLES = """
- name: Get a regkey license from a stash without deleting it
  bigiq_regkey_license:
    key: "{{ lookup('license_hopper', 'filename=/path/to/licenses.txt') }}"
    state: present
    pool: regkey1

- name: Get a regkey license from a stash and delete the key from the file
  bigiq_regkey_license:
    key: "{{ lookup('license_hopper', 'filename=/path/to/licenses.txt', remove=True) }}"
    state: present
    pool: regkey1
"""

RETURN = """
  _raw:
    description:
      - random item
"""

import random

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.module_utils.network.f5.bigiq import F5RestClient
from ansible.plugins.lookup import LookupBase

BOOLEANS_TRUE = frozenset(('y', 'yes', 'on', '1', 'true', 'True', 't', 1, 1.0, True))


class LookupModule(LookupBase):
    def __init__(self, loader=None, templar=None, **kwargs):
        super(LookupModule, self).__init__(loader, templar, **kwargs)
        self.username = None
        self.password = None
        self.validate_certs = True
        self.host = None
        self.pool_name = None
        self.port = 443
        self.client = None

    def _validate_params(self, **kwargs):
        self.username = kwargs.pop('username', 'admin')
        self.password = kwargs.pop('password', 'admin')
        self.validate_certs = kwargs.pop('validate_certs', True)
        self.host = kwargs.pop('host', None)
        self.port = kwargs.pop('port', 443)
        self.pool_name = kwargs.pop('pool_name', None)

        if self.host is None:
            raise AnsibleError('A valid hostname or IP for BIGIQ needs to be provided')
        if self.pool_name is None:
            raise AnsibleError('License pool name needs to be specified')

    def _get_pool_uuid(self):
        uri = "https://{0}:{1}/mgmt/cm/device/licensing/pool/regkey/licenses".format(self.host, self.port)
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise AnsibleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise AnsibleError(response['message'])
            else:
                raise AnsibleError(resp.content)
        if 'items' not in response:
            raise AnsibleError('No license pools configured on BIGIQ')

        resource = next((x for x in response['items'] if x.name == self.pool_name), None)
        if resource is None:
            raise AnsibleError("Could not find the specified license pool.")
        return resource.id

    def _get_registation_keys(self, pool_id):
        uri = 'https://{0}:{1}/mgmt/cm/device/licensing/pool/regkey/licenses/{2}/offerings/'.format(
            self.host,
            self.port,
            pool_id,
        )

        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise AnsibleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise AnsibleError(response['message'])
            else:
                raise AnsibleError(resp.content)
        regkeys = [x.registrationKey for x in response['items']]

        if not regkeys:
            raise AnsibleError('Failed to obtain registration keys')

        return regkeys

    def run(self, terms, variables=None, **kwargs):
        self._validate_params(**kwargs)
        self.client = F5RestClient(user**module.params)
        pool_id = self._get_pool_uuid()
        regkeys = self._get_registation_keys(pool_id)
        keys = []
        for key in regkeys:
            uri = 'https://{0}:{1}/mgmt/cm/device/licensing/pool/regkey/licenses/{2}/offerings/{3}/members'.format(
                self.host,
                self.port,
                pool_id,
                key
            )
            resp = self.client.api.get(uri)
            try:
                response = resp.json()
            except ValueError as ex:
                raise AnsibleError(str(ex))

            if 'code' in response and response['code'] == 400:
                if 'message' in response:
                    raise AnsibleError(response['message'])
                else:
                    raise AnsibleError(resp.content)

            if not response['items']:
                keys.append(key)

        result = random.choice(keys)
        return result



