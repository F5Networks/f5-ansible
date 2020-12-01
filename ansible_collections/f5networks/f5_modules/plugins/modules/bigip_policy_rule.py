#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bigip_policy_rule
short_description: Manage LTM policy rules on a BIG-IP
description:
  - This module will manage LTM policy rules on a BIG-IP.
version_added: "1.0.0"
options:
  description:
    description:
      - Description of the policy rule.
    type: str
  actions:
    description:
      - The actions you want the policy rule to perform.
      - The available attributes vary by the action, however, each action requires
        you specify a C(type).
      - These conditions can be specified in any order. Despite the fact they are in a list,
        the order in the list does not matter to the BIG-IP.
    type: list
    elements: dict
    suboptions:
      type:
        description:
          - The action type. This value controls which of the following options are required.
          - When C(type) is C(forward), the system associates a given C(pool), or C(virtual),
            or C(node) with this rule.
          - When C(type) is C(enable), the system associates a given C(asm_policy) with
            this rule.
          - When C(type) is C(ignore), the system removes all existing actions from this
            rule.
          - When C(type) is C(redirect), the system redirects an HTTP request to a different URL.
          - When C(type) is C(reset), the system resets the connection upon C(event).
          - When C(type) is C(persist), the system associates C(cookie_insert) and C(cookie_expiry) with this rule.
          - When C(type) is C(set_variable), the system sets a variable based on the evaluated Tcl C(expression) based on C(event).
        type: str
        required: true
        choices:
          - forward
          - enable
          - ignore
          - redirect
          - reset
          - persist
          - set_variable
      pool:
        description:
          - Pool to which you want to forward traffic.
          - This parameter is only valid with the C(forward) type.
        type: str
      virtual:
        description:
          - Virtual Server to which you want to forward traffic.
          - This parameter is only valid with the C(forward) type.
        type: str
      node:
        description:
          - Node to which you want to forward traffic.
          - This parameter is only valid with the C(forward) type.
        type: str
        version_added: "1.2.0"
      asm_policy:
        description:
          - ASM policy to enable.
          - This parameter is only valid with the C(enable) type.
        type: str
      location:
        description:
          - The new URL for which a redirect response will be sent.
          - A Tcl command substitution can be used for this field.
        type: str
      event:
        description:
          - Events on which actions, such as reset, can be triggered.
          - With the C(set_variable) action, it is used for specifying
            an action event, such as request or response.
        type: str
      expression:
        description:
          - A tcl expression used with the C(set_variable) action.
        type: str
      variable_name:
        description:
           - Variable name used with the C(set_variable) action.
        type: str
      cookie_insert:
        description:
          - Cookie name on which you want to persist.
          - This parameter is only valid with the C(persist) type.
        type: str
        version_added: "1.1.0"
      cookie_expiry:
        description:
          - Optional argument, specifying the time for which the session will be persisted.
          - This parameter is only valid with the C(persist) type.
        type: int
        version_added: "1.1.0"
  policy:
    description:
      - The name of the policy you want to associate this rule with.
    type: str
    required: True
  name:
    description:
      - The name of the rule.
    type: str
    required: True
  conditions:
    description:
      - A list of attributes that describe the condition.
      - See suboptions for details on how to construct each list entry.
      - The ordering of this list is important, the module will ensure the order is
        kept when modifying the task.
      - The suboption options listed below are not required for all condition types,
        read the description for more details.
      - These conditions can be specified in any order. Despite the fact they are in a list,
        the order in the list does not matter to the BIG-IP.
    type: list
    elements: dict
    suboptions:
      type:
        description:
          - The condition type. This value controls which of the following options are required.
          - When C(type) is C(http_uri), the system associates a given C(path_begins_with_any)
            list of strings with which the HTTP URI should begin. Any item in the
            list will provide a match.
          - When C(type) is C(all_traffic), the system removes all existing conditions from
            this rule.
        type: str
        required: True
        choices:
          - http_uri
          - all_traffic
          - http_host
          - ssl_extension
      path_begins_with_any:
        description:
          - A list of strings of characters the HTTP URI should start with.
          - This parameter is only valid with the C(http_uri) type.
        type: list
        elements: str
      host_is_any:
        description:
          - A list of strings of characters the HTTP Host should match.
          - This parameter is only valid with the C(http_host) type.
        type: list
        elements: str
      host_is_not_any:
        description:
          - A list of strings of characters the HTTP Host should not match.
          - This parameter is only valid with the C(http_host) type.
        type: list
        elements: str
      host_begins_with_any:
        description:
          - A list of strings of characters the HTTP Host should start with.
          - This parameter is only valid with the C(http_host) type.
        type: list
        elements: str
      server_name_is_any:
        description:
          - A list of strings of characters the SSL Extension should match.
          - This parameter is only valid with the C(ssl_extension) type.
        type: list
        elements: str
      event:
        description:
          - Events on which conditions such as SSL Extension can be triggered.
        type: str
  state:
    description:
      - When C(present), ensures the key is uploaded to the device. When
        C(absent), ensures the key is removed from the device. If the key
        is currently in use, the module will not be able to remove the key.
    type: str
    choices:
      - present
      - absent
    default: present
  partition:
    description:
      - Device partition to manage resources on.
    type: str
    default: Common
