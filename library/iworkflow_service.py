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
module: iworkflow_service
short_description: Manages L4/L7 Services on iWorkflow.
description:
  - Manages L4/L7 Service on iWorkflow. Services can only be created and
    otherwise managed by tenants on iWorkflow. Since all of the F5 modules
    assume the use of the administrator account, the user of this module
    will need to include the C(tenant) option if they want to use this
    module with the admin account.
version_added: "2.4"
options:
  tenant:
    description:
      - The tenant whose service is going to be managed. This is a required
        option when using the system's C(admin) account as the admin is not
        a tenant, and therefore cannot manipulate any of the L4/L7 services
        that exist. If the C(user) option is not the C(admin) account, then
        this tenant option is assumed to be the user who is connecting to
        the BIG-IP. This assumption can always be changed by setting this
        option to whatever tenant you wish.
    required: False
    default: None
  name:
    description:
      - Name of the L4/L7 service.
    required: True
  parameters:
    description:
      - A dictionary containing the values of input parameters that the
        service administrator has made available for tenant editing.
    required: False
    default: None
  connector:
    description:
      - The cloud connector associated with this L4/L7 service. This option
        is required when C(state) is C(present).
    required: False
    default: None
  service_template:
    description:
      - The Service Template that you want to base this L4/L7 Service off of.
        This option is required when C(state) is C(present).
    required: False
    default: None
notes:
  - Requires the f5-sdk Python package on the remote host. This is as easy as
    pip install f5-sdk.
  - L4/L7 Services cannot be updated once they have been created. Instead, you
    must first delete the service and then re-create it.
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


class Parameters(AnsibleF5Parameters):
    api_map = {
        'properties': 'connector'
    }

    returnables = ['vars']

    api_attributes = [
        'name', 'vars', 'tables', 'tenantTemplateReference', 'tenantReference', 'properties'
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
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
            return result
        except Exception:
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

    def _username_has_admin_role(self, username):
        collection = self._get_users_with_admin_role()
        for resource in collection.userReferences:
            if resource.name == username:
                return True
        return False

    def _get_users_with_admin_role(self):
        return self.client.shared.authz.roles_s.role.load(
            name='Administrator',
            requests_params=dict(
                params='$expand=userReferences'
            )
        )

    @property
    def tenant(self):
        if self._values['tenant'] is None:
            if self._username_has_admin_role(self.want.user):
                raise F5ModuleError(
                    "A 'tenant' must be specified when using an "
                    "Administrator account"
                )
            else:
                # This allows tenant users to assume their username
                # is the tenant that is interacting with iWorkflow.
                return str(self.want.user)
        else:
            return str(self._values['tenant'])

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
            columns = table.get('columnNames', None)
            if columns:
                tmp['columnNames'] = []
                for column in columns:
                    tmp['columnNames'].append(
                        dict((str(k),str(v)) for k,v in iteritems(column))
                    )
                # You cannot have rows without columns
                rows = table.get('rows', None)
                if rows:
                    tmp['rows'] = list(list())
                    for row in rows:
                        # This looks weird, but iWorkflow puts the "many" rows
                        # into a single row. The actual payload looks like this
                        #
                        # "rows": [
                        #   [
                        #     "12.0.1.11",
                        #     "80"
                        #   ],
                        #   [
                        #     "12.0.1.12"
                        #   ]
                        # ]
                        tmp['rows'][0].append([str(x) for x in row])
            description = table.get('description', None)
            if description:
                tmp['description'] = str(description)
            section = table.get('section', None)
            if section:
                tmp['section'] = str(section)
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
            return None
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
        else:
            return [
                dict(
                    id="cloudConnectorReference",
                    value=connector
                )
            ]

    @property
    def tenantTemplateReference(self):
        result = dict(
            link="https://localhost/mgmt/cm/cloud/tenant/templates/iapp/{0}".format(
                self._values['service_template']
            )
        )
        return result


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
        tenant = self.client.api.cm.cloud.tenants_s.tenant.load(name=self.want.tenant)
        result = tenant.services.iapps.iapp.exists(name=self.want.name)
        return result

    def present(self):
        if self.exists():
            return False
        else:
            return self.create()

    def create(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        if self.want.service_template is None:
            raise F5ModuleError(
                "A 'service_template' is required when creating a new L4/L7 Service"
            )
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.want.api_params()
        tenant = self.client.api.cm.cloud.tenants_s.tenant.load(name=self.want.tenant)
        resource = tenant.services.iapps.iapp.create(
            isF5Example=False,
            **params
        )
        self._wait_for_state_to_activate(resource)

    def _wait_for_state_to_activate(self, resource):
        # Wait no more than half an hour
        for x in range(1, 180):
            resource.refresh()
            try:
                stats = resource.stats.load()
                attrs = stats.attrs
                placement = int(attrs['entries']['health.placement']['value'])
                description = str(attrs['entries']['health.placement']['description'])
                if placement == 1:
                    break
                elif placement == 0 and 'Failed' in description:
                    raise F5ModuleError(
                        str(resource.error)
                    )
            except KeyError:
                pass
            time.sleep(10)

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
        tenant = self.client.api.cm.cloud.tenants_s.tenant.load(name=self.want.tenant)
        resource = tenant.services.iapps.iapp.load(name=self.want.name)
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(required=True),
            service_template=dict(
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
            tenant=dict(
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
