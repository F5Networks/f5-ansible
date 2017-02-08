#!/usr/bin/python
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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
module: bigip_static_route
short_description: Manipulate static routes on a BIG-IP.
description:
  - Manipulate static routes on a BIG-IP.
version_added: 2.3
options:
  name:
    description:
      - Name of the static route
    required: True
  description:
    description:
      - Descriptive text that identifies the route.
    required: False
    default: None
  destination:
    description:
      - Specifies an IP address, and netmask, for the static entry in the
        routing table.
    required: When C(state) is C(present)
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
        to the destination.
    required:
      - When C(gateway_address) is a link-local IPv6 address.
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
    install netaddr
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 1.5.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

import netaddr

try:
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


from ansible.module_utils.six import iteritems
from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *


_CONNECTION = None


def setup_connection(**kwargs):
    global _CONNECTION
    _CONNECTION = ManagementRoot(
        kwargs['server'],
        kwargs['user'],
        kwargs['password'],
        port=kwargs['server_port'],
        token='tmos'
    )


def _get_connection():
    if _CONNECTION is None:
        setup_connection()
    return _CONNECTION


def normalize_partition(partition):
    result = partition.strip('/')
    return '/' + result + '/'


def format_with_path(param, partition):
    if partition is None:
        partition = 'Common'
    partition = normalize_partition(partition)
    if param.startswith(partition):
        return param
    else:
        return partition + param


class F5AnsibleModule(AnsibleModule):
    def __init__(self):
        self.params = None
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(F5AnsibleModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode,
            mutually_exclusive=[
                ['gateway_address', 'vlan', 'pool', 'reject']
            ]
        )

    def init_meta_args(self):
        args = dict(
            name=dict(required=True),
            description=dict(
                required=False,
                default=None
            ),
            destination=dict(
                required=False,
                default=None
            ),
            gateway_address=dict(
                required=False,
                default=None
            ),
            vlan=dict(
                required=False,
                default=None
            ),
            pool=dict(
                required=False,
                default=None
            ),
            mtu=dict(
                required=False,
                default=None
            ),
            reject=dict(
                required=False,
                default=None,
                choices=BOOLEANS_TRUE
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.meta_args = args

    def init_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)


class ModuleManager(object):
    have = dict()
    want = dict()

    def __init__(self, *args, **kwargs):
        self.changes = dict()
        self.module = kwargs['module']
        self.return_key_map = dict(
            gw='gateway_address',
            tmInterface='vlan',
            blackhole='reject'
        )

    def apply_changes(self):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.want = self.format_params(self.module.params)

        changed = False
        result = dict()
        state = self.want.get('state')

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.changes)
        result.update(dict(changed=changed))
        result = self.map_to_return_keys(result)
        return result

    def map_to_return_keys(self, keys):
        result = dict()
        for k,v in iteritems(keys):
            new_key = self.return_key_map.get(k, None)
            if new_key is None:
                result[k] = v
            else:
                result[new_key] = v
        result = {k: v for k, v in result.items() if v is not None }
        return result

    def exists(self):
        api = _get_connection()
        return api.tm.net.routes.route.exists(name=self.want.name)

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):
        required_resources = ['pool', 'vlan', 'reject', 'gateway_address']

        if self.module.check_mode:
            return True

        if self.want['destination'] is None:
            raise F5ModuleError(
                'destination must be specified when creating a static route'
            )
        if all(self.want[v] is None for v in required_resources):
            raise F5ModuleError(
                "You must specify at least one of "
                + ', '.join(required_resources)
            )
        self.update_changed_params()
        self.create_on_device(self.changes)
        return True

    def update(self):
        current = self.read_current_from_device(self.want['name'])
        self.have = self.format_params(current)
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device(self.changes)
        return True

    def should_update(self):
        self.update_changed_params()
        if len(self.changes.keys()) > 2:
            return True
        return False

    def update_changed_params(self):
        result = dict(
            name=str(self.want['name']),
            partition=str(self.want['partition']),
        )
        self.update_attribute(result, 'mtu')
        self.update_attribute(result, 'description')
        self.update_attribute(result, 'network', self.network_address_validator)
        self.update_attribute(result, 'pool')
        self.update_attribute(result, 'gw', self.network_address_validator)
        self.update_attribute(result, 'tmInterface')
        self.update_attribute(result, 'reject')
        self.changes = result

    def network_address_validator(self, address):
        if address is None:
            return
        try:
            netaddr.IPNetwork(address)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                'The provided IP address or network mask was invalid'
            )

    def update_attribute(self, result, attribute, validator=None):
        want = self.want.get(attribute, None)
        have = self.have.get(attribute, None)
        if want != have and want is not None:
            result[attribute] = want
        if validator is None:
            return
        validator(want)

    def update_on_device(self, params):
        api = _get_connection()
        route = api.tm.net.routes.route.load(name=self.want.name)
        route.update(**params)

    def read_current_from_device(self, identifier):
        api = _get_connection()
        route = api.tm.net.routes.route.load(name=identifier)
        if not route:
            return dict()
        current = route.to_dict()
        current.pop('_meta_data')
        return current

    def format_params(self, params):
        result = dict()
        for k,v in iteritems(self.module.params):
            if k in params and params[k] is not None:
                result[k] = str(params[k])
            else:
                result[k] = v
        route = result.get('vlan', None)
        if route:
            result['tmInterface'] = format_with_path(route, params['partition'])
        return result

    def create_on_device(self, params):
        api = _get_connection()
        api.cm.cloud.connectors.locals.local.create(**params)

    def absent(self, ):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the static route")
        return True

    def remove_from_device():
        api = _get_connection()
        route = api.tm.net.routes.route.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if route:
            route.delete()


def main():
    module = F5AnsibleModule()
    setup_connection(**module.params)

    try:
        obj = ModuleManager(module=module)
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
