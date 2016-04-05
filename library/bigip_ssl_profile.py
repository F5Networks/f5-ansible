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
short_description: A module to manage SSL profiles
description:
    - This module will manage SSL Profiles on F5 BIG-IP LTM systems.
      Options not specified in your playbook will not be modified on the
      destination LTM.  For most options, a value of 'default' will set the
      option back to inherit from the parent profile.
      Currently, only ClientSSL profiles are supported, with only
      the options listed below.

version_added: ".1"
author: "Kevin Coming <kevcom@gmail.com>"
notes:
    - "Requires BIG-IP software version >= 11.5"
    - "Best run as a local_action in your playbook"
requirements:
    - "bigsuds"


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
            - SSL Profile Name
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
    partition:
        description:
            - BIG-IP Partition that node resides in
        required: False
        default: Common
        choices: []
        aliases: []
    profile_type:
        description:
            - SSL Profile type.  Currently only clientssl is supported.
        required: False
        default: clientssl
        choices: [clientssl]
        aliases: []
    chain:
        description:
            - Specifies the ssl certificate chain file to be used 
        required: False
        default: none
        choices: []
        aliases: []
    parent:
        description:
            - Specifies the parent ssl profile to inhert.
        required: False
        default: clientssl
        choices: []
        aliases: []
    renegotiation:
        description:
            - Enable/Disable Secure Renegotiation 
        required: False
        default: none
        choices: [default, enabled, disabled]
    renegotiation_mode:
        description:
            - Set secure renegotiation mode
        required: False
        default: none
        choices: [default, request, require, strict]
    renegotiation_period:
        description:
            - Specifies renegotiation period, in seconds.  -1 is indefinite.
        required: False
        default: none
        choices: []
        aliases: []
    renegotiation_size:
        description:
            - Specifies renegotiation size, in megabytes.  -1 is indefinite.
        required: False
        default: none
        choices: []
        aliases: []
    renegotiation_max_record_delay:
        description:
            - Specifies renegotiation max records, in records
        required: False
        default: none
        choices: []
        aliases: []
    cert:
        description:
            - SSL certificate filename to be used in the ssl profile
        required: False
        default: none
        choices: []
        aliases: []
    key:
        description:
            - SSL key to be used in the ssl profile
        required: False
        default: none
        choices: []
        aliases: []
    passphrase:
        description:
            - Passphrase for the SSL key
        required: False
        default: none
        choices: []
        aliases: []
    cipher_list:
        description:
            - A list of SSL ciphers to be used.  If 'default' is in the list,
              the ciphers will be set to inerit from the parent profile.
              Also note, 'DEFAULT' differs from 'default', as 'DEFAULT'
              sets the DEFAULT in the cipher list on the device, and 'default'
              set the ciphers to inherit from the parent profile.  Also, you
              probably need quotes around expressions that start with special
              characters, i.e. !
        required: False
        default: none
        choices: [ [] ]
        aliases: [ciphers]
    option_list:
        description:
            - A list of SSL options to be used.  If 'default' is in the list,
              the options will be set to inherit from the parent profile.
              If 'none' is in the list, options on device will be set to
              'All Options Disabled'
        required: False
        default: none
        choices: [ [] ]
        aliases: [options]
    validate_cert:
        description:
            -Specifies if the SSL connection to the BIG-IP will be validated.
        required: False
        default: True
        choices: [True, False]
        aliases: []
'''
EXAMPLES = '''
  - name: Create Client SSL Profile
  local_action:
      name: test_ClientSSL
      module: bigip_ssl_profile
      server: f5_ltm_hostname
      username: username
      password: password
      state: present
      partition: Common
      certificate: testcert.crt
      key: testcert.key
      profile_type: clientssl
      option_list:
          - SSL_OPTION_NO_SSL_V2
          - SSL_OPTION_CIPHER_SERVER_PREFERENCE
          - SSL_OPTION_DONT_INSERT_EMPTY_FRAGMENTS
      cipher_list:
          - 'DEFAULT'
          - '!RC4'
      renegotiation: enabled
      renegotiation_mode: strict
