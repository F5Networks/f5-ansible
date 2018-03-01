#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_gtm_virtual_server
short_description: Manages F5 BIG-IP GTM virtual servers
description:
  - Manages F5 BIG-IP GTM virtual servers. A GTM server can have many virtual servers
    associated with it. They are arranged in much the same way that pool members are
    to pools.
version_added: 2.6
options:
  name:
    description:
      - Specifies the name of the virtual server.
  server_name:
    description:
      - Specifies the name of the server that the virtual server is associated with.
  address:
    description:
      - Specifies the IP Address of the virtual server.
  port:
    description:
      - Specifies the service port number for the virtual server or pool member. For example,
        the HTTP service is typically port 80.
      - To specify all ports, use an C(*).
  translation_address:
    description:
      - Specifies the translation IP address for the virtual server.
  translation_port:
    description:
      - Specifies the translation port number or service name for the virtual server.
      - To specify all ports, use an C(*).
  availability_requirements:
    suboptions:
      type:
        description:
          - Monitor rule type when C(monitors) is specified.
          - When creating a new pool, if this value is not specified, the default of 'all' will be used.
        choices: ['all', 'at_least', 'require']
      at_least:
        description:
          - Specifies the minimum number of active health monitors that must be successful
            before the link is considered up.
          - This parameter is only relevant when a C(type) of C(at_least) is used.
          - This parameter will be ignored if a type of either C(all) or C(require) is used.
      number_of_probes:
        description:
          - Specifies the minimum number of probes that must succeed for this server to be declared up.
          - When creating a new virtual server, if this parameter is specified, then the C(number_of_probers)
            parameter must also be specified.
          - The value of this parameter should always be B(lower) than, or B(equal to), the value of C(number_of_probers).
          - This parameter is only relevant when a C(type) of C(require) is used.
          - This parameter will be ignored if a type of either C(all) or C(at_least) is used.
      number_of_probers:
        description:
          - Specifies the number of probers that should be used when running probes.
          - When creating a new virtual server, if this parameter is specified, then the C(number_of_probes)
            parameter must also be specified.
          - The value of this parameter should always be B(higher) than, or B(equal to), the value of C(number_of_probers).
          - This parameter is only relevant when a C(type) of C(require) is used.
          - This parameter will be ignored if a type of either C(all) or C(at_least) is used. 
  monitors:
    description:
      - Specifies the health monitors that the system currently uses to monitor this resource.
  virtual_server_dependencies:
    description:
      - Specifies the virtual servers on which the current virtual server depends.
      - If any of the specified servers are unavailable, the current virtual server is also listed as unavailable.
  link:
    description:
      - Specifies a link to assign to the server or virtual server.
  limits:
    description:
      - Specifies resource thresholds or limit requirements at the server level.
      - When you enable one or more limit settings, the system then uses that data to take servers in and out
        of service.
      - You can define limits for any or all of the limit settings. However, when a server does not meet the resource
        threshold limit requirement, the system marks the entire server as unavailable and directs load-balancing
        traffic to another resource.
      - The limit settings available depend on the type of server.
    suboptions:
      bits_enabled:
        description:
          - Whether the bits limit it enabled or not.
          - This parameter allows you to switch on or off the effect of the limit.
        type: bool
      packets_enabled:
        description:
          - Whether the packets limit it enabled or not.
          - This parameter allows you to switch on or off the effect of the limit.
        type: bool
      connections_enabled:
        description:
          - Whether the current connections limit it enabled or not.
          - This parameter allows you to switch on or off the effect of the limit.
        type: bool
      bits_limit:
        description:
          - Specifies the maximum allowable data throughput rate, in bits per second, for the virtual servers on the server.
          - If the network traffic volume exceeds this limit, the system marks the server as unavailable.
      packets_limit:
        description:
          - Specifies the maximum allowable data transfer rate, in packets per second, for the virtual servers on the server.
          - If the network traffic volume exceeds this limit, the system marks the server as unavailable.
      connections_limit:
        description:
          - Specifies the maximum number of concurrent connections, combined, for all of the virtual servers on the server.
          - If the connections exceed this limit, the system marks the server as unavailable.
  partition:
    description:
      - Device partition to manage resources on.
    default: Common
  state:
    description:
      - When C(present), ensures that the resource exists.
      - When C(absent), ensures the resource is removed.
    default: present
    choices:
      - present
      - absent
      - enabled
      - disabled
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Enable virtual server
  bigip_gtm_virtual_server:
    server: lb.mydomain.com
    user: admin
    password: secret
    virtual_server_name: myname
    virtual_server_server: myserver
    state: enabled
  delegate_to: localhost
