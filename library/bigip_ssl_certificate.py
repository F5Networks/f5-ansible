#!/usr/bin/python
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
    - This module will import/delete SSL certificates on BIG-IP LTM
      systems from a certificate file on the filesystem where the playbook
      is run from.  Currently this only supports certificates to be used
      within SSL Profiles.  PEM format with certificate and key in seperate
      files, or PKCS12 format are supported.
options:
    state:
        description:
            - Node member state
        required: true
        default: present
        choices: ['present', 'absent']
        aliases: []
    server:
        description:
            - BIG-IP host
        required: true
        default: null
        choices: []
        aliases: []
    user:
        description:
            - BIG-IP Username
        required: true
        default: null
        choices: []
        aliases: [username]

    password:
        description:
            - BIG-IP Password
        required: true
        default: null
        choices: []
        aliases: []
    name:
        description:
            - SSL Certificate Name
        required: True
        default: none
        choices: []
        aliases: []
    connection:
        description:
            - Connection API.  Only iControl SOAP is supported at this time
            - REST will be added when f5-sdk implements needed functionality
        required: False
        default: icontrol
        choices: [icontrol]
        aliases: transport
    cert_format:
        description:
            - The format that the certificate file you want to import is in.
            - PCKS12 and PEM formats are supported.
        required: false
        default: pem
        choices: [pem, pcks12]
        aliases: []
    cert_pem_file:
        description:
            - Required if the format is PEM.
            - This is the filename of the certificate.
        required: False
        default: none
        choices: []
        aliases: []
    key_pem_file:
        description:
            - Require if the format is PEM.
            - This is the filename of the private key,
        required: False
        default: none
        choices: []
        aliases: []
    pkcs12_file:
        description:
            - Required if the format is pkcs12.
            - This is the filename of the pkcs12 file
        required: False
        default: none
        choices: []
        aliases: []
    pkcs12_password:
        description:
            - Required if the format is pkcs12.
            - This is the password for the pkcs12 file
        required: False
        default: none
        choices: []
        aliases: []
    validata_cert:
        description:
            - Validate the SSL certificate on the API connection
        required: False
        default: True
        choices: [true. false]
        aliases: []
    overwrite:
        description:
            - Determines if an existing certificate will be overwritten or not.
            - This will only work provided the private key is still valid.
            - You cannot overwrite both the key and the cert.
            - Please make sure you understand what this means before setting
            - to True.  It isn't useful unless you have a new cert with 
            - the same private key, such as a renewal.
        required: False
        default: False
        choices: [true, false]
        aliases: []
notes:
    - icontrol interface requires bigsuds module
    - SSL operations require OpenSSL module
requirements:
    - bigsuds
    - pyOpenSSL
author:
    - Kevin Coming <kevcom@gmail.com> (@waffie1)

'''

EXAMPLES = '''
    - name: "Import PEM Certificate"
      local_action:
        name: certificate-name
        module: bigip_ssl_certificate
        server: bigip-addr
        username: username
        password: password
        state: present
        cert_format: pem
        cert_pem_file: /path/to/cert.crt
        key_pem_file: /path/to/key.key


    - name: "Import P12 Certificate"
      local_action:
        name: certificate-name
        module: bigip_ssl_certificate
        server: bigip-addr
        username: username
        password: password
        state: present
        cert_format: pkcs12
        pkcs12_file: /path/to/cert.pkcs12
        pkcs12_password: password
        overwrite: false

    - name: "Delete Certificate"
      local_action:
        name: certificate-name
        module: bigip_ssl_certificate
        server: bigip-addr
        username: username
        password: password
        state: absent

