#!/usr/bin/python
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

DOCUMENTATION = '''
module: bigip_remote_syslog
short_description: Manipulate remote syslog settings on a BIG-IP.
description:
  - Manipulate remote syslog settings on a BIG-IP.
version_added: 2.4
options:
  remote_host:
    description:
      - Specifies the IP address, or hostname, for the remote system to
        which the system sends log messages.
    required: True
  remote_port:
    description:
      - Specifies the port that the system uses to send messages to the
        remote logging server. The default is C(514) when the C(state)
        option is C(present).
    required: False
    default: None
  local_ip:
    description:
      - Specifies the local IP address of the system that is logging.
    required: False
    default: None
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.2.0
    - ansible >= 2.3.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add a remote syslog server to log to
  bigip_remote_syslog:
      remote_host: "10.10.10.10"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
      validate_certs: "false"
  delegate_to: localhost

- name: Add a remote syslog server on a non-standard port to log to
  bigip_remote_syslog:
      remote_host: "10.10.10.10"
      remote_port: "1234"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
      validate_certs: "false"
  delegate_to: localhost
'''

RETURN = '''

'''

from ansible.module_utils.f5_utils import *


class Parameters(AnsibleF5Parameters):
    updatables = [
        'remote_port', 'local_ip',
    ]

    returnables = [
        'remote_port', 'local_ip'
    ]

    api_attributes = [
        'remoteServers'
    ]

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
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = None

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

    def exec_module(self):
        result = dict()

        try:
            changed = self.update()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def update_on_device(self):
        params = self.want.api_params()
        result = self.client.api.tm.sys.snmp.load()
        result.modify(**params)

    def read_current_from_device(self):
        resource = self.client.api.tm.sys.snmp.load()
        result = resource.attrs
        return Parameters(result)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            remote_host=dict(
                required=True,
                default=None
            ),
            remote_port=dict(
                required=False,
                default=None
            ),
            local_ip=dict(
                required=False,
                default=None
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
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
