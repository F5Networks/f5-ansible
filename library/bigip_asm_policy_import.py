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

import os
import time
from icontrol.exceptions import iControlUnexpectedHTTPError
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    defaultdict,
    HAS_F5SDK,
    F5ModuleError,
    iteritems
)


class Parameters(AnsibleF5Parameters):
    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        if params:
            self.update(params=params)

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
                        # If the mapped value does not have
                        # an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    updatables = []
    returnables = []
    api_attributes = ['name', 'file', 'filename', 'policyTemplateReference']
    api_map = {}

    @property
    def file(self):
        path = self._values['file']
        inline = self._values['inline']
        if inline:
            with open(path, 'r') as f:
                contents = f.read()
                self._values['file_read'] = contents
            return self._values['file_read']
        else:
            return self._values['file']

    @property
    def template(self):
        want_name = self._values['template']
        if want_name is None:
            return None
        if self._template_exists_on_device(want_name):
            return self._values['template']
        else:
            raise F5ModuleError('Template with the given name: {0} does not exist'.format(want_name))

    def _template_exists_on_device(self, name):
        collection = self._templates_on_device()
        for resource in collection:
            if resource.name == name:
                link = {'link': resource.selfLink}
                self._values['template_link'] = link
                return True
        return False

    def _templates_on_device(self):
        collection = self.client.api.tm.asm.policy_templates_s.get_collection()
        return collection

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
                result[api_attribute] = getattr(self,
                                                self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters()
        self.want.client = self.client
        self.want.update(self.client.module.params)
        self.changes = Parameters()

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "activate":
                changed = self.activated()
            elif state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

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

    def activated(self):
        pass

    def present(self):
        pass

    def absent(self):
        pass

    def policy_exists_on_device(self):
        policies = self.policies_on_device()
        for policy in policies:
            if policy.name == self.want.name:
                return True
        return False

    def policy_self_link(self):
        policies = self.policies_on_device()
        for policy in policies:
            if policy.name == self.want.name:
                return policy.selfLink

    def policies_on_device(self):
        policies = self.client.api.tm.asm.policies_s.get_collection()
        return policies

    def upload_to_device(self):
        self.client.api.tm.asm.file_transfer.uploads.upload_file(self.want.file)

    def import_policy_to_device(self):
        if self.want.inline:
            self.client.api.tm.asm.tasks.import_policy_s.import_policy.create(name=self.want.name, file=self.want.file)
        else:
            self.upload_to_device()
            time.sleep(3)
            name = os.path.split(self.want.file)[1]
            self.client.api.tm.asm.tasks.import_policy_s.import_policy.create(name=self.want.name, filename=name)

    def apply_policy_on_device(self):
        selflink = self.policy_self_link()
        link = {'link': selflink}
        apply = self.client.api.tm.asm.tasks.apply_policy_s.apply_policy.create(policyReference=link)
        return apply

# To do list:
# Add status checking for policy apply/import to verify success
# Add policy create/delete without import
# Split to separate module managers if this gets too convoluted?
# Add policy status check (i.e active/inactive)
# Unit tests
# Functional tests
