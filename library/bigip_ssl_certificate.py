#!/usr/bin/python
#
# (c) 2016, Kevin Coming (@waffie1)
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

DOCUMENTATION = '''
module: bigip_ssl_certificate
short_description: Import/Delete certificates from BIG-IP
description:
  - This module will import/delete SSL certificates on BIG-IP LTM.
    Certificates can be imported from certificate and key files on the local
    disk, in PEM format.
    Currently lacking the ability to compare/modify, import will exit
    unchanged if a certificate with the same name already exists and state is
    present.
version_added: 2.2
options:
  state:
    description:
      - Certificate state, determines if certificate is imported or deleted
    required: true
    default: present
    choices:
      - present
      - absent
  server:
    description:
      - BIG-IP host
    required: true
  server_port:
    description:
      - BIG-IP server port
    required: false
    default: 443
  user:
    description:
      - BIG-IP Username
    required: true
  password:
    description:
      - BIG-IP Password
    required: true
  partition:
    description:
      - BIG-IP partition to use when adding/deleting certificate
    required: false
    default: Common
  validate_certs:
    description:
      - Assuming this should not validate the SSL certificate of the BIG-IP
        for self signed certs, but f5-sdk does not appear to support this.
    required: false
    default: true
    choices:
      - true
      - false
  name:
    description:
      - SSL Certificate Name.  This is the cert/key pair name used
        when importing a certificate/key into the F5.  It also
        determines the filenames of the objects on the LTM
        (:Partition:name.cer_11111_1 and :Partition_name.key_11111_1)
    required: true
    default: none
  cert_pem_file:
    description:
      - Required if state is present
      - This is the local filename of the certificate.
    required: false
    default: none
  key_pem_file:
    description:
      - Require if state is present
      - This is the local filename of the private key,
    required: false
    default: none
  passphrase:
    description:
      - Passphrase on certificate private key
    required: false
requirements:
    - f5-sdk >= 0.1.7
    - BigIP >= v12
author:
    - Kevin Coming (@waffie1)
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: "Import PEM Certificate"
    local_action:
    name: certificate-name
    module: bigip_ssl_certificate
    server: bigip-addr
    user: username
    password: password
    state: present
    cert_format: pem
    cert_pem_file: /path/to/cert.crt
    key_pem_file: /path/to/key.key

- name: "Delete Certificate"
  bigip_ssl_certificate
    name: "certificate-name"
    server: "bigip-addr"
    user: username
    password: password
    state: absent
'''

RETURN = """
"""


try:
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


class BigIpSslCertificate(object):
    def __init__(self, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])
        self.params = kwargs

    def delete_cert(self, name):
        try:
            c = self.api.tm.sys.crypto.certs.cert.load(
                name=name,
                partition=self.params['partition']
            )
            c.delete()
        except iControlUnexpectedHTTPError as e:
            if e.response.status_code == 404:
                return False
            else:
                raise F5ModuleError(e)
        else:
            return True

    def delete_key(self, name):
        try:
            k = self.api.tm.sys.crypto.keys.key.load(
                name=name,
                partition=self.params['partition']
            )
            k.delete()
        except iControlUnexpectedHTTPError as e:
            if e.response.status_code == 404:
                return False
            else:
                raise F5ModuleError(e)
        else:
            return True

    def exists_cert(self, name):
        return self.api.tm.sys.crypto.certs.cert.exists(
            name=name,
            partition=self.params['partition']
        )

    def exists_key(self, name):
        return self.api.tm.sys.crypto.keys.key.exists(
            name=name,
            partition=self.params['partition']
        )

    def flush(self):
        result = {'changed': False}
        if self.params['state'] == 'present':
            if 'cert_pem_file' not in self.params:
                raise F5ModuleError('cert_pem_file required when state '
                                    'is present')
            if 'key_pem_file' not in self.params:
                raise F5ModuleError('key_pem_file required when state '
                                    'is present')
            try:
                if self.exists_cert('%s.crt' % self.params['name']):
                    return result
                if self.exists_key('%s.key' % self.params['name']):
                    return result
                self.import_cert()
                result['changed'] = True
            except iControlUnexpectedHTTPError as e:
                raise F5ModuleError(str(e))
        else:
            try:
                if self.exists_cert('%s.crt' % self.params['name']):
                    r = self.delete_cert('%s.crt' % self.params['name'])
                    if r:
                        result['changed'] = True
                if self.exists_key('%s.key' % self.params['name']):
                    r = self.delete_key('%s.key' % self.params['name'])
                    if r:
                        result['changed'] = True
            except iControlUnexpectedHTTPError as e:
                raise F5ModuleError(str(e))
        return result

    def import_cert(self):
        self.upload(self.params['cert_pem_file'])
        self.install_cert(os.path.basename(self.params['cert_pem_file']))
        self.upload(self.params['key_pem_file'])
        self.install_key(os.path.basename(self.params['key_pem_file']))

    def install_cert(self, certfilename):
        filename = os.path.join('/var/config/rest/downloads', certfilename)
        params = {'from-local-file': filename,
                  'name': self.params['name'],
                  'partition': self.params['partition']}
        self.api.tm.sys.crypto.certs.exec_cmd('install', **params)

    def install_key(self, keyfilename):
        filename = os.path.join('/var/config/rest/downloads', keyfilename)
        params = {'from-local-file': filename,
                  'name': self.params['name'],
                  'partition': self.params['partition']}
        if self.params['passphrase']:
            params['passphrase'] = self.params['passphrase']
        self.api.tm.sys.crypto.keys.exec_cmd('install', **params)

    def upload(self, filename):
        self.api.shared.file_transfer.uploads.upload_file(filename)


def main():
    argument_spec = f5_argument_spec()
    meta_args = dict(
        name=dict(type='str', required=True),
        cert_pem_file=dict(type='str'),
        key_pem_file=dict(type='str'),
        passphrase=dict(type='str'),
    )
    argument_spec.update(meta_args)
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        obj = BigIpSslCertificate(**module.params)
        result = obj.flush()
    except F5ModuleError as e:
        module.fail_json(msg=str(e))
    module.exit_json(**result)

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
