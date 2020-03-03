#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
---
module: bigip_device_auth
short_description: Manage system authentication on a BIG-IP
description:
  - Manage the system authentication configuration. This module can assist in configuring
    a number of different system authentication types. Note that this module can not be used
    to configure APM authentication types.
version_added: 2.7
options:
  type:
    description:
      - The authentication type to manage with this module.
      - Take special note that the parameters supported by this module will vary depending
        on the C(type) that you are configuring.
      - This module only supports a subset, at this time, of the total available auth types.
    type: str
    choices:
      - radius
      - tacacs
      - local
  servers:
    description:
      - Specifies a list of the IPv4 addresses for servers using the Terminal
        Access Controller Access System (TACACS)+ protocol with which the system
        communicates to obtain authorization data.
      - Specifies a list of the IPv4 addresses for servers using the RADIUS protocol with which the system
        communicates to obtain authorization data   
      - For each address, an alternate TCP port number may be optionally specified
        by specifying the C(port) key.
      - If no port number is specified, the default port C(49163) is used.
      - This parameter is supported by the C(tacacs) type.
    type: raw
    suboptions:
      address:
        description:
          - The IP address of the server.
          - This field is required, unless you are specifying a simple list of servers.
            In that case, the simple list can specify server IPs. See examples for
            more clarification.
      port:
        description:
          - The port of the server.           
  secret:
    description:
      - Secret key used to encrypt and decrypt packets sent or received from the
        server.
      - B(Do not) use the pound/hash sign in the secret for TACACS+ servers.
      - When configuring TACACS+ auth for the first time, this value is required.
      - When configuring RADIUS auth, provide 
    type: str
  service_name:
    description:
      - Specifies the name of the service that the user is requesting to be
        authorized to use.
      - Identifying what the user is asking to be authorized for, enables the
        TACACS+ server to behave differently for different types of authorization
        requests.
      - When configuring this form of system authentication, this setting is required.
      - Note that the majority of TACACS+ implementations are of service type C(ppp),
        so try that first.
    type: str
    choices:
      - slip
      - ppp
      - arap
      - shell
      - tty-daemon
      - connection
      - system
      - firewall
  timeout:
    description: 
      - This setting applies only for RADIUS.
      - Specifies the timeout value in seconds.
    type: str
    default: 3
  retries:
    description:
      - This setting applies only for RADIUS.
      - Specifies the number of authentication retries that the BIG-IP local traffic management system allows before authentication fails. 
    default: 3
    choices:
      - 0
      - 1
      - 2
      - 3
      - 4
      - 5      
  service_type:
    description: 
      - Specifies the type of service requested from the RADIUS server. The default value is authenticate-only
    type: str
    choices: 
      - authenticate-only
      - login
      - default
      - framed
      - callback-login
      - callback-framed
      - outbound
      - administrative
      - nas-prompt
      - callback-nas-prompt
      - call-check
      - callback-administrative
  protocol_name:
    description:
      - Specifies the protocol associated with the value specified in C(service_name),
        which is a subset of the associated service being used for client authorization
        or system accounting.
      - Note that the majority of TACACS+ implementations are of protocol type C(ip),
        so try that first.
    type: str
    choices:
      - lcp
      - ip
      - ipx
      - atalk
      - vines
      - lat
      - xremote
      - tn3270
      - telnet
      - rlogin
      - pad
      - vpdn
      - ftp
      - http
      - deccp
      - osicp
      - unknown
  authentication:
    description:
      - Specifies the process the system employs when sending authentication requests.
      - When C(use-first-server), specifies that the system sends authentication
        attempts to only the first server in the list.
      - When C(use-all-servers), specifies that the system sends an authentication
        request to each server until authentication succeeds, or until the system has
        sent a request to all servers in the list.
      - This parameter is supported by the C(tacacs) type.
    type: str
    choices:
      - use-first-server
      - use-all-servers
  accounting:
    description:
      - Specifies how the system returns accounting information, such as which services
        users access and how much network resources they consume, to the TACACS+ server.
      - When C(send-to-first-server), specifies that the system transmits accounting
        information back to the first available TACACS+ server in the list.
      - When C(send-to-all-servers), specifies that the system transmits accounting
        information back to all TACACS+ servers in the list.
      - This parameter is supported by the C(tacacs) type.
    version_added: "f5_modules 1.1"
    type: str
    choices:
      - send-to-first-server
      - send-to-all-servers
  use_for_auth:
    description:
      - Specifies whether or not this auth source is put in use on the system.
    type: bool
  state:
    description:
      - The state of the authentication configuration on the system.
      - When C(present), guarantees that the system is configured for the specified C(type).
      - When C(absent), sets the system auth source back to C(local).
    type: str
    choices:
      - absent
      - present
    default: present
  update_secret:
    description:
      - C(always) will allow to update secrets if the user chooses to do so.
      - C(on_create) will only set the secret when a C(use_auth_source) is C(yes)
        and TACACS+ is not currently the auth source.
    type: str
    choices:
      - always
      - on_create
    default: always
