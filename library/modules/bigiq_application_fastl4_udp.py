#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigiq_application_fastl4_udp
short_description: Manages BIG-IQ FastL4 UDP applications
description:
  - Manages BIG-IQ applications used for load balancing a UDP-based application
    with a FastL4 profile.
version_added: 2.6
options:
  name:
    description:
      - Name of the new application.
    required: True
  description:
    description:
      - Description of the application.
  servers:
    description:
      - A list of servers that the application is hosted on.
      - If you are familiar with other BIG-IP setting, you might also refer to this
        list as the list of pool members.
      - When creating a new application, at least one server is required.
    suboptions:
      address:
        description:
          - The IP address of the server.
        required: True
      port:
        description:
          - The port of the server.
          - When creating a new application and specifying a server, if this parameter
            is not provided, the default of C(8000) will be used.
        default: 8000
  inbound_virtual:
    description:
      - Settings to configure the virtual which will receive the inbound connection.
    suboptions:
      address:
        description:
          - Specifies destination IP address information to which the virtual server
            sends traffic.
          - This parameter is required when creating a new application.
        required: True
      netmask:
        description:
          - Specifies the netmask to associate with the given C(destination).
          - This parameter is required when creating a new application.
        required: True
      port:
        description:
          - The port that the virtual listens for connections on.
          - When creating a new application, if this parameter is not specified, the
            default value of C(53) will be used.
        default: 53
  service_environment:
    description:
      - Specifies the name of service environment that the application will be
        deployed to.
      - When creating a new application, this parameter is required.
      - The service environment type will be discovered by this module automatically.
        Therefore, it is crucial that you maintain unique names for items in the
        different service environment types.
      - SSGs are not supported for this type of application.
  add_analytics:
    description:
      - Collects statistics of the BIG-IP that the application is deployed to.
      - This parameter is only relevant when specifying a C(service_environment) which
        is a BIG-IP; not an SSG.
    type: bool
    default: no
  state:
    description:
      - The state of the resource on the system.
      - When C(present), guarantees that the resource exists with the provided attributes.
      - When C(absent), removes the resource from the system.
    default: present
    choices:
      - absent
      - present
  wait:
    description:
      - If the module should wait for the application to be created, deleted or updated.
    type: bool
    default: yes
extends_documentation_fragment: f5
notes:
  - This module does not support updating of your application (whether deployed or not).
    If you need to update the application, the recommended practice is to remove and
    re-create.
  - Requires BIG-IQ version 6.0 or greater.
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Load balance a UDP-based application with a FastL4 profile
  bigiq_application_fastl4_udp:
    name: my-app
    description: My description
    service_environment: my-bigip-device
    servers:
      - address: 1.2.3.4
        port: 8080
      - address: 5.6.7.8
        port: 8080
    inbound_virtual:
      name: foo
      destination: 2.2.2.2
      netmask: 255.255.255.255
      port: 53
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
    state: present
  delegate_to: localhost
'''

RETURN = r'''
description:
  description: The new description of the application of the resource.
  returned: changed
  type: string
  sample: My application
service_environment:
  description: The environment which the service was deployed to.
  returned: changed
  type: string
  sample: my-ssg1
inbound_virtual_destination:
  description: The destination of the virtual that was created.
  returned: changed
  type: string
  sample: 6.7.8.9
inbound_virtual_netmask:
  description: The network mask of the provided inbound destination.
  returned: changed
  type: string
  sample: 255.255.255.0
inbound_virtual_port:
  description: The port the inbound virtual address listens on.
  returned: changed
  type: int
  sample: 80
servers:
  description: List of servers, and their ports, that make up the application.
  type: complex
  returned: changed
  contains:
    address:
      description: The IP address of the server.
      returned: changed
      type: string
      sample: 2.3.4.5
    port:
      description: The port that the server listens on.
      returned: changed
      type: int
      sample: 8080
  sample: hash/dictionary of values
