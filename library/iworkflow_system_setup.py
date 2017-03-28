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

DOCUMENTATION = '''
module: iworkflow_system_setup
short_description: Manage system setup related configuration on iWorkflow
description:
  - Manage system setup related configuration on iWorkflow.
version_added: 2.4
options:
  hostname:
    description:
      - Sets the hostname of the iWorkflow device
    required: True
  management_address:
    description:
      - Management address of the iWorkflow instance.
    required: True
  dns_servers:
    description:
      - List of DNS servers to set on the iWorkflow device for name
        resolution.
    default: None
    required: False
  dns_search_domains:
    description:
      - Default search domain that should be used for DNS queries
    default: None
    required: False
  ntp_servers:
    description:
      - List of NTP servers to set on the iWorkflow device for time
        synchronization.
    default: ['pool.ntp.org']
    required: False
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Required the netaddr Python package on the host. This is as easy as pip
    install netaddr.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.2.2
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Disable iWorkflow setup screen and set accounts as unchanged
  iworkflow_system_setup:
      is_admin_password_changed: "no"
      is_root_password_changed: "no"
      is_system_setup: "yes"
      password: "secret"
      server: "iwf.mydomain.com"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''

'''

import re
from netaddr import IPNetwork

from ansible.module_utils.basic import BOOLEANS_TRUE
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    F5ModuleError,
    HAS_F5SDK,
    iControlUnexpectedHTTPError
)


class Parameters(AnsibleF5Parameters):
    api_map = {
        'managementIpAddress': 'management_address',
        'dnsServerAddresses': 'dns_servers',
        'dnsSearchDomains': 'dns_search_domain',
        'ntpServerAddresses': 'ntp_servers',
        'isSystemSetup': 'is_system_setup',
        'discoveryAddress': 'discovery_address'
    }

    returnables = [
        'management_address', 'dns_servers', 'dns_search_domain', 'ntp_servers',
        'hostname'
    ]

    api_attributes = [
        'managementIpAddress', 'dnsServerAddresses', 'dnsSearchDomains',
        'ntpServerAddresses', 'hostname'
    ]

    updatables = [
        'management_address', 'dns_servers', 'dns_search_domain', 'ntp_servers',
        'hostname'
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

    @property
    def hostname(self):
        if self._values['hostname'] is None:
            return None
        pattern = r'.*([\w\-]+)\.([\w\-]+).*'
        matches = re.search(pattern, self._values['hostname'], re.I)
        if matches:
            return self._values['hostname']
        elif self._values['hostname'] == 'iworkflow1':
            # This is what iWorkflow uses if you dont give it a
            # hostname
            return self._values['hostname']
        raise F5ModuleError(
            "The provided hostname must be an FQDN"
        )

    @property
    def management_address(self):
        if self._values['management_address'] is None:
            return None
        try:
            address = IPNetwork(self._values['management_address'])
            return str(address)
        except Exception:
            raise F5ModuleError(
                "The provided management address is not a valid IP address"
            )


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

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
        if self.have.is_system_setup in BOOLEANS_TRUE:
            return True
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

    def read_current_from_device(self):
        result = dict()
        s = self.client.api.shared.system.setup.load()
        result.update(s.attrs)
        e = self.client.api.shared.system.easy_setup.load()
        result.update(e.attrs)
        d = self.client.api.shared.identified_devices.config.discovery.load()
        result.update(d.attrs)
        return Parameters(result)

    def update_on_device(self):
        params = self.want.api_params()
        e = self.client.api.shared.system.easy_setup.load()
        e.modify(**params)

        s = self.client.api.shared.system.setup.load()
        s.update(
            isSystemSetup=True,
        )

        d = self.client.api.shared.identified_devices.config.discovery.load()
        d.update(
            discoveryAddress=self.want.discovery_address
        )
        return True


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            hostname=dict(
                required=True
            ),
            discovery_address=dict(
                required=True,
            ),
            management_address=dict(
                required=True,
            ),
            dns_servers=dict(
                required=False,
                type='list',
                default=None
            ),
            dns_search_domains=dict(
                required=False,
                type='list',
                default=None
            ),
            ntp_servers=dict(
                required=False,
                type='list',
                default=['pool.ntp.org']
            )
        )
        self.f5_product_name = 'iworkflow'


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
