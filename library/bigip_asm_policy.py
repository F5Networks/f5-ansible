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


# To do list:
# Unit tests
# Functional tests


import os
import time
from icontrol.exceptions import iControlUnexpectedHTTPError
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    defaultdict,
    HAS_F5SDK,
    F5ModuleError,
    iteritems,
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

    updatables = [
        'active', 'name'
    ]

    returnables = [
        'name', 'template', 'file', 'active'
    ]

    api_attributes = [
        'name', 'file'
    ]
    api_map = {
        'filename': 'file'
    }

    @property
    def template(self):
        tmpl_name = self._values['template']
        if tmpl_name is None:
            return None
        if self._template_exists_on_device(tmpl_name):
            return self._values['template']
        else:
            raise F5ModuleError('Template with the given name: {0} does not exist'.format(tmpl_name))

    def _template_exists_on_device(self, name):
        collection = self._templates_on_device()
        for resource in collection:
            if resource.name == name:
                self._set_template_selflink(resource)
                return True
        return False

    def _set_template_selflink(self, template):
        link = {'link': template.selfLink}
        self._values['template_link'] = link

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
        if self.exists():
            if self.is_activated():
                return False
            else:
                if self.client.check_mode:
                    return True
                self.activate()
                return True
        else:
            self._set_changed_options()
            if self.client.check_mode:
                return True
            self.install()
            self.activate()
            return True

    def present(self):
        if self.exists():
            return False
        else:
            self._set_changed_options()
            if self.client.check_mode:
                return True
            self.install()
            return True

    def absent(self):
        if not self.exists():
            return False
        else:
            self._set_changed_options()
            if self.client.check_mode:
                return True
            self.delete()

    def exists(self):
        if self.client.check_mode:
            return True
        result = self.policy_exists_on_device()
        return result

    def install(self):
        template = self.want.template
        path = self.want.file
        if self.client.check_mode:
            return True
        if template is None and path is None:
            self.create()
            return True
        if template is None:
            task = self.import_policy_to_device()
        if path is None:
            task = self.create_policy_from_template_on_device()
        if task:
            if self.wait_for_task(task):
                return True
            else:
                raise F5ModuleError('Import policy task failed.')
        return False

    def create(self):
        self.create_policy_on_device()
        if self.policy_exists_on_device():
            return True
        else:
            raise F5ModuleError('Failed to create ASM policy: {0}'.format(self.want.name))

    def delete(self):
        result = self.delete_policy_on_device()
        return result

    def activate(self):
        task = self.apply_policy_on_device()
        if self.wait_for_task(task):
            self.want.active = True
            self._set_changed_options()
            return True
        else:
            raise F5ModuleError('Apply policy task failed.')

    def wait_for_task(self, task):
        while True:
            task.refresh()
            if task.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        if task.status == 'FAILURE':
            return False
        if task.status == 'COMPLETED':
            return True

    def is_activated(self):
        result = self.policy_active()
        if self.client.check_mode:
            return True
        return result

    def policy_active(self):
        policy = self.return_policy()
        if policy.active is True:
            return True
        else:
            self._update_changed_options()
            return False

    def return_policy(self):
        policies = self.policies_on_device()
        for policy in policies:
            if policy.name == self.want.name:
                return policy

    def policy_exists_on_device(self):
        policy = self.return_policy()
        if policy:
            self.have = Parameters(policy.attrs)
            return True
        else:
            return False

    def policies_on_device(self):
        policies = self.client.api.tm.asm.policies_s.get_collection()
        return policies

    def upload_to_device(self):
        self.client.api.tm.asm.file_transfer.uploads.upload_file(self.want.file)

    def import_policy_to_device(self):
        self.upload_to_device()
        time.sleep(2)
        name = os.path.split(self.want.file)[1]
        result = self.client.api.tm.asm.tasks.import_policy_s.import_policy.create(name=self.want.name, filename=name)
        return result

    def apply_policy_on_device(self):
        policy = self.return_policy()
        link = {'link': policy.selflink}
        result = self.client.api.tm.asm.tasks.apply_policy_s.apply_policy.create(policyReference=link)
        return result

    def create_policy_from_template_on_device(self):
        result = self.client.api.tm.asm.tasks.import_policy_s.import_policy.create(
            name=self.want.name, policyTemplateReference=self.want.template_link
        )
        return result

    def create_policy_on_device(self):
        result = self.client.api.tm.asm.policies_s.policy.create(name=self.want.name)
        return result

    def delete_policy_on_device(self):
        policy = self.return_policy()
        policy.delete()
        if policy.exists():
            raise F5ModuleError('Failed to delete ASM policy: {0}'.format(self.want.name))
        return True


class ArgumentSpec(object):
    def __init__(self):
        self.states = ['absent', 'activate', 'present']
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(
                required=True,
            ),
            file=dict(),
            template=dict(),
            state=dict(
                default='activate',
                choices=self.states
            )
        )
        self.f5_product_name = 'bigip'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name,
        mutually_exclusive=[
            ['file', 'template']
        ]
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
