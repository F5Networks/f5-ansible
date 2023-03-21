#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bigiq_application_http
short_description: Manages BIG-IQ HTTP applications
description:
  - Manages BIG-IQ applications used for load balancing an HTTP application on
    port 80 on BIG-IP systems.
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the new application.
    type: str
    required: True
  description:
    description:
      - Description of the application.
    type: str
  servers:
    description:
      - A list of servers on which the application is hosted.
      - If you are familiar with other BIG-IP settings, you might also refer to this
        list as the list of pool members.
      - When creating a new application, at least one server is required.
    type: list
    elements: dict
    suboptions:
      address:
        description:
          - The IP address of the server.
        type: str
        required: True
      port:
        description:
          - The port of the server.
          - When creating a new application and specifying a server, if this parameter
            is not provided, the default is C(80).
        type: str
        default: 80
  inbound_virtual:
    description:
      - Settings to configure the virtual which receives the inbound connection.
      - This virtual is used to host the HTTP endpoint of the application.
    suboptions:
      address:
        description:
          - Specifies destination IP address information to which the virtual server
            sends traffic.
          - This parameter is required when creating a new application.
        type: str
        required: True
      netmask:
        description:
          - Specifies the netmask to associate with the given C(destination).
          - This parameter is required when creating a new application.
        type: str
        required: True
      port:
        description:
          - The port on which the virtual listens for connections.
          - When creating a new application, if this parameter is not specified, the
            default value is C(80).
        type: str
        default: 80
    type: dict
  service_environment:
    description:
      - Specifies the name of service environment to which the application is
        deployed.
      - When creating a new application, this parameter is required.
      - The service environment type is automatically discovered by this module.
        Therefore, it is crucial that you maintain unique names for items in the
        different service environment types (at this time, SSGs and BIG-IPs).
    type: str
  add_analytics:
    description:
      - Collects statistics of the BIG-IP to which the application is deployed.
      - This parameter is only relevant when specifying a C(service_environment) which
        is a BIG-IP; not an SSG.
    type: bool
    default: false
  state:
    description:
      - The state of the resource on the system.
      - When C(present), guarantees the resource exists with the provided attributes.
      - When C(absent), removes the resource from the system.
    type: str
    choices:
      - absent
      - present
    default: present
  wait:
    description:
      - If the module should wait for the application to be created, deleted, or updated.
    type: bool
    default: true
extends_documentation_fragment: f5networks.f5_modules.f5
notes:
  - This module does not support updating of your application (whether deployed or not).
    If you need to update the application, we recommend removing and recreating it.
  - This module will not work on BIG-IQ version 6.1.x or greater.
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Load balance an HTTP application on port 80 on BIG-IP
  bigiq_application_http:
    name: my-app
    description: Redirect HTTP to HTTPS
    service_environment: my-ssg
    servers:
      - address: 1.2.3.4
        port: 8080
      - address: 5.6.7.8
        port: 8080
    inbound_virtual:
      name: foo
      address: 2.2.2.2
      netmask: 255.255.255.255
      port: 443
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
  type: str
  sample: My application
service_environment:
  description: The environment to which the service was deployed.
  returned: changed
  type: str
  sample: my-ssg1
inbound_virtual_destination:
  description: The destination of the virtual that was created.
  returned: changed
  type: str
  sample: 6.7.8.9
inbound_virtual_netmask:
  description: The network mask of the provided inbound destination.
  returned: changed
  type: str
  sample: 255.255.255.0
inbound_virtual_port:
  description: The port on which the inbound virtual address listens.
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
      type: str
      sample: 2.3.4.5
    port:
      description: The port on which the server listens.
      returned: changed
      type: int
      sample: 8080
  sample: hash/dictionary of values
