#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: bigip_monitor_https
short_description: Manages F5 BIG-IP LTM HTTPS monitors
description: Manages F5 BIG-IP LTM HTTPS monitors.
version_added: "1.0.0"
options:
  name:
    description:
      - Monitor name.
    type: str
    required: True
  description:
    description:
      - The description of the monitor.
    type: str
  parent:
    description:
      - The parent template of this monitor template. Once this value has
        been set, it cannot be changed. By default, this value is the C(https)
        parent on the C(Common) partition.
    type: str
    default: /Common/https
  send:
    description:
      - The Send string for the monitor call. When creating a new monitor, if
        this value is not provided, the default C(GET /\\r\\n) is used.
    type: str
  receive:
    description:
      - The Receive string for the monitor call.
    type: str
  receive_disable:
    description:
      - This setting works like C(receive), except the system marks the node
        or pool member disabled when its response matches the C(receive_disable)
        string but not C(receive). To use this setting, you must specify both
        C(receive_disable) and C(receive).
    type: str
  ip:
    description:
      - IP address part of the IP/port definition. If this parameter is not
        provided when creating a new monitor, the default value is '*'.
    type: str
  port:
    description:
      - Port address part of the IP/port definition. If this parameter is not
        provided when creating a new monitor, the default value is
        '*'. If specifying an IP address, you must specify a value between 1 and 65535.
    type: str
  interval:
    description:
      - The interval specifying how frequently the monitor instance of this
        template runs. If this parameter is not provided when creating
        a new monitor, the default value is 5. This value B(must)
        be less than the C(timeout) value.
    type: int
  timeout:
    description:
      - The number of seconds in which the node or service must respond to
        the monitor request. If the target responds within the set time
        period, it is considered up. If the target does not respond within
        the set time period, it is considered down. You can change this
        to any number, however, it should be 3 times the
        interval number of seconds plus 1 second. If this parameter is not
        provided when creating a new monitor, the default value is 16.
    type: int
  time_until_up:
    description:
      - Specifies the amount of time in seconds after the first successful
        response before a node is marked up. A value of 0 causes a
        node to be marked up immediately after a valid response is received
        from the node. If this parameter is not provided when creating
        a new monitor, then the default value is 0.
    type: int
  target_username:
    description:
      - Specifies the user name, if the monitored target requires authentication.
    type: str
  target_password:
    description:
      - Specifies the password, if the monitored target requires authentication.
    type: str
  reverse:
    description:
      - Specifies whether the monitor operates in reverse mode.
      - When the monitor is in reverse mode, a successful receive string match
        marks the monitored object down instead of up. You can use the
        this mode only if you configure the C(receive) option.
      - This parameter is not compatible with the C(time_until_up) parameter. If
        C(time_until_up) is specified, it must be C(0). Or, if it already exists, it
        must be C(0).
    type: bool
    version_added: "1.12.0"
  ssl_profile:
    description:
      - Specifies the SSL profile to use for the HTTPS monitor.
      - Defining SSL profiles enables refined customization of the SSL attributes
        for an HTTPS monitor.
      - This parameter is only supported on BIG-IP versions 13.x and later.
    type: str
  up_interval:
    description:
      - Specifies the interval for the system to use to perform the health check
        when a resource is up.
      - When C(0), specifies the system uses the interval specified in
        C(interval) to check the health of the resource.
      - When any other number, enables you to specify a different interval
        when checking the health of a resource that is up.
    type: int
  cipher_list:
    description:
      - Specifies the list of ciphers for this monitor.
      - The items in the cipher list are separated with a colon C(:).
    type: str
    version_added: "1.3.0"
  partition:
    description:
      - Device partition to manage resources on.
    type: str
    default: Common
  state:
    description:
      - When C(present), ensures the monitor exists.
      - When C(absent), ensures the monitor is removed.
    type: str
    choices:
      - present
      - absent
    default: present
notes:
  - Requires BIG-IP software version >= 12
extends_documentation_fragment: f5networks.f5_modules.f5
author:
  - Tim Rupp (@caphrim007)
  - Wojciech Wypior (@wojtek0806)
'''

EXAMPLES = r'''
- name: Create HTTPS Monitor
  bigip_monitor_https:
    name: my_http_monitor
    state: present
    ip: 10.10.10.10
    provider:
      server: lb.mydomain.com
      user: admin
      password: secret
  delegate_to: localhost

- name: Remove HTTPS Monitor
  bigip_monitor_https:
    name: my_http_monitor
    state: absent
    provider:
      server: lb.mydomain.com
      user: admin
      password: secret
  delegate_to: localhost
'''

RETURN = r'''
parent:
  description: New parent template of the monitor.
  returned: changed
  type: str
  sample: https
ip:
  description: The new IP of IP/port definition.
  returned: changed
  type: str
  sample: 10.12.13.14
