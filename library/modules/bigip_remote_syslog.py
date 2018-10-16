#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_remote_syslog
short_description: Manipulate remote syslog settings on a BIG-IP
description:
  - Manipulate remote syslog settings on a BIG-IP.
version_added: 2.5
options:
  remote_host:
    description:
      - Specifies the IP address, or hostname, for the remote system to
        which the system sends log messages.
    required: True
  remote_port:
    description:
      - Specifies the port that the system uses to send messages to the
        remote logging server. When creating a remote syslog, if this parameter
        is not specified, the default value C(514) is used.
  local_ip:
    description:
      - Specifies the local IP address of the system that is logging. To
        provide no local IP, specify the value C(none). When creating a
        remote syslog, if this parameter is not specified, the default value
        C(none) is used.
  state:
    description:
      - When C(present), guarantees that the remote syslog exists with the provided
        attributes.
      - When C(absent), removes the remote syslog from the system.
    default: present
    choices:
      - absent
      - present
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
  - Wojciech Wypior (@wojtek0806)
'''

EXAMPLES = r'''
- name: Add a remote syslog server to log to
  bigip_remote_syslog:
    remote_host: 10.10.10.10
    password: secret
    server: lb.mydomain.com
    user: admin
    validate_certs: no
  delegate_to: localhost

- name: Add a remote syslog server on a non-standard port to log to
  bigip_remote_syslog:
    remote_host: 10.10.10.10
    remote_port: 1234
    password: secret
    server: lb.mydomain.com
    user: admin
    validate_certs: no
  delegate_to: localhost
'''

RETURN = r'''
remote_port:
  description: New remote port of the remote syslog server.
  returned: changed
  type: int
  sample: 514
local_ip:
  description: The new local IP of the remote syslog server
  returned: changed
  type: string
  sample: 10.10.10.10