extends_documentation_fragment: f5networks.f5_modules.f5
requirements:
  - BIG-IP >= v12.1.0
author:
  - Tim Rupp (@caphrim007)
  - Wojciech Wypior (@wojtek0806)
  - Greg Crosby (@crosbygw)
  - Nitin Khanna (@nitinthewiz)
  - Andrey Kashcheev (@andreykashcheev)
'''

EXAMPLES = r'''
- name: Create policies
  bigip_policy:
    name: Policy-Foo
    state: present
    provider:
      server: lb.mydomain.com
      user: admin
      password: secret
  delegate_to: localhost

- name: Add a rule to the new policy
  bigip_policy_rule:
    policy: Policy-Foo
    name: rule3
    conditions:
      - type: http_uri
        path_begins_with_any:
          - /ABC
    actions:
      - type: forward
        pool: pool-svrs
    provider:
      server: lb.mydomain.com
      user: admin
      password: secret
  delegate_to: localhost

- name: Add multiple rules to the new policy
  bigip_policy_rule:
    policy: Policy-Foo
    name: "{{ item.name }}"
    conditions: "{{ item.conditions }}"
    actions: "{{ item.actions }}"
    provider:
      server: lb.mydomain.com
      user: admin
      password: secret
  delegate_to: localhost
  loop:
    - name: rule1
      actions:
        - type: forward
          pool: pool-svrs
      conditions:
        - type: http_uri
          path_begins_with_any:
            - /euro
    - name: rule2
      actions:
        - type: forward
          pool: pool-svrs
      conditions:
        - type: http_uri
          path_begins_with_any:
            - /HomePage/
    - name: rule3
      actions:
        - type: set_variable
          variable_name: user-agent
          expression: tcl:[HTTP::header User-Agent]
          event: request
      conditions:
        - type: http_uri
          path_begins_with_any:
            - /HomePage/

- name: Remove all rules and confitions from the rule
  bigip_policy_rule:
    policy: Policy-Foo
    name: rule1
    conditions:
      - type: all_traffic
    actions:
      - type: ignore
    provider:
      server: lb.mydomain.com
      user: admin
      password: secret
  delegate_to: localhost
'''

RETURN = r'''
actions:
  description: The new list of actions applied to the rule.
  returned: changed
  type: complex
  contains:
    type:
      description: The action type.
      returned: changed
      type: str
      sample: forward
    pool:
      description: Pool for forwarding to.
      returned: changed
      type: str
      sample: foo-pool
  sample: hash/dictionary of values
conditions:
  description: The new list of conditions applied to the rule.
  returned: changed
  type: complex
  contains:
    type:
      description: The condition type.
      returned: changed
      type: str
      sample: http_uri
    path_begins_with_any:
      description: List of strings that the URI begins with.
      returned: changed
      type: list
      sample: [foo, bar]
  sample: hash/dictionary of values
description:
  description: The new description of the rule.
  returned: changed
  type: str
  sample: My rule
