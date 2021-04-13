#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bigip_timer_policy
short_description: Manage timer policies on a BIG-IP
description:
  - Manage timer policies on a BIG-IP system.
version_added: "1.0.0"
options:
  name:
    description:
      - Specifies the name of the timer policy.
    type: str
    required: True
  description:
    description:
      - Specifies descriptive text that identifies the timer policy.
    type: str
  rules:
    description:
      - Rules you want assigned to the timer policy.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The name of the rule.
        type: str
        required: True
      protocol:
        description:
          - Specifies the IP protocol entry for which the timer policy rule is being
            configured. This could be a layer-4 protocol (such as C(tcp), C(udp) or
            C(sctp).
          - Only flows matching the configured protocol will make use of this rule.
          - When C(all-other) is specified, if there are no specific ip-protocol rules
            that match the flow, the flow matches all the other ip-protocol rules.
          - When specifying rules, if this parameter is not specified, the default is
            C(all-other).
        type: str
        default: all-other
        choices:
          - all-other
          - ah
          - bna
          - esp
          - etherip
          - gre
          - icmp
          - ipencap
          - ipv6
          - ipv6-auth
          - ipv6-crypt
          - ipv6-icmp
          - isp-ip
          - mux
          - ospf
          - sctp
          - tcp
          - udp
          - udplite
      destination_ports:
        description:
          - The list of destination ports on which to match the rule.
          - Specify a port range by specifying start and end ports separated by a
            dash (-).
          - This field is only available if you have selected the C(sctp), C(tcp), or
            C(udp) protocol.
        type: list
        elements: str
      idle_timeout:
        description:
          - Specifies an idle timeout, in seconds, for protocol and port pairs that
            match the timer policy rule.
          - When C(infinite), specifies the protocol and port pairs that match
            the timer policy rule have no idle timeout.
          - When specifying rules, if this parameter is not specified, the default is
            C(unspecified).
        type: str
        default: unspecified
  partition:
    description:
      - Device partition to manage resources on.
    type: str
    default: Common
  state:
    description:
      - When C(present), ensures the resource exists.
      - When C(absent), ensures the resource is removed.
    type: str
    choices:
      - present
      - absent
    default: present
extends_documentation_fragment: f5networks.f5_modules.f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Create a timer policy
  bigip_timer_policy:
    name: timer1
    description: My timer policy
    rules:
      - name: rule1
        protocol: tcp
        idle_timeout: indefinite
        destination_ports:
          - 443
          - 80
      - name: rule2
        protocol: 200
      - name: rule3
        protocol: sctp
        idle_timeout: 200
        destination_ports:
          - 21
    state: present
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost

- name: Remove a timer policy and all its associated rules
  bigip_timer_policy:
    name: timer1
    description: My timer policy
    state: absent
    provider:
      user: admin
      password: secret
      server: lb.mydomain.com
  delegate_to: localhost
'''

RETURN = r'''
description:
  description: The new description of the timer policy.
  returned: changed
  type: str
  sample: true
'''
from datetime import datetime

from ansible.module_utils.basic import (
    AnsibleModule, env_fallback
)

from ..module_utils.bigip import F5RestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, transform_name, f5_argument_spec
)
from ..module_utils.compare import compare_complex_list
from ..module_utils.icontrol import tmos_version
from ..module_utils.teem import send_teem


class Parameters(AnsibleF5Parameters):
    api_map = {

    }

    api_attributes = [
        'description',
        'rules',
    ]

    returnables = [
        'description',
        'rules',
    ]

    updatables = [
        'description',
        'rules',
    ]


class ApiParameters(Parameters):
    @property
    def rules(self):
        if self._values['rules'] is None:
            return None
        results = []
        for rule in self._values['rules']:
            result = dict()
            result['name'] = rule['name']
            if 'ipProtocol' in rule:
                result['protocol'] = str(rule['ipProtocol'])
            if 'timers' in rule:
                result['idle_timeout'] = str(rule['timers'][0]['value'])
            if 'destinationPorts' in rule:
                ports = list(set([str(x['name']) for x in rule['destinationPorts']]))
                ports.sort()
                result['destination_ports'] = ports
            results.append(result)
            results = sorted(results, key=lambda k: k['name'])
        return results


class ModuleParameters(Parameters):
    @property
    def rules(self):
        if self._values['rules'] is None:
            return None
        if len(self._values['rules']) == 1 and self._values['rules'][0] == '':
            return ''
        results = []
        for rule in self._values['rules']:
            result = dict()
            result['name'] = rule['name']
            if 'protocol' in rule and rule['protocol']:
                result['protocol'] = str(rule['protocol'])
            else:
                result['protocol'] = 'all-other'

            if 'idle_timeout' in rule and rule['idle_timeout']:
                result['idle_timeout'] = str(rule['idle_timeout'])
            else:
                result['idle_timeout'] = 'unspecified'

            if 'destination_ports' in rule and rule['destination_ports']:
                ports = list(set([str(x) for x in rule['destination_ports']]))
                ports.sort()
                ports = [str(self._validate_port_entries(x)) for x in ports]
                result['destination_ports'] = ports
            results.append(result)
            results = sorted(results, key=lambda k: k['name'])
        return results

    def _validate_port_entries(self, port):
        if port == 'all-other':
            return 0
        if '-' in port:
            parts = port.split('-')
            if len(parts) != 2:
                raise F5ModuleError(
                    "The correct format for a port range is X-Y, where X is the start"
                    "port and Y is the end port."
                )
            try:
                start = int(parts[0])
                end = int(parts[1])
            except ValueError:
                raise F5ModuleError(
                    "The ports in a range must be numbers."
                    "You provided '{0}' and '{1}'.".format(parts[0], parts[1])
                )
            if start == end:
                return start
            if start > end:
                return '{0}-{1}'.format(end, start)
            else:
                return port
        else:
            try:
                return int(port)
            except ValueError:
                raise F5ModuleError(
                    "The specified destination port is not a number."
                )


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            raise
        return result


class UsableChanges(Changes):
    @property
    def rules(self):
        if self._values['rules'] is None:
            return None
        results = []
        for rule in self._values['rules']:
            result = dict()
            result['name'] = rule['name']
            if 'protocol' in rule:
                result['ipProtocol'] = rule['protocol']

            if 'destination_ports' in rule:
                if rule['protocol'] not in ['tcp', 'udp', 'sctp']:
                    raise F5ModuleError(
                        "Only the 'tcp', 'udp', and 'sctp' protocols support 'destination_ports'."
                    )
                ports = [dict(name=str(x)) for x in rule['destination_ports']]
                result['destinationPorts'] = ports
            else:
                result['destinationPorts'] = []

            if 'idle_timeout' in rule:
                if rule['idle_timeout'] in ['indefinite', 'immediate', 'unspecified']:
                    timeout = rule['idle_timeout']
                else:
                    try:
                        int(rule['idle_timeout'])
                        timeout = rule['idle_timeout']
                    except ValueError:
                        raise F5ModuleError(
                            "idle_timeout must be a number, or, one of 'indefinite', 'immediate', or 'unspecified'."
                        )
                result['timers'] = [
                    dict(name='flow-idle-timeout', value=timeout)
                ]
            results.append(result)
            results = sorted(results, key=lambda k: k['name'])
        return results


class ReportableChanges(Changes):
    pass


class Difference(object):
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

    @property
    def rules(self):
        if self.want.rules is None:
            return None
        if self.have.rules is None and self.want.rules == '':
            return None
        if self.have.rules is not None and self.want.rules == '':
            return []
        if self.have.rules is None:
            return self.want.rules

        want = [tuple(x.pop('destination_ports')) for x in self.want.rules if 'destination_ports' in x]
        have = [tuple(x.pop('destination_ports')) for x in self.have.rules if 'destination_ports' in x]
        if set(want) != set(have):
            return self.want.rules
        if compare_complex_list(self.want.rules, self.have.rules):
            return self.want.rules


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.want = ModuleParameters(params=self.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = UsableChanges(params=changed)

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
        send_teem(start, self.client, self.module, version)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
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
        self.update_on_device()
        return True

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        return True

    def create(self):
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True

    def exists(self):
        uri = "https://{0}:{1}/mgmt/tm/net/timer-policy/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name),
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

    def create_on_device(self):
        params = self.changes.api_params()
        params['name'] = self.want.name
        params['partition'] = self.want.partition
        uri = "https://{0}:{1}/mgmt/tm/net/timer-policy/".format(
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
        return response['selfLink']

    def update_on_device(self):
        params = self.changes.api_params()
        uri = "https://{0}:{1}/mgmt/tm/net/timer-policy/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name),
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
        uri = "https://{0}:{1}/mgmt/tm/net/timer-policy/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name),
        )
        response = self.client.api.delete(uri)
        if response.status == 200:
            return True
        raise F5ModuleError(response.content)

    def read_current_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/net/timer-policy/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name),
        )
        resp = self.client.api.get(uri)
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
            name=dict(required=True),
            description=dict(),
            rules=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(required=True),
                    protocol=dict(
                        default='all-other',
                        choices=[
                            'all-other',
                            'ah',
                            'bna',
                            'esp',
                            'etherip',
                            'gre',
                            'icmp',
                            'ipencap',
                            'ipv6',
                            'ipv6-auth',
                            'ipv6-crypt',
                            'ipv6-icmp',
                            'isp-ip',
                            'mux',
                            'ospf',
                            'sctp',
                            'tcp',
                            'udp',
                            'udplite',
                        ]
                    ),
                    idle_timeout=dict(default='unspecified'),
                    destination_ports=dict(
                        type='list',
                        elements='str',
                    )
                )
            ),
            state=dict(
                default='present',
                choices=['present', 'absent']
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
