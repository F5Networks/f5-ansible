#!/usr/bin/python
#
# Copyright 2017 F5 Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
module: bigip_ssl_certificate
short_description: Import/Delete certificates from BIG-IP
description:
  - This module will import/delete SSL certificates on BIG-IP LTM.
    Certificates can be imported from certificate and key files on the local
    disk, in PEM format.
version_added: 2.2
options:
  cert_content:
    description:
      - When used instead of 'cert_src', sets the contents of a certificate directly
        to the specified value. This is used with lookup plugins or for anything
        with formatting or templating. Either one of C(key_src),
        C(key_content), C(cert_src) or C(cert_content) must be provided when
        C(state) is C(present).
    required: false
  key_content:
    description:
      - When used instead of 'key_src', sets the contents of a certificate key
        directly to the specified value. This is used with lookup plugins or for
        anything with formatting or templating. Either one of C(key_src),
        C(key_content), C(cert_src) or C(cert_content) must be provided when
        C(state) is C(present).
    required: false
  state:
    description:
      - Certificate and key state. This determines if the provided certificate
        and key is to be made C(present) on the device or C(absent).
    required: true
    default: present
    choices:
      - present
      - absent
  partition:
    description:
      - BIG-IP partition to use when adding/deleting certificate.
    required: false
    default: Common
  name:
    description:
      - SSL Certificate Name.  This is the cert/key pair name used
        when importing a certificate/key into the F5. It also
        determines the filenames of the objects on the LTM
        (:Partition:name.cer_11111_1 and :Partition_name.key_11111_1).
    required: true
  cert_src:
    description:
      - This is the local filename of the certificate. Either one of C(key_src),
        C(key_content), C(cert_src) or C(cert_content) must be provided when
        C(state) is C(present).
    required: false
  key_src:
    description:
      - This is the local filename of the private key. Either one of C(key_src),
        C(key_content), C(cert_src) or C(cert_content) must be provided when
        C(state) is C(present).
    required: false
  passphrase:
    description:
      - Passphrase on certificate private key
    required: false
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 1.5.0
    - BigIP >= v12
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Import PEM Certificate from local disk
  bigip_ssl_certificate:
      name: "certificate-name"
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "present"
      cert_src: "/path/to/cert.crt"
      key_src: "/path/to/key.key"
  delegate_to: localhost

- name: Use a file lookup to import PEM Certificate
  bigip_ssl_certificate:
      name: "certificate-name"
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "present"
      cert_content: "{{ lookup('file', '/path/to/cert.crt') }}"
      key_content: "{{ lookup('file', '/path/to/key.key') }}"
  delegate_to: localhost

- name: "Delete Certificate"
  bigip_ssl_certificate:
      name: "certificate-name"
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "absent"
  delegate_to: localhost
'''

RETURN = '''
cert_name:
    description: The name of the certificate that the user provided
    returned:
        - created
    type: string
    sample: "cert1"
cert_filename:
    description:
        - The name of the SSL certificate. The C(cert_filename) and
          C(key_filename) will be similar to each other, however the
          C(cert_filename) will have a C(.crt) extension.
    returned:
        - created
    type: string
    sample: "cert1.crt"
key_filename:
    description:
        - The name of the SSL certificate key. The C(key_filename) and
          C(cert_filename) will be similar to each other, however the
          C(key_filename) will have a C(.key) extension.
    returned:
        - created
    type: string
    sample: "cert1.key"
key_checksum:
    description: SHA1 checksum of the key that was provided.
    return:
        - changed
        - created
    type: string
    sample: "cf23df2207d99a74fbe169e3eba035e633b65d94"
cert_checksum:
    description: SHA1 checksum of the cert that was provided.
    return:
        - changed
        - created
    type: string
    sample: "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0"
cert_source_path:
    description: Path on BIG-IP where the source of the certificate is stored.
    return: created
    type: string
    sample: "/var/config/rest/downloads/cert1.crt"
key_source_path:
    description: Path on BIG-IP where the source of the key is stored
    return: created
    type: string
    sample: "/var/config/rest/downloads/cert1.key"