interval:
  description: The new interval at which to run the monitor check.
  returned: changed
  type: int
  sample: 2
description:
  description: The description of the monitor.
  returned: changed
  type: str
  sample: Important Monitor
timeout:
  description: The new timeout in which the remote system must respond to the monitor.
  returned: changed
  type: int
  sample: 10
time_until_up:
  description: The new time in which to mark a system as up after first successful response.
  returned: changed
  type: int
  sample: 2
reverse:
  description: Whether the monitor operates in reverse mode.
  returned: changed
  type: bool
  sample: true
up_interval:
  description: Interval for the system to use to perform the health check when a resource is up.
  returned: changed
  type: int
  sample: 0
cipher_list:
  description: The new value for the cipher list.
  returned: changed
  type: str
  sample: +3DES:+kEDH
'''
from datetime import datetime

from ansible.module_utils.basic import (
    AnsibleModule, env_fallback
)

from ..module_utils.bigip import F5RestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, transform_name, f5_argument_spec, flatten_boolean, fq_name
)
from ..module_utils.compare import cmp_str_with_none
from ..module_utils.ipaddress import is_valid_ip
from ..module_utils.icontrol import tmos_version
from ..module_utils.teem import send_teem


class Parameters(AnsibleF5Parameters):
    api_map = {
        'timeUntilUp': 'time_until_up',
        'defaultsFrom': 'parent',
        'recv': 'receive',
        'recvDisable': 'receive_disable',
        'sslProfile': 'ssl_profile',
        'upInterval': 'up_interval',
        'cipherlist': 'cipher_list',
    }

    api_attributes = [
        'timeUntilUp',
        'defaultsFrom',
        'interval',
        'timeout',
        'recv',
        'send',
        'destination',
        'username',
        'password',
        'recvDisable',
        'description',
        'reverse',
        'sslProfile',
        'upInterval',
        'cipherlist',
    ]

    returnables = [
        'parent',
        'send',
        'receive',
        'ip',
        'port',
        'interval',
        'timeout',
        'time_until_up',
        'receive_disable',
        'description',
        'reverse',
        'ssl_profile',
        'up_interval',
        'cipher_list',
    ]

    updatables = [
        'destination',
        'send',
        'receive',
        'interval',
        'timeout',
        'time_until_up',
        'target_username',
        'target_password',
        'receive_disable',
        'description',
        'reverse',
        'ssl_profile',
        'up_interval',
        'cipher_list',
    ]

    @property
    def username(self):
        return self._values['target_username']

    @property
    def password(self):
        return self._values['target_password']

    @property
    def destination(self):
        if self.ip is None and self.port is None:
            return None
        destination = '{0}:{1}'.format(self.ip, self.port)
        return destination

    @destination.setter
    def destination(self, value):
        ip, d, port = value.rpartition('.')
        if not is_valid_ip(ip) and ip != '*':
            ip, d, port = value.rpartition(':')
        self._values['ip'] = ip
        self._values['port'] = port

    @property
    def interval(self):
        if self._values['interval'] is None:
            return None

        # Per BZ617284, the BIG-IP UI does not raise a warning about this.
        # So I do
        if 1 > int(self._values['interval']) > 86400:
            raise F5ModuleError(
                "Interval value must be between 1 and 86400"
            )
        return int(self._values['interval'])

    @property
    def timeout(self):
        if self._values['timeout'] is None:
            return None
        return int(self._values['timeout'])

    @property
    def ip(self):
        if self._values['ip'] is None:
            return None
        elif self._values['ip'] in ['*', '0.0.0.0']:
            return '*'
        elif is_valid_ip(self._values['ip']) or is_valid_ip(self._values['ip'].split("%")[0]):
            return self._values['ip']
        raise F5ModuleError(
            "The provided 'ip' parameter is not an IP address."
        )

    @property
    def port(self):
        if self._values['port'] is None:
            return None
        elif self._values['port'] == '*':
            return '*'
        return int(self._values['port'])

    @property
    def time_until_up(self):
        if self._values['time_until_up'] is None:
            return None
        return int(self._values['time_until_up'])

    @property
    def parent(self):
        if self._values['parent'] is None:
            return None
        result = fq_name(self.partition, self._values['parent'])
        return result

    @property
    def type(self):
        return 'https'

    @property
    def reverse(self):
        return flatten_boolean(self._values['reverse'])


class ApiParameters(Parameters):
    @property
    def description(self):
        if self._values['description'] in [None, 'none']:
            return None
        return self._values['description']


class ModuleParameters(Parameters):
    @property
    def description(self):
        if self._values['description'] is None:
            return None
        elif self._values['description'] in ['none', '']:
            return ''
        return self._values['description']

    @property
    def ssl_profile(self):
        if self._values['ssl_profile'] is None:
            return None
        if self._values['ssl_profile'] in ['', 'none']:
            return ''
        result = fq_name(self.partition, self._values['ssl_profile'])
        return result


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
    def reverse(self):
        if self._values['reverse'] is None:
            return None
        elif self._values['reverse'] == 'yes':
            return 'enabled'
        return 'disabled'


class ReportableChanges(Changes):
    @property
    def reverse(self):
        return flatten_boolean(self._values['reverse'])


class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            result = self.__default(param)
            return result

    @property
    def parent(self):
        if self.want.parent != self.have.parent:
            raise F5ModuleError(
                "The parent monitor cannot be changed"
            )

    @property
    def destination(self):
        if self.want.ip is None and self.want.port is None:
            return None
        if self.want.port is None:
            self.want.update({'port': self.have.port})
        if self.want.ip is None:
            self.want.update({'ip': self.have.ip})

        if self.want.port in [None, '*'] and self.want.ip != '*':
            raise F5ModuleError(
                "Specifying an IP address requires that a port number be specified"
            )

        if self.want.destination != self.have.destination:
            return self.want.destination

    @property
    def interval(self):
        if self.want.timeout is not None and self.want.interval is not None:
            if self.want.interval >= self.want.timeout:
                raise F5ModuleError(
                    "Parameter 'interval' must be less than 'timeout'."
                )
        elif self.want.timeout is not None:
            if self.have.interval >= self.want.timeout:
                raise F5ModuleError(
                    "Parameter 'interval' must be less than 'timeout'."
                )
        elif self.want.interval is not None:
            if self.want.interval >= self.have.timeout:
                raise F5ModuleError(
                    "Parameter 'interval' must be less than 'timeout'."
                )
        if self.want.interval != self.have.interval:
            return self.want.interval

    @property
    def ssl_profile(self):
        if self.want.ssl_profile is None:
            return None
        if self.want.ssl_profile == '' and self.have.ssl_profile is None:
            return None
        if self.want.ssl_profile != self.have.ssl_profile:
            return self.want.ssl_profile

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1

    @property
    def description(self):
        return cmp_str_with_none(self.want.description, self.have.description)

    @property
    def receive(self):
        return cmp_str_with_none(self.want.receive, self.have.receive)

    @property
    def receive_disable(self):
        return cmp_str_with_none(self.want.receive_disable, self.have.receive_disable)


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

    def exists(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/monitor/https/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
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

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.want.reverse == 'enabled':
            if not self.want.receive and not self.have.receive:
                raise F5ModuleError(
                    "A 'receive' string must be specified when setting 'reverse'."
                )
            if self.want.time_until_up != 0 and self.have.time_until_up != 0:
                raise F5ModuleError(
                    "Monitors with the 'reverse' attribute are not currently compatible with 'time_until_up'."
                )
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
        if self.want.reverse == 'enabled':
            if self.want.time_until_up != 0:
                raise F5ModuleError(
                    "Monitors with the 'reverse' attribute are not currently compatible with 'time_until_up'."
                )
            if not self.want.receive:
                raise F5ModuleError(
                    "A 'receive' string must be specified when setting 'reverse'."
                )
        self._set_default_creation_values()
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True

    def _set_default_creation_values(self):
        if self.want.timeout is None:
            self.want.update({'timeout': 16})
        if self.want.interval is None:
            self.want.update({'interval': 5})
        if self.want.time_until_up is None:
            self.want.update({'time_until_up': 0})
        if self.want.ip is None:
            self.want.update({'ip': '*'})
        if self.want.port is None:
            self.want.update({'port': '*'})
        if self.want.send is None:
            self.want.update({'send': 'GET /\r\n'})

    def create_on_device(self):
        params = self.changes.api_params()
        params['name'] = self.want.name
        params['partition'] = self.want.partition
        uri = "https://{0}:{1}/mgmt/tm/ltm/monitor/https/".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(resp.content)

    def update_on_device(self):
        params = self.changes.api_params()
        uri = "https://{0}:{1}/mgmt/tm/ltm/monitor/https/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(resp.content)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/monitor/https/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp = self.client.api.delete(uri)
        if resp.status == 200:
            return True

    def read_current_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/monitor/https/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return ApiParameters(params=response)
        raise F5ModuleError(resp.content)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            name=dict(required=True),
            parent=dict(default='/Common/https'),
            description=dict(),
            send=dict(),
            receive=dict(),
            receive_disable=dict(),
            ip=dict(),
            up_interval=dict(type='int'),
            port=dict(),
            interval=dict(type='int'),
            reverse=dict(type='bool'),
            timeout=dict(type='int'),
            time_until_up=dict(type='int'),
            target_username=dict(),
            target_password=dict(no_log=True),
            ssl_profile=dict(),
            cipher_list=dict(),
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
        supports_check_mode=spec.supports_check_mode,
    )

    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
