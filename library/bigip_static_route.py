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
      - Specifies an IP address for the Destination column of the
        routing table.
    required: Only when C(state) is C(present)
    default: None
  netmask:
    description:
      - Specifies the netmask for a destination address. This value appears
        in the Netmask column of the routing table.
    required: Only when C(state) is C(present)
    default: None
  resource:
    description:
      - Specifies the particular gateway IP address, router pool, or VLAN
        through which the system forwards packets to the route destination.
        When C(use_gateway), specifies that the system forwards packets to
        the destination through the gateway whose IP address you specify.
        When C(use_pool), specifies that the system forwards packets to the
        destination through the pool you specify. When C(use_vlan), specifies
        that the system forwards packets to the destination through the VLAN
        or tunnel you specify. When C(reject), specifies that the system drops
        packets sent to the destination.
    required: Only when C(state) is C(present)
    choices:
      - use_gateway
      - use_vlan
      - use_pool
      - reject
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
      - When C(resource) is set to C(use_vlan), or when C(gateway_address)
        is a link-local IPv6 address.
    default: None
  pool:
    description:
      - Specifies the pool through which the system forwards packets to the
        destination.
    required: When C(resource) param is set to C(use_pool)
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

try:
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *


def connect_to_f5(**kwargs):
    return ManagementRoot(kwargs['server'],
                          kwargs['user'],
                          kwargs['password'],
                          port=kwargs['server_port'],
                          token='local')


class BigIpStaticRouteParams(object):
    name = None

    def difference(self, obj):
        """Compute difference between one object and another

        :param obj:
        Returns:
            Returns a new set with elements in s but not in t (s - t)
        """
        excluded = [
            'password', 'server', 'user', 'server_port', 'validate_certs'
        ]
        return self._difference(self, obj, excluded)

    def _difference(self, obj1, obj2, excluded):
        dict1 = obj1.__dict__
        dict2 = obj2.__dict__
        result = dict()
        for k,v in dict1.items():
            if k in excluded:
                continue
            if not k in dict2:
                result.update(dict(
                    k=v
                ))
            if v != dict2[k]:
                result.update(dict(
                    k=dict2[k]
                ))
        return result

    @classmethod
    def from_module(cls, module):
        """Create instance from dictionary of Ansible Module params

        This method accepts a dictionary that is in the form supplied by
        the

        Args:
             module: An AnsibleModule object's `params` attribute.

        Returns:
            A new instance of iWorkflowSystemSetupParams. The attributes
            of this object are set according to the param data that is
            supplied by the user.
        """
        result = cls()
        for key in module:
            setattr(result, key, module[key])
        return result


class BigIpStaticRouteModule(AnsibleModule):
    def __init__(self):
        self.params = None
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.init_meta_args()
        self.init_argument_spec()
        super(BigIpStaticRouteModule, self).__init__(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode,
            required_if=[
                ['resource', 'use_vlan', ['vlan']],
                ['resource', 'use_pool', ['pool']],
                ['state', 'present', ['resource', 'netmask', 'destination']]
            ]
        )

    def __set__(self, instance, value):
        if isinstance(value, BigIpStaticRouteModule):
            instance.params = BigIpStaticRouteParams.from_module(
                self.params
            )
        else:
            super(BigIpStaticRouteModule, self).__set__(instance, value)

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
            netmask=dict(
                required=False,
                default=None
            ),
            resource=dict(
                required=False,
                default=None,
                choices=[
                    'use_gateway',
                    'use_vlan',
                    'use_pool',
                    'reject'
                ]
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


class BigIpStaticRouteManager(object):
    params = BigIpStaticRouteParams()
    current = BigIpStaticRouteParams()
    module = None

    def __init__(self):
        self.api = None
        self.changes = None
        self.config = None
        self.module = BigIpStaticRouteModule()

    def apply_changes(self):
        """Apply the user's changes to the device

        This method is the primary entry-point to this module. Based on the
        parameters supplied by the user to the class, this method will
        determine which `state` needs to be fulfilled and delegate the work
        to more specialized helper methods.

        Additionally, this method will return the result of applying the
        changes so that Ansible can communicate this result to the user.

        Raises:
            F5ModuleError: An error occurred communicating with the device
        """
        result = dict()
        state = self.params.state

        try:
            self.api = connect_to_f5(**self.params.__dict__)
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.params.difference(self.current)
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def exists(self):
        """Checks to see if a connector exists.

        This method does not use ODATA queries because that functionality
        is broken in iWorkflow. Therefore, we iterate over all connectors
        until we find the one we're interested in.

        :return:
        """
        connectors = self.api.cm.cloud.connectors.locals.get_collection()
        for connector in connectors:
            if connector.displayName != "BIG-IP":
                continue
            if connector.name != self.params.name:
                continue
            return True
        return False

    def present(self):
        if self.exists():
            return self.update_bigip_connector()
        else:
            return self.create_bigip_connector()

    def create_bigip_connector(self):
        if self.module.check_mode:
            return True
        self.create_bigip_connector_on_device()
        return True

    def update_bigip_connector(self):
        changed = False
        current = self.read_current()
        if self.description_changed(current):
            changed = True
        if self.name_changed(current):
            changed = True

        if not changed:
            return False

        if self.module.check_mode:
            return True
        self.update_local_connector_on_device(current)
        return True

    def update_local_connector_on_device(self, current):
        pass

    def read_current(self):
        connector = None
        connectors = self.api.cm.cloud.connectors.locals.get_collection()
        for connector in connectors:
            if connector.displayName != "BIG-IP":
                continue
            if connector.name != self.params.name:
                continue
            break
        if not connector:
            return None
        current = BigIpStaticRouteParams()
        current.owner_machine_id = str(connector.ownerMachineId)
        current.connector_id = str(connector.connectorId)
        if hasattr(current, 'displayName'):
            current.display_name = str(connector.displayName)
        if hasattr(current, 'name'):
            current.name = str(connector.name)
        self.current = current
        return self.current

    def create_bigip_connector_on_device(self):
        self.api.cm.cloud.connectors.locals.local.create(
            name=self.params.name
        )
        return True

    def absent(self):
        if self.exists():
            return self.remove_bigip_connector()
        return False

    def remove_bigip_connector(self):
        if self.module.check_mode:
            return True
        self.remove_bigip_connector_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the BIG-IP connector")
        return True

    def remove_bigip_connector_from_device(self):
        connector = None
        connectors = self.api.cm.cloud.connectors.locals.get_collection()
        for connector in connectors:
            if connector.displayName != "BIG-IP":
                continue
            if connector.name != self.params.name:
                continue
            break
        if connector:
            connector.delete()


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    module = BigIpStaticRouteModule()

    try:
        obj = BigIpStaticRouteManager()
        obj.module = module
        result = obj.apply_changes()
        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
