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
        module before uploading the new one. Existing modules cannot be
        removed, even with C(force), if a service has been instantiated
        from that template.
    required: False
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
  content:
    description:
      - When used instead of 'src', sets the contents of an iApp template
        directly to the specified value. This is for simple values, but
        can be used with lookup plugins for anything complex or with
        formatting. Either one of C(src) or C(content) must be provided.
  src:
    description:
      - The iApp template to interpret and upload to the BIG-IP. Either one
        of C(src) or C(content) must be provided.
    required: true
  state:
    description:
      - Whether the iRule should exist or not.
    required: false
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

try:
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def connect_to_bigip(**kwargs):
    return ManagementRoot(kwargs['server'],
                          kwargs['user'],
                          kwargs['password'],
                          port=kwargs['server_port'],
                          token=True)


class BigIpiAppTemplateManager(object):
    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = None
        self.pattern = r'sys application template (?P<name>[\w_\.-/]+)\s+{?'

    def apply_changes(self):
        result = dict()
        changed = False

        try:
            self.api = connect_to_bigip(**self.params)

            if self.params['state'] == "present":
                changed = self.present()
            elif self.params['state'] == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.changed_params)
        result.update(dict(changed=changed))
        return result

    def present(self):
        source = self.params['src']
        content = self.params['content']

        self.set_iapp_template_source(source, content)
        self.set_iapp_template_name(self.params['content'])

        if self.iapp_template_exists():
            return False
        else:
            return self.ensure_iapp_template_is_present()

    def absent(self):
        changed = False
        if self.iapp_template_exists():
            changed = self.ensure_iapp_template_is_absent()
        return changed

    def set_iapp_template_name(self, source):
        matches = re.search(self.pattern, source)
        if not matches:
            raise F5ModuleError(
                "An iApp template must include a name"
            )
        self.params['name'] = os.path.basename(matches.group('name'))

    def set_iapp_template_source(self, source=None, content=None):
        if source:
            with open(source) as fh:
                result = fh.read()
        elif content:
            result = content
        else:
            raise F5ModuleError(
                "Either 'content' or 'src' must be provided"
            )
        self.params['content'] = result

    def iapp_template_exists(self):
        return self.api.tm.sys.application.templates.template.exists(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def ensure_iapp_template_is_present(self):
        if self.params['check_mode']:
            return True
        self.create_iapp_template_on_device(self.params)
        if self.iapp_template_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the iApp template")

    def create_iapp_template_on_device(self, params):
        remote_path = "/var/config/rest/downloads/{0}".format(params['name'])
        load_command = 'tmsh load sys application template {0}'.format(remote_path)

        template = StringIO(params['content'])

        upload = self.api.shared.file_transfer.uploads
        upload.upload_stringio(template, self.params['name'])
        output = self.api.tm.util.bash.exec_cmd(
            'run',
            utilCmdArgs='-c "{0}"'.format(load_command)
        )

        if hasattr(output, 'commandResult'):
            result = output.commandResult
        if 'Syntax Error' in result:
            raise F5ModuleError(output.commandResult)

    def ensure_iapp_template_is_absent(self):
        if self.params['check_mode']:
            return True
        self.delete_iapp_template_from_device()
        if self.iapp_template_exists():
            raise F5ModuleError("Failed to delete the iApp template")
        return True

    def delete_iapp_template_from_device(self):
        tpl = self.api.tm.sys.application.templates.template.load(
            name=self.params['name'],
            partition=self.params['partition']
        )
        tpl.delete()


class BigIpiAppTemplateModuleConfig(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.states = ['present', 'absent']

        self.initialize_meta_args()
        self.initialize_argument_spec()

    def initialize_meta_args(self):
        args = dict(
            name=dict(required=False),
            state=dict(
                type='str',
                default='present',
                choices=self.states
            ),
            force=dict(
                choices=BOOLEANS,
                required=False
            ),
            content=dict(required=False, default=None),
            src=dict(required=False, default=None),
        )
        self.meta_args = args

    def initialize_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)

    def create(self):
        return AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode,
            mutually_exclusive=[
                ['content', 'src']
            ]
        )


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    config = BigIpiAppTemplateModuleConfig()
    module = config.create()

    try:
        obj = BigIpiAppTemplateManager(
            check_mode=module.check_mode, **module.params
        )
        result = obj.apply_changes()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