'''


import json
from ansible.module_utils.basic import *

try:
    from OpenSSL import crypto

except:
    found_OpenSSL = False
else:
    found_OpenSSL = True

try:
    import bigsuds
except:
    found_bigsuds = False
else:
    found_bigsuds = True

# I added this asn1 checks in because I learned the hard way that
# Some versions of BIGIP store as RSA PCKS#1 and some versions store
# as PCKS#8 for the private keys.  I believe converting the PEM
# to DER should produce the same result from both PEM formats.
def certs_match(c1, c2):
    if c1 == c2:
        return True
    c1_pub = crypto.load_certificate(crypto.FILETYPE_PEM, c1)
    c2_pub = crypto.load_certificate(crypto.FILETYPE_PEM, c1)
    c1_asn1 = crypto.dump_certificate(crypto.FILETYPE_ASN1, c1_pub)
    c2_asn1 = crypto.dump_certificate(crypto.FILETYPE_ASN1, c2_pub)
    if c1_asn1 == c2_asn1:
        return True

def keys_match(k1, k2):
    if k1 == k2:
        return True
    k1_priv = crypto.load_privatekey(crypto.FILETYPE_PEM, k1)
    k2_priv = crypto.load_privatekey(crypto.FILETYPE_PEM, k2)
    k1_asn1 = crypto.dump_privatekey(crypto.FILETYPE_ASN1, k1_priv)
    k2_asn1 = crypto.dump_privatekey(crypto.FILETYPE_ASN1, k2_priv)
    if k1_asn1 == k2_asn1:
        return True

def read_file(filename):
    with open(filename) as f:
        data = f.read()
    return data

def pkcs12_to_pem(pkcs12data, password=''):
    pkcs12 = crypto.load_pkcs12(pkcs12data, password)
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
    return (cert, key)

class ConnectionError(Exception):
    pass

class APIError(Exception):
    pass

class BigIPCommon:
    def __init__(self, hostname, username, password, verify=True):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.verify = verify
        self.api = self.connection()
        self.baseurl = 'https://%s/mgmt/' % hostname



class BigIPiControl(BigIPCommon):
    def connection(self):
        api = bigsuds.BIGIP(hostname=self.hostname,
                            username=self.username,
                            password=self.password,
                            verify=self.verify
                           )
        try:
            api.with_session_id()
        except bigsuds.ConnectionError as e:
            raise ConnectionError(e.message)
        else:
            return api

    def delete_cert(self, name):
        try:
            self.api.Management.KeyCertificate.certificate_delete(
                mode='MANAGEMENT_MODE_DEFAULT',
                cert_ids=[name])
        except bigsuds.ConnectionError as e:
            raise ConnectioNError(e.message)
        except bigsuds.ServerError as e:
            raise APIError(e.message)
        else:
            return True
    def delete_key(self, name):
        try:
            self.api.Management.KeyCertificate.key_delete(
                mode='MANAGEMENT_MODE_DEFAULT',
                key_ids=[name])
        except bigsuds.ConnectionError as e:
            raise ConnectioNError(e.message)
        except bigsuds.ServerError as e:
            raise APIError(e.message)
        else:
            return True

    def export_cert(self, name):
        try:
            data = self.api.Management.KeyCertificate.certificate_export_to_pem(
                    mode='MANAGEMENT_MODE_DEFAULT',
                    cert_ids=[name])
        except bigsuds.ConnectionError as e:
            raise ConnectionError(e)
        except bigsuds.ServerError as e:
            if 'Not Found' in str(e.fault):
                return False
            else:
                raise APIError(e)
        return data[0]

    def export_key(self, name):
        try:
            data = self.api.Management.KeyCertificate.key_export_to_pem(
                    mode='MANAGEMENT_MODE_DEFAULT',
                    key_ids=[name])
        except bigsuds.ConnectionError as e:
            raise ConnectionError(e)
        except bigsuds.ServerError as e:
            if 'Not Found' in str(e.fault):
                return False
        return data[0]

    def import_cert(self, name, data, overwrite=False):
        try:
            self.api.Management.KeyCertificate.certificate_import_from_pem(
                    mode='MANAGEMENT_MODE_DEFAULT',
                    cert_ids=[name], pem_data=[data], overwrite=overwrite)
        except bigsuds.ConnectionError as e:
            raise ConnectioNError(e.message)
        except bigsuds.ServerError as e:
            raise APIError(e.message)
        else:
            return True

    def import_key(self, name, data, overwrite=False):
        try:
            self.api.Management.KeyCertificate.key_import_from_pem(
                    mode='MANAGEMENT_MODE_DEFAULT',
                    key_ids=[name], pem_data=[data], overwrite=overwrite)
        except bigsuds.ConnectionError as e:
            raise ConnectioNError(e.message)
        except bigsuds.ServerError as e:
            raise APIError(e.message)
        else:
            return True


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state = dict(type='str', default='present',
                    choices = ['absent', 'present']),
            user = dict(type='str', required=True, aliases=['username']),
            password = dict(type='str', required=True),
            server = dict(type='str', required=True),
            name = dict(type='str', required=True),
            partition = dict(type='str', default='Common'),
            connection = dict(type='str', default='icontrol',
                    choices=['icontrol', 'rest'], aliases=['transport']),
            cert_format = dict(type='str', default='pem',
                    choices=['pem', 'pkcs12']),
            cert_pem_file = dict(type='str'),
            key_pem_file = dict(type='str'),
            pkcs12_file = dict(type='str'),
            pkcs12_password = dict(type='str'),
            validate_cert = dict(type='bool', default=True),
            overwrite = dict(type='bool', default=False)
        )
    )
    result = {'changed' : False}
    if module.params['connection'] == 'icontrol':
        if not found_bigsuds:
            module.fail_json(msg='connection type icontrol requires bigsuds')
        try:
            api = BigIPiControl(module.params['server'], module.params['user'],
                module.params['password'], module.params['validate_cert'])
        except ConnectionError as e:
            module.fail_json(msg='Connection Error: %s' % e)
    elif module.params['connection'] == 'rest':
        module.fail_json(msg='REST API will not be implemented')
    else:
        module.fail_json(msg='connection type %s is unsupported' %
                module.params['connection'])
    if module.params['state'] == 'present':
        if module.params['cert_format'] == 'pkcs12':
            if not found_OpenSSL:
                module.fail_json(msg='P12 certificate format requires OpenSSL')
            if not module.params['pkcs12_password']:
                module.fail_json(
                        msg='pkcs12_password required for pkcs12 certs')
            if not module.params['pkcs12_file']:
                module.fail_json(msg='pkcs12_file required for pkcs12 certs')
            try:
                pkcs12_data = read_file(module.params['pkcs12_file'])
                cert_data, key_data = pkcs12_to_pem(pkcs12_data,
                        module.params['pkcs12_password'])
            except IOError as e:
                module.fail_json(msg='Error opening certificate file: %s' % e)
            except crypto.Error as e:
                module.fail_json(msg='Error converting pkcs12 file to pem: %s'
                        % e)
        elif module.params['cert_format'] == 'pem':
            if not (module.params['key_pem_file'] and
                        module.params['cert_pem_file']):
                module.fail_json(msg='pem format requires cert_pem_file '
                        'and key_pem_file')
            try:
                cert_data = read_file(module.params['cert_pem_file'])
            except IOError as e:
                module.fail_json(msg='Error opening certificate file: %s' % e)
            try:
                key_data = read_file(module.params['key_pem_file'])
            except IOError as e:
                module.fail_json(msg='Error opening key file: %s' % e)

        try:
            cert_on_bigip = api.export_cert(module.params['name'])
            key_on_bigip = api.export_key(module.params['name'])
            if not cert_on_bigip:
                api.import_cert(module.params['name'], cert_data,
                        module.params['overwrite'])
                result['changed'] = True
            elif not certs_match(cert_on_bigip, cert_data):
                if not module.params['overwrite']:
                    module.fail_json( msg='overwrite is False but '
                            'certificate on device is different')
                api.import_cert(module.params['name'], cert_data,
                            module.params['overwrite'])
                result['changed'] = True
            if not key_on_bigip:
                api.import_key(module.params['name'], key_data,
                        module.params['overwrite'])
                result['changed'] = True
            elif not keys_match(key_on_bigip, key_data):
                if not module.params['overwrite']:
                    module.fail_json(msg='overwrite is False but key on '
                            'device is different')
                api.import_key(module.params['name'], key_data,
                            module.params['overwrite'])
                result['changed'] = True
        except ConnectionError as e:
            module.fail_json(msg='Connection Error: %s' % e)
        except APIError as e:
            module.fail_json(msg='API Error: %s' % e)
    else:
        try:
            if api.export_cert(module.params['name']):
                api.delete_cert(module.params['name'])
                result['changed'] = True
            if api.export_key(module.params['name']):
                api.delete_key(module.params['name'])
                result['changed'] = True
        except ConnectionError as e:
            module.fail_json(msg='Connection Error: %s' % e)
        except APIError as e:
            module.fail_json(msg='API Error: %s' % e)
    module.exit_json(**result)

if __name__ == '__main__':
    main()
