#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.1'
}

DOCUMENTATION = '''
---
module: bigip_vcmp_guest
short_description: Manages vCMP guests on a BIG-IP
description:
  - Manages vCMP guests on a BIG-IP. This functionality only exists on
    actual hardware and must be enabled by provisioning C(vcmp) with the
    C(bigip_provision) module.
version_added: "2.5"
options:
  name:
    description:
      - The name of the vCMP guest to manage.
    required: True
  vlans:
    description:
      - VLANs that the guest uses to communicate with other guests, the host, and with
        the external network. The available VLANs in the list are those that are
        currently configured on the vCMP host.
  initial_image:
    description:
      - Specifies the base software release ISO image file for installing the TMOS
        hypervisor instance and any licensed BIG-IP modules onto the guest's virtual
        disk. When creating a new guest, this parameter is required.
  mgmt_network:
    description:
      - Specifies the method by which the management address is used in the vCMP guest.
      - When C(bridged), specifies that the guest can communicate with the vCMP host's
        management network.
      - When C(isolated), specifies that the guest is isolated from the vCMP host's
        management network. In this case, the only way that a guest can communicate
        with the vCMP host is through the console port or through a self IP address
        on the guest that allows traffic through port 22.
      - When C(host only), prevents the guest from installing images and hotfixes other
        than those provided by the hypervisor.
      - If the guest setting is C(isolated) or C(host only), the C(mgmt_address) does
        not apply.
      - Concerning mode changing, changing C(bridged) to C(isolated) causes the vCMP
        host to remove all of the guest's management interfaces from its bridged
        management network. This immediately disconnects the guest's VMs from the
        physical management network. Changing C(isolated) to C(bridged) causes the
        vCMP host to dynamically add the guest's management interfaces to the bridged
        management network. This immediately connects all of the guest's VMs to the
        physical management network. Changing this property while the guest is in the
        C(configured) or C(provisioned) state has no immediate effect.
    choices:
      - bridged
      - isolated
      - host only
  delete_virtual_disk:
    description:
      - When C(state) is C(absent), will additionally delete the virtual disk associated
        with the vCMP guest. By default, this value is C(no).
    default: no
  mgmt_address:
    description:
      - Specifies the IP address, and subnet or subnet mask that you use to access
        the guest when you want to manage a module running within the guest. This
        parameter is required if the C(mgmt_network) parameter is C(bridged).
      - If you do not specify a network or network mask, a default of C(/24)
        (C(255.255.255.0)) will be assumed.
  mgmt_route:
    description:
      - Specifies the gateway address for the C(mgmt_address).
  state:
    description:
      - The state of the  on the system. When C(present), guarantees
        that the VLAN exists with the provided attributes. When C(absent),
        removes the VLAN from the system.
    default: "present"
    choices:
      - disabled
      - provisioned
      - deployed
      - absent
      - present
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - This module can take a lot of time to deploy vCMP guests. This is an intrinsic
    limitation of the vCMP system because it is booting real VMs on the BIG-IP
    device. This boot time is very similar in length to the time it takes to
    boot VMs on any other virtualization platform; public or private.
  - When BIG-IP starts, the VMs are booted sequentially; not in parallel. This
    means that it is not unusual for a vCMP host with many guests to take a
    long time (60+ minutes) to reboot and bring all the guests online. The
    BIG-IP chassis will be available before all vCMP guests are online.
requirements:
  - f5-sdk >= 2.2.3
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Create a vCMP guest
  bigip_vcmp_guest:
      name: "foo"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
      mgmt_network: "bridge"
      mgmt_address: "10.20.30.40/24"
  delegate_to: localhost

- name: Create a vCMP guest with specific VLANs
  bigip_vcmp_guest:
      name: "foo"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
      mgmt_network: "bridge"
      mgmt_address: "10.20.30.40/24"
      vlans:
          - vlan1
          - vlan2
  delegate_to: localhost
'''

