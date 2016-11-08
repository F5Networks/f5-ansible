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

DOCUMENTATION = '''
---
module: bigip_iapp_template
short_description: Manages TCL iApps on a BIG-IP
description:
  - Manages TCL iApps on a BIG-IP
version_added: "2.3"
options:
  name:
    description:
      - The name of the template being uploaded.
    required: True
  content:
    description:
      - When used instead of 'src', sets the contents of an iRule directly to
        the specified value. This is for simple values, but can be used with
        lookup plugins for anything complex or with formatting. Either one
        of C(src) or C(content) must be provided.
  src:
    description:
      - The iRule file to interpret and upload to the BIG-IP. Either one
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
  - Requires the pyparsing Python package on the host. This is as easy as pip
    install pyparsing.
  - This module cannot yet manage 'cli script' sections that are found in
    some iApp templates
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add the iApp contained in template iapp.tmpl
  bigip_iapp_template:
      content: "{{ lookup('template', 'iapp.tmpl') }}"
      name: "my-iapp"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

try:
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

try:
    from pyparsing import Optional, nestedExpr, Word, originalTextFor, \
        CaselessLiteral, alphanums, OneOrMore, Forward, Suppress, alphas, \
        nums

    HAS_PYPARSING = True
except:
    HAS_PYPARSING = False


class iAppGrammar:
    """Grammar parser for a subset of iApp V1

    This class is a parser for a subset of allowed iApp template code.
    This subset is represented by the code below.

    cli script <SCRIPT-NAME> {

    }
    cli admin-partitions {
        update-partition <PARTITION>
    }
    sys application template <TEMPLATE> {
        actions {
            definition {
                html-help {
                }
                implementation {
                }
                presentation {
                }
            }
        }
        description none
        ignore-verification false
        requires-bigip-version-max none
        requires-bigip-version-min none
        signing-key none
        tmpl-signature none
        requires-modules { ltm gtm }
    }

    While other code is technically allowed in an iApp, this parser will
    not find it.
    """
    def __init__(self):
        self.test = None
        self.parsed_results = None
        self.sections = ['implementation', 'presentation', 'html_help',
                         'scripts']
        self.properties = ['partition', 'description', 'verification',
                           'version_max', 'version_min', 'signing_key',
                           'signature', 'required_modules']

    def parse_string(self, test):
        self.test = test
        return self.parse_results()

    def parse_results(self):
        result = dict()

        for section in self.sections:
            result[section] = self.__parse_raw_text(section)
        for property in self.properties:
            result[property] = self.__parse_property(property)
        return result

    def generate_parser(self):
        """
        This BNF is incomplete and is only my own interpretation of syntax
        based off of people I've talked to. It was not taken from internal
        sources, and can probably be improved as its performance is not
        fantastic.

        <labr> ::= "{"
        <rabr> ::= "}"
        <cli> ::= "cli"
        <script> ::= "script"
        <admin-partitions> ::= "admin-partitions"
        <uppercase> ::= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' |
                        'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' |
                        'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
        <lowercase> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' |
                        'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' |
                        's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
        <nums> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
        <alphas> ::= <uppercase> <lowercase>
        <alphanums> ::= <alphas> <nums>
        <iapp> ::= <cli-part> | <application-template-part>
        <cli-part> ::= <cli-script> | <cli-admin-partitions>
        <cli-script> ::= <cli> <script>
        <cli-admin-partitions> ::= <cli> <admin-partitions> <labr> <admin-partition-components> <rabr>
        <admin-partition-components> ::= <update-partition> <text1>
        <update-partition> ::= 'update-partition' <alphas>
        <name> ::= <alphas> | <name>
        <application-template-part> ::= 'sys' 'application' 'template'
        """

        # General definitions and declarations
        toplevel = Forward()
        CL = CaselessLiteral
        lbra, rbra = map(Suppress, "{}")

        # Reserved Literals
        cli_ = CL('cli')
        admin_partition_ = CL('admin-partitions')
        update_partition_ = CL('update-partition')
        sys_ = CL('sys')
        script_ = CL('script')
        application_ = CL('application')
        template_ = CL('template')
        actions_ = CL('actions').suppress()
        definition_ = CL('definition').suppress()
        description_ = CL('description')
        htmlhelp_ = CL("html-help")
        implementation_ = CL("implementation")
        presentation_ = CL("presentation")
        verify_ = CL('ignore-verification')
        version_max = CL('requires-bigip-version-max')
        version_min = CL('requires-bigip-version-min')
        key_ = CL('signing-key')
        signature_ = CL('tmpl-signature')
        modules_ = CL('requires-modules')

        # Reserved words whose values we suppress from parsed results
        raw_text = originalTextFor(nestedExpr('{', '}'))

        # Raw text tokens
        script_text = raw_text.setResultsName('scripts')
        help_text = raw_text.setResultsName('html_help')
        implementation_text = raw_text.setResultsName('implementation')
        presentation_text_ = raw_text.setResultsName('presentation')

        # Sections
        actions = (Optional(htmlhelp_ + help_text) &
                   Optional(implementation_ + implementation_text) &
                   Optional(presentation_ + presentation_text_ )
                   )
        # Parameter values
        bools = (Word('true') | Word('false'))
        word_nums = (Word(nums + '.') | 'none')
        name = Word(alphanums + '._-/')

        # Named values used when referencing results
        description_val = name.setResultsName('description')
        verify_val = bools.setResultsName('verification')
        version_max_val = word_nums.setResultsName('version_max')
        version_min_val = word_nums.setResultsName('version_min')
        key_val = word_nums.setResultsName('signing_key')
        signature_val = word_nums.setResultsName('signature')
        modules_val = OneOrMore(Word(alphas)).setResultsName('required_modules')
        partition_val = Word(alphanums + '._-').setResultsName('partition')

        # Properties that can be set on the iApp
        property_description = Optional(description_ + description_val)
        property_verify = Optional(verify_ & verify_val)
        property_version_max = Optional(version_max & version_max_val)
        property_version_min = Optional(version_min & version_min_val)
        property_key = Optional(key_ & key_val)
        property_signature = Optional(signature_ & signature_val)
        property_modules = Optional(modules_ + lbra + modules_val + rbra)
        properties = property_description & \
                     property_verify & \
                     property_version_max & \
                     property_version_min & \
                     property_key & \
                     property_signature & \
                     property_modules

        # Top-level sections that are commonly found in iApps

        partition = cli_ + admin_partition_ + lbra + \
                    update_partition_ + partition_val + rbra

        cli_scripts = cli_ + script_ + name + script_text

        application_template = sys_ + application_ + template_ + \
                               name + lbra + actions_ + lbra + \
                               definition_ + lbra + actions + rbra + \
                               rbra & properties

        template = Optional(partition) & \
                   Optional(cli_scripts) & \
                   Optional(application_template)
        toplevel << template

        return toplevel

    def __parse_property(self, section):
        """Returns a simple value

        :return:
        """
        result=None
        toplevel = self.generate_parser()
        parsed = toplevel.parseString(self.test)
        if not hasattr(parsed, section):
            return result

        if section == 'required_modules':
            return list(parsed.required_modules)

        return getattr(parsed, section)

    def __parse_raw_text(self, section):
        """Returns a block of raw text

        Some of the sections in an iApp include raw tmsh commands. These
        need to be sent to the REST API endpoints as their raw contents
        so that the BIG-IP will register them correctly.

        :return:
        """
        result=None
        toplevel = self.generate_parser()
        parsed = toplevel.parseString(self.test)

        if hasattr(parsed, section):
            # This slice will remove leading and trailing braces
            result = getattr(parsed, section)[1:-1]
        return result


class BigIpiAppTemplateManager(object):
    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = None

    def apply_changes(self):
        result = dict()
        changed = False

        try:
            self.api = self.connect_to_bigip(**self.params)

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
        if self.iapp_template_exists():
            # TODO: Add ability to update existing template
            return True
        else:
            if self.present_parameters_are_valid(self.params):
                return self.ensure_iapp_template_is_present()
            else:
                raise F5ModuleError(
                    "Either 'content' or 'src' must be provided"
                )

    def present_parameters_are_valid(self, params):
        if not params['content'] and not params['src']:
            return False
        else:
            return True

    def absent(self):
        changed = False
        if self.iapp_template_exists():
            changed = self.ensure_iapp_template_is_absent()
        return changed

    def connect_to_bigip(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

    def iapp_template_exists(self):
        return self.api.tm.sys.application.templates.template.exists(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def ensure_iapp_template_is_present(self):
        params = self.get_iapp_template_creation_parameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.create_iapp_template_on_device(params)
        if self.iapp_template_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the iApp template")

    def get_iapp_template_creation_parameters(self):
        result = dict(
            name=self.params['name'],
            partition=self.params['partition']
        )

        if self.params['src']:
            with open(self.params['src']) as f:
                result['template'] = f.read()
        elif self.params['content']:
            result['template'] = self.params['content']

        return result

    def create_iapp_template_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            api.tm.sys.application.templates.template.create(**params)

    def ensure_iapp_template_is_absent(self):
        if self.params['check_mode']:
            return True
        self.delete_iapp_template_from_device()
        if self.iapp_template_exists():
            raise F5ModuleError("Failed to delete the iApp template")
        return True

    def delete_iapp_template_from_device(self):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            tpl = api.tm.sys.application.templates.template.load(
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
            state=dict(
                type='str',
                default='present',
                choices=self.states
            ),
            name=dict(
                type='str',
                required=True
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

    if not HAS_PYPARSING:
        raise F5ModuleError("The python pyparsing module is required")

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
from ansible.module_utils.ec2 import camel_dict_to_snake_dict
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
