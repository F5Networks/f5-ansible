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
module: iworkflow_iapp_template
short_description: Manages iApp templates
description:
  - Manages TCL iApp services on a BIG-IP.
version_added: "2.4"
options:
  name:
    description:
      - The name of the iApp template that you want to create on the
        device. This is usually included in the template itself. This
        option is typically used in cases where the template no longer
        exists on disk (to reference) and the C(state) is C(absent).
    required: False
    default: None
  template_content:
    description:
      - The contents of a valid iApp template in a tmpl file. This iApp
        Template should be versioned and tested for compatibility with
        iWorkflow Tenant Services and a BIG-IP version of 11.5.3.2 or later.
        This option is only required when creating new template in iWorkflow.
        When you are deleting iApp templates, you will need to specify either
        one of C(name) or C(template_content).
    required: False
    default: None
  device:
    description:
      - Managed BIG-IP that you want to get template JSON from. This option
        is only required when C(state) is C(present).
    required: False
    default: None
  state:
    description:
      - When C(present), ensures that the iApp service is created and running.
        When C(absent), ensures that the iApp service has been removed.
    required: False
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.3.0
    - iWorkflow >= 2.1.0
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add AppSvcs Integration to iWorkflow
  iworkflow_iapp_template:
      device: "my-bigip-1"
      template_content: "{{ lookup('file', 'appsvcs_integration_v2.0_001.tmpl') }}"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost

- name: Remove AppSvcs Integration from iWorkflow
  iworkflow_iapp_template:
      name: "appsvcs_integration_v2.0_001"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

import re
import time

from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    defaultdict,
    F5ModuleError,
    HAS_F5SDK,
    iControlUnexpectedHTTPError,
    iteritems,
)
from f5.utils.iapp_parser import (
    IappParser,
    NonextantTemplateNameException
)


class Parameters(AnsibleF5Parameters):
    api_map = {
        'templateContent': 'template_content'
    }

    api_attributes = [
        'templateContent', 'deviceForJSONTransformation'
    ]

    returnables = []

    updatables = [
        'template_content',
    ]

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

    def _squash_template_name_prefix(self):
        name = self._get_template_name()
        pattern = r'sys\s+application\s+template\s+/Common/{0}'.format(name)
        replace = 'sys application template {0}'.format(name)
        self._values['template_content'] = re.sub(pattern, replace, self._values['template_content'])

    def _get_template_name(self):
        parser = IappParser(self._values['template_content'])
        tmpl = parser.parse_template()
        return tmpl['name']

    def _get_device_collection(self):
        dg = self.client.api.shared.resolver.device_groups
        result = dg.cm_cloud_managed_devices.devices_s.get_collection()
        return result

    def _get_device_selflink(self, device, collection):
        for resource in collection:
            if str(resource.product) != "BIG-IP":
                continue
            # The supplied device can be in several formats.
            if str(resource.hostname) == device:
                return str(resource.selfLink)
            elif str(resource.address) == device:
                return str(resource.selfLink)
            elif str(resource.managementAddress) == device:
                return str(resource.selfLink)
        raise F5ModuleError(
            "Device {0} was not found".format(device)
        )

    @property
    def name(self):
        if self._values['name']:
            return self._values['name']

        if self._values['template_content']:
            try:
                self._squash_template_name_prefix()
                name = self._get_template_name()
                self._values['name'] = name
                return name
            except NonextantTemplateNameException:
                return F5ModuleError(
                    "No template name was found in the template"
                )
        return None

    @property
    def device(self):
        if isinstance(self._values['device'], basestring):
            collection = self._get_device_collection()
            result = self._get_device_selflink(str(self._values['device']), collection)
            return result
        elif 'deviceForJSONTransformation' in self._values['device']:
            # Case for the REST API
            item = self._values['device']['deviceForJSONTransformation']
            return str(item['deviceReference']['link'])

    @device.setter
    def device(self, value):
        self._values['device'] = value

    @property
    def deviceForJSONTransformation(self):
        result = dict(
            link=self.device
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
        self.changes.client = self.client

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
                    changed[key] = attr1
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

        result.update(**self.changes.to_return())
        result.update(dict(changed=changed))
        return result

    def exists(self):
        return self.client.api.cm.cloud.templates.iapps.iapp.exists(
            name=self.want.name
        )

    def present(self):
        if self.exists():
            return False
        else:
            return self.create()

    def create(self):
        if self.client.check_mode:
            return True
        if self.want.template_content is None:
            raise F5ModuleError(
                ""
            )
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.want.api_params()
        params['name'] = self.want.name
        self.client.api.cm.cloud.templates.iapps.iapp.create(
            **params
        )
        time.sleep(5)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the iApp template")
        return True

    def remove_from_device(self):
        resource = self.client.api.cm.cloud.templates.iapps.iapp.load(
            name=self.want.name
        )
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(
                required=False,
                default=None
            ),
            template_content=dict(required=False),
            device=dict(
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