extends_documentation_fragment: f5networks.f5_modules.f5
author:
  - Tim Rupp (@caphrim007)
  - Nitin Khanna (@nitinthewiz)
  - Andrey Kashcheev (@andreykashcheev)
'''

EXAMPLES = r'''
- name: Set the system auth to RADIUS, default server port
  bigip_device_auth:
    type: radius
    secret: secret
    servers:
      - address: 10.10.10.10
      port: 1812
    state: present
    use_for_auth: yes
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost
  
- name: Set the system auth to TACACS+, default server port
  bigip_device_auth:
    type: tacacs
    authentication: use-all-servers
    accounting: send-to-all-servers
    protocol_name: ip
    secret: secret
    servers:
      - 10.10.10.10
      - 10.10.10.11
    service_name: ppp
    state: present
    use_for_auth: yes
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost

- name: Set the system auth to TACACS+, override server port
  bigip_device_auth:
    type: tacacs
    authentication: use-all-servers
    protocol_name: ip
    secret: secret
    servers:
      - address: 10.10.10.10
        port: 1234
      - 10.10.10.11
    service_name: ppp
    use_for_auth: yes
    state: present
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost
'''

RETURN = r'''
servers:
  description: List of servers used in TACACS authentication.
  returned: changed
  type: list
  sample: ['1.2.2.1', '4.5.5.4']
authentication:
  description: Process the system uses to serve authentication requests when using TACACS.
  returned: changed
  type: str
  sample: use-all-servers
accounting:
  description: Which servers to send information to when using TACACS.
  returned: changed
  type: str
  sample: send-to-all-servers
service_name:
  description: Name of the service the user is requesting to be authorized to use.
  returned: changed
  type: str
  sample: ppp
protocol_name:
  description: Name of the protocol associated with C(service_name) used for client authentication.
  returned: changed
  type: str
  sample: ip
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import string_types

try:
    from library.module_utils.network.f5.bigip import F5RestClient
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import f5_argument_spec
except ImportError:
    from ansible_collections.f5networks.f5_modules.plugins.module_utils.bigip import F5RestClient
    from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import F5ModuleError
    from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import AnsibleF5Parameters
    from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import f5_argument_spec


class BaseParameters(AnsibleF5Parameters):
    @property
    def api_map(self):
        return {}

    @property
    def api_attributes(self):
        return []

    @property
    def returnables(self):
        return []

    @property
    def updatables(self):
        return []


class BaseApiParameters(BaseParameters):
    pass


class BaseModuleParameters(BaseParameters):
    pass