'''

import time
import traceback
from datetime import datetime

try:
    from packaging.version import Version
except ImportError:
    HAS_PACKAGING = False
    Version = None
    PACKAGING_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_PACKAGING = True
    PACKAGING_IMPORT_ERROR = None

from ansible.module_utils.basic import (
    AnsibleModule, missing_required_lib
)

from ..module_utils.bigip import F5RestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, f5_argument_spec
)
from ..module_utils.icontrol import bigiq_version
from ..module_utils.ipaddress import is_valid_ip
from ..module_utils.teem import send_teem


class Parameters(AnsibleF5Parameters):
    api_map = {
        'templateReference': 'template_reference',
        'subPath': 'sub_path',
        'ssgReference': 'ssg_reference',
        'configSetName': 'config_set_name',
        'defaultDeviceReference': 'default_device_reference',
        'addAnalytics': 'add_analytics'
    }

    api_attributes = [
        'resources', 'description', 'configSetName', 'subPath', 'templateReference',
        'ssgReference', 'defaultDeviceReference', 'addAnalytics'
    ]

    returnables = [
        'resources', 'description', 'config_set_name', 'sub_path', 'template_reference',
        'ssg_reference', 'default_device_reference', 'servers', 'inbound_virtual',
        'add_analytics'
    ]

    updatables = [
        'resources', 'description', 'config_set_name', 'sub_path', 'template_reference',
        'ssg_reference', 'default_device_reference', 'servers', 'add_analytics'
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
        filter = "name+eq+'Default-f5-HTTP-lb-template'"
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
            filter = "address+eq+'{0}'".format(self.service_environment)
        else:
            # Assume a hostname was specified
            filter = "hostname+eq+'{0}'".format(self.service_environment)

        uri = "https://{0}:{1}/mgmt/shared/resolver/device-groups/cm-adccore-allbigipDevices/devices/" \
              "?$filter={2}&$top=1&$select=selfLink".format(self.client.provider['server'],
                                                            self.client.provider['server_port'], filter)
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status == 200 and response['totalItems'] == 0:
            return None
        elif 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp._content)
        result = dict(link=response['items'][0]['selfLink'])
        return result

    @property
    def ssg_reference(self):
        filter = "name+eq+'{0}'".format(self.service_environment)
        uri = "https://{0}:{1}/mgmt/cm/cloud/service-scaling-groups/?$filter={2}&$top=1&$select=selfLink".format(
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
            return None
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
        result.update(self.http_profile)
        result.update(self.http_monitor)
        result.update(self.virtual)
        result.update(self.pool)
        result.update(self.nodes)
        return result

    @property
    def virtual(self):
        result = dict()
        result['ltm:virtual::b487671f29ba'] = [
            dict(
                parameters=dict(
                    name='virtual',
                    destinationAddress=self.inbound_virtual['address'],
                    mask=self.inbound_virtual['netmask'],
                    destinationPort=self.inbound_virtual.get('port', 80)
                ),
                subcollectionResources=self.profiles
            )
        ]
        return result

    @property
    def profiles(self):
        result = {
            'profiles:9448fe71611e': [
                dict(
                    parameters=dict()
                )
            ],
            'profiles:03a4950ab656': [
                dict(
                    parameters=dict()
                )
            ]
        }
        return result

    @property
    def pool(self):
        result = dict()
        result['ltm:pool:9a593d17495b'] = [
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
        result['members:5109c66dfbac'] = []
        for x in self.servers:
            member = dict(
                parameters=dict(
                    port=x.get('port', 80),
                    nodeReference=dict(
                        link='#/resources/ltm:node:9e76a6323321/{0}'.format(x['address']),
                        fullPath='# {0}'.format(x['address'])
                    )
                )
            )
            result['members:5109c66dfbac'].append(member)
        return result

    @property
    def http_profile(self):
        result = dict()
        result['ltm:profile:http:03a4950ab656'] = [
            dict(
                parameters=dict(
                    name='profile_http'
                )
            )
        ]
        return result

    @property
    def http_monitor(self):
        result = dict()
        result['ltm:monitor:http:ea4346e49cdf'] = [
            dict(
                parameters=dict(
                    name='monitor-http'
                )
            )
        ]
        return result

    @property
    def nodes(self):
        result = dict()
        result['ltm:node:9e76a6323321'] = []
        for x in self.servers:
            tmp = dict(
                parameters=dict(
                    name=x['address'],
                    address=x['address']
                )
            )
            result['ltm:node:9e76a6323321'].append(tmp)
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
        self.client = F5RestClient(**self.module.params)
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

    def check_bigiq_version(self, version):
        if Version(version) >= Version('6.1.0'):
            raise F5ModuleError(
                'Module supports only BIGIQ version 6.0.x or lower.'
            )

    def exec_module(self):
        start = datetime.now().isoformat()
        version = bigiq_version(self.client)
        self.check_bigiq_version(version)
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
        send_teem(start, self.client, self.module, version)
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
        uri = "https://{0}:{1}/mgmt/ap/query/v1/tenants/default/reports/AllApplicationsList" \
              "?$filter=name+eq+'{2}'".format(self.client.provider['server'],
                                              self.client.provider['server_port'],
                                              self.want.name)
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if (resp.status == 200 and 'result' in response
           and 'totalItems' in response['result'] and response['result']['totalItems'] == 0):
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

    def has_no_service_environment(self):
        if self.want.default_device_reference is None and self.want.ssg_reference is None:
            return True
        return False

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

        if self.has_no_service_environment():
            raise F5ModuleError(
                "The specified 'service_environment' ({0}) was not found.".format(self.want.service_environment)
            )

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
                elements='dict',
                options=dict(
                    address=dict(required=True),
                    port=dict(default=80)
                )
            ),
            inbound_virtual=dict(
                type='dict',
                options=dict(
                    address=dict(required=True),
                    netmask=dict(required=True),
                    port=dict(default=80)
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

    if not HAS_PACKAGING:
        module.fail_json(
            msg=missing_required_lib('packaging'),
            exception=PACKAGING_IMPORT_ERROR
        )

    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
