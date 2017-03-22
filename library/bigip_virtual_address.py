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
module: bigip_virtual_address
short_description: Manage LTM virtual addresses on a BIG-IP
description:
  - Manage LTM virtual addresses on a BIG-IP
version_added: "2.3"
options:
  address:
    description:
      - Virtual address
    required: true
    aliases:
      - name
  netmask:
    description:
      - Netmask of the provided virtual address. This value cannot be
        modified after it is set.
    required: false
    default: 255.255.255.255
  connection_limit:
    description:
      - Specifies the number of concurrent connections that the system
        allows on this virtual address.
    required: false
    default: None
  arp_state:
    description:
      - Specifies whether the system accepts ARP requests. When (disabled),
        specifies that the system does not accept ARP requests. Note that
        both ARP and ICMP Echo must be disabled in order for forwarding
        virtual servers using that virtual address to forward ICMP packets.
        If (enabled), then the packets are dropped.
    choices:
      - enabled
      - disabled
  auto_delete:
    description:
      - Specifies whether the system automatically deletes the virtual
        address with the deletion of the last associated virtual server.
        When C(disabled), specifies that the system leaves the virtual
        address even when all associated virtual servers have been deleted.
        When creating the virtual address, the default value is C(enabled).
    choices:
      - enabled
      - disabled
  icmp_echo:
    description:
      - Specifies how the systems sends responses to (ICMP) echo requests
        on a per-virtual address basis for enabling route advertisement.
        When C(enabled), the BIG-IP system intercepts ICMP echo request
        packets and responds to them directly. When C(disabled), the BIG-IP
        system passes ICMP echo requests through to the backend servers.
        When (selective), causes the BIG-IP system to internally enable or
        disable responses based on virtual server state; C(when_any_available),
        C(when_all_available, or C(always), regardless of the state of any
        virtual servers.
    choices:
      - enabled
      - disabled
      - selective
  state:
    description:
      - The virtual address state. If C(absent), an attempt to delete the
        virtual address will be made. This will only succeed if this
        virtual address is not in use by a virtual server. C(present) creates
        the virtual address and enables it. If C(enabled), enable the virtual
        address if it exists. If C(disabled), create the virtual address if
        needed, and set state to C(disabled).
    required: false
    default: present
    choices:
      - present
      - absent
      - enabled
      - disabled
  advertise_route:
    description:
      - Specifies what routes of the virtual address the system advertises.
        When C(when_any_available), advertises the route when any virtual
        server is available. When C(when_all_available), advertises the
        route when all virtual servers are available. When (always), always
        advertises the route regardless of the virtual servers available.
    choices:
      - always
      - when_all_available
      - when_any_available
    required: false
    default: None
  use_route_advertisement:
    description:
      - Specifies whether the system uses route advertisement for this
        virtual address. When disabled, the system does not advertise
        routes for this virtual address.
    choices:
      - yes
      - no
    required: false
    default: None
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add virtual address
  bigip_virtual_address:
      server: lb.mydomain.net
      user: admin
      password: secret
      state: present
      partition: Common
      address: 10.10.10.10
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


class BigIpVirtualAddressManager(object):
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
        if self.virtual_address_exists():
            return self.update_virtual_address()
        else:
            return self.ensure_virtual_address_is_present()

    def absent(self):
        changed = False
        if self.virtual_address_exists():
            changed = self.ensure_virtual_address_is_absent()
        return changed

    def connect_to_bigip(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

    def read_virtual_address_information(self):
        address = self.load_virtual_address()
        return self.format_virtual_address_information(address)

    def format_virtual_address_information(self, address):
        result = dict()
        result['name'] = str(address.name)
        result['address'] = str(address.address)
        result['netmask'] = str(address.mask)
        if hasattr(address, 'arp'):
            result['arp'] = str(address.arp)
        if hasattr(address, 'autoDelete'):
            result['auto_delete'] = str(address.autoDelete)
        if hasattr(address, 'connectionLimit'):
            result['connection_limit'] = str(address.connectionLimit)
        if hasattr(address, 'enabled'):
            result['enabled'] = str(address.enabled)
        if hasattr(address, 'icmpEcho'):
            result['icmp_echo'] = str(address.icmpEcho)
        if hasattr(address, 'autoDelete'):
            result['auto_delete'] = str(address.autoDelete)
        if hasattr(address, 'routeAdvertisement'):
            result['use_route_advertisement'] = str(address.routeAdvertisement)
        if hasattr(address, 'advertiseRoute'):
            advertise_route = str(advertiseRoute)
            if advertise_route == 'any':
                result['advertise_route'] = 'when_any_available'
            elif advertise_route == 'all':
                result['advertise_route'] = 'when_all_available'
            elif advertise_route == 'none':
                result['advertise_route'] = 'always'
        return result

    def load_virtual_address(self):
        return self.api.tm.ltm.virtual_address_s.virtual_address.load(
            name=self.params['address'],
            partition=self.params['partition']
        )

    def virtual_address_exists(self):
        return self.api.tm.ltm.virtual_address_s.virtual_address.exists(
            name=self.params['address'],
            partition=self.params['partition']
        )

    def update_virtual_address(self):
        params = self.get_changed_parameters()
        if params:
            self.changed_params = camel_dict_to_snake_dict(params)
            if self.params['check_mode']:
                return True
        else:
            return False
        params['name'] = self.params['address']
        params['partition'] = self.params['partition']
        self.update_virtual_address_on_device(params)
        return True

    def update_virtual_address_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            address = api.tm.ltm.virtual_address_s.virtual_address.load(
                name=self.params['address'],
                partition=self.params['partition']
            )
            address.modify(**params)

    def get_changed_parameters(self):
        result = dict()
        current = self.read_virtual_address_information()
        if self.is_connection_limit_changed(current):
            result['connectionLimit'] = self.params['connection_limit']
        if self.is_arp_state_changed(current):
            result['arp'] = self.params['arp_state']
        if self.is_auto_delete_changed(current):
            result['autoDelete'] = self.params['auto_delete']
        if self.is_icmp_echo_changed(current):
            result['icmpEcho'] = self.params['icmp_echo']
        if self.is_advertise_route_changed(current):
            result['serverScope'] = self.params['advertise_route']
        if self.is_use_route_advertisement_changed(current):
            result['routeAdvertisement'] = self.params['use_route_advertisement']
        return result

    def is_connection_limit_changed(self, current):
        limit = self.params['connection_limit']
        if limit is None:
            return False
        if 'limit' not in current:
            return True
        if limit != current['connection_limit']:
            return True
        else:
            return False

    def is_arp_state_changed(self, current):
        state = self.params['arp_state']
        if state is None:
            return False
        if 'state' not in current:
            return True
        if state != current['arp_state']:
            return True
        else:
            return False

    def is_auto_delete_changed(self, current):
        auto_delete = self.params['auto_delete']
        if auto_delete is None:
            return False
        if 'auto_delete' not in current:
            return True
        if auto_delete != current['auto_delete']:
            return True
        else:
            return False

    def is_icmp_echo_changed(self, current):
        icmp = self.params['icmp_echo']
        if icmp is None:
            return False
        if 'icmp_echo' not in current:
            return True
        if icmp != current['icmp_echo']:
            return True
        else:
            return False

    def is_advertise_route_changed(self, current):
        route = self.params['advertise_route']
        if route is None:
            return False
        if 'advertise_route' not in current:
            return True
        if route != current['advertise_route']:
            return True
        else:
            return False

    def is_use_route_advertisement_changed(self, current):
        route = self.params['use_route_advertisement']
        if route is None:
            return False
        if 'use_route_advertisement' not in current:
            return True
        if route != current['use_route_advertisement']:
            return True
        else:
            return False

    def ensure_virtual_address_is_present(self):
        params = self.get_virtual_address_creation_parameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.create_virtual_address_on_device(params)
        if self.virtual_address_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the virtual address")

    def get_virtual_address_creation_parameters(self):
        result = dict(
            name=self.params['address'],
            partition=self.params['partition']
        )
        return result

    def create_virtual_address_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            api.tm.ltm.virtual_address_s.virtual_address.create(**params)

    def ensure_virtual_address_is_absent(self):
        if self.params['check_mode']:
            return True
        self.delete_virtual_address_from_device()
        if self.virtual_address_exists():
            raise F5ModuleError("Failed to delete the virtual address")
        return True

    def delete_virtual_address_from_device(self):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            address = api.tm.ltm.virtual_address_s.virtual_address.load(
                name=self.params['address'],
                partition=self.params['partition']
            )
            address.delete()


class BigIpVirtualAddressModuleConfig(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.states = ['present', 'absent', 'disabled', 'enabled']
        self.advertise_route_states = [
            'always', 'when_all_available', 'when_any_available'
        ]

        self.initialize_meta_args()
        self.initialize_argument_spec()

    def initialize_meta_args(self):
        args = dict(
            state=dict(
                type='str',
                default='present',
                choices=self.states
            ),
            address=dict(
                type='str',
                required=True,
                aliases=['name']
            ),
            netmask=dict(
                type='str',
                default='255.255.255.255',
                required=False
            ),
            connection_limit=dict(required=False),
            arp_state=dict(
                choices=['enabled', 'disabled'],
                required=False
            ),
            auto_delete=dict(
                required=False,
                choices=['enabled', 'disabled']
            ),
            icmp_echo=dict(
                required=False,
                choices=['enabled', 'disabled', 'selective']
            ),
            advertise_route=dict(
                required=False,
                choices=self.advertise_route_states
            ),
            use_route_advertisement=dict(
                required=False,
                choices=BOOLEANS
            )
        )
        self.meta_args = args

    def initialize_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)

    def create(self):
        return AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    config = BigIpVirtualAddressModuleConfig()
    module = config.create()

    try:
        obj = BigIpVirtualAddressManager(
            check_mode=module.check_mode, **module.params
        )
        result = obj.apply_changes()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import camel_dict_to_snake_dict
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