'''


import hashlib
import StringIO
import os
import re

from ansible.module_utils.f5_utils import *


class Parameters(AnsibleF5Parameters):
    api_map = dict(
        vlan='tmInterface',
        gateway_address='gw',
        destination='network',
        reject='blackhole'
    )

    updatables = [
        'vlan', 'gateway_address', 'destination', 'pool', 'description',
        'mtu', 'reject'
    ]

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result

    def _get_hash(self, content):
        k = hashlib.sha1()
        s = StringIO.StringIO(content)
        while True:
            data = s.read(1024)
            if not data:
                break
            k.update(data)
        return k.hexdigest()


class KeyParameters(Parameters):
    api_attributes = ['passphrase']

    @property
    def key_filename(self):
        fname, fext = os.path.splitext(self.name)
        if fext == '':
            return fname + '.key'
        else:
            return self.name

    @property
    def key_checksum(self):
        if self.key_content is None:
            return None
        return self._get_hash(self.key_content)

    @property
    def key_src(self, value):
        try:
            with open(value) as fh:
                self.key_content = fh.read()
        except IOError:
            raise F5ModuleError(
                "The specified 'key_src' does not exist"
            )

    @property
    def key_source_path(self):
        return 'file://' + os.path.join(
            BaseManager.download_path,
            self.key_filename
        )


class CertParameters(Parameters):
    @property
    def cert_checksum(self):
        if self.cert_content is None:
            return None
        return self._get_hash(self.cert_content)

    @property
    def cert_filename(self):
        fname, fext = os.path.splitext(self.name)
        if fext == '':
            return fname + '.crt'
        else:
            return self.name

    @property
    def cert_source_path(self):
        return 'file://' + os.path.join(
            BaseManager.download_path,
            self.cert_filename
        )

    @property
    def checksum(self):
        pattern = r'SHA1:\d+:(?P<value>[\w+]{40})'
        matches = re.match(pattern, sha1)
        if matches:
            return matches.group('value')
        else:
            return None


class ModuleManager(object):
    def __init__(self, client):
        self.client = client

    def exec_module(self):
        manager1 = self.get_manager('certificate')
        manager2 = self.get_manager('key')
        return self.execute_managers([manager1, manager2])

    def execute_managers(self, managers):
        results = {}
        for manager in managers:
            result = manager.exec_module()
            for k,v in iteritems(result):
                if k == 'changed' and v is True:
                    results['changed'] = True
                else:
                    results[k] = v
        return results

    def get_manager(self, type):
        if type == 'certificate':
            return CertificateManager(self.client)
        elif type =='key':
            return KeyManager(self.client)


class BaseManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.download_path = '/var/config/rest/downloads'

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = attr1
        if changed:
            self.changes = Parameters(changed)
            return True
        return False

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the Wide IP")
        return True


class CertificateManager(BaseManager):
    def __init__(self, client):
        super(CertificateManager, self).__init__(client)
        self.want = CertParameters(self.client.module.params)
        self.changes = None

    def create(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def exists(self):
        return self.api.tm.sys.file.ssl_certs.ssl_cert.exists(
            name=self.have.cert_filename,
            partition=self.have.partition
        )

    def present(self):
        if self.want.key_content is None:
            raise F5ModuleError(
                "The 'cert_content' option is required when "
                "state is 'present'"
            )
        return super(CertificateManager, self).present()

    def should_update(self):
        self._update_changed_options()
        if self.changes:
            return True
        return False

    def update_on_device(self):
        resource = self.client.api.tm.sys.file.ssl_certs.ssl_cert.load(
            name=self.have.cert_filename,
            partition=self.have.partition
        )
        resource.update()

    def create_on_device(self):
        cstring = StringIO.StringIO(self.have.cert_content)
        self.client.api.shared.file_transfer.uploads.upload_stringio(
            cstring, self.have.cert_filename
        )
        self.client.api.tm.sys.file.ssl_certs.ssl_cert.create(
            sourcePath=self.have.cert_source_path,
            name=self.have.cert_filename,
            partition=self.have.partition
        )

    def read_current_from_device(self):
        resource = self.api.tm.sys.file.ssl_certs.ssl_cert.load(
            name=self.params.cert_filename,
            partition=self.params.partition
        ).to_dict()
        resource.pop('_meta_data', None)
        return Parameters(resource)

    def remove_from_device(self):
        resource = self.client.api.tm.sys.file.ssl_certs.ssl_cert.load(
            name=self.params.cert_filename,
            partition=self.params.partition
        )
        resource.delete()


class KeyManager(BaseManager):
    def __init__(self, client):
        super(KeyManager, self).__init__(client)
        self.want = KeyParameters(self.client.module.params)
        self.changes = KeyParameters()

    def update_on_device(self):
        resource = self.client.api.tm.sys.file.ssl_keys.ssl_key.load(
            name=self.have.key_filename,
            partition=self.have.partition
        )
        resource.update()

    def exists(self):
        return self.api.tm.sys.file.ssl_keys.ssl_key.exists(
            name=self.params.key_filename,
            partition=self.params.partition
        )

    def present(self):
        if self.want.key_content is None:
            raise F5ModuleError(
                "The 'key_content' option is required when "
                "state is 'present'"
            )
        return super(KeyManager, self).present()

    def read_current_from_device(self):
        resource = self.api.tm.sys.file.ssl_keys.ssl_key.load(
            name=self.params.cert_filename,
            partition=self.params.partition
        ).to_dict()
        resource.pop('_meta_data', None)
        return Parameters(resource)

    def create_on_device(self):
        kstring = StringIO.StringIO(self.have.key_content)
        self.client.api.shared.file_transfer.uploads.upload_stringio(
            kstring, self.have.key_filename
        )
        self.client.api.tm.sys.file.ssl_certs.ssl_cert.create(
            sourcePath=self.have.key_source_path,
            name=self.have.key_filename,
            partition=self.have.partition
        )




        params = dict(
            sourcePath="file://" + filepath,
            name=self.params.key_filename,
            partition=self.params.partition
        )
        if self.params.passphrase:
            params['passphrase'] = self.params.passphrase
        else:
            params['passphrase'] = None
        api.tm.sys.file.ssl_keys.ssl_key.create(**params)
        return True

    def remove_from_device(self):
        resource = self.client.api.tm.sys.file.ssl_keys.ssl_key.load(
            name=self.params.key_filename,
            partition=self.params.partition
        )
        resource.delete()

    def key_is_changed(self, current):
        if current.key_checksum != self.params.key_checksum:
            return True
        return False


class ArgumentSpec(object):
    def __init__(self):
        deprecated = ['key_src']
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(
                type='str',
                required=True
            ),
            cert_content=dict(
                type='str',
                default=None
            ),
            cert_src=dict(
                type='path',
                default=None
            ),
            key_content=dict(
                type='str',
                default=None
            ),
            key_src=dict(
                type='path',
                default=None
            ),
            passphrase=dict(
                type='str',
                default=None,
                no_log=True
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.mutually_exclusive = [
            ['key_content', 'key_src'],
            ['cert_content', 'cert_src']
        ]
        self.f5_product_name = 'bigip'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        mutually_exclusive=spec.mutually_exclusive,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
