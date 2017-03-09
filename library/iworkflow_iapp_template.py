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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: iworkflow_iapp_template
short_description: Manages iApp templates
description:
  - Manages TCL iApp services on a BIG-IP.
version_added: "2.4"
options:
  template_content:
    description:
      - The contents of a valid iApp template in a tmpl file. This iApp
        Template should be versioned and tested for compatibility with
        iWorkflow Tenant Services and a BIG-IP version of 11.5.3.2 or later.
    required: True
    default: None
  template:
    description:
      - A JSON representation of the iApp template that was imported into
        iWorkflow.
    required: False
    default: None
  device:
    description:
      - Managed BIG-IP that you want to get template JSON from. Either one
        of C(managed_device) or C(template) must be provided.
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
  min_bigip_version:
    description:
      - asdasd
    required: False
    default: None
  max_bigip_version:
    description:
      - asdasd
    required: False
    default: None
  unsupported_bigip_versions:
    description:
      - asdasd
    required: False
    default: None
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Create HTTP iApp service from iApp template
  bigip_iapp_template:
      name: "foo-service"
      template: "f5.http"
      parameters: "{{ lookup('file', 'f5.http.parameters.json') }}"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''


from ansible.module_utils.f5_utils import *
from deepdiff import DeepDiff
from distutils.version import LooseVersion


class Parameters(AnsibleF5Parameters):
    returnables = [
        'min_bigip_version', 'max_bigip_version', 'unsupported_bigip_versions'
    ]

    api_attributes = [
        'templateContent', 'deviceForJSONTransformation', 'template',
        'minSupportedBIGIPVersion', 'maxSupportedBIGIPVersion',
        'unsupportedBIGIPVersions'
    ]

    updatables = [
        'template_content', 'min_bigip_version'
    ]

    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        if params:
            for k,v in iteritems(params):
                setattr(self, k, v)

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

    @property
    def min_bigip_version(self, value):
        absolute_minimum = LooseVersion('11.5.3.2')
        version = LooseVersion(value)
        if version < absolute_minimum:
            raise F5ModuleError(
                "The specified 'min_bigip_version' is not supported by iWorkflow"
            )
        self._values['min_bigip_version'] = value

    @property
    def template(self):
        if self._values['template'] is None:
            return None
        if self._values['template'].startswith("/"+self.partition):
            return self._values['template']
        else:
            return '/{0}/{1}'.format(
                self.partition, self._values['template']
            )

    @template.setter
    def template(self, value):
        self._values['template'] = value


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = None

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
                    changed[key] = str(DeepDiff(attr1,attr2))
        if changed:
            self.changes = Parameters(changed)
            return True
        return False

    def exec_module(self):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

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
        return self.client.api.tm.sys.application.services.service.exists(
            name=self.want.name,
            partition=self.want.partition
        )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):

        if self.client.check_mode:
            return True
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
        resource = self.client.api.tm.sys.application.services.service.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.update(**params)

    def read_current_from_device(self):
        result = self.client.api.tm.sys.application.services.service.load(
            name=self.want.name,
            partition=self.want.partition
        ).to_dict()
        result.pop('_meta_data', None)
        return Parameters(result)

    def format_params(self, params):
        result = dict()
        for k,v in iteritems(self.module.params):
            if k in params and params[k] is not None:
                result[k] = str(params[k])
            else:
                result[k] = v
        source = result.get('parameters_src', None)
        content = result.get('parameters', None)
        if source or content:
            result['content'] = self.get_iapp_template_source(source, content)
        return result

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.sys.application.services.service.create(
            name=self.want.name,
            partition=self.want.partition,
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
        resource = self.client.api.tm.sys.application.services.service.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            template_content=dict(required=True),
            template=dict(
                required=False,
                default=None
            ),
            device=dict(
                required=False,
                default=None
            ),
            min_bigip_version=dict(
                required=False,
                default=None
            ),
            max_bigip_version=dict(
                required=False,
                default=None
            ),
            unsupported_bigip_versions=dict(
                required=False,
                type='list',
                default=None
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.mutually_exclusive = [
            ['template', 'managed_device']
        ]
        self.f5_product_name = 'iworkflow'


def main():
    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        mutually_exclusive=spec.mutually_exclusive,
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
