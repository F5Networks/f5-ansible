#!/usr/bin/python
#
# Copyright 2016 F5 Networks Inc.
#
# Based off the original work of Kevin Coming (@waffie1)
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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

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
    - f5-sdk >= 1.3.1
    - BigIP >= v12
author:
    - Kevin Coming (@waffie1)
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


try:
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


import hashlib
import StringIO
import os
import re

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *


def connect_to_bigip(**kwargs):
    return ManagementRoot(kwargs['server'],
                          kwargs['user'],
                          kwargs['password'],
                          port=kwargs['server_port'],
                          token=True)


class F5CommonHashMixin(object):
    @staticmethod
    def get_hash(content):
        k = hashlib.sha1()
        s = StringIO.StringIO(content)
        while True:
            data = s.read(1024)
            if not data:
                break
            k.update(data)
        return k.hexdigest()


class F5SslParamBase(object):
    def __get__(self, instance, owner):
        return instance.__dict__.get(self._name, None)


class F5SslKeySrc(F5SslParamBase):
    _name = 'key_src'

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        if not value:
            return
        with open(value) as fh:
            instance.key_content = fh.read()


class F5SslKeyContent(F5CommonHashMixin, F5SslParamBase):
    _name = 'key_content'

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        if not value:
            return
        instance.key_checksum = self.get_hash(value)


class F5SslCertSrc(F5SslParamBase):
    _name = 'cert_src'

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        if not value:
            return
        with open(value) as fh:
            instance.cert_content = fh.read()


class F5SslCertContent(F5CommonHashMixin, F5SslParamBase):
    _name = 'cert_content'

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        if not value:
            return
        instance.cert_checksum = self.get_hash(value)


class F5SslCertName(F5SslParamBase):
    _name = 'cert_name'

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        fname, fext = os.path.splitext(value)
        instance.key_filename = fname + '.key'
        instance.cert_filename = fname + '.crt'


class BigIpSslCertificateParams(object):
    cert_checksum = None
    cert_content = F5SslCertContent()
    cert_filename = None
    cert_src = F5SslCertSrc()
    key_checksum = None
    key_content = F5SslKeyContent()
    key_filename = None
    key_src = F5SslKeySrc()
    name = F5SslCertName()

    def difference(self, obj):
        """Compute difference between one object and another

        :param obj:
        Returns:
            Returns a new set with elements in s but not in t (s - t)
        """
        excluded_keys = [
            'passphrase', 'cert_content', 'password', 'server', 'key_content',
            'state', 'user', 'server_port', 'validate_certs'
        ]
        return self._difference(self, obj, excluded_keys)

    def _difference(self, obj1, obj2, excluded_keys):
        """

        Code take from https://www.djangosnippets.org/snippets/2281/

        :param obj1:
        :param obj2:
        :param excluded_keys:
        :return:
        """
        d1, d2 = obj1.__dict__, obj2.__dict__
        new = {}
        for k,v in d1.items():
            if k in excluded_keys:
                continue
            try:
                if v != d2[k]:
                    new.update({k: d2[k]})
            except KeyError:
                new.update({k: v})
        return new

    @classmethod
    def from_module(cls, module):
        """Create instance from dictionary of Ansible Module params

        This method accepts a dictionary that is in the form supplied by
        the

        Args:
             module: An AnsibleModule object's `params` attribute.

        Returns:
            A new instance of BigIpSslCertificateParams. The attributes
            of this object are set according to the param data that is
            supplied by the user.
        """
        result = cls()
        for key in module:
            setattr(result, key, module[key])
        return result


class BigIpSslCertificateModule(AnsibleModule):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.required_args = [
            'key_content', 'key_src', 'cert_content', 'cert_src'
        ]
        self.init_meta_args()
        self.init_argument_spec()
        super(BigIpSslCertificateModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode,
            mutually_exclusive=[
                ['key_content', 'key_src'],
                ['cert_content', 'cert_src']
            ]
        )

    def __set__(self, instance, value):
        if isinstance(value, BigIpSslCertificateModule):
            instance.params = BigIpSslCertificateParams.from_module(self.params)
        else:
            super(BigIpSslCertificateModule, self).__set__(instance, value)

    def init_meta_args(self):
        args = dict(
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
            )
        )
        self.meta_args = args

    def init_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)


