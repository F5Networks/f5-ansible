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
module: bigip_device_auth_radius
short_description: Manage RADIUS authentication on a BIG-IP
description:
  - Manage the RADIUS authentication configuration.
version_added: 2.9
options:
  servers:
    description:
      - Specifies RADIUS servers configurations for use with RADIUS authentication profiles
    type: list
    suboptions:
      server:
        description:
          - The IP address of the server.
          - This field is required.
            In that case, the simple list can specify server IPs. See examples for
            more clarification.
        type: str
      port:
        description:
          - The port of the server.
          - If no port number is specified, the default port C(1812) is used.
        type: int
        default: 1812
      secret:
        description:
          - Specifies secret used for accessing RADIUS server.
        type: str
      timeout:
        description:
          - Specifies the timeout value in seconds.
          - The default timeout value is C(3) seconds.
        type: int
        default: 3
  accounting_bug:
    description:
      - Enables or disables validation of the accounting response vector.
      - This option should be necessary only on older servers
    type: str
    default: disabled
  retries:
    description:
      - Specifies the number of authentication retries that the BIG-IP local traffic management system allows before authentication fails.
      - The default value is C(3).
    type: int
    default: 3
  service_type:
    description:
      - Specifies the type of service requested from the RADIUS server. The default value is authenticate-only
    type: str
    default: authenticate-only
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
        and Radius+ is not currently the auth source.
    type: str
    choices:
      - always
      - on_create
    default: always
extends_documentation_fragment: f5networks.f5_modules.f5
author:
  - Tim Rupp (@caphrim007)
  - Nitin Khanna (@nitinthewiz)
'''

EXAMPLES = r'''
- name: Set the system auth to RADIUS, override server port and timeout
  bigip_device_auth_radius:
    servers:
      - server: 10.10.10.10
        port: 1812
        timeout: 5
        secret: secret1
      - server: 11.10.10.11
        port: 1813
        timeout: 10
        secret: secret2
    retries: 3
    service_type: authenticate-only
    accounting_bug: disabled
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
  description: List of servers used in RADIUS authentication.
  returned: changed
  type: list
  sample: ['1.2.2.1', '4.5.5.4']
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


class Parameters(AnsibleF5Parameters):
    api_map = {
        'serviceType': 'service_type',
        'accountingBug': 'accounting_bug'
    }

    api_attributes = [
        'accountingBug',
        'serviceType',
        'servers',
        'retries'
    ]

    returnables = [
        'accounting_bug',
        'servers',
        'service_type',
        'retries'
    ]

    updatables = [
        'accounting_bug',
        'servers',
        'service_type',
        'retries'
    ]


class ApiParameters(Parameters):
    pass


class ModuleParameters(Parameters):
    @property
    def servers(self):
        if self._values['servers'] is None:
            return None
        result = []
        for server in self._values['servers']:
            if isinstance(server, dict):
                if 'server' not in server:
                    raise F5ModuleError(
                        "A 'server' field must be provided when specifying separate fields to the 'servers' parameter."
                    )
                if 'secret' not in server:
                    raise F5ModuleError(
                        "A 'secret' field must be provided when specifying separate fields to the 'servers' parameter."
                    )

                result.append({
                    "server": server.get('server'),
                    "port": server.get('port', None),
                    "timeout": server.get('timeout', None),
                    "secret": server.get('secret')
                })
            else:
                raise F5ModuleError(
                    "Servers list requires providing dict of server(s)"
                )
        return result

    @property
    def auth_source(self):
        return 'radius'


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class UsableChanges(Changes):
    pass