'''

from ansible.module_utils.basic import *
try:
    import bigsuds
except:
    found_bigsuds = False
else:
    found_bigsuds = True

class ConnectionError(Exception):
    pass

class APIError(Exception):
    pass

class BigIPCommon:
    def __init__(self, **kwargs):
        self.server = kwargs['server']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.verify = kwargs['validate_cert']
        self.profile_type = kwargs['profile_type']
        self.api = self.client()
        self.apiPath = self.set_apiPath()



class BigIPiControlCommon(BigIPCommon):
    def client(self):
        api = bigsuds.BIGIP(hostname=self.server,
                            username=self.username,
                            password=self.password,
                            verify=self.verify
                           )
        try:
            api = api.with_session_id()
        except bigsuds.ConnectionError as e:
            raise ConnectionError(e.message)
        else:
            return api

class BigIPiControlClient(BigIPiControlCommon):

    def set_apiPath(self):
        return self.api.LocalLB.ProfileClientSSL

    def add_certificate_key_chain(self, name, cert, key):
        key_chain_obj = cert.split('.')[0]
        self.apiPath.add_certificate_key_chain([name], [[key_chain_obj]],
            [[{'cert' : cert, 'key' : key}]])

    def create(self, name, cert, key):
        self.apiPath.create_v2(
                        [name],
                        [{'value' : key,
                          'default_flag' : False}],
                        [{'value' : cert,
                          'default_flag' : False}]
                        )

    def create_profile(self, params):
        try:
            with bigsuds.Transaction(self.api):
                self.create(params['name'], params['cert'], params['key'])
                if params['cipher_list']:
                    self.set_cipher_list(params['name'], params['cipher_list'])
                if params['parent']:
                    self.set_default_profile(params['name'], params['parent'])
                if params['passphrase']:
                    self.set_passphrase(params['name'], params['passphrase'])
                if params['renegotiation']:
                    self.set_renegotiation_state(params['name'],
                            params['renegotiation'])
                if params['renegotiation_mode']:
                    self.set_renegotiation_mode(params['name'],
                            params['renegotiation_mode'])
                if params['option_list']:
                    if 'none' in params['option_list']:
                        params['option_list'] = []
                    self.set_ssl_option(params['name'], params['option_list'])
                if params['renegotiation_period']:
                    self.set_renegotiation_period(params['name'],
                            params['renegotiation_period'])
                if params['renegotiation_size']:
                    self.set_renegotiation_size(params['name'],
                            params['renegotiation_size'])
                if params['renegotiation_max_record_delay']:
                    self.set_renegotiation_max_record_delay(params['name'],
                            params['renegotiation_max_record_delay'])
            # There is probably a better way to deal with this, but
            # I cannot set the chain until the transaction commits.
            if params['chain']:
                self.set_chain_file(params['name'], params['chain'])
        except bigsuds.ConnectionError as e:
            raise ConnectionError(e.message)
        except bigsuds.ServerError as e:
            raise APIError(e.message)
        else:
            return True

    def delete_profile(self, name):
        self.apiPath.delete_profile([name])
        return True

    def get_certificate_key_chain_name(self, name):
        r = self.apiPath.get_certificate_key_chain([name])
        if r:
            return r[0][0]
        else:
            return False
    def get_chain_file(self, profile, keychain):
        r = self.apiPath.get_certificate_key_chain_chain_file([profile], 
            [[keychain]])
        if r:
            return r[0][0]
        else:
            return False

    def get_certificate_file(self, profile, keychain):
        r = self.apiPath.get_certificate_key_chain_certificate_file(
                [profile], [[keychain]])
        if r:
            return r[0][0]
        else:
            return False

    def get_cipher_list(self, name):
        r = self.apiPath.get_cipher_list([name])[0]
        if r['default_flag']:
            return ['default']
        else:
            return r['values']

    def get_default_profile(self, name):
        return self.apiPath.get_default_profile([name])[0]

    def get_key_file(self, profile, keychain):
        r = self.apiPath.get_certificate_key_chain_key_file(
                [profile], [[keychain]])
        if r:
            return r[0][0]
        else:
            return False

    def get_renegotiation_max_record_delay(self, name):
        r = self.apiPath.get_renegotiation_maximum_record_delay([name])[0]
        if r['default_flag']:
            return 'default'
        else:
            return str(r['value'])

    def get_renegotiation_mode(self, name):
        r = self.apiPath.get_secure_renegotiation_mode([name])[0]
        if r['default_flag']:
            return 'default'
        elif r['value'] == 'SECURE_RENEGOTIATION_MODE_REQUEST':
            return 'request'
        elif r['value'] == 'SECURE_RENEGOTIATION_MODE_REQUIRE':
            return 'require'
        elif r['value'] == 'SECURE_RENEGOTIATION_MODE_REQUIRE_STRICT':
            return 'strict'

    def get_renegotiation_period(self, name):
        r = self.apiPath.get_renegotiation_period([name])[0]
        if r['default_flag']:
            return 'default'
        else:
            return str(r['value'])

    def get_renegotiation_state(self, name):
        r = self.apiPath.get_renegotiation_state([name])[0]
        if r['default_flag']:
            return 'default'
        elif r['value'] == 'STATE_ENABLED':
            return 'enabled'
        elif r['value'] == 'STATE_DISABLED':
            return['disabled']

    def get_renegotiation_size(self, name):
        r = self.apiPath.get_renegotiation_throughput([name])[0]
        if r['default_flag']:
            return 'default'
        else:
            return str(r['value'])

    def get_ssl_option(self, name):
        r = self.apiPath.get_ssl_option([name])[0]
        if r['default_flag']:
            return ['default']
        else:
            return r['values']


    def modify_profile(self, params):
        #chain
        changed = False
        try:
            with bigsuds.Transaction(self.api):
                if params['cert'] or params['key']:
                    keychain = self.get_certificate_key_chain_name(
                            params['name'])
                    current_cert = self.get_certificate_file(params['name'],
                            keychain)
                    current_key = self.get_key_file(params['name'],
                            keychain)
                    if not (params['cert'] == current_cert and
                        params['key'] == current_key):
                        if not keychain:
                            self.add_certificate_key_chain(params['name'],
                                    params['cert'],
                                    params['key'])
                            self.remove_certificate_key_chain(params['name'],'')
                            changed = True
                        else:
                            self.set_certificate_key(params['name'],
                                    params['cert'],
                                    params['key'],
                                    keychain)
                            changed = True

                    elif params['cert'] != current_cert:
                        self.set_certificate_file(params['name'],
                                params['cert'],
                                keychain)
                        changed = True

                if params['chain'] != None:
                    current = self.get_chain_file(params['name'], keychain)
                    if params['chain'] != current:
                        self.set_chain_file(params['name'], params['chain'])
                        changed = True
                if params['option_list']:
                    current = self.get_ssl_option(params['name'])
                    if 'none' in params['option_list']:
                        self.set_ssl_option(params['name'], [])
                        changed = True
                    elif ('default' in params['option_list'] and not
                                'default' in current):
                        self.set_ssl_option(params['name'], 'default')
                        changed = True
                    elif not set(current) == set(params['option_list']):
                        self.set_ssl_option(params['name'], params['option_list'])
                        changed = True
                if params['cipher_list']:
                    current = self.get_cipher_list(params['name'])
                    if  ('default' in params['cipher_list'] and not
                                'default' in current):
                        self.set_cipher_list(params['name'], 'default')
                        changed = True
                    elif not set(current) == set(params['cipher_list']):
                        self.set_cipher_list(params['name'], params['cipher_list'])
                        changed = True
                if params['renegotiation']:
                    current = self.get_renegotiation_state(params['name'])
                    if (params['renegotiation']  == 'default' and not
                                current == 'default'):
                        self.set_renegotiation_state(params['name'], 'default')
                        changed = True
                    elif current != params['renegotiation']:
                        self.set_renegotiation_state(params['name'],
                                params['renegotiation'])
                        changed = True
                if params['renegotiation_mode']:
                    current = self.get_renegotiation_mode(params['name'])
                    if (params['renegotiation_mode'] == 'default' and not
                                current == 'default'):
                        self.set_renegotiation_mode(params['name'], 'default')
                        changed = True
                    elif current != params['renegotiation_mode']:
                        self.set_renegotiation_mode(params['name'],
                                params['renegotiation_mode'])
                        changed = True
                if params['renegotiation_period']:
                    current = self.get_renegotiation_period(params['name'])
                    if (params['renegotiation_period'] == 'default' and not
                                current == 'default'):
                        self.set_renegotiation_period(params['name'], 'default')
                        changed = True
                    elif current != params['renegotiation_period']:
                        self.set_renegotiation_period(params['name'],
                                params['renegotiation_period'])
                        changed = True
                if params['renegotiation_size']:
                    current = self.get_renegotiation_size(params['name'])
                    if (params['renegotiation_size'] == 'default' and not
                                current == 'default'):
                        self.set_renegotiation_size(params['name'], 'default')
                        changed = True
                    elif current != params['renegotiation_size']:
                        self.set_renegotiation_size(params['name'],
                                params['renegotiation_size'])
                        changed = True
                if params['renegotiation_max_record_delay']:
                    current = self.get_renegotiation_max_record_delay(
                            params['name'])
                    if (params['renegotiation_max_record_delay'] == 'default' and not
                                current == 'default'):
                        self.set_renegotiation_max_record_delay(params['name'], 'default')
                        changed = True
                    elif current != params['renegotiation_max_record_delay']:
                        self.set_renegotiation_max_record_delay(params['name'],
                                                      params['renegotiation_max_record_delay'])
                        changed = True
                if params['parent']:
                    current = self.get_default_profile(params['name'])
                    if current != params['parent']:
                        self.set_default_profile(params['name'],
                                params['parent'])
                        changed = True
        except bigsuds.ConnectionError as e:
            raise ConnectionError(e.message)
        except bigsuds.ServerError as e:
            raise APIError(e.message)
        except bigsuds.ArgumentError as e:
            raise APIError(e.message)
        else:
            return changed

    def profile_exists(self, name):
        profile_list = self.apiPath.get_list()
        if name in profile_list:
            return True

    def remove_certificate_key_chain(self, name, keychain):
        self.apiPath.remove_certificate_key_chain([name], [[keychain]])

    def set_certificate_key(self, profile, cert, key, keychain):
        self.apiPath.set_certificate_key_chain_members([profile], [[keychain]],
                        [[{'cert' : cert, 'key' : key}]])

    def set_chain_file(self, name, value):
        if value:
            self.apiPath.set_chain_file_v2(
                        [name],
                        [{'value' : value,
                          'default_flag' : False}]
                        )
        else:
            self.apiPath.set_chain_file_v2(
                        [name],
                        [{'default_flag' : True}]
                        )

    def set_cipher_list(self, name, value_list):
        if 'default' in value_list:
            ProfileStringArray = {'default_flag' : True}
        else:
            ProfileStringArray = {'values' : value_list,
                                  'default_flag' : False}
        self.apiPath.set_cipher_list(
                        [name], [ProfileStringArray])

    def set_default_profile(self, name, value):
        self.apiPath.set_default_profile(
                        [name],[value])

    def set_passphrase(self, name, value):
        ProfileString = {'value' : value,
                         'default_flag' : False}
        self.apiPath.set_passphrase(
                        [name], [ProfileString])

    def set_renegotiation_mode(self, name, value):
        if value == 'request':
            value = 'SECURE_RENEGOTIATION_MODE_REQUEST'
        elif value == 'require':
            value = 'SECURE_RENEGOTIATION_MODE_REQUIRE'
        elif value == 'strict':
            value = 'SECURE_RENEGOTIATION_MODE_REQUIRE_STRICT'
        if value == 'default':
            #This errors out if you don't pass a valid mode, and even
            #errors out with the unknown mode.  The below value
            #is ignored since the flag it True, but it needs to be set
            #or this returns InvalidArgument
            ProfileSecureRenegotiationMode = {
                        'value' : 'SECURE_RENEGOTIATION_MODE_REQUEST',
                        'default_flag' : True}
        else:
            ProfileSecureRenegotiationMode = {'value' : value,
                                              'default_flag' : False}
        self.apiPath.set_secure_renegotiation_mode(
                        [name], [ProfileSecureRenegotiationMode])

    def set_renegotiation_max_record_delay(self, name, value):
        if 'default' in value:
            ProfileULong = {'default_flag' : True, 'value' : -1}
        else:
            ProfileULong = {'default_flag' : False, 'value' : int(value)}
        self.apiPath.set_renegotiation_maximum_record_delay([name], [ProfileULong])

    def set_renegotiation_period(self, name, value):
        if 'default' in value:
            ProfileULong = {'default_flag' : True, 'value' : -1}
        else:
            ProfileULong = {'default_flag' : False, 'value' : int(value)}
        self.apiPath.set_renegotiation_period([name], [ProfileULong])

    def set_renegotiation_size(self, name, value):
        if 'default' in value:
            ProfileULong = {'default_flag' : True, 'value' : -1}
        else:
            ProfileULong = {'default_flag' : False, 'value' : int(value)}
        self.apiPath.set_renegotiation_throughput([name], [ProfileULong])

    def set_renegotiation_state(self, name, state):
        if state == 'enabled':
            ProfileEnabledState = {'value' : 'STATE_ENABLED',
                                   'default_flag' : False}
        elif state == 'disabled':
            ProfileEnabledState = {'value' : 'STATE_DISABLED',
                                   'default_flag' : False}
        elif state == 'default':
            #This errors out if you don't pass a valid state. The below value
            #is ignored since the flag it True, but it needs to be set
            #or this returns InvalidArgument
            ProfileEnabledState = {'value' : 'STATE_ENABLED',
                                   'default_flag' : True}
        self.apiPath.set_renegotiation_state(
                        [name], [ProfileEnabledState])

    def set_ssl_option(self, name, value_list):
        if 'default' in value_list:
            ProfileSSLOption = {'default_flag' : True}
        else:
            ProfileSSLOption = {'values' : value_list,
                                'default_flag' : False}
        self.apiPath.set_ssl_option([name],
                        [ProfileSSLOption])


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
            profile_type = dict(type='str', default='clientssl',
                    choices=['clientssl', 'serverssl']),
            chain = dict(type='str'),
            parent = dict(type='str', default='clientssl'),
            renegotiation=dict(type='str',
                    choices=['enabled', 'disabled', 'default']),
            renegotiation_mode=dict(type='str',
                    choices=['strict', 'request', 'require', 'default']),
            renegotiation_period=dict(type='str'),
            renegotiation_size=dict(type='str'),
            renegotiation_max_record_delay=dict(type='str'),
            cert = dict(type='str', required=False,),
            key = dict(type='str', required=False),
            passphrase = dict(type='str'),
            cipher_list = dict(type='list', aliases=['ciphers']),
            option_list = dict(type='list', aliases=['options']),
            validate_cert = dict(type='bool', default=True)
        )
    )
    result = {'changed' : False}
    for x in ['name', 'cert', 'key', 'chain', 'parent']:
        if (module.params[x] != 'default' and
                module.params[x] and not module.params[x].startswith('/')):
            module.params[x] = '/%s/%s' % (module.params['partition'],
                                           module.params[x])
    if module.params['connection'] == 'icontrol':
        if found_bigsuds:
            if module.params['profile_type'] == 'clientssl':
                api = BigIPiControlClient(**module.params)
                #api.profile_type(module.params['profile_type'])
            else:
                module.fail_json(msg="serverssl not implemented")
        else:
            module.fail_json(msg="bigsuds is required for icontrol connections")
    elif module.params['connection'] == 'rest':
        module.fail_json(msg='rest not implemented')
    if module.params['state'] == 'present':
        try:
            if api.profile_exists(module.params['name']):
                result['changed'] = api.modify_profile(module.params)
            else:
                #Add check that certificate and key are present
                result['changed'] = api.create_profile(module.params)
        except APIError as e:
            module.fail_json(msg="APIError: %s" % e)
        except ConnectionError as e:
            module.fail_json(msg="Connection Error: %s" % e)
    else:
        api.delete_profile(module.params['name'])
        result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()