RETURN = '''
vlans:
    description: The VLANs assigned to the vCMP guest, in their full path format.
    returned: changed
    type: list
    sample: ['/Common/vlan1', '/Common/vlan2']
'''


from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError
from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
from ansible.module_utils.f5_utils import iteritems
from ansible.module_utils.f5_utils import defaultdict


try:
    from netaddr import IPAddress, AddrFormatError, IPNetwork
    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False


class Parameters(AnsibleF5Parameters):
    api_map = {
        'managementGw': 'mgmt_route',
        'managementNetwork': 'mgmt_network',
        'managementIp': 'mgmt_address',
        'initialImage': 'initial_image',
    }

    api_attributes = [
        'vlans', 'managementNetwork', 'managementIp', 'initialImage', 'managementGw'
    ]

    returnables = [
        'vlans', 'mgmt_network', 'mgmt_address', 'initial_image', 'mgmt_route'
    ]

    updatables = [
        'vlans', 'mgmt_network', 'mgmt_address', 'initial_image', 'mgmt_route'
    ]

    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        self._values['__warnings'] = []
        if params:
            self.update(params=params)

    def update(self, params=None):
        if params:
            for k, v in iteritems(params):
                if self.api_map is not None and k in self.api_map:
                    map_key = self.api_map[k]
                else:
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have
                        # an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
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
    def mgmt_route(self):
        if self._values['mgmt_route'] is None:
            return None
        try:
            result = IPAddress(self._values['mgmt_route'])
            return str(result)
        except AddrFormatError:
            raise F5ModuleError(
                "The specified 'mgmt_route' is not a valid IP address"
            )

    @property
    def mgmt_address(self):
        if self._values['mgmt_address'] is None:
            return None


class Changes(Parameters):
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


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.want = Parameters(self.client.module.params)
        self.changes = Changes()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Changes(changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                changed[k] = change
        if changed:
            self.changes = Parameters(changed)
            return True
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state in ['disabled', 'provisioned', 'deployed', 'present']:
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def _fqdn_name(self, value):
        if value is not None and not value.startswith('/'):
            return '/{0}/{1}'.format(self.partition, value)
        return value

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def exists(self):
        result = self.client.api.tm.vcmp.guests.guest.exists(
            name=self.want.name
        )
        return result

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def remove(self):
        if self.client.check_mode:
            return True
        if self.want.delete_virtual_disk:
            self.have = self.read_current_from_device()
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        if self.want.delete_virtual_disk:
            self.remove_virtual_disk_from_device()
        return True

    def create(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        self.create_on_device()
        if state == 'disabled':
            self.disable()
        return True

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.vcmp.guests.guest.create(
            name=self.want.name,
            **params
        )

    def update_on_device(self):
        params = self.want.api_params()
        resource = self.client.api.tm.vcmp.guests.guest.load(
            name=self.want.name
        )
        resource.modify(**params)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove_from_device(self):
        resource = self.client.api.tm.vcmp.guests.guest.load(
            name=self.want.name
        )
        if resource:
            resource.delete()

    def read_current_from_device(self):
        resource = self.client.api.tm.vcmp.guests.guest.load(
            name=self.want.name
        )
        result = resource.attrs
        return Parameters(result)

    def remove_virtual_disk_from_device(self):
        resource = self.client.api.tm.vcmp.guests.guest.load(
            name=self.want.name
        )
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(required=True),
            vlans=dict(type='list'),
            mgmt_network=dict(choices=['bridged', 'isolated', 'host only']),
            mgmt_address=dict(),
            mgmt_route=dict(),
            initial_image=dict(),
            state=dict(
                default='deployed',
                choices=['disabled', 'provisioned', 'deployed', 'absent', 'present']
            ),
            delete_virtual_disk=dict(
                type='bool', default='no'
            )
        )
        self.f5_product_name = 'bigip'
        self.required_if = [
            ['mgmt_network', 'bridged', ['mgmt_address']]
        ]


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    if not HAS_NETADDR:
        raise F5ModuleError("The python netaddr module is required")

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