class ReportableChanges(Changes):
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
    def servers(self):
        if self.want.update_secret == 'on_create':
            count = 0
            for server in self.want.servers:
                if server['server'] != self.have.servers[count]['server']:
                    return self.want.servers
                if server['port'] != self.have.servers[count]['port']:
                    return self.want.servers
                if server['timeout'] != self.have.servers[count]['timeout']:
                    return self.want.servers
        else:
            return self.want.servers


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.want = self.get_module_parameters(params=self.module.params)
        self.have = self.get_api_parameters()
        self.changes = self.get_usable_changes()

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

        When ``state`` equal to ``absent``, before you can delete the Radius+ configuration,
        you must set the system auth to "something else". The system ships with a system
        auth called "local", so this is the logical "something else" to use.

        When ``use_for_auth`` is no, the same situation applies as when ``state`` equal
        to ``absent`` is done above.

        When ``use_for_auth`` is ``yes``, this method will set the current system auth
        state to Radius+.

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
        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        return response['type']

    @property
    def returnables(self):
        return Parameters.returnables

    @property
    def updatables(self):
        return Parameters.updatables

    def get_usable_changes(self, params=None):
        return UsableChanges(params=params)

    def get_reportable_changes(self, params=None):
        return ReportableChanges(params=params)

    def get_module_parameters(self, params=None):
        return ModuleParameters(params=params)

    def get_api_parameters(self, params=None):
        return ApiParameters(params=params)

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
        count = 1

        for server in params['servers']:
            if count < 3:
                server['name'] = 'system_auth_name{0}'.format(str(count))
                self.create_radius_serves_on_device(server)
            count = count + 1

        if count > 2:
            params['servers'] = ['system_auth_name1', 'system_auth_name2']
        else:
            params['servers'] = ['system_auth_name1']

        self.create_radius_config_on_device(params)

    def create_radius_config_on_device(self, params):
        params['name'] = 'system-auth'
        uri = 'https://{0}:{1}/mgmt/tm/auth/radius'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        resp = self.client.api.post(uri, json=params)

        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] in [400, 403]:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def create_radius_serves_on_device(self, params):
        uri_radius_server = "https://{0}:{1}/mgmt/tm/auth/radius-server".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        resp = self.client.api.post(uri_radius_server, json=params)

        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] in [400, 403]:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def update_radius_servers_on_device(self, params, count):
        uri = "https://{0}:{1}/mgmt/tm/auth/radius-server/~Common~{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            'system_auth_name' + str(count)
        )
        resp = self.client.api.patch(uri, json=params)

        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] in [400, 403]:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def update_radius_config_on_device(self, params):
        if not params:
            return True

        uri = 'https://{0}:{1}/mgmt/tm/auth/radius/~Common~system-auth'.format(
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

        return True

    def update_on_device(self):
        params = self.changes.api_params()

        if not params:
            return False

        if 'servers' in params:
            count = 1
            for server in params['servers']:
                self.update_radius_servers_on_device(server, count)
                count = count + 1
            params.pop('servers')

        return self.update_radius_config_on_device(params)

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

    def read_current_radius_config(self):
        uri = "https://{0}:{1}/mgmt/tm/auth/radius/~Common~system-auth".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        resp = self.client.api.get(uri)

        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

        return response

    def read_current_radius_servers(self):
        servers = list()
        for name in ['system_auth_name1', 'system_auth_name2']:
            uri = "https://{0}:{1}/mgmt/tm/auth/radius-server/~Common~{2}".format(
                self.client.provider['server'],
                self.client.provider['server_port'],
                name
            )
            resp = self.client.api.get(uri)
            try:
                response = resp.json()
                servers.append(resp.json())
            except ValueError as ex:
                raise F5ModuleError(str(ex))
            if 'code' in response and response['code'] == 400:
                if 'message' in response:
                    raise F5ModuleError(response['message'])
                else:
                    raise F5ModuleError(resp.content)
        return servers

    def read_current_from_device(self):
        result = dict()
        curr_config = self.read_current_radius_config()

        if 'serviceType' in curr_config:
            result['service_type'] = curr_config['serviceType']
        if 'retries' in curr_config:
            result['retries'] = curr_config['retries']
        if 'accountingBug' in curr_config:
            result['accounting_bug'] = curr_config['accountingBug']

        result['servers'] = self.read_current_radius_servers()
        result['auth_source'] = self.read_current_auth_source_from_device()
        return self.get_api_parameters(params=result)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            retries=dict(
                default=3,
                type='int'
            ),
            service_type=dict(
                choices=[
                    'authenticate-only', 'login', 'default', 'framed', 'callback-login', 'callback-framed', 'outbound', 'administrative',
                    'nas-prompt', 'callback-nas-prompt', 'call-check', 'callback-administrative'
                ],
                default='authenticate-only'
            ),
            accounting_bug=dict(
                default='disabled'
            ),
            servers=dict(
                type='list',
                elements='dict',
                options=dict(
                    server=dict(
                        required=True
                    ),
                    port=dict(
                        type='int',
                        default=1812
                    ),
                    timeout=dict(
                        type='int',
                        default=3
                    ),
                    secret=dict(
                        required=True,
                        no_log=True
                    )
                )
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