class BigIpSslCertificateManager(object):
    params = BigIpSslCertificateParams()
    current = BigIpSslCertificateParams()
    module = BigIpSslCertificateModule()

    def __init__(self):
        """
        Attributes:
            has_key: A boolean holding the cached value from the first call
                to key_exists().
            has_cert: A boolean holding the cached value from the first call
                to cert_exists().
        """
        self.has_key = None
        self.has_cert = None
        self.config = None
        self.api = None
        self.dlpath = '/var/config/rest/downloads'
        self.changes = None

    def apply_changes(self):
        """Apply the user's changes to the device

        This method is the primary entry-point to this module. Based on the
        parameters supplied by the user to the class, this method will
        determine which `state` needs to be fulfilled and delegate the work
        to more specialized helper methods.

        Additionally, this method will return the result of applying the
        changes so that Ansible can communicate this result to the user.

        Raises:
            F5ModuleError: An error occurred communicating with the device
        """
        changed = False
        result = dict()
        state = self.params.state

        try:
            self.api = connect_to_bigip(**self.params.__dict__)

            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.params.difference(self.current)
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        cert = self.cert_exists()
        key = self.key_exists()

        if cert and key:
            return True
        else:
            return False

    def ensure_required_params_are_specified(self):
        if not self.module:
            raise F5ModuleError(
                "A config object has not yet been created"
            )
        required = self.module.required_args
        values = self.params.__dict__
        if any(values[k] is not None for k in required):
            return

        raise F5ModuleError(
            "Either 'key_content', 'key_src', 'cert_content' or "
            "'cert_src' must be provided"
        )

    def no_content_specified(self):
        """Determine whether no content was specified, or not

        :return:
        """
        if not self.params.cert_content and not self.params.key_content:
            return True
        return False

    def present(self):
        self.ensure_required_params_are_specified()
        if self.no_content_specified():
            return False
        if self.key_and_cert_exist():
            return self.update_key_and_cert()
        elif self.key_exists():
            return self.create_cert_update_key()
        elif self.cert_exists():
            return self.create_key_update_cert()
        else:
            return self.create_key_and_cert()

    def cert_and_key_are_changed(self, current):
        if current.key_checksum != self.params.key_checksum:
            return True
        if current.cert_checksum != self.params.cert_checksum:
            return True
        return False

    def update_key_and_cert(self):
        """Updates both a key and certificate on a remote device

        :return:
        """
        current = self.read_current()
        if not self.cert_and_key_are_changed(current):
            return False
        if self.module.check_mode:
            return True
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            self.upload_key(api)
            self.update_key(api)
            self.upload_cert(api)
            self.update_cert(api)
        return True

    def create_key_and_cert(self):
        if self.module.check_mode:
            return True
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            self.upload_key(api)
            self.create_key(api)
            self.upload_cert(api)
            self.create_cert(api)
        return True

    def create_cert_update_key(self):
        current = self.read_current()
        if not self.key_is_changed(current):
            return False
        if self.module.check_mode:
            return True
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            self.upload_key(api)
            self.update_key(api)
            self.upload_cert(api)
            self.create_cert(api)
        return True

    def key_is_changed(self, current):
        if current.key_checksum != self.params.key_checksum:
            return True
        return False

    def create_key_update_cert(self):
        current = self.read_current()
        if not self.cert_is_changed(current):
            return False
        if self.module.check_mode:
            return True
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            self.upload_key(api)
            self.create_key(api)
            self.upload_cert(api)
            self.create_cert(api)
        return True

    def cert_is_changed(self, current):
        if current.cert_checksum != self.params.cert_checksum:
            return True
        return False

    def update_key(self, api):
        params = dict(
            name=self.params.key_filename,
            partition=self.params.partition
        )
        key = api.tm.sys.file.ssl_keys.ssl_key.load(**params)

        params = dict()
        if self.params.passphrase:
            params['passphrase'] = self.params.passphrase
        else:
            params['passphrase'] = None
        key.update(**params)
        return True

    def upload_cert(self, api):
        # Upload the content of a certificate as a StringIO object
        cstring = StringIO.StringIO(self.params.cert_content)
        filepath = os.path.join(self.dlpath, self.params.cert_filename)
        api.shared.file_transfer.uploads.upload_stringio(
            cstring, self.params.cert_filename
        )
        self.params.cert_source_path = filepath

    def update_cert(self, api):
        params = dict(
            name=self.params.cert_filename,
            partition=self.params.partition
        )
        cert = api.tm.sys.file.ssl_certs.ssl_cert.load(**params)
        # This works because, while the source path is the same,
        # calling update causes the file to be re-read
        cert.update()
        return True

    def create_cert(self, api):
        filepath = os.path.join(self.dlpath, self.params.cert_filename)
        params = dict(
            sourcePath="file://" + filepath,
            name=self.params.cert_filename,
            partition=self.params.partition
        )
        api.tm.sys.file.ssl_certs.ssl_cert.create(**params)
        return True

    def upload_key(self, api):
        # Upload the content of a certificate key as a StringIO object
        kstring = StringIO.StringIO(self.params.key_content)
        filepath = os.path.join(self.dlpath, self.params.key_filename)
        api.shared.file_transfer.uploads.upload_stringio(
            kstring, self.params.key_filename
        )
        self.params.key_source_path = filepath

    def create_key(self, api):
        filepath = os.path.join(self.dlpath, self.params.key_filename)
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

    def key_and_cert_exist(self):
        return self.key_exists() and self.cert_exists()

    def key_exists(self):
        if self.has_key is not None:
            return self.has_key
        if self.read_existing_key():
            self.has_key = True
        else:
            self.has_key = False
        return self.has_key

    def cert_exists(self):
        if self.has_cert is not None:
            return self.has_cert
        if self.read_existing_cert():
            self.has_cert = True
        else:
            self.has_cert = False
        return self.has_cert

    def read_existing_key(self):
        result = dict()
        try:
            key = self.api.tm.sys.file.ssl_keys.ssl_key.load(
                name=self.params.key_filename,
                partition=self.params.partition
            )
            if hasattr(key, 'checksum'):
                formatted = self.format_sha1_value_from_device(key.checksum)
                result['key_checksum'] = formatted
            if hasattr(key, 'sourcePath'):
                path = self.format_source_path_from_device(key.sourcePath)
                result['key_source_path'] = path
            return result
        except iControlUnexpectedHTTPError:
            return None

    def read_existing_cert(self):
        result = dict()
        try:
            cert = self.api.tm.sys.file.ssl_certs.ssl_cert.load(
                name=self.params.cert_filename,
                partition=self.params.partition
            )
            if hasattr(cert, 'checksum'):
                formatted = self.format_sha1_value_from_device(cert.checksum)
                result['cert_checksum'] = formatted
            if hasattr(cert, 'sourcePath'):
                path = self.format_source_path_from_device(cert.sourcePath)
                result['cert_source_path'] = path
            return result
        except iControlUnexpectedHTTPError:
            return None

    def format_source_path_from_device(self, path):
        """Formats a source path for Ansible consumption

        The `sourcePath` value that is provided by BIG-IP has a protocol
        string attached to it. Usually this is "file://". This method just
        strips that prefix off so that the path matches one sent by the user.

        Arguments:
            path: The path that needs to be formatted

        Returns:
            A new string formatted to remove any leading protocol prefix
        """
        return str(path).replace('file://', '')

    def format_sha1_value_from_device(self, sha1):
        """Formats a SHA1 for Ansible consumption

        The `checksum` value that is provided by BIG-IP has several prefixes
        as part of the value that we are not interested in. This value, when
        returned by BIG-IP, normally looks like this.

            SHA1:5752:b390c93c0e34c618b7559d9cf510ade6c062c6f3

        This method strips off the unnecessary information and leaves the
        checksum behind so that the module is able to compare against it
        with the values provided by the user

        Arguments:
            sha1: The checksum from the BIG-IP that needs to be formatted

        Returns:
            A new string formatted to remote extraneous information in the
            checksum.
        """
        pattern = r'SHA1:\d+:(?P<value>[\w+]{40})'
        matches = re.match(pattern, sha1)
        if matches:
            return matches.group('value')
        else:
            return None

    def read_current(self):
        existing_key = self.read_existing_key()
        existing_cert = self.read_existing_cert()
        current = BigIpSslCertificateParams()
        current.name = self.params.name
        current.partition = self.params.partition
        current.key_checksum = existing_key['key_checksum']
        current.cert_checksum = existing_cert['cert_checksum']
        current.cert_source_path = existing_cert['cert_source_path']
        current.key_source_path = existing_key['key_source_path']
        self.current = current
        return self.current

    def absent(self):
        changed = False
        if self.exists():
            changed = self.delete()
        return changed

    def delete(self):
        if self.key_and_cert_exist():
            return self.delete_key_and_cert()
        elif self.key_exists():
            return self.only_delete_key()
        elif self.cert_exists():
            return self.only_delete_cert()
        else:
            return False

    def delete_key_and_cert(self):
        if self.module.check_mode:
            return True
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            self.delete_key(api)
            self.delete_cert(api)
        return True

    def only_delete_cert(self):
        if self.module.check_mode:
            return True
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            self.delete_cert(api)
        return True

    def only_delete_key(self):
        if self.module.check_mode:
            return True
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            self.delete_key(api)
        return True

    def delete_cert(self, api):
        c = api.tm.sys.file.ssl_certs.ssl_cert.load(
            name=self.params.cert_filename,
            partition=self.params.partition
        )
        c.delete()
        return True

    def delete_key(self, api):
        k = api.tm.sys.file.ssl_keys.ssl_key.load(
            name=self.params.key_filename,
            partition=self.params.partition
        )
        k.delete()
        return True


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module = BigIpSslCertificateModule()

    try:
        obj = BigIpSslCertificateManager()
        obj.module = module
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
