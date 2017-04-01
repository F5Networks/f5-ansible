#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
---
module: iworkflow_service_template
short_description: Manages Service Templates on iWorkflow.
description:
  - Manages Service Templates on iWorkflow. Service templates are created
    by the iWorkflow administrator and are consumed by iWorkflow tenants
    in the form of L4/L7 services. The Service Template can be configured
    to allow tenants to change certain values of the template such as
    the IP address of a VIP, or the port that a Virtual Server listens on.
version_added: "2.4"
options:
  name:
    description:
      - Name of the service template.
    required: True
  parameters:
    description:
      - A dictionary containing the values of input parameters that the
        Service Template contains. You will see these in iWorkflow's UI
        labeled as "Application Tier Information" and "Sections". This
        is the way by which you customize the Service Template and specify
        which values are tenant editable. Since this value can be particularly
        large, the recommended practice is to put it in an external file
        and include it with the Ansible C(file) or C(template) lookup plugins.
        This option is required when C(state) is C(present).
    required: False
    default: None
  connector:
    description:
      - The cloud connector associated with this Service Template. If you want
        to have this Service Template associated with all clouds, then specify
        a C(connector) of C(all). When creating a new Service Template, if no
        connector is specified, then C(all) clouds will be the default.
    required: False
    default: None
  base_template:
    description:
      - The iApp template that you want to base this Service Template off
        of. Note that, while iWorkflow's UI also allows you to specify another
        Service Template for the C(base_template), this module does not yet
        let you do that. This option is required when C(state) is C(present).
    required: False
    default: None
notes:
  - Requires the f5-sdk Python package on the remote host. This is as easy as
    pip install f5-sdk
  - Requires the deepdiff Python package on the Ansible controller host. This
    is as easy as pip install deepdiff.
requirements:
    - f5-sdk >= 2.3.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

from ansible.module_utils.f5_utils import *
from deepdiff import DeepDiff


class Parameters(AnsibleF5Parameters):
    api_map = {
        'templateName': 'name',
        'properties': 'connector',
        'overrides': 'parameters'
    }

    returnables = ['vars']

    api_attributes = [
        'overrides', 'templateName', 'parentReference', 'properties'
    ]

    updatables = ['tables', 'vars']

    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        if params:
            self.update(params=params)

    def update(self, params=None):
        if params:
            for k,v in iteritems(params):
                if self.api_map is not None and k in self.api_map:
                    map_key = self.api_map[k]
                else:
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    def _get_connector_collection(self):
        return self.client.api.cm.cloud.connectors.locals.get_collection()

    def _get_connector_selflink(self, connector, collection):
        for resource in collection:
            if str(resource.displayName) != "BIG-IP":
                continue
            if str(resource.name) != connector:
                continue
            return str(resource.selfLink)
        return None

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result

    @property
    def tables(self):
        result = []
        if not self._values['tables']:
            return None
        tables = self._values['tables']
        for table in tables:
            tmp = dict()
            name = table.get('name', None)
            if name is None:
                raise F5ModuleError(
                    "One of the provided tables does not have a name"
                )
            tmp['name'] = str(name)
            columns = table.get('columns', None)
            if columns:
                tmp['columns'] = []
                for column in columns:
                    tmp['columns'].append(
                        dict((str(k),str(v)) for k,v in iteritems(column))
                    )
                # You cannot have rows without columns
                rows = table.get('rows', None)
                if rows:
                    tmp['rows'] = []
                    for row in rows:
                        tmp['rows'].append([str(x) for x in row])
            description = table.get('description', None)
            tmp['description'] = str(description)
            result.append(tmp)
        result = sorted(result, key=lambda k: k['name'])
        return result

    @tables.setter
    def tables(self, value):
        self._values['tables'] = value

    @property
    def vars(self):
        result = []
        if not self._values['vars']:
            return None
        variables = self._values['vars']
        for variable in variables:
            tmp = dict((str(k), v) for k, v in iteritems(variable))
            result.append(tmp)
        result = sorted(result, key=lambda k: k['name'])
        return result

    @vars.setter
    def vars(self, value):
        self._values['vars'] = value

    @property
    def parameters(self):
        return dict(
            tables=self.tables,
            vars=self.vars
        )

    @parameters.setter
    def parameters(self, value):
        if value is None:
            return
        if 'tables' in value:
            self.tables = value['tables']
        if 'vars' in value:
            self.vars = value['vars']

    @property
    def connector(self):
        connector = None
        if self._values['connector'] is None:
            return self._values['connector']
        elif self._values['connector'] == 'all':
            connector = 'all'
        elif isinstance(self._values['connector'], basestring):
            collection = self._get_connector_collection()
            result = self._get_connector_selflink(str(self._values['connector']), collection)
            connector = result
        elif 'provider' in self._values['connector'][0]:
            # Case for the REST API
            item = self._values['connector'][0]['provider']
            connector = str(item)
        if connector is None:
            raise F5ModuleError(
                "The specified connector was not found"
            )
        elif connector == 'all':
            result = [
                dict(
                    id="cloudConnectorReference",
                    isRequired=True,
                    defaultValue=""
                )
            ]
            return result
        else:
            result = [
                dict(
                    id="cloudConnectorReference",
                    isRequired=True,
                    provider=connector
                )
            ]
            return result

    @property
    def parentReference(self):
        return dict(
            link="https://localhost/mgmt/cm/cloud/templates/iapp/{0}".format(
                self._values['base_template']
            )
        )

    @parentReference.setter
    def parentReference(self, value):
        self._values['base_template'] = value['link']


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters()
            self.changes.client = self.client
            self.changes.update(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = str(DeepDiff(attr1,attr2))
        if changed:
            self.changes = Parameters()
            self.changes.client = self.client
            self.changes.update(changed)
            return True
        return False

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        result = self.client.api.cm.cloud.provider.templates.iapps.iapp.exists(
            name=self.want.name
        )
        return result

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):
        self._set_changed_options()
        if self.want.connector is None:
            self.want.update({'connector': 'all'})

        if self.client.check_mode:
            return True
        if self.want.base_template is None:
            raise F5ModuleError(
                "A 'base_template' is required when creating a new Service Template"
            )
        self.create_on_device()
        return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update_on_device(self):
        params = self.want.api_params()
        resource = self.client.api.cm.cloud.provider.templates.iapps.iapp.load(
            name=self.want.name
        )
        resource.update(**params)

    def read_current_from_device(self):
        resource = self.client.api.cm.cloud.provider.templates.iapps.iapp.load(
            name=self.want.name,
        )
        result = resource.attrs
        result['parameters'] = result.pop('overrides', None)
        params = Parameters()
        params.client = self.client
        params.update(result)

        return params

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.cm.cloud.provider.templates.iapps.iapp.create(
            isF5Example=False,
            **params
        )

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the iApp service")
        return True

    def remove_from_device(self):
        resource = self.client.api.cm.cloud.provider.templates.iapps.iapp.load(
            name=self.want.name,
        )
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(required=True),
            base_template=dict(
                required=False,
                default=None
            ),
            parameters=dict(
                required=False,
                default=None,
                type='dict'
            ),
            connector=dict(
                required=False,
                default=None
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.f5_product_name = 'iworkflow'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