'''

RETURN = r'''
server_name:
  description: The server name associated with the virtual server.
  returned: changed
  type: string
  sample: /Common/my-gtm-server
address:
  description: The new address of the resource.
  returned: changed
  type: string
  sample: 1.2.3.4
port:
  description: The new port of the resource.
  returned: changed
  type: int
  sample: 500
translation_address:
  description: The new translation address of the resource.
  returned: changed
  type: int
  sample: 500
translation_port:
  description: The new translation port of the resource.
  returned: changed
  type: int
  sample: 500
availability_requirements:
  description: The new availability requirement configurations for the resource.
  returned: changed
  type: dict
  sample: {'type': 'all'}
monitors:
  description: The new list of monitors for the resource.
  returned: changed
  type: list
  sample: ['/Common/monitor1', '/Common/monitor2']
virtual_server_dependencies:
  description: The new list of virtual server dependencies for the resource
  returned: changed
  type: list
  sample: ['/Common/vs1', '/Common/vs2'] 
link:
  description: The new link value for the resource.
  returned: changed
  type: string
  sample: /Common/my-link
limits:
  description: The new limit configurations for the resource.
  returned: changed
  type: dict
  sample: { 'bits_enabled': true, 'bits_limit': 100 }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback

HAS_DEVEL_IMPORTS = False

try:
    from library.module_utils.network.f5.bigip import HAS_F5SDK
    from library.module_utils.network.f5.bigip import F5Client
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import cleanup_tokens
    from library.module_utils.network.f5.common import fq_name
    from library.module_utils.network.f5.common import f5_argument_spec
    try:
        from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False
    HAS_DEVEL_IMPORTS = True
except ImportError:
    # Upstream Ansible
    from ansible.module_utils.network.f5.bigip import HAS_F5SDK
    from ansible.module_utils.network.f5.bigip import F5Client
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import AnsibleF5Parameters
    from ansible.module_utils.network.f5.common import cleanup_tokens
    from ansible.module_utils.network.f5.common import fq_name
    from ansible.module_utils.network.f5.common import f5_argument_spec
    try:
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    api_map = {
        'limitMaxBps': 'bits_limit',
        'limitMaxBpsStatus': 'bits_enabled',
        'limitMaxConnections': 'connections_limit',
        'limitMaxConnectionsStatus': 'connections_enabled',
        'limitMaxPps': 'packets_limit',
        'limitMaxPpsStatus': 'packets_enabled',
        'translationAddress': 'translation_address',
        'translationPort': 'translation_port',
        'dependsOn': 'virtual_server_dependencies',
        'explicitLinkName': 'link',
    }

    api_attributes = [
        'limitMaxBps', 'limitMaxBpsStatus', 'limitMaxConnections', 'limitMaxConnectionsStatus',
        'limitMaxPps', 'limitMaxPpsStatus', 'translationAddress', 'translationPort',
        'dependsOn', 'explicitLinkName', 'monitor', 'enabled', 'disabled', 'destination'
    ]

    returnables = [
        'bits_limit', 'bits_enabled', 'connections_limit', 'connections_enabled',
        'packets_limit', 'packets_enabled', 'translation_address', 'translation_port',
        'virtual_server_dependencies', 'link', 'destination'
    ]

    updatables = [
        'bits_limit', 'bits_enabled', 'connections_limit', 'connections_enabled',
        'packets_limit', 'packets_enabled', 'translation_address', 'translation_port',
        'virtual_server_dependencies', 'link', 'destination'
    ]


class ApiParameters(Parameters):
    pass


