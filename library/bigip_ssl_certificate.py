#!/usr/bin/python


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
#
# TODO: pkcs12 support when f5-sdk adds it, or convert locally to pem?
#       Would be nice if f5-sdk file upload could take a string like soap
#       cert/key import, then we could convert in memory and import
# TODO: Exception Handling

from ansible.module_utils.basic import *

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
    server:
        description:
            - BIG-IP host
        required: true
        default: null
    user:
        description:
            - BIG-IP Username
        required: true
        default: null
        aliases: [username]

    password:
        description:
            - BIG-IP Password
        required: true
        default: null
    name:
        description:
            - SSL Certificate Name.  This is the cert/key pair name used
            - when importing a certificate/key into the F5
        required: True
        default: none
    connection:
        description:
            - Connection API.  Only iControl SOAP is supported at this time
            - REST will be added when f5-sdk implements needed functionality
        required: False
        default: rest
        choices: [icontrol, rest]
        aliases: transport
    cert_format:
        description:
            - The format that the certificate file you want to import is in.
            - PEM is currently the only supported format.
            - PKCS12 will be implamented
            - when f5-sdk supports it.
        required: false
        default: pem
        choices: [pem]
    cert_pem_file:
        description:
            - Required if the format is PEM.
            - This is the filename of the certificate.
        required: False
        default: none
    key_pem_file:
        description:
            - Require if the format is PEM.
            - This is the filename of the private key,
        required: False
        default: none
    pkcs12_file:
        description:
            - Current unused
        required: False
        default: none
    pkcs12_password:
        description:
            - Currently unused
        required: False
        default: none
    validata_cert:
        description:
            - Validate the SSL certificate on the API connection
        required: False
        default: True
        choices: [true. false]
notes:
    - icontrol interface requires bigsuds module
    - SSL operations require OpenSSL module
requirements:
    - bigsuds
    - f5-sdk
author:
    - Kevin Coming <kevcom@gmail.com>

'''

EXAMPLES = '''
    - name: "Import PEM Certificate"
      local_action:
        name: certificate-name
        module: bigip_ssl_certificate
        server: bigip-addr
        username: username
        password: password
        connection: rest
        state: present
        cert_format: pem
        cert_pem_file: /path/to/cert.crt
        key_pem_file: /path/to/key.key

    - name: "Delete Certificate"
      local_action:
        name: certificate-name
        module: bigip_ssl_certificate
        server: bigip-addr
        username: username
        password: password
        state: absent
        connection: rest

