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
module: bigip_snmp_contact
short_description: Manipulate SNMP contact information on a BIG-IP.
description:
  - Manipulate SNMP contact information on a BIG-IP.
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
    from f5.bigip import ManagementRoot as BigIpMgmt
    from f5.bigiq import ManagementRoot as BigIqMgmt
    from f5.iworkflow import ManagementRoot as iWorkflowMgmt
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

from ansible.module_utils.six import iteritems
from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *


class AnsibleF5Client(object):
    def __init__(self, argument_spec=None, supports_check_mode=False,
                 mutually_exclusive=None, required_together=None,
                 required_if=None, f5_product_name='bigip'):

        merged_arg_spec = dict()
        common_args = f5_argument_spec()
        merged_arg_spec.update(common_args)
        if argument_spec:
            merged_arg_spec.update(argument_spec)
            self.arg_spec = merged_arg_spec

        mutually_exclusive_params = []
        if mutually_exclusive:
            mutually_exclusive_params += mutually_exclusive

        required_together_params = []
        if required_together:
            required_together_params += required_together

        self.module = AnsibleModule(
            argument_spec=merged_arg_spec,
            supports_check_mode=supports_check_mode,
            mutually_exclusive=mutually_exclusive_params,
            required_together=required_together_params,
            required_if=required_if
        )

        self.check_mode = self.module.check_mode
        self._connect_params = self._get_connect_params()

        try:
            self.api = self._get_mgmt_root(
                f5_product_name, **self._connect_params
            )
        except iControlUnexpectedHTTPError as exc:
            self.fail(str(exc))

    def fail(self, msg):
        self.module.fail_json(msg=msg)

    def _get_connect_params(self):
        params = dict(
            user=self.module.params['user'],
            password=self.module.params['password'],
            server=self.module.params['server'],
            server_port=self.module.params['server_port'],
            validate_certs=self.module.params['validate_certs']
        )
        return params

    def _get_mgmt_root(self, type, **kwargs):
        if type == 'bigip':
            return BigIpMgmt(
                kwargs['server'],
                kwargs['user'],
                kwargs['password'],
                port=kwargs['server_port'],
                token='tmos'
            )
        elif type == 'iworkflow':
            return iWorkflowMgmt(
                kwargs['server'],
                kwargs['user'],
                kwargs['password'],
                port=kwargs['server_port'],
                token='local'
            )
        elif type == 'bigiq':
            return BigIqMgmt(
                kwargs['server'],
                kwargs['user'],
                kwargs['password'],
                port=kwargs['server_port'],
                token='local'
            )


class Parameters(object):
    def __init__(self, params=None):
        self._vlan = None
        self._partition = None
        self._gateway_address = None
        self._destination = None
        self._reject = None
        if params is None:
            return
        for key, value in iteritems(params):
            setattr(self, key, value)

    @property
    def partition(self):
        if self._partition is None:
            return 'Common'
        return self._partition.strip('/')

    @partition.setter
    def partition(self, value):
        self._partition = value

    @property
    def vlan(self):
        if self._vlan is None:
            return None
        if self._vlan.startswith(self.partition):
            return self._vlan
        else:
            return '/{0}/{1}'.format(self.partition, self._vlan)

    @vlan.setter
    def vlan(self, value):
        self._vlan = value

    @property
    def gateway_address(self):
        if self._gateway_address is None:
            return None
        try:
            ip = netaddr.IPNetwork(self._gateway_address)
            return str(ip.ip)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided gateway_address is not an IP address"
            )

    @gateway_address.setter
    def gateway_address(self, value):
        self._gateway_address = value

    @property
    def reject(self):
        if self._reject in BOOLEANS_TRUE:
            return True
        else:
            return False

    @reject.setter
    def reject(self, value):
        self._reject = value

    @property
    def destination(self):
        if self._destination is None:
            return None
        try:
            ip = netaddr.IPNetwork(self._destination)
            return '{0}/{1}'.format(ip.ip, ip.prefixlen)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided destination is not an IP address"
            )

    @destination.setter
    def destination(self, value):
        self._destination = value

    @classmethod
    def from_api(cls, params):
        params['vlan'] = params.pop('tmInterface', None)
        params['gateway_address'] = params.pop('gw', None)
        params['reject'] = params.pop('blackhole', False)
        params['destination'] = params.pop('network', None)
        p = cls(params)
        return p

    def __getattr__(self, item):
        return None

    def api_params(self):
        result = dict(
            tmInterface=self.vlan,
            network=self.destination,
            pool=self.pool,
            gw=self.gateway_address,
            description=self.description,
            mtu=self.mtu,
            blackhole=self.reject
        )
        return dict((k, v) for k, v in result.iteritems() if v is not None)


class StaticRouteManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def exec_module(self):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

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

        #result.update(**self.changes)
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

        if self.client.check_mode:
            return True

        if self.want.destination is None:
            raise F5ModuleError(
                'destination must be specified when creating a static route'
            )
        if all(getattr(self.want, v) is None for v in required_resources):
            raise F5ModuleError(
                "You must specify at least one of "
                + ', '.join(required_resources)
            )
        self.create_on_device()
        return True

    def should_update(self):
        updateable = [
            'description', 'gateway_address', 'vlan',
            'pool', 'mtu', 'reject'
        ]

        for key in updateable:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    setattr(self.changes, key, getattr(self.want, key))
                    return True

    def update(self):
        self.have = self.read_current_from_device()
        if self.have.destination != self.want.destination:
            raise F5ModuleError(
                "The destination cannot be changed. Delete and recreate the"
                "static route if you need to do this."
            )
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def update_attribute(self, result, attribute):
        want = getattr(self.want, attribute, None)
        have = getattr(self.have, attribute, None)
        if want != have and want is not None:
            result[attribute] = want

    def update_on_device(self):
        params = self.want.api_params()

        # The 'network' attribute is not updateable
        params.pop('network', None)
        route = self.client.api.tm.net.routes.route.load(
            name=self.want.name,
            partition=self.want.partition
        )
        route.modify(**params)

    def read_current_from_device(self):
        result = self.client.api.tm.net.routes.route.load(
            name=self.want.name,
            partition=self.want.partition
        ).to_dict()
        result.pop('_meta_data', 'None')
        return Parameters.from_api(result)

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
        route = self.client.api.tm.net.routes.route.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if route:
            route.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
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
        self.mutually_exclusive = [
            ['gateway_address', 'vlan', 'pool', 'reject']
        ]
        self.f5_product_name = 'bigip'


def main():
    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        mutually_exclusive=spec.mutually_exclusive,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    mm = StaticRouteManager(client)
    results = mm.exec_module()
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
