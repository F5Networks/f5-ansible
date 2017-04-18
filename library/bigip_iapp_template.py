#!/usr/bin/python
# -*- coding: utf-8 -*-
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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
---
module: bigip_iapp_template
short_description: Manages TCL iApp templates on a BIG-IP
description:
  - Manages TCL iApp templates on a BIG-IP
version_added: "2.3"
options:
  force:
    description:
      - Specifies whether or not to force the uploading of an iApp. This
        module does not handle the case of updating iApps in place. When
        forcing an update, this module will attempt to remove the existing
        iApp before uploading the new one. Existing iApps cannot be
        removed, even with C(force), if a service has been instantiated
        from the iApp template.
    required: False
    default: None
    choices:
      - yes
      - no
  name:
    description:
      - The name of the iApp template that you want to delete. This option
        is only available when specifying a C(state) of C(absent) and is
        provided as a way to delete templates that you may no longer have
        the source of.
    required: False
    default None
  content:
    description:
      - Sets the contents of an iApp template directly to the specified
        value. This is for simple values, but can be used with lookup
        plugins for anything complex or with formatting. C(content) must
        be provided when creating new templates.
    required: False
    default: None
  state:
    description:
      - Whether the iRule should exist or not.
    required: False
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add the iApp contained in template iapp.tmpl
  bigip_iapp_template:
      content: "{{ lookup('template', 'iapp.tmpl') }}"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

import re
import os

from ansible.module_utils.basic import BOOLEANS
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    HAS_F5SDK,
    F5ModuleError,
    iControlUnexpectedHTTPError
)

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class Parameters(AnsibleF5Parameters):
    api_attributes = []
    returnables = []

    @property
    def name(self):
        if self._values['name']:
            return self._values['name']

        pattern = r'sys application template (?P<name>[\w_\.-/]+)\s+{?'
        matches = re.search(pattern, self.content)
        if not matches:
            raise F5ModuleError(
                "An iApp template must include a name"
            )
        result = os.path.basename(matches.group('name'))
        return result

    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
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


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def exec_module(self):
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

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def update(self):
        if not self.want.force:
            return False
        if self.client.check_mode:
            return True
        self.absent()
        return self.create()

    def absent(self):
        changed = False
        if self.exists():
            changed = self.remove()
        return changed

    def exists(self):
        result = self.client.api.tm.sys.application.templates.template.exists(
            name=self.want.name,
            partition=self.want.partition
        )
        return result

    def create(self):
        if self.client.check_mode:
            return True
        self.create_on_device()
        if self.exists():
            return True
        else:
            raise F5ModuleError("Failed to create the iApp template")

    def create_on_device(self):
        remote_path = "/var/config/rest/downloads/{0}".format(self.want.name)
        load_command = 'tmsh load sys application template {0}'.format(remote_path)

        template = StringIO(self.want.content)

        upload = self.client.api.shared.file_transfer.uploads
        upload.upload_stringio(template, self.want.name)
        output = self.client.api.tm.util.bash.exec_cmd(
            'run',
            utilCmdArgs='-c "{0}"'.format(load_command)
        )

        if hasattr(output, 'commandResult'):
            result = output.commandResult
        if 'Syntax Error' in result:
            raise F5ModuleError(output.commandResult)

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the iApp template")
        return True

    def remove_from_device(self):
        resource = self.client.api.tm.sys.application.templates.template.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(
                required=False,
                default=None
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            force=dict(
                choices=BOOLEANS,
                required=False,
                default=None,
                type='bool'
            ),
            content=dict(
                required=False,
                default=None
            )
        )
        self.f5_product_name = 'bigip'
        self.mutually_exclusive = [
            ['sync_device_to_group', 'sync_group_to_device']
        ]


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name,
        mutually_exclusive=spec.mutually_exclusive
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