'''

import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback

try:
    from library.module_utils.network.f5.bigiq import F5RestClient
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import f5_argument_spec
    from library.module_utils.network.f5.common import exit_json
    from library.module_utils.network.f5.common import fail_json
    from library.module_utils.network.f5.ipaddress import is_valid_ip
except ImportError:
    from ansible.module_utils.network.f5.bigiq import F5RestClient
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import AnsibleF5Parameters
    from ansible.module_utils.network.f5.common import f5_argument_spec
    from ansible.module_utils.network.f5.common import exit_json
    from ansible.module_utils.network.f5.common import fail_json
    from ansible.module_utils.network.f5.ipaddress import is_valid_ip


class Parameters(AnsibleF5Parameters):
    api_map = {
        'templateReference': 'template_reference',
        'subPath': 'sub_path',
        'configSetName': 'config_set_name',
        'defaultDeviceReference': 'default_device_reference',
        'addAnalytics': 'add_analytics'
    }

    api_attributes = [
        'resources', 'description', 'configSetName', 'subPath', 'templateReference',
        'defaultDeviceReference', 'addAnalytics'
    ]

    returnables = [
        'resources', 'description', 'config_set_name', 'sub_path', 'template_reference',
        'default_device_reference', 'servers', 'inbound_virtual', 'add_analytics'
    ]

    updatables = [
        'resources', 'description', 'config_set_name', 'sub_path', 'template_reference',
        'default_device_reference', 'servers', 'add_analytics'
    ]


class ApiParameters(Parameters):
    pass


class ModuleParameters(Parameters):
    @property
    def http_profile(self):
        return "profile_http"

    @property
    def config_set_name(self):
        return self.name

    @property
    def sub_path(self):
        return self.name

    @property
    def template_reference(self):
        filter = "name+eq+'Default-f5-FastL4-UDP-lb-template'"
        uri = "https://{0}:{1}/mgmt/cm/global/templates/?$filter={2}&$top=1&$select=selfLink".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            filter
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status == 200 and response['totalItems'] == 0:
            raise F5ModuleError(
                "No default HTTP LB template was found."
            )
        elif 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp._content)

        result = dict(
            link=response['items'][0]['selfLink']
        )
        return result

    @property
    def default_device_reference(self):
        if is_valid_ip(self.service_environment):
            # An IP address was specified
            filter = "address+eq+'{0}'".format(self.service_environment)
        else:
            # Assume a hostname was specified
            filter = "hostname+eq+'{0}'".format(self.service_environment)

        uri = "https://{0}:{1}/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices/?$filter={2}&$top=1&$select=selfLink".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            filter
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status == 200 and response['totalItems'] == 0:
            raise F5ModuleError(
                "The specified service_environment '{0}' was found.".format(self.service_environment)
            )
        elif 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp._content)
        result = dict(
            link=response['items'][0]['selfLink']
        )
        return result


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
    @property
    def resources(self):
        result = dict()
        result.update(self.udp_monitor)
        result.update(self.virtual)
        result.update(self.pool)
        result.update(self.nodes)
        return result

    @property
    def virtual(self):
        result = dict()
        result['ltm:virtual:c2e739ba116f'] = [
            dict(
                parameters=dict(
                    name='virtual',
                    destinationAddress=self.inbound_virtual['address'],
                    mask=self.inbound_virtual['netmask'],
                    destinationPort=self.inbound_virtual.get('port', 53)
                ),
                subcollectionResources=self.profiles
            )
        ]
        return result

    @property
    def profiles(self):
        result = {
            'profiles:53f9b3028d90': [
                dict(
                    parameters=dict()
                )
            ]
        }
        return result

    @property
    def pool(self):
        result = dict()
        result['ltm:pool:e6879775458c'] = [
            dict(
                parameters=dict(
                    name='pool_0'
                ),
                subcollectionResources=self.pool_members
            )
        ]
        return result

    @property
    def pool_members(self):
        result = dict()
        result['members:b19842fe713a'] = []
        for x in self.servers:
            member = dict(
                parameters=dict(
                    port=x.get('port', 8000),
                    nodeReference=dict(
                        link='#/resources/ltm:node:b19842fe713a/{0}'.format(x['address']),
                        fullPath='# {0}'.format(x['address'])
                    )
                )
            )
            result['members:b19842fe713a'].append(member)
        return result

    @property
    def udp_monitor(self):
        result = dict()
        result['ltm:monitor:udp:22cdcfda0a40'] = [
            dict(
                parameters=dict(
                    name='monitor-udp'
                )
            )
        ]
        return result

    @property
    def nodes(self):
        result = dict()
        result['ltm:node:b19842fe713a'] = []
        for x in self.servers:
            tmp = dict(
                parameters=dict(
                    name=x['address'],
                    address=x['address']
                )
            )
            result['ltm:node:b19842fe713a'].append(tmp)
        return result

    @property
    def node_addresses(self):
        result = [x['address'] for x in self.servers]
        return result


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
        self.want.client = self.client
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

        if state == "present":
            changed = self.present()
        elif state == "absent":
            changed = self.absent()

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
            return False
        else:
            return self.create()

    def exists(self):
        uri = "https://{0}:{1}/mgmt/ap/query/v1/tenants/default/reports/AllApplicationsList?$filter=name+eq+'{2}'".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            self.want.name
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status == 200 and 'result' in response and 'totalItems' in response['result'] and response['result']['totalItems'] == 0:
            return False
        return True

    def remove(self):
        if self.module.check_mode:
            return True
        self_link = self.remove_from_device()
        if self.want.wait:
            self.wait_for_apply_template_task(self_link)
            if self.exists():
                raise F5ModuleError("Failed to delete the resource.")
        return True

    def create(self):
        if self.want.service_environment is None:
            raise F5ModuleError(
                "A 'service_environment' must be specified when creating a new application."
            )
        if self.want.servers is None:
            raise F5ModuleError(
                "At least one 'servers' item is needed when creating a new application."
            )
        if self.want.inbound_virtual is None:
            raise F5ModuleError(
                "An 'inbound_virtual' must be specified when creating a new application."
            )
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self_link = self.create_on_device()
        if self.want.wait:
            self.wait_for_apply_template_task(self_link)
            if not self.exists():
                raise F5ModuleError(
                    "Failed to deploy application."
                )
        return True

    def create_on_device(self):
        params = self.changes.api_params()
        params['mode'] = 'CREATE'

        uri = 'https://{0}:{1}/mgmt/cm/global/tasks/apply-template'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp._content)
        return response['selfLink']

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove_from_device(self):
        params = dict(
            configSetName=self.want.name,
            mode='DELETE'
        )
        uri = 'https://{0}:{1}/mgmt/cm/global/tasks/apply-template'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )

        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp._content)
        return response['selfLink']

    def wait_for_apply_template_task(self, self_link):
        host = 'https://{0}:{1}'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        uri = self_link.replace('https://localhost', host)

        while True:
            resp = self.client.api.get(uri)
            try:
                response = resp.json()
            except ValueError as ex:
                raise F5ModuleError(str(ex))

            if response['status'] == 'FINISHED' and response.get('currentStep', None) == 'DONE':
                return True
            elif 'errorMessage' in response:
                raise F5ModuleError(response['errorMessage'])
            time.sleep(5)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            name=dict(required=True),
            description=dict(),
            servers=dict(
                type='list',
                options=dict(
                    address=dict(required=True),
                    port=dict(default=8000)
                )
            ),
            inbound_virtual=dict(
                type='dict',
                options=dict(
                    address=dict(required=True),
                    netmask=dict(required=True),
                    port=dict(default=53)
                )
            ),
            service_environment=dict(),
            add_analytics=dict(type='bool', default='no'),
            state=dict(
                default='present',
                choices=['present', 'absent']
            ),
            wait=dict(type='bool', default='yes')
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

    try:
        client = F5RestClient(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        exit_json(module, results, client)
    except F5ModuleError as ex:
        fail_json(module, ex, client)


if __name__ == '__main__':
    main()
