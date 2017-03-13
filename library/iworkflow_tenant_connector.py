#!/usr/bin/python
#
# Copyright 2016 F5 Networks Inc.
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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
module: iworkflow_tenant
short_description: Manage tenants in iWorkflow.
description:
  - Manage tenants in iWorkflow.
version_added: 2.3
options:
  connector:
    description:
      - Connector that you want to associate with the tenant
    required: True
  tenant:
    description:
      - Tenant that you wish to modify.
    required: True
  state:
    description:
      - Whether the managed device should exist, or not, in iWorkflow.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Tenants are not useful unless you associate them with a connector
    using the C(iworkflow_tenant_connector) module.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.2.0
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
        'addressContact': 'address'
    }
    returnables = []

    api_attributes = [
        'description', 'addressContact', 'phone', 'email'
    ]

    updatables = []

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = attr1
        if changed:
            self.changes = Parameters(changed)
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
        connector = self.get_connector_from_connector_name(
            self.want.connector
        )
        if not connector:
            raise F5ModuleError(
                "The specified connector was not found"
            )
        tenant = self.get_tenant_from_tenant_name(self.want.tenant)
        if not tenant:
            raise F5ModuleError(
                "The specified tenant was not found"
            )
        if not hasattr(tenant, 'cloudConnectorReferences'):
            return False

        connector_refs = self.get_selflinks_from_connectors(
            self.want.connector
        )
        for reference in tenant.cloudConnectorReferences:
            if str(reference['link']) in connector_refs:
                return True
        return False

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def update(self):
        # TODO:  update this to ensure the list of tenants is correct for the connector
        pass

    def create(self):
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def get_connector_from_connector_name(self, name):
        connector = None
        connectors = self.client.api.cm.cloud.connectors.locals.get_collection()
        for connector in connectors:
            if connector.displayName != "BIG-IP":
                continue
            if connector.name != name:
                continue
            break
        return connector

    def get_tenant_from_tenant_name(self, name):
        tenants = self.client.api.cm.cloud.tenants_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(name)
            )
        )
        return tenants.pop(0)

    def get_selflinks_from_connectors(self, connectors):
        links = []
        for connector in connectors:
            conn = self.get_connector_from_connector_name(connector)
            links.append(conn.selfLink)
        return links

    def create_on_device(self):
        connector_refs = self.get_selflinks_from_connectors(
            self.want.connector
        )
        connectors = [dict(link=link) for link in connector_refs]
        tenant = self.get_tenant_from_tenant_name(
            self.want.tenant
        )
        tenant.update(cloudConnectorReferences=connectors)
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the tenant connector")
        return True

    def remove_from_device(self):
        tenant = self.get_tenant_from_tenant_name(
            self.want.tenant
        )
        current = [x['link'] for x in tenant.cloudConnectorReferences]
        remove = self.get_selflinks_from_connectors(
            self.want.connector
        )
        result = set(current) - set(remove)
        connectors = [dict(link=link) for link in result]
        tenant.update(cloudConnectorReferences=connectors)
        return True


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            connector=dict(
                required=True,
                type='list'
            ),
            tenant=dict(
                required=True
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