'''
from datetime import datetime

from ansible.module_utils.basic import (
    AnsibleModule, env_fallback
)
from ansible.module_utils.six import iteritems

from ..module_utils.bigip import F5RestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, transform_name, f5_argument_spec, fq_name
)
from ..module_utils.icontrol import tmos_version
from ..module_utils.teem import send_teem


class Parameters(AnsibleF5Parameters):
    api_map = {
        'actionsReference': 'actions',
        'conditionsReference': 'conditions',
    }
    api_attributes = [
        'description',
        'actions',
        'conditions',
    ]

    updatables = [
        'actions',
        'conditions',
        'description',
    ]

    returnables = [
        'description',
        'action',
        'conditions'
    ]

    @property
    def name(self):
        return self._values.get('name', None)

    @property
    def description(self):
        return self._values.get('description', None)

    @property
    def policy(self):
        if self._values['policy'] is None:
            return None
        return self._values['policy']


class ApiParameters(Parameters):
    def _remove_internal_keywords(self, resource):
        items = [
            'kind', 'generation', 'selfLink', 'poolReference', 'offset',
        ]
        for item in items:
            try:
                del resource[item]
            except KeyError:
                pass

    @property
    def actions(self):
        result = []
        if self._values['actions'] is None or 'items' not in self._values['actions']:
            return [dict(type='ignore')]
        for item in self._values['actions']['items']:
            action = dict()
            self._remove_internal_keywords(item)
            if 'forward' in item:
                action.update(item)
                action['type'] = 'forward'
                del action['forward']
            elif 'enable' in item:
                action.update(item)
                action['type'] = 'enable'
                del action['enable']
            elif 'redirect' in item:
                action.update(item)
                action['type'] = 'redirect'
                del action['redirect']
            elif 'setVariable' in item:
                action.update(item)
                action['type'] = 'set_variable'
                del action['fullPath']
                del action['code']
                del action['expirySecs']
                del action['length']
                del action['port']
                del action['status']
                del action['vlanId']
                del action['timeout']
            elif 'shutdown' in item:
                action.update(item)
                action['type'] = 'reset'
                del action['shutdown']
            if 'persist' in item:
                action.update(item)
                action['type'] = 'persist'
                del action['persist']
            result.append(action)
        result = sorted(result, key=lambda x: x['name'])
        return result

    @property
    def conditions(self):
        result = []
        if self._values['conditions'] is None or 'items' not in self._values['conditions']:
            return [dict(type='all_traffic')]
        for item in self._values['conditions']['items']:
            action = dict()
            self._remove_internal_keywords(item)
            if 'httpUri' in item:
                action.update(item)
                action['type'] = 'http_uri'
                del action['httpUri']

                # Converts to common stringiness
                #
                # The tuple set "issubset" check that happens in the Difference
                # engine does not recognize that a u'foo' and 'foo' are equal "enough"
                # to consider them a subset. Therefore, we cast everything here to
                # whatever the common stringiness is.
                if 'values' in action:
                    action['values'] = [str(x) for x in action['values']]
            elif 'httpHost' in item:
                action.update(item)
                action['type'] = 'http_host'
                if 'values' in action:
                    action['values'] = [str(x) for x in action['values']]
            elif 'sslExtension' in item:
                action.update(item)
                action['type'] = 'ssl_extension'
                if 'values' in action:
                    action['values'] = [str(x) for x in action['values']]
            result.append(action)
        # Names contains the index in which the rule is at.
        result = sorted(result, key=lambda x: x['name'])
        return result


class ModuleParameters(Parameters):
    @property
    def actions(self):
        result = []
        if self._values['actions'] is None:
            return None
        for idx, item in enumerate(self._values['actions']):
            action = dict()
            if 'name' in item:
                action['name'] = str(item['name'])
            else:
                action['name'] = str(idx)
            if item['type'] == 'forward':
                self._handle_forward_action(action, item)
            elif item['type'] == 'set_variable':
                self._handle_set_variable_action(action, item)
            elif item['type'] == 'enable':
                self._handle_enable_action(action, item)
            elif item['type'] == 'ignore':
                return [dict(type='ignore')]
            elif item['type'] == 'redirect':
                self._handle_redirect_action(action, item)
            elif item['type'] == 'reset':
                self._handle_reset_action(action, item)
                del action['shutdown']
            elif item['type'] == 'persist':
                self._handle_persist_action(action, item)
            result.append(action)
        result = sorted(result, key=lambda x: x['name'])
        return result

    @property
    def conditions(self):
        result = []
        if self._values['conditions'] is None:
            return None
        for idx, item in enumerate(self._values['conditions']):
            action = dict()
            if 'name' in item:
                action['name'] = str(item['name'])
            else:
                action['name'] = str(idx)
            if item['type'] == 'http_uri':
                self._handle_http_uri_condition(action, item)
            elif item['type'] == 'http_host':
                self._handle_http_host_condition(action, item)
            elif item['type'] == 'ssl_extension':
                self._handle_ssl_extension_condition(action, item)
            elif item['type'] == 'all_traffic':
                return [dict(type='all_traffic')]
            result.append(action)
        result = sorted(result, key=lambda x: x['name'])
        return result

    def _handle_http_host_condition(self, action, item):
        action['type'] = 'http_host'
        if 'host_begins_with_any' in item and item['host_begins_with_any'] is not None:
            if isinstance(item['host_begins_with_any'], list):
                values = item['host_begins_with_any']
            else:
                values = [item['host_begins_with_any']]
            action.update(dict(
                host=True,
                startsWith=True,
                values=values
            ))
        elif 'host_is_any' in item and item['host_is_any'] is not None:
            if isinstance(item['host_is_any'], list):
                values = item['host_is_any']
            else:
                values = [item['host_is_any']]
            action.update(dict(
                equals=True,
                host=True,
                values=values
            ))
        elif 'host_is_not_any' in item and item['host_is_not_any'] is not None:
            if isinstance(item['host_is_not_any'], list):
                values = item['host_is_not_any']
            else:
                values = [item['host_is_not_any']]
            action.update({
                'equals': True,
                'host': True,
                'not': True,
                'values': values
            })

    def _handle_http_uri_condition(self, action, item):
        """Handle the nuances of the forwarding type

        Right now there is only a single type of forwarding that can be done. As that
        functionality expands, so-to will the behavior of this, and other, methods.
        Therefore, do not be surprised that the logic here is so rigid. It's deliberate.

        :param action:
        :param item:
        :return:
        """
        action['type'] = 'http_uri'
        if 'path_begins_with_any' not in item:
            raise F5ModuleError(
                "A 'path_begins_with_any' must be specified when the 'http_uri' type is used."
            )
        if isinstance(item['path_begins_with_any'], list):
            values = item['path_begins_with_any']
        else:
            values = [item['path_begins_with_any']]
        action.update(dict(
            path=True,
            startsWith=True,
            values=values
        ))

    def _handle_ssl_extension_condition(self, action, item):
        action['type'] = 'ssl_extension'
        if 'server_name_is_any' in item:
            if isinstance(item['server_name_is_any'], list):
                values = item['server_name_is_any']
            else:
                values = [item['server_name_is_any']]
            action.update(dict(
                equals=True,
                serverName=True,
                values=values
            ))
        if 'event' not in item:
            raise F5ModuleError(
                "An 'event' must be specified when the 'ssl_extension' condition is used."
            )
        elif 'ssl_client_hello' in item['event']:
            action.update(dict(
                sslClientHello=True
            ))
        elif 'ssl_server_hello' in item['event']:
            action.update(dict(
                sslServerHello=True
            ))

    def _handle_forward_action(self, action, item):
        """Handle the nuances of the forwarding type

        Right now there is only a single type of forwarding that can be done. As that
        functionality expands, so-to will the behavior of this, and other, methods.
        Therefore, do not be surprised that the logic here is so rigid. It's deliberate.

        :param action:
        :param item:
        :return:
        """
        action['type'] = 'forward'
        if not any(x for x in ['pool', 'virtual', 'node'] if x in item):
            raise F5ModuleError(
                "A 'pool' or 'virtual' or 'node' must be specified when the 'forward' type is used."
            )
        if item.get('pool', None):
            action['pool'] = fq_name(self.partition, item['pool'])
        elif item.get('virtual', None):
            action['virtual'] = fq_name(self.partition, item['virtual'])
        elif item.get('node', None):
            action['node'] = item['node']

    def _handle_set_variable_action(self, action, item):
        """Handle the nuances of the set_variable type

        :param action:
        :param item:
        :return:
        """
        if 'expression' not in item and 'variable_name' not in item:
            raise F5ModuleError(
                "A 'variable_name' and 'expression' must be specified when the 'set_variable' type is used."
            )

        if 'event' in item and item['event'] is not None:
            action[item['event']] = True
        else:
            action['request'] = True
        action.update(dict(
            type='set_variable',
            expression=item['expression'],
            tmName=item['variable_name'],
            setVariable=True,
            tcl=True
        ))

    def _handle_enable_action(self, action, item):
        """Handle the nuances of the enable type

        :param action:
        :param item:
        :return:
        """
        action['type'] = 'enable'
        if 'asm_policy' not in item:
            raise F5ModuleError(
                "An 'asm_policy' must be specified when the 'enable' type is used."
            )
        action.update(dict(
            policy=fq_name(self.partition, item['asm_policy']),
            asm=True
        ))

    def _handle_redirect_action(self, action, item):
        """Handle the nuances of the redirect type

        :param action:
        :param item:
        :return:
        """
        action['type'] = 'redirect'
        if 'location' not in item:
            raise F5ModuleError(
                "A 'location' must be specified when the 'redirect' type is used."
            )
        action.update(
            location=item['location'],
            httpReply=True,
        )

    def _handle_reset_action(self, action, item):
        """Handle the nuances of the reset type

        :param action:
        :param item:
        :return:
        """
        action['type'] = 'reset'
        if 'event' not in item:
            raise F5ModuleError(
                "An 'event' must be specified when the 'reset' type is used."
            )
        elif 'ssl_client_hello' in item['event']:
            action.update(dict(
                sslClientHello=True,
                connection=True,
                shutdown=True
            ))

    def _handle_persist_action(self, action, item):
        """Handle the nuances of the persist type

        :param action:
        :param item:
        :return:
        """
        action['type'] = 'persist'
        if 'cookie_insert' not in item:
            raise F5ModuleError(
                "A 'cookie_insert' must be specified when the 'persist' type is used."
            )
        elif 'cookie_expiry' in item:
            action.update(
                cookieInsert=True,
                tmName=item['cookie_insert'],
                expiry=str(item['cookie_expiry'])
            )
        else:
            action.update(
                cookieInsert=True,
                tmName=item['cookie_insert']
            )


class Changes(Parameters):
    def to_return(self):
        result = {}
        for returnable in self.returnables:
            try:
                result[returnable] = getattr(self, returnable)
                result = self._filter_params(result)
            except Exception:
                raise
        return result


class ReportableChanges(Changes):
    returnables = [
        'description', 'actions', 'conditions'
    ]

    @property
    def actions(self):
        result = []
        if self._values['actions'] is None:
            return [dict(type='ignore')]
        for item in self._values['actions']:
            action = dict()
            if 'forward' in item:
                action.update(item)
                action['type'] = 'forward'
                del action['forward']
            elif 'set_variable' in item:
                action.update(item)
                action['type'] = 'set_variable'
                del action['set_variable']
            elif 'enable' in item:
                action.update(item)
                action['type'] = 'enable'
                del action['enable']
            elif 'redirect' in item:
                action.update(item)
                action['type'] = 'redirect'
                del action['redirect']
                del action['httpReply']
            elif 'reset' in item:
                action.update(item)
                action['type'] = 'reset'
                del action['connection']
                del action['shutdown']
            elif 'persist' in item:
                action.update(item)
                action['type'] = 'persist'
                action['cookie_insert'] = action['tmName']
                if 'expiry' in item:
                    action['cookie_expiry'] = int(action['expiry'])
                    del action['expiry']
                del action['tmName']
                del action['persist']
                del action['cookieInsert']
            result.append(action)
        result = sorted(result, key=lambda x: x['name'])
        return result

    @property
    def conditions(self):
        result = []
        if self._values['conditions'] is None:
            return [dict(type='all_traffic')]
        for item in self._values['conditions']:
            action = dict()
            if 'httpUri' in item:
                action.update(item)
                action['type'] = 'http_uri'
                del action['httpUri']
            elif 'httpHost' in item:
                action.update(item)
                action['type'] = 'http_host'
                del action['httpHost']
            elif 'sslExtension' in item:
                action.update(item)
                action['type'] = 'ssl_extension'
                del action['sslExtension']
            result.append(action)
        # Names contains the index in which the rule is at.
        result = sorted(result, key=lambda x: x['name'])
        return result


class UsableChanges(Changes):
    @property
    def actions(self):
        if self._values['actions'] is None:
            return None
        result = []
        for action in self._values['actions']:
            if 'type' not in action:
                continue
            if action['type'] == 'forward':
                action['forward'] = True
                del action['type']
            elif action['type'] == 'enable':
                action['enable'] = True
                del action['type']
            elif action['type'] == 'set_variable':
                action['setVariable'] = True
                action['tcl'] = True
                del action['type']
            elif action['type'] == 'ignore':
                result = []
                break
            elif action['type'] == 'redirect':
                action['httpReply'] = True
                action['redirect'] = True
                del action['type']
            elif action['type'] == 'reset':
                action['shutdown'] = True
                action['connection'] = True
                del action['type']
            elif action['type'] == 'persist':
                action['persist'] = True
                del action['type']
            result.append(action)
        return result

    @property
    def conditions(self):
        if self._values['conditions'] is None:
            return None
        result = []
        for condition in self._values['conditions']:
            if 'type' not in condition:
                continue
            if condition['type'] == 'http_uri':
                condition['httpUri'] = True
                del condition['type']
            elif condition['type'] == 'http_host':
                condition['httpHost'] = True
                del condition['type']
            elif condition['type'] == 'ssl_extension':
                condition['sslExtension'] = True
                del condition['type']
            elif condition['type'] == 'all_traffic':
                result = []
                break
            result.append(condition)
        return result


class Difference(object):
    updatables = [
        'actions', 'conditions', 'description'
    ]

    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            return self.__default(param)

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1

    def to_tuple(self, items):
        result = []
        for x in items:
            tmp = [(str(k), str(v)) for k, v in iteritems(x)]
            result += tmp
        return result

    def _diff_complex_items(self, want, have):
        if want == [] and have is None:
            return None
        if want is None:
            return None
        w = self.to_tuple(want)
        h = self.to_tuple(have)
        if set(w).issubset(set(h)):
            return None
        else:
            return want

    @property
    def actions(self):
        result = self._diff_complex_items(self.want.actions, self.have.actions)
        if self._conditions_missing_default_rule_for_asm(result):
            raise F5ModuleError(
                "Valid options when using an ASM policy in a rule's 'enable' action include all_traffic, http_uri, or http_host."
            )
        return result

    @property
    def conditions(self):
        result = self._diff_complex_items(self.want.conditions, self.have.conditions)
        return result

    def _conditions_missing_default_rule_for_asm(self, want_actions):
        if want_actions is None:
            actions = self.have.actions
        else:
            actions = want_actions
        if actions is None:
            return False
        if any(x for x in actions if x['type'] == 'enable'):
            conditions = self._diff_complex_items(self.want.conditions, self.have.conditions)
            if conditions is None:
                return False
            if any(y for y in conditions if y['type'] not in ['all_traffic', 'http_uri', 'http_host']):
                return True
        return False


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.want = ModuleParameters(params=self.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = UsableChanges(params=changed)
            return True
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def exec_module(self):
        start = datetime.now().isoformat()
        version = tmos_version(self.client)
        changed = False
        result = dict()
        state = self.want.state

        if state == "present":
            changed = self.present()
        elif state == "absent":
            changed = self.absent()
        reportable = ReportableChanges(params=self.changes.to_return())
        changes = reportable.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        send_teem(start, self.module, version)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        if self.draft_exists():
            redraft = True
        else:
            redraft = False
            self._create_existing_policy_draft_on_device()
        self.update_on_device()
        if redraft is False:
            self.publish_on_device()
        return True

    def remove(self):
        if self.module.check_mode:
            return True
        if self.draft_exists():
            redraft = True
        else:
            redraft = False
            self._create_existing_policy_draft_on_device()
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        if redraft is False:
            self.publish_on_device()
        return True

    def create(self):
        self.should_update()
        if self.module.check_mode:
            return True
        if self.draft_exists():
            redraft = True
        else:
            redraft = False
            self._create_existing_policy_draft_on_device()
        self.create_on_device()
        if redraft is False:
            self.publish_on_device()
        return True

    def exists(self):
        if self.draft_exists():
            uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}/rules/{3}".format(
                self.client.provider['server'],
                self.client.provider['server_port'],
                transform_name(self.want.partition, self.want.policy, sub_path='Drafts'),
                self.want.name
            )
        else:
            uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}/rules/{3}".format(
                self.client.provider['server'],
                self.client.provider['server_port'],
                transform_name(self.want.partition, self.want.policy),
                self.want.name
            )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status == 404 or 'code' in response and response['code'] == 404:
            return False
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True

        errors = [401, 403, 409, 500, 501, 502, 503, 504]

        if resp.status in errors or 'code' in response and response['code'] in errors:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def draft_exists(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.policy, sub_path='Drafts')
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status == 404 or 'code' in response and response['code'] == 404:
            return False
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True

        errors = [401, 403, 409, 500, 501, 502, 503, 504]

        if resp.status in errors or 'code' in response and response['code'] in errors:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def _create_existing_policy_draft_on_device(self):
        params = dict(createDraft=True)
        uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.policy)
        )
        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        return True

    def publish_on_device(self):
        params = dict(
            name=fq_name(self.want.partition,
                         self.want.policy,
                         sub_path='Drafts'
                         ),
            command="publish"

        )
        uri = "https://{0}:{1}/mgmt/tm/ltm/policy/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] in [400, 403]:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        return True

    def create_on_device(self):
        params = self.changes.api_params()
        params['name'] = self.want.name
        uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}/rules/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.policy, sub_path='Drafts'),
        )
        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] in [400, 403]:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        return response['selfLink']

    def update_on_device(self):
        params = self.changes.api_params()
        uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}/rules/{3}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.policy, sub_path='Drafts'),
            self.want.name
        )
        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def remove_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}/rules/{3}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.policy, sub_path='Drafts'),
            self.want.name
        )
        response = self.client.api.delete(uri)
        if response.status == 200:
            return True
        raise F5ModuleError(response.content)

    def read_current_from_device(self):
        if self.draft_exists():
            uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}/rules/{3}".format(
                self.client.provider['server'],
                self.client.provider['server_port'],
                transform_name(self.want.partition, self.want.policy, sub_path='Drafts'),
                self.want.name
            )
        else:
            uri = "https://{0}:{1}/mgmt/tm/ltm/policy/{2}/rules/{3}".format(
                self.client.provider['server'],
                self.client.provider['server_port'],
                transform_name(self.want.partition, self.want.policy),
                self.want.name
            )
        query = "?expandSubcollections=true"
        resp = self.client.api.get(uri + query)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        return ApiParameters(params=response)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            description=dict(),
            actions=dict(
                type='list',
                elements='dict',
                options=dict(
                    type=dict(
                        choices=[
                            'forward',
                            'enable',
                            'ignore',
                            'redirect',
                            'reset',
                            'persist',
                            'set_variable'
                        ],
                        required=True
                    ),
                    pool=dict(),
                    node=dict(),
                    asm_policy=dict(),
                    virtual=dict(),
                    location=dict(),
                    event=dict(),
                    cookie_insert=dict(),
                    cookie_expiry=dict(type='int'),
                    expression=dict(),
                    variable_name=dict()
                ),
                mutually_exclusive=[
                    ['pool', 'asm_policy', 'virtual', 'location', 'cookie_insert', 'node']
                ]
            ),
            conditions=dict(
                type='list',
                elements='dict',
                options=dict(
                    type=dict(
                        choices=[
                            'http_uri',
                            'http_host',
                            'ssl_extension',
                            'all_traffic'
                        ],
                        required=True
                    ),
                    path_begins_with_any=dict(
                        type='list',
                        elements='str',
                    ),
                    host_begins_with_any=dict(
                        type='list',
                        elements='str',
                    ),
                    host_is_any=dict(
                        type='list',
                        elements='str',
                    ),
                    host_is_not_any=dict(
                        type='list',
                        elements='str',
                    ),
                    server_name_is_any=dict(
                        type='list',
                        elements='str',
                    ),
                    event=dict()
                ),
            ),
            name=dict(required=True),
            policy=dict(required=True),
            state=dict(
                default='present',
                choices=['absent', 'present']
            ),
            partition=dict(
                default='Common',
                fallback=(env_fallback, ['F5_PARTITION'])
            )
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )

    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