class BaseChanges(BaseParameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class BaseUsableChanges(BaseChanges):
    pass


class BaseReportableChanges(BaseChanges):
    pass


class TacacsParameters(BaseParameters):
    api_map = {
        'protocol': 'protocol_name',
        'service': 'service_name'
    }

    api_attributes = [
        'authentication',
        'accounting',
        'protocol',
        'service',
        'secret',
        'servers',
        'service_name'
    ]

    returnables = [
        'servers',
        'secret',
        'authentication',
        'accounting',
        'service_name',
        'protocol_name'
    ]

    updatables = [
        'servers',
        'secret',
        'authentication',
        'accounting',
        'service_name',
        'protocol_name',
        'auth_source',
    ]

class RadiusParameters(BaseParameters):
    api_map = {
        'serviceType': 'service_type'
    }

    api_attributes = [
        'secret',
        'servers',
        'serviceType',
        'timeout',
        'retries'
    ]

    returnables = [
        'servers',
        'secret',
        'service_type',
        'type',
        'timeout',
        'retries'
    ]

    updatables = [
        'servers',
        'secret',
        'service_type',
        'timeout',
        'retries'
    ]

class TacacsApiParameters(TacacsParameters):
    pass


class RadiusApiParameters(RadiusParameters):
    pass

class RadiusModuleParameters(RadiusParameters):
    @property
    def servers(self):
        if self._values['servers'] is None:
            return None
        result = []
        for server in self._values['servers']:
            if isinstance(server, dict):
                if 'address' not in server:
                    raise F5ModuleError(
                        "An 'address' field must be provided when specifying separate fields to the 'servers' parameter."
                    )
                address = server.get('address')
                port = server.get('port', None)
            elif isinstance(server, string_types):
                address = server
                port = None
            if port is None:
                result.append({
                    "address": address
                })
            else:
                result.append({
                    "address" : address,
                    "port": port
                })
        return result

    @property
    def auth_source(self):
        return 'radius'




class TacacsModuleParameters(TacacsParameters):
    @property
    def servers(self):
        if self._values['servers'] is None:
            return None
        result = []
        for server in self._values['servers']:
            if isinstance(server, dict):
                if 'address' not in server:
                    raise F5ModuleError(
                        "An 'address' field must be provided when specifying separate fields to the 'servers' parameter."
                    )
                address = server.get('address')
                port = server.get('port', None)
            elif isinstance(server, string_types):
                address = server
                port = None
            if port is None:
                result.append('{0}'.format(address))
            else:
                result.append('{0}:{1}'.format(address, port))
        return result

    @property
    def auth_source(self):
        return 'tacacs'


class TacacsChanges(BaseChanges, TacacsParameters):
    pass


class RadiusChanges(BaseChanges, RadiusParameters):
    pass

class TacacsUsableChanges(TacacsChanges):
    pass

class RadiusUsableChanges(RadiusChanges):
    pass

class TacacsReportableChanges(TacacsChanges):
    @property
    def secret(self):
        return None


class RadiusReportableChanges(RadiusChanges):
    @property
    def secret(self):
        return None

class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            return self.__default(param)

    def __default(self, param):
        want = getattr(self.want, param)
        try:
            have = getattr(self.have, param)
            if want != have:
                return want
        except AttributeError:
            return want

    @property
    def secret(self):
        if self.want.secret != self.have.secret and self.want.update_secret == 'always':
            return self.want.secret


class BaseManager(object):
    def _set_changed_options(self):
        changed = {}
        for key in self.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = self.get_usable_changes(params=changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = self.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = self.get_usable_changes(params=changed)
            return True
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        if state == "present":
            changed = self.present()
        elif state == "absent":
            changed = self.absent()

        reportable = self.get_reportable_changes(params=self.changes.to_return())
        changes = reportable.to_return()
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
        return self.create()

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def update_auth_source_on_device(self, source):
        """Set the system auth source.

        Configuring the authentication source is only one step in the process of setting
        up an auth source. The other step is to inform the system of the auth source
        you want to use.

        This method is used for situations where

        * The ``use_for_auth`` parameter is set to ``yes``
        * The ``use_for_auth`` parameter is set to ``no``
        * The ``state`` parameter is set to ``absent``

        When ``state`` equal to ``absent``, before you can delete the TACACS+ configuration,
        you must set the system auth to "something else". The system ships with a system
        auth called "local", so this is the logical "something else" to use.

        When ``use_for_auth`` is no, the same situation applies as when ``state`` equal
        to ``absent`` is done above.

        When ``use_for_auth`` is ``yes``, this method will set the current system auth
        state to TACACS+.

        Arguments:
            source (string): The source that you want to set on the device.
        """
        params = dict(
            type=source
        )
        uri = 'https://{0}:{1}/mgmt/tm/auth/source/'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def read_current_auth_source_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/auth/source".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return response['type']
        raise F5ModuleError(resp.content)


class LocalManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.want = self.get_module_parameters(params=self.module.params)
        self.have = self.get_api_parameters()
        self.changes = self.get_usable_changes()

    @property
    def returnables(self):
        return []

    @property
    def updatables(self):
        return []

    def get_parameters(self, params=None):
        return BaseParameters(params=params)

    def get_usable_changes(self, params=None):
        return BaseUsableChanges(params=params)

    def get_reportable_changes(self, params=None):
        return BaseReportableChanges(params=params)

    def get_module_parameters(self, params=None):
        return BaseModuleParameters(params=params)

    def get_api_parameters(self, params=None):
        return BaseApiParameters(params=params)

    def exists(self):
        uri = "https://{0}:{1}/mgmt/tm/auth/source".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            if response['type'] == 'local':
                return True
            return False
        raise F5ModuleError(resp.content)

    def create(self):
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.update_auth_source_on_device('local')
        return True

    def present(self):
        if not self.exists():
            return self.create()

    def absent(self):
        raise F5ModuleError(
            "The 'local' type cannot be removed. "
            "Instead, specify a 'state' of 'present' on other types."
        )

class RadiusManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.want = self.get_module_parameters(params=self.module.params)
        self.have = self.get_api_parameters()
        self.changes = self.get_usable_changes()

    @property
    def returnables(self):
        return RadiusParameters.returnables

    @property
    def updatables(self):
        return RadiusParameters.updatables

    def get_usable_changes(self, params=None):
        return RadiusUsableChanges(params=params)

    def get_reportable_changes(self, params=None):
        return RadiusReportableChanges(params=params)

    def get_module_parameters(self, params=None):
        return RadiusModuleParameters(params=params)

    def get_api_parameters(self, params=None):
        if params == None:
            return RadiusApiParameters(params=params)
        temp_params=dict()
        if 'radius_server_1' in  temp_params:
            temp_params['servers']=list()
            temp_params['servers'].append({
                'address': params['radius_server_1']['server'],
                'port': params['radius_server_1']['port'],
            })
        if 'radius_server_2' in temp_params:
            temp_params['servers'].append({
                'address': params['radius_server_2']['server'],
                'port': params['radius_server_2']['port'],
            })
        temp_params['service_type']=params['radius_config']['serviceType']
        return RadiusApiParameters(params=temp_params)

    def exists(self):
        uri = "https://{0}:{1}/mgmt/tm/auth/radius/~Common~system-auth".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError:
            return False
        if resp.status == 404 or 'code' in response and response['code'] == 404:
            return False
        return True

    def create(self):
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.create_on_device()
        if self.want.use_for_auth:
            self.update_auth_source_on_device('radius')
        return True

    def create_on_device(self):
        params = self.changes.api_params()

        uri_radius_server = "https://{0}:{1}/mgmt/tm/auth/radius-server".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        uri_radius_config = "https://{0}:{1}/mgmt/tm/auth/radius".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        radius_servers = []
        count=1
        for server in params['servers']:
            if count < 3:
                params['name'] = 'system_auth_name{0}'.format(str(count))
                count=count+1
                radius_servers.append(params['name'])
                params['server'] = server['address']
                if 'port' in server:
                    params['port'] = server['port']
                else:
                    params['port'] = None
                resp1 = self.client.api.post(uri_radius_server, json=params)
        params = self.changes.api_params()
        params['name'] = 'system-auth'
        params['servers'] = radius_servers
        resp2 = self.client.api.post(uri_radius_config, json=params)

        try:
            response1 = resp1.json()
            response2 = resp2.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if ('code' in response2 and response2['code'] in [400, 403]) or ('code' in response1 and response1['code'] in [400, 403]):
            if 'message' in response2:
                raise F5ModuleError(response2['message'])
            elif 'message' in response1:
                raise F5ModuleError(response1['message'])
            else:
                raise F5ModuleError(resp2.content)

    def read_current_from_device(self):
        response=dict()
        uri_radius_config = "https://{0}:{1}/mgmt/tm/auth/radius/~Common~system-auth".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )

        try:
            count = 1
            for name in ['system_auth_name1', 'system_auth_name2']:
                uri_radius_server = "https://{0}:{1}/mgmt/tm/auth/radius-server/~Common~{2}".format(
                    self.client.provider['server'],
                    self.client.provider['server_port'],
                    name
                )
                resp = self.client.api.get(uri_radius_server)
                response['radius_server_' + str(count)] = resp.json()
                count = count+1
            resp = self.client.api.get(uri_radius_config)
            response['radius_config'] = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if ('code' in response['radius_config'] and response['radius_config']['code'] == 400) or \
            ('code' in response['radius_server_1'] and response['radius_server_1']['code'] == 400) or \
            ('code' in response['radius_server_2'] and response['radius_server_2']['code'] == 400):
            if 'message' in response['radius_config']:
                raise F5ModuleError(response['radius_config']['message'])
            elif 'message' in response['radius_server_1']:
                raise F5ModuleError(response['radius_server_1']['message'])
            elif 'message' in response['radius_server_2']:
                raise F5ModuleError(response['radius_server_2']['message'])
            else:
                raise F5ModuleError(resp.content)
        response['auth_source'] = self.read_current_auth_source_from_device()
        return self.get_api_parameters(params=response)

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        result = False
        if self.update_on_device():
            result = True
        if self.want.use_for_auth and self.changes.auth_source == 'radius':
            self.update_auth_source_on_device('radius')
            result = True
        return result

    def update_on_device(self):
        params = self.changes.api_params()
        if not params:
            return False
        response = dict()

        uri_radius_config = 'https://{0}:{1}/mgmt/tm/auth/radius/~Common~system-auth'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        try:
            if 'servers' in params:
                count=1
                for server in params['servers']:
                    uri_radius_server = "https://{0}:{1}/mgmt/tm/auth/radius-server/~Common~{2}".format(
                        self.client.provider['server'],
                        self.client.provider['server_port'],
                        'system_auth_name' + str(count)
                    )
                    params['server'] = server['address']
                    if 'port' in server:
                        params['port'] = server['port']
                    else:
                        params['port'] = '1812'

                    resp = self.client.api.patch(uri_radius_server, json=params)
                    response['radius_server' + str(count)] = resp.json()
                    count=count+1
            else:
                count=1
                for name in ['system_auth_name1', 'system_auth_name2']:
                    uri_radius_server = "https://{0}:{1}/mgmt/tm/auth/radius-server/~Common~{2}".format(
                        self.client.provider['server'],
                        self.client.provider['server_port'],
                        name
                    )
                    resp = self.client.api.patch(uri_radius_server, json=params)
                    response['radius_server' + str(count)] = resp.json()
                    count=count+1

            if 'server' in params:
                params.pop('server')
            if 'port' in params:
                params.pop('port')
            if 'servers' in params:
                params.pop('servers')
            if 'timeout' in params:
                params.pop('timeout')

            if len(params.keys()) > 1:
                resp=self.client.api.patch(uri_radius_config, json=params)
                response['radius_config'] = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if ('radius_config' in response and 'code' in response['radius_config'] and response['radius_config']['code'] == 400) or \
            ('radius_server_1' in response and 'code' in response['radius_server_1'] and response['radius_server_1']['code'] == 400) or \
            ('radius_server_2' in response and 'code' in response['radius_server_2'] and response['radius_server_2']['code'] == 400):
            if 'message' in response['radius_config']:
                raise F5ModuleError(response['radius_config']['message'])
            elif 'message' in response['radius_server_1']:
                raise F5ModuleError(response['radius_server_1']['message'])
            elif 'message' in response['radius_server_2']:
                raise F5ModuleError(response['radius_server_2']['message'])
            else:
                raise F5ModuleError(resp.content)

        return True

    def remove(self):
        if self.module.check_mode:
            return True
        self.update_auth_source_on_device('local')
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        return True

    def remove_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/auth/radius/~Common~system-auth".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        resp = self.client.api.delete(uri)
        if not resp.status == 200:
            raise F5ModuleError(resp.content)
        uri = "https://{0}:{1}/mgmt/tm/auth/radius-server/~Common~system_auth_name1".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        resp = self.client.api.delete(uri)
        if not resp.status == 200:
            raise F5ModuleError(resp.content)
        uri = "https://{0}:{1}/mgmt/tm/auth/radius-server/~Common~system_auth_name2".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        self.client.api.delete(uri)
        return True


class TacacsManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.want = self.get_module_parameters(params=self.module.params)
        self.have = self.get_api_parameters()
        self.changes = self.get_usable_changes()

    @property
    def returnables(self):
        return TacacsParameters.returnables

    @property
    def updatables(self):
        return TacacsParameters.updatables

    def get_usable_changes(self, params=None):
        return TacacsUsableChanges(params=params)

    def get_reportable_changes(self, params=None):
        return TacacsReportableChanges(params=params)

    def get_module_parameters(self, params=None):
        return TacacsModuleParameters(params=params)

    def get_api_parameters(self, params=None):
        return TacacsApiParameters(params=params)

    def exists(self):
        errors = [401, 403, 409, 500, 501, 502, 503, 504]
        uri = "https://{0}:{1}/mgmt/tm/auth/tacacs/~Common~system-auth".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status == 404 or 'code' in response and response['code'] == 404:
            return False
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True

        if resp.status in errors or 'code' in response and response['code'] in errors:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def create(self):
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.create_on_device()
        if self.want.use_for_auth:
            self.update_auth_source_on_device('tacacs')
        return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        result = False
        if self.update_on_device():
            result = True
        if self.want.use_for_auth and self.changes.auth_source == 'tacacs':
            self.update_auth_source_on_device('tacacs')
            result = True
        return result

    def remove(self):
        if self.module.check_mode:
            return True
        self.update_auth_source_on_device('local')
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        return True

    def create_on_device(self):
        params = self.changes.api_params()
        params['name'] = 'system-auth'
        uri = "https://{0}:{1}/mgmt/tm/auth/tacacs".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(resp.content)

    def update_on_device(self):
        params = self.changes.api_params()
        if not params:
            return False

        uri = 'https://{0}:{1}/mgmt/tm/auth/tacacs/~Common~system-auth'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(resp.content)

    def remove_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/auth/tacacs/~Common~system-auth".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        response = self.client.api.delete(uri)

        if response.status in [200, 201]:
            return True
        raise F5ModuleError(response.content)

    def read_current_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/auth/tacacs/~Common~system-auth".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            response['auth_source'] = self.read_current_auth_source_from_device()
            return self.get_api_parameters(params=response)
        raise F5ModuleError(resp.content)


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.kwargs = kwargs

    def exec_module(self):
        manager = self.get_manager(self.module.params['type'])
        return manager.exec_module()

    def get_manager(self, type):
        if type == 'tacacs':
            return TacacsManager(**self.kwargs)
        elif type == 'radius':
            return RadiusManager(**self.kwargs)
        elif type == 'local':
            return LocalManager(**self.kwargs)
        else:
            raise F5ModuleError(
                "The provided 'type' is unknown."
            )


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            type=dict(
                required=True,
                choices=['local', 'tacacs', 'radius']
            ),
            servers=dict(type='raw'),
            secret=dict(no_log=True),
            service_name=dict(
                choices=[
                    'slip', 'ppp', 'arap', 'shell', 'tty-daemon',
                    'connection', 'system', 'firewall'
                ]
            ),
            retries=dict(
                default='3',
                choices=[
                    '0', '1', '2',
                    '3', '4', '5'
                ]
            ),
            timeout=dict(
                default='3'
            ),
            service_type=dict(
                choices=[
                    'authenticate-only', 'login', 'default', 'framed', 'callback-login', 'callback-framed', 'outbound', 'administrative',
                    'nas-prompt', 'callback-nas-prompt', 'call-check', 'callback-administrative'
                ],
                default='authenticate-only'
            ),
            protocol_name=dict(
                choices=[
                    'lcp', 'ip', 'ipx', 'atalk', 'vines', 'lat',
                    'xremote', 'tn3270', 'telnet', 'rlogin', 'pad',
                    'vpdn', 'ftp', 'http', 'deccp', 'osicp', 'unknown'
                ]
            ),
            authentication=dict(
                choices=[
                    'use-first-server',
                    'use-all-servers'
                ]
            ),
            accounting=dict(
                choices=[
                    'send-to-first-server',
                    'send-to-all-servers'
                ]
            ),
            use_for_auth=dict(type='bool'),
            update_secret=dict(
                choices=['always', 'on_create'],
                default='always'
            ),
            state=dict(
                default='present',
                choices=['present', 'absent']
            ),

        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
    )

    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