'''

import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems

try:
    from library.module_utils.network.f5.bigip import F5RestClient
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import cleanup_tokens
    from library.module_utils.network.f5.common import f5_argument_spec
    from library.module_utils.network.f5.common import exit_json
    from library.module_utils.network.f5.common import fail_json
    from library.module_utils.network.f5.ipaddress import is_valid_ip
except ImportError:
    from ansible.module_utils.network.f5.bigip import F5RestClient
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import AnsibleF5Parameters
    from ansible.module_utils.network.f5.common import cleanup_tokens
    from ansible.module_utils.network.f5.common import f5_argument_spec
    from ansible.module_utils.network.f5.common import exit_json
    from ansible.module_utils.network.f5.common import fail_json
    from ansible.module_utils.network.f5.ipaddress import is_valid_ip


class Parameters(AnsibleF5Parameters):
    updatables = [
        'remote_port', 'local_ip', 'remoteServers',
    ]

    returnables = [
        'remote_port', 'local_ip',
    ]

    api_attributes = [
        'remoteServers',
    ]


class ApiParameters(Parameters):
    pass


class ModuleParameters(Parameters):
    @property
    def remote_host(self):
        if is_valid_ip(self._values['remote_host']):
            return self._values['remote_host']
        elif self.is_valid_hostname(self._values['remote_host']):
            return str(self._values['remote_host'])
        raise F5ModuleError(
            "The provided 'remote_host' is not a valid IP or hostname"
        )

    def is_valid_hostname(self, host):
        """Reasonable attempt at validating a hostname

        Compiled from various paragraphs outlined here
        https://tools.ietf.org/html/rfc3696#section-2
        https://tools.ietf.org/html/rfc1123

        Notably,
        * Host software MUST handle host names of up to 63 characters and
          SHOULD handle host names of up to 255 characters.
        * The "LDH rule", after the characters that it permits. (letters, digits, hyphen)
        * If the hyphen is used, it is not permitted to appear at
          either the beginning or end of a label

        :param host:
        :return:
        """
        if len(host) > 255:
            return False
        host = host.rstrip(".")
        allowed = re.compile(r'(?!-)[A-Z0-9-]{1,63}(?<!-)$', re.IGNORECASE)
        return all(allowed.match(x) for x in host.split("."))

    @property
    def remote_port(self):
        if self._values['remote_port'] is None:
            return None
        if self._values['remote_port'] == 0:
            raise F5ModuleError(
                "The 'remote_port' value must between 1 and 65535"
            )
        return int(self._values['remote_port'])

    @property
    def local_ip(self):
        if self._values['local_ip'] in [None, 'none']:
            return None
        if is_valid_ip(self._values['local_ip']):
            return self._values['local_ip']
        else:
            raise F5ModuleError(
                "The provided 'local_ip' is not a valid IP address"
            )


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                change = getattr(self, returnable)
                if isinstance(change, dict):
                    result.update(change)
                else:
                    result[returnable] = change
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class UsableChanges(Changes):
    pass


class ReportableChanges(Changes):
    @property
    def remote_port(self):
        return self._values['remote_port']

    @property
    def local_ip(self):
        return self._values['local_ip']


class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have
        self._local_ip = None
        self._remote_port = None

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
    def remoteServers(self):
        """Return changed list of remote servers

        The order of this list does not matter as BIG-IP will send to all the
        items in it.

        :return:
        """

        changed = False
        if self.want.remote_host is None:
            return None
        if self.have.remoteServers is None:
            remote = dict()
        else:
            remote = self.have.remoteServers
        current_hosts = dict((d['host'], d) for (i, d) in enumerate(remote))

        if self.want.state == 'absent':
            del current_hosts[self.want.remote_host]
            result = [v for (k, v) in iteritems(current_hosts)]
            return result

        if self.want.remote_host in current_hosts:
            item = current_hosts[self.want.remote_host]
            if self.want.remote_port is not None:
                if int(item['remotePort']) != self.want.remote_port:
                    item['remotePort'] = self.want.remote_port
                    self._remote_port = self.want.remote_port
                    changed = True
            if self.want.local_ip is not None:
                if item['localIp'] != self.want.local_ip:
                    item['localIp'] = self.want.local_ip
                    self._local_ip = self.want.local_ip
                    changed = True
        else:
            changed = True
            count = len(current_hosts.keys()) + 1
            host = self.want.remote_host
            current_hosts[self.want.remote_host] = dict(
                name="/Common/remotesyslog{0}".format(count),
                host=host
            )
            if self.want.remote_port is not None:
                current_hosts[host]['remotePort'] = self.want.remote_port
                self._remote_port = self.want.remote_port
            if self.want.local_ip is not None:
                current_hosts[host]['localIp'] = self.want.local_ip
                self._local_ip = self.want.local_ip
        if changed:
            result = [v for (k, v) in iteritems(current_hosts)]
            return result
        return None

    @property
    def remote_port(self):
        _ = self.remoteServers
        if self._remote_port:
            return self._remote_port

    @property
    def local_ip(self):
        _ = self.remoteServers
        if self._local_ip:
            return self._local_ip


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.pop('module', None)
        self.client = kwargs.pop('client', None)
        self.want = ModuleParameters(params=self.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = UsableChanges(params=changed)
            self.changes.update({'remote_host': self.want.remote_host})

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
            self.changes.update({'remote_host': self.want.remote_host})
            return True
        return False

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        if state == "present":
            changed = self.update()
        elif state == "absent":
            changed = self.absent()

        reportable = ReportableChanges(params=self.changes.to_return())
        changes = reportable.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        return result

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the remote syslog.")
        return True

    def create(self):
        self._set_valid_defaults()
        self._update_changed_options()
        if self.module.check_mode:
            return True

        # This is an unnamed resource, so we only need to update
        self.update_on_device()
        return True

    def _set_valid_defaults(self):
        if self.changes.local_ip is None:
            self.changes.update({'local_ip': None})
        if self.changes.remote_port is None:
            self.changes.update({'remote_port': 514})
        remote_servers = [
            dict(
                name='/{0}/remotesyslog1'.format(self.want.partition),
                host=self.want.remote_host,
                localIp=self.changes.local_ip,
                remotePort=self.changes.remote_port
            )
        ]
        self.changes.update({'remoteServers': remote_servers})

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def exists(self):
        self.have = self.read_current_from_device()
        if self.have.remoteServers is None:
            return False

        for server in self.have.remoteServers:
            if server['host'] == self.want.remote_host:
                return True

    def update_on_device(self):
        params = self.changes.api_params()
        uri = "https://{0}:{1}/mgmt/tm/sys/syslog/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
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

    def read_current_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/sys/syslog/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
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

    def remove_from_device(self):
        self._update_changed_options()
        params = self.changes.api_params()
        uri = "https://{0}:{1}/mgmt/tm/sys/syslog/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
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


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            remote_host=dict(
                required=True
            ),
            remote_port=dict(),
            local_ip=dict(),
            state=dict(
                default='present',
                choices=['absent', 'present']
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

    client = F5RestClient(**module.params)

    try:
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        exit_json(module, results, client)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        fail_json(module, ex, client)


if __name__ == '__main__':
    main()