class ModuleParameters(Parameters):
    def _get_limit_value(self, type):
        if self._values['limits'][type] is None:
            return None
        return int(self._values['limits'][type])

    def _get_limit_status(self, type):
        if self._values['limits'][type] is None:
            return None
        if self._values['limits'][type]:
            return 'enabled'
        return 'disabled'

    @property
    def port(self):
        if self._values['port'] is None:
            return None
        if self._values['port'] == '*':
            return 0
        return int(self._values['port'])

    @property
    def destination(self):
        result = '{0}:{1}'.format(self.address, self.port)
        return result

    @property
    def link(self):
        if self._values['link'] is None:
            return None
        return fq_name(self.partition, self._values['link'])

    @property
    def bits_limit(self):
        return self._get_limit_value('bits_limit')

    @property
    def packets_limit(self):
        return self._get_limit_value('packets_limit')

    @property
    def connections_limit(self):
        return self._get_limit_value('connections_limit')

    @property
    def bits_enabled(self):
        return self._get_limit_status('bits_enabled')

    @property
    def packets_enabled(self):
        return self._get_limit_status('packets_enabled')

    @property
    def connections_enabled(self):
        if self._values['limits']['connections_enabled'] is None:
            return None
        if self._values['limits']['connections_enabled']:
            return 'enabled'
        return 'disabled'


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
    pass


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
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = kwargs.get('client', None)
        self.want = ModuleParameters(params=self.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = UsableChanges(params=changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
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
            self.changes = UsableChanges(params=changed)
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

        try:
            if state in ['present', 'enabled', 'disabled']:
                changed = self.present()
            elif state == 'absent':
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        reportable = ReportableChanges(params=self.changes.to_return())
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
        else:
            return self.create()

    def exists(self):
        resource = self.client.api.tm.gtm.servers.server.load(
            name=self.want.server_name,
            partition=self.want.partition
        )
        result = resource.virtual_servers_s.virtual_server.exists(
            name=self.want.name
        )
        return result

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        return True

    def create(self):
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.changes.api_params()
        resource = self.client.api.tm.gtm.servers.server.load(
            name=self.want.server_name,
            partition=self.want.partition
        )
        resource.virtual_servers_s.virtual_server.create(
            name=self.want.name,
            **params
        )

    def update_on_device(self):
        params = self.changes.api_params()
        resource = self.client.api.tm.gtm.servers.server.load(
            name=self.want.server_name,
            partition=self.want.partition
        )
        resource = resource.virtual_servers_s.virtual_server.load(
            name=self.want.name
        )
        resource.modify(**params)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove_from_device(self):
        resource = self.client.api.tm.gtm.servers.server.load(
            name=self.want.server_name,
            partition=self.want.partition
        )
        resource = resource.virtual_servers_s.virtual_server.load(
            name=self.want.name
        )
        if resource:
            resource.delete()

    def read_current_from_device(self):
        resource = self.client.api.tm.gtm.servers.server.load(
            name=self.want.server_name,
            partition=self.want.partition
        )
        resource = resource.virtual_servers_s.virtual_server.load(
            name=self.want.name
        )
        result = resource.attrs
        return ApiParameters(params=result)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            name=dict(required=True),
            server_name=dict(required=True),
            address=dict(),
            port=dict(type='int'),
            translation_address=dict(),
            translation_port=dict(type='int'),
            availability_requirements=dict(
                type='dict',
                suboptions=dict(
                    type=dict(),
                    at_least=dict(),
                    number_of_probes=dict(),
                    number_of_probers=dict()
                )
            ),
            monitors=dict(type='list'),
            virtual_server_dependencies=dict(type='list'),
            link=dict(),
            limits=dict(
                type='dict',
                suboptions=dict(
                    bits_enabled=dict(type='bool'),
                    packets_enabled=dict(type='bool'),
                    connections_enabled=dict(type='bool'),
                    bits_limit=dict(type='int'),
                    packets_limit=dict(type='int'),
                    connections_limit=dict(type='int')
                )
            ),
            state=dict(
                default='present',
                choices=['present', 'absent', 'disabled', 'enabled']
            ),
            partition=dict(
                default='Common',
                fallback=(env_fallback, ['F5_PARTITION'])
            )
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    if not HAS_F5SDK:
        module.fail_json(msg="The python f5-sdk module is required")

    try:
        client = F5Client(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        module.exit_json(**results)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
