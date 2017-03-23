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
module: iworkflow_tenant_connector
short_description: Manage connectors associated with tenants in iWorkflow.
description:
  - Manage connectors associated with tenants in iWorkflow.
version_added: 2.4
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
    - f5-sdk >= 2.3.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Register connector to tenant
  iworkflow_tenant_connector:
      tenant: "tenant-foo"
      connector: "connector-foo"
      server: "iwf.mydomain.com"
      user: "admin"
      password: "secret"
      validate_certs: "no"
      state: "present"

- name: Register multiple connectors to tenant
  iworkflow_tenant_connector:
      tenant: "tenant-foo"
      connector: "{{ item }}"
      server: "iwf.mydomain.com"
      user: "admin"
      password: "secret"
      validate_certs: "no"
      state: "present"
  with_items:
      - "connector-one"
      - "connector-two"

- name: Unregister connector from tenant
  iworkflow_tenant_connector:
      tenant: "tenant-foo"
      connector: "connector-foo"
      server: "iwf.mydomain.com"
      user: "admin"
      password: "secret"
      validate_certs: "no"
      state: "absent"
'''

RETURN = '''

'''

import re

from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    defaultdict,
    F5ModuleError,
    HAS_F5SDK,
    iteritems
)


class Connector(object):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        self._values = defaultdict(lambda: None)

    def update(self, params=None):
        params = str(params)
        resource = None
        collection = self._get_connector_collection()
        if re.search(r'([0-9-a-z]+\-){4}[0-9-a-z]+', params, re.I):
            # Handle cases where the REST API sent us self links
            for connector in collection:
                if str(connector.displayName) != "BIG-IP":
                    continue
                if str(connector.selfLink) != params:
                    continue
                resource = connector
                break
        else:
            # Handle the case where a user sends us a list of connector names
            for connector in collection:
                if str(connector.displayName) != "BIG-IP":
                    continue
                if str(connector.name) != params:
                    continue
                resource = connector
                break
        if not resource:
            raise F5ModuleError(
                "Connector {0} was not found".format(params)
            )
        self._values['name'] = resource.name
        self._values['selfLink'] = resource.selfLink

    def _get_connector_collection(self):
        return self.client.api.cm.cloud.connectors.locals.get_collection()

    @property
    def name(self):
        return str(self._values['name'])

    @property
    def selfLink(self):
        return str(self._values['selfLink'])


class Tenant(object):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        self._values = defaultdict(lambda: None)
        self.connectors = []

    def update(self, params=None):
        # Handle the case where the Ansible user provides a name as string
        if isinstance(params, basestring):
            self._values['name'] = params
            resource = self._load_resource_by_name()
            try:
                for reference in resource.cloudConnectorReferences:
                    connector = Connector()
                    connector.client = self.client
                    connector.update(reference['link'])
                    self.connectors.append(connector)
            except AttributeError:
                pass
        else:
            # Handle the case where the REST API provides a dict
            self._values['name'] = params['name']
            try:
                for reference in params['cloudConnectorReferences']:
                    connector = Connector()
                    connector.client = self.client
                    connector.update(reference['link'])
                    self.connectors.append(connector)
            except AttributeError:
                pass

    def _load_resource_by_name(self):
        resource = self.client.api.cm.cloud.tenants_s.tenant.load(
            name=self.name
        )
        return resource

    @property
    def name(self):
        return str(self._values['name'])


class Parameters(AnsibleF5Parameters):
    returnables = []
    api_attributes = []

    def __init__(self, params=None, client=None):
        self.client = client
        self._values = defaultdict(lambda: None)
        if params:
            self.update(params)

    def update(self, params=None):
        if params:
            for k, v in iteritems(params):
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
    def tenant(self):
        return self._values['tenant']

    @tenant.setter
    def tenant(self, value):
        tenant = Tenant()
        tenant.client = self.client
        tenant.update(value)
        self._values['tenant'] = tenant

    @property
    def connector(self):
        return self._values['connectors']

    @connector.setter
    def connector(self, connector):
        result = []
        conn = Connector()
        conn.client = self.client
        conn.update(connector)
        result.append(conn)
        self._values['connectors'] = result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None

        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)

        self.changes = Parameters()
        self.changes.client = self.client

    def _set_changed_options(self):
        changed = {}
        want = set([x.selfLink for x in self.want.tenant.connectors])
        changed['connections'] = want
        self.changes = Parameters()
        self.changes.client = self.client
        self.changes.update(changed)
        return True

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except IOError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        if not self.want.tenant.connectors:
            return False

        # Getting new sets of parameters here ensures that nothing is
        # cached when, for example, delete is used.
        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)

        tcr = set([x.selfLink for x in self.want.tenant.connectors])
        cr = set([x.selfLink for x in self.want.connectors])
        if cr.issubset(tcr):
            return True
        return False

    def present(self):
        if self.exists():
            return False
        else:
            return self.create()

    def create(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        connector_refs = self.to_add()
        resource = self.client.api.cm.cloud.tenants_s.tenant.load(
            name=self.want.tenant.name
        )
        resource.update(
            cloudConnectorReferences=connector_refs
        )
        return True

    def to_add(self):
        want = [x.selfLink for x in self.want.connectors]
        have = [x.selfLink for x in self.want.tenant.connectors]
        references = set(want + have)
        return [dict(link=x) for x in references]

    def read_current_from_device(self):
        result = dict()
        resource = self.client.api.cm.cloud.tenants_s.tenant.load(
            name=self.want.tenant.name
        )
        result['tenant'] = resource.attrs
        params = Parameters()
        params.client = self.client
        params.update(result)
        return params

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        self.have = self.read_current_from_device()
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the tenant connector reference")
        return True

    def remove_from_device(self):
        references = self.to_remove()
        resource = self.client.api.cm.cloud.tenants_s.tenant.load(
            name=self.want.tenant.name
        )
        resource.update(cloudConnectorReferences=references)
        return True

    def to_remove(self):
        want = set([x.selfLink for x in self.want.connectors])
        have = set([x.selfLink for x in self.want.tenant.connectors])
        references = set(have - want)
        return [dict(link=x) for x in references]


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            connector=dict(
                required=True,
                type='str'
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
