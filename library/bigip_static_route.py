#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
module: bigip_static_route
short_description: Manipulate static routes on a BIG-IP
description:
  - Manipulate static routes on a BIG-IP.
version_added: 2.3
options:
  name:
    description:
      - Name of the static route.
    required: True
  description:
    description:
      - Descriptive text that identifies the route.
    required: False
    default: None
  destination:
    description:
      - Specifies an IP address, and netmask, for the static entry in the
        routing table. When C(state) is C(present), this value is required.
    required: False
    default: None
  gateway_address:
    description:
      - Specifies the router for the system to use when forwarding packets
        to the destination host or network. Also known as the next-hop router
        address. This can be either an IPv4 or IPv6 address. When it is an
        IPv6 address that starts with C(FE80:), the address will be treated
        as a link-local address. This requires that the C(vlan) parameter
        also be supplied.
    required: False
    default: None
  vlan:
    description:
      - Specifies the VLAN or Tunnel through which the system forwards packets
        to the destination. When C(gateway_address) is a link-local IPv6
        address, this value is required
    required: False
    default: None
  pool:
    description:
      - Specifies the pool through which the system forwards packets to the
        destination.
    required: False
    default: None
  reject:
    description:
      - Specifies that the system drops packets sent to the destination.
    required: False
    default: None
  mtu:
    description:
      - Specifies a specific maximum transmission unit (MTU).
    required: False
    default: None
  state:
    description:
      - When C(present), ensures that the cloud connector exists. When
        C(absent), ensures that the cloud connector does not exist.
    required: False
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Requires the netaddr Python package on the host. This is as easy as pip
    install netaddr.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.2.3
    - netaddr
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Create static route with gateway address
  bigip_static_route:
    destination: 10.10.10.10
    gateway_address: 10.2.2.3
    name: test-route
    password: secret
    server: lb.mydomain.come
    user: admin
    validate_certs: no
  delegate_to: localhost
'''

RETURN = r'''
vlan:
  description: Whether the banner is enabled or not.
  returned: changed
  type: string
  sample: true
gateway_address:
  description: Whether the banner is enabled or not.
  returned: changed
  type: string
  sample: true
destination:
  description: Whether the banner is enabled or not.
  returned: changed
  type: string
  sample: true
pool:
  description: Whether the banner is enabled or not.
  returned: changed
  type: string
  sample: true
description:
  description: Whether the banner is enabled or not.
  returned: changed
  type: string
  sample: true
reject:
  description: Whether the banner is enabled or not.
  returned: changed
  type: string
  sample: true
'''


try:
    import netaddr
    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False

from ansible.module_utils.parsing.convert_bool import BOOLEANS_TRUE
from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError

try:
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    api_map = {
        'tmInterface': 'vlan',
        'gw': 'gateway_address',
        'network': 'destination',
        'blackhole': 'reject'
    }

    updatables = [
        'description', 'gateway_address', 'vlan',
        'pool', 'mtu', 'reject'
    ]

    returnables = [
        'vlan', 'gateway_address', 'destination', 'pool', 'description',
        'reject', 'mtu'
    ]

    api_attributes = [
        'tmInterface', 'gw', 'network', 'blackhole', 'description', 'pool', 'mtu'
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
    def vlan(self):
        if self._values['vlan'] is None:
            return None
        if self._values['vlan'].startswith('/' + self.partition):
            return self._values['vlan']
        else:
            return '/{0}/{1}'.format(self.partition, self._values['vlan'])

    @property
    def gateway_address(self):
        if self._values['gateway_address'] is None:
            return None
        try:
            ip = netaddr.IPNetwork(self._values['gateway_address'])
            return str(ip.ip)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided gateway_address is not an IP address"
            )

    @property
    def reject(self):
        if self._values['reject'] in BOOLEANS_TRUE:
            return True
        else:
            # None is the value accepted by the API
            return None

    @property
    def destination(self):
        if self._values['destination'] is None:
            return None
        if self._values['destination'] == 'default':
            self._values['destination'] = '0.0.0.0/0'
        try:
            ip = netaddr.IPNetwork(self._values['destination'])
            return '{0}/{1}'.format(ip.ip, ip.prefixlen)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided destination is not an IP address"
            )


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(changed)

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
        changed = False
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

    def exists(self):
        collection = self.client.api.tm.net.routes.get_collection()
        for resource in collection:
            if resource.name == self.want.name:
                if resource.partition == self.want.partition:
                    return True
        return False

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):
        required_resources = ['pool', 'vlan', 'reject', 'gateway_address']
        self._set_changed_options()
        if self.want.destination is None:
            raise F5ModuleError(
                'destination must be specified when creating a static route'
            )
        if all(getattr(self.want, v) is None for v in required_resources):
            raise F5ModuleError(
                "You must specify at least one of " + ', '.join(required_resources)
            )
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if self.want.destination is not None:
            if self.have.destination != self.want.destination:
                raise F5ModuleError(
                    "The destination cannot be changed. Delete and recreate"
                    "the static route if you need to do this."
                )
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def update_on_device(self):
        params = self.want.api_params()

        # The 'network' attribute is not updatable
        params.pop('network', None)
        result = self.client.api.tm.net.routes.route.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result.modify(**params)

    def read_current_from_device(self):
        resource = self.client.api.tm.net.routes.route.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result = resource.attrs
        return Parameters(result)

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.net.routes.route.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the static route")
        return True

    def remove_from_device(self):
        result = self.client.api.tm.net.routes.route.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if result:
            result.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(required=True),
            description=dict(),
            destination=dict(),
            gateway_address=dict(),
            vlan=dict(),
            pool=dict(),
            mtu=dict(),
            reject=dict(
                type='bool'
            ),
            state=dict(
                default='present',
                choices=['absent', 'present']
            )
        )
        self.mutually_exclusive = [
            ['gateway_address', 'vlan', 'pool', 'reject']
        ]
        self.f5_product_name = 'bigip'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    if not HAS_NETADDR:
        raise F5ModuleError("The python netaddr module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        mutually_exclusive=spec.mutually_exclusive,
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