'''


try:
    from OpenSSL import crypto

except:
    found_OpenSSL = False
else:
    found_OpenSSL = True

try:
    import bigsuds
except:
    bigsuds_found = False
else:
    bigsuds_found = True

try:
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
except:
    f5sdk_found = False
else:
    f5sdk_found = True


def read_file(filename):
    with open(filename) as f:
        data = f.read()
    return data


def pkcs12_to_pem(pkcs12data, password=''):
    pkcs12 = crypto.load_pkcs12(pkcs12data, password)
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                   pkcs12.get_certificate())
    return (cert, key)


class F5ModuleError(Exception):
    pass


class BigIPCommon:
    def __init__(self, hostname, username, password, verify=True):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.verify = verify
        self.api = self.connection(hostname, username, password, verify)


class BigIPiControl(BigIPCommon):
    def connection(self, hostname, username, password, verify):
        api = bigsuds.BIGIP(hostname=hostname,
                            username=username,
                            password=password,
                            verify=verify
                            )
        return api.with_session_id()

    def delete(self, name):
        changed = False
        if self.exists_cert(name + '.crt'):
            self.delete_cert(name + '.crt')
            changed = True
        if self.exists_key(name + '.key'):
            self.delete_key(name + '.key')
            changed = True
        return changed

    def delete_cert(self, name):
        self.api.Management.KeyCertificate.certificate_delete(
                mode='MANAGEMENT_MODE_DEFAULT',
                cert_ids=[name])
        return True

    def delete_key(self, name):
        self.api.Management.KeyCertificate.key_delete(
                mode='MANAGEMENT_MODE_DEFAULT',
                key_ids=[name])
        return True

    def exists_cert(self, name):
        result = self.api.Management.KeyCertificate.get_certificate_list_v2(
                    mode='MANAGEMENT_MODE_DEFAULT')
        for r in result:
            if r['file_name'].split('/')[-1] == name:
                return True

    def exists_key(self, name):
        result = self.api.Management.KeyCertificate.get_key_list(
                    mode='MANAGEMENT_MODE_DEFAULT')
        for r in result:
            if r['file_name'].split('/')[-1] == name:
                return True

    def import_cert(self, **kwargs):
        cert_format = kwargs['cert_format']
        if cert_format == 'pem':
            try:
                certname = kwargs['name']
            except KeyError:
                certname = os.path.basename(certfilename[:-4])
            try:
                certfilename = kwargs['certfilename']
            except KeyError:
                pass
            else:
                cert_data = read_file(certfilename)
                self.install_cert(certname, cert_data)
            try:
                keyfilename = kwargs['keyfilename']
            except KeyError:
                pass
            else:
                key_data = read_file(keyfilename)
                self.install_key(certname, key_data)
            return True

    def install_cert(self, name, data):
        self.api.Management.KeyCertificate.certificate_import_from_pem(
                    mode='MANAGEMENT_MODE_DEFAULT',
                    cert_ids=[name],
                    pem_data=[data],
                    overwrite=False)

    def install_key(self, name, data):
        self.api.Management.KeyCertificate.key_import_from_pem(
                    mode='MANAGEMENT_MODE_DEFAULT',
                    key_ids=[name],
                    pem_data=[data],
                    overwrite=False)


class BigIPRest(BigIPCommon):
    def connection(self, hostname, username, password, verify):
        return ManagementRoot(hostname=hostname,
                              username=username,
                              password=password)

    def delete(self, name):
        result = False
        r = self.delete_cert(name + '.crt')
        if r:
            result = True
        r = self.delete_key(name + '.key')
        if r:
            result = True
        return result

    def delete_cert(self, name):
        try:
            c = self.api.tm.sys.crypto.certs.cert.load(name=name)
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
            k = self.api.tm.sys.crypto.keys.key.load(name=name)
            k.delete()
        except iControlUnexpectedHTTPError as e:
            if e.response.status_code == 404:
                return False
            else:
                raise F5ModuleError(e)
        else:
            return True

    def exists_cert(self, name):
        return self.api.tm.sys.crypto.certs.cert.exists(name=name)

    def exists_key(self, name):
        return self.api.tm.sys.crypto.keys.key.exists(name=name)

    def import_cert(self, **kwargs):
        name = kwargs['name']
        cert_format = kwargs['cert_format']
        if cert_format == 'pem':
            try:
                certfilename = kwargs['certfilename']
            except KeyError:
                certfilename = kwargs['name'] + '.crt'
            else:
                self.upload(certfilename)
                self.install_cert(name, os.path.basename(certfilename))
            try:
                keyfilename = kwargs['keyfilename']
            except KeyError:
                pass
            else:
                self.upload(keyfilename)
                self.install_key(name, os.path.basename(keyfilename))
            return True
        elif cert_format == 'pkcs12':
            raise F5ModuleError("pkcs12 not supported by f5-sdk")

    def install_cert(self, name, certfilename):
        filename = os.path.join('/var/config/rest/downloads', certfilename)
        params = {'from-local-file': filename, 'name': name}
        self.api.tm.sys.crypto.certs.exec_cmd('install', **params)

    def install_key(self, name, keyfilename):
        filename = os.path.join('/var/config/rest/downloads', keyfilename)
        params = {'from-local-file': filename, 'name': name}
        self.api.tm.sys.crypto.keys.exec_cmd('install', **params)

    def upload(self, filename):
        self.api.shared.file_transfer.uploads.upload_file(filename)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present',
                       choices=['absent', 'present']),
            user=dict(type='str', required=True, aliases=['username']),
            password=dict(type='str', required=True, no_log=True),
            server=dict(type='str', required=True),
            name=dict(type='str', required=True),
            partition=dict(type='str', default='Common'),
            connection=dict(type='str', default='rest',
                            choices=['icontrol', 'rest'],
                            aliases=['transport']),
            cert_format=dict(type='str', default='pem',
                             choices=['pem']),
            cert_pem_file=dict(type='str'),
            key_pem_file=dict(type='str'),
            pkcs12_file=dict(type='str'),
            pkcs12_password=dict(type='str', no_log=True),
            validate_cert=dict(type='bool', default=True),
            # overwrite=dict(type='bool', default=False)
        )
    )
    result = {'changed': False}
    if module.params['connection'] == 'icontrol':
        if not bigsuds_found:
            module.fail_json(msg='connection type icontrol requires bigsuds')
        try:
            api = BigIPiControl(module.params['server'],
                                module.params['user'],
                                module.params['password'],
                                module.params['validate_cert'])
        except F5ModuleError as e:
            module.fail_json(msg='Connection Error: %s' % e)
    elif module.params['connection'] == 'rest':
        if not f5sdk_found:
            module.fail_json(msg='connection type rest requires '
                             'f5-common-python')
        api = BigIPRest(module.params['server'],
                        module.params['user'],
                        module.params['password'],
                        module.params['validate_cert'])
    else:
        module.fail_json(msg='connection type %s is unsupported' %
                         module.params['connection'])

    if module.params['state'] == 'present':
        if module.params['cert_format'] == 'pem':
            if not (module.params['key_pem_file'] and
                    module.params['cert_pem_file']):
                module.fail_json(msg='pem format requires cert_pem_file '
                                 'and key_pem_file')
            certargs = {}
            if not api.exists_cert('%s.crt' % module.params['name']):
                certargs['certfilename'] = module.params['cert_pem_file']
            if not api.exists_key('%s.key' % module.params['name']):
                certargs['keyfilename'] = module.params['key_pem_file']
            if certargs:
                certargs['name'] = module.params['name']
                certargs['cert_format'] = 'pem'
        if certargs:
            try:
                r = api.import_cert(**certargs)
            except F5ModuleError as e:
                module.fail_json(msg="F5ModuleError: %s" % e)
            else:
                if r:
                    result['changed'] = True
    elif module.params['state'] == 'absent':
        # TODO Delete cert and key separately???
        try:
            r = api.delete(module.params['name'])
        except F5ModuleError as e:
            module.fail_json(msg="F5ModuleError: %s" % e)
        except ConnectioError as e:
            module.fail_json(msg="F5ModuleError: %s" % e)
        else:
            if r is True:
                result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()
