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
---
module: bigip_virtual_server
short_description: Manage LTM virtual servers on a BIG-IP.
description:
  - Manage LTM virtual servers on a BIG-IP
version_added: "2.1"
options:
  state:
    description:
      - The virtual server state. If C(absent), delete the virtual server
        if it exists. C(present) creates the virtual server and enable it.
        If C(enabled), enable the virtual server if it exists. If C(disabled),
        create the virtual server if needed, and set state to C(disabled).
    default: present
    choices:
      - present
      - absent
      - enabled
      - disabled
  name:
    description:
      - Virtual server name.
    required: True
    aliases:
      - vs
  destination:
    description:
      - Destination IP of the virtual server (only host is currently
        supported). Required when state=present and vs does not exist.
    required: True
    aliases:
      - address
      - ip
  port:
    description:
      - Port of the virtual server. Required when C(state) is C(present)
        and virtual server does not exist.
  profiles:
    description:
      - List of all Profiles (HTTP, ClientSSL, ServerSSL, etc) that must be
        used by the virtual server. The module will delegate to the device
        whether the specified profile list is valid or not.
    aliases:
      - all_profiles
  irules:
    version_added: "2.2"
    description:
      - List of rules to be applied in priority order.
    aliases:
      - all_rules
  enabled_vlans:
    version_added: "2.2"
    description:
      - List of VLANs to be enabled. When a VLAN named C(ALL) is used, all
        VLANs will be allowed. VLANs can be specified with or without the
        leading partition. If the partition is not specified in the VLAN,
        then the `partition` option of this module will be used.
  pool:
    description:
      - Default pool for the virtual server.
  snat:
    description:
      - Source network address policy.
    required: false
    choices:
      - None
      - Automap
      - Name of a SNAT pool (eg "/Common/snat_pool_name") to enable SNAT
        with the specific pool
  default_persistence_profile:
    description:
      - Default Profile which manages the session persistence.
  route_advertisement_state:
    description:
      - Enable route advertisement for destination.
    choices:
      - enabled
      - disabled
    version_added: "2.3"
    deprecated: Deprecated in 2.4. Use the bigip_virtual_address module instead.
  description:
    description:
      - Virtual server description.
notes:
  - Requires BIG-IP software version >= 11
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Requires the netaddr Python package on the host. This is as easy as pip
    install netaddr.
requirements:
  - f5-sdk
  - netaddr
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add virtual server
  bigip_virtual_server:
      server: lb.mydomain.net
      user: admin
      password: secret
      state: present
      partition: Common
      name: my-virtual-server
      destination: "10.10.10.10"
      port: 443
      pool: "my-pool"
      snat: Automap
      description: Test Virtual Server
      profiles_both:
          - http
          - fix
      profiles_server_side:
          - clientssl
      profiles_client_side:
          - ilx
      enabled_vlans:
          - /Common/vlan2
  delegate_to: localhost

- name: Modify Port of the Virtual Server
  bigip_virtual_server:
      server: lb.mydomain.net
      user: admin
      password: secret
      state: present
      partition: Common
      name: my-virtual-server
      port: 8080
  delegate_to: localhost

- name: Delete virtual server
  bigip_virtual_server:
      server: lb.mydomain.net
      user: admin
      password: secret
      state: absent
      partition: Common
      name: my-virtual-server
  delegate_to: localhost
'''

RETURN = '''
---
deleted:
    description: Name of a virtual server that was deleted
    returned: changed
    type: string
    sample: "my-virtual-server"
'''


import netaddr
import re

from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    HAS_F5SDK,
    F5ModuleError,
    iControlUnexpectedHTTPError,
    defaultdict,
    iteritems
)


class Parameters(AnsibleF5Parameters):
    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
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

    @property
    def destination(self):
        if self._values['destination'] is None:
            return None
        destination = self._values['destination']
        try:
            netaddr.IPAddress(destination.split("%")[0])
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided destination is not a valid IP address"
            )
        result = '/{0}/{1}:{2}'.format(
            self.partition, self._values['destination'], self.port
        )
        return result

    @destination.setter
    def destination(self, value):
        if value is None:
            return
        matches = re.search(r'.*\/(?P<destination>.*):(?P<port>\d+)', value)
        if matches:
            self._values['destination'] = matches.group('destination')
            self._values['port'] = matches.group('port')
        else:
            self._values['destination'] = value

    @property
    def destination_address(self):
        return self._values['destination']

    @destination_address.setter
    def destination_address(self, value):
        self._values['destination'] = value

    @property
    def port(self):
        if self._values['port'] is None:
            return None
        try:
            port = int(self._values['port'])
        except ValueError:
            raise F5ModuleError(
                "The specified port was not a valid integer"
            )
        if 0 <= port <= 65535:
            return port
        raise F5ModuleError(
            "Valid ports must be in range 0 - 65535"
        )

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


class VirtualAddressParameters(Parameters):
    api_map = {
        'routeAdvertisement': 'route_advertisement_state'
    }
    returnables = [
        'route_advertisement_state'
    ]

    updatables = [
        'route_advertisement_state'
    ]

    api_attributes = [
        'routeAdvertisement'
    ]

    @property
    def route_advertisement_state(self):
        # TODO: Remove in 2.5
        if self._values['route_advertisement_state'] is None:
            return None
        if self._values['__warnings'] is None:
            self._values['__warnings'] = []
        self._values['__warnings'].append(
            dict(
                msg="Usage of the 'route_advertisement_state' parameter is deprecated. Use the bigip_virtual_address module instead",
                version='2.4'
            )
        )
        return str(self._values['route_advertisement_state'])


class VirtualServerParameters(Parameters):
    api_map = {
        'sourceAddressTranslation': 'snat'
    }

    api_attributes = [
        'destination', 'enabled', 'disabled', 'pool',
        'vlans', 'persist', 'sourceAddressTranslation', 'profiles',
        'vlansEnabled', 'vlansDisabled'
    ]

    updatables = [
        'destination', 'enabled', 'disabled', 'pool', 'port',
        'irules', 'profiles', 'enabled_vlans', 'default_persistence_profile'
    ]

    returnables = [
        'destination', 'enabled', 'disabled', 'pool', 'port',
        'irules', 'profiles', 'enabled_vlans', 'default_persistence_profile'
    ]

    @property
    def irules(self):
        results = []
        if self._values['irules'] is None:
            return None
        for irule in self._values['irules']:
            if not irule.startswith(self.partition):
                irule = '/{0}/{1}'.format(self.partition, irule)
            results.append(irule)
        return results

    @property
    def profiles_both(self):
        result = []
        mutually_exclusive_profiles = [
            'sip', 'sipsession', 'iiop', 'rtsp', 'http', 'diameter',
            'diametersession', 'radius', 'ftp', 'tftp', 'dns', 'pptp', 'fix'
        ]
        if self._values['profiles_both'] is None:
            return None
        profiles = set(self._values['profiles_both'])
        mutually_exclusive = [x for x in profiles if x in mutually_exclusive_profiles]
        if len(mutually_exclusive) > 1:
            raise F5ModuleError(
                "Profiles {0} are mutually exclusive".format(
                    ', '.join(mutually_exclusive_profiles).strip()
                )
            )
        for profile in profiles:
            result.append({
                'name': str(profile),
                'context': 'all'
            })
        return result

    @property
    def profiles_client_side(self):
        result = []
        if self._values['profiles_client_side'] is None:
            return None
        profiles = set(self._values['profiles_client_side'])
        for profile in profiles:
            result.append({
                'name': str(profile),
                'context': 'clientside'
            })
        return result

    @property
    def profiles_server_side(self):
        result = []
        if self._values['profiles_server_side'] is None:
            return None
        profiles = set(self._values['profiles_server_side'])
        for profile in profiles:
            result.append({
                'name': str(profile),
                'context': 'serverside'
            })
        return result

    @property
    def pool(self):
        if self._values['pool'] is None:
            return None
        if self._values['pool'].startswith('/' + self.partition):
            return self._values['pool']
        else:
            return '/{0}/{1}'.format(self.partition, self._values['pool'])

    @property
    def vlansEnabled(self):
        if self._values['enabled_vlans'] is None:
            return False
        return True

    @property
    def vlansDisabled(self):
        if self._values['enabled_vlans'] in [None, '', 'ALL']:
            return True
        return False

    @property
    def enabled_vlans(self):
        if self._values['vlans'] is None:
            return None
        elif 'ALL' in self._values['vlans']:
            return []
        results = []
        vlans = set(self._values['vlans'])
        for vlan in vlans:
            if vlan.startswith('/' + self.partition):
                results.append(vlan)
            else:
                vlan = '/{0}/{1}'.format(self.partition, vlan)
                results.append(vlan)
        return list(set(results))

    @property
    def disabled_vlans(self):
        return None

    @property
    def vlans(self):
        if self.diabled_vlans:
            return self.disabled_vlans
        return self.enabled_vlans

    @enabled_vlans.setter
    def enabled_vlans(self, value):
        self._values['vlans'] = value

    @property
    def description(self):
        if self._values['description'] is None:
            return None
        return str(self._values['description'])

    @property
    def state(self):
        if self._values['state'] == 'present':
            return 'enabled'
        return self._values['state']

    @property
    def default_persistence_profile(self):
        if self._values['default_persistence_profile'] is None:
            return None
        return str(self._values['default_persistence_profile'])

    @property
    def snat(self):
        if self._values['snat'] is None:
            return None
        lowercase = self._values['snat'].lower()
        if lowercase in ['automap', 'none']:
            return dict(
                type=lowercase
            )
        snat_pool = '/{0}/{1}'.format(
            self.partition, self._values['snat']
        )
        return dict(
            pool=snat_pool,
            type='snat'
        )

    @property
    def profilesReference(self):
        return self._values['profilesReference']

    @profilesReference.setter
    def profilesReference(self, value):
        self._values['profiles_both'] = []
        self._values['profiles_client_side'] = []
        self._values['profiles_server_side'] = []

        if 'items' not in value:
            return

        for item in value['items']:
            context = str(item['context'])
            name = str(item['name'])
            if context == 'all':
                self._values['profiles_both'].append(name)
            elif context == 'serverside':
                self._values['profiles_server_side'].append(name)
            elif context == 'clientside':
                self._values['profiles_client_side'].append(name)
            else:
                raise F5ModuleError(
                    "Unknown profile context found"
                )


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
    def destination(self):
        if self.want.destination is None and self.want.port is None:
            return None

        if self.want.destination is None:
            self.want.destination_address = self.have.destination_address
        elif self.want.port is None:
            self.want.update({'port': self.have.port})

        if self.want.destination == self.have.destination:
            return None
        else:
            return self.want.destination

    @property
    def enabled_vlans(self):
        if self.want.vlans is None:
            return None
        elif self.want.vlans == [] and self.have.vlans is None:
            return None
        elif self.want.vlans == self.have.vlans:
            return None
        else:
            return self.want.vlans

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

    def exec_module(self):
        managers = list()
        managers.append(self.get_manager('virtual_server'))
        if self.client.module.params['route_advertisement_state'] is not None:
            managers.append(self.get_manager('virtual_address'))
        result = self.execute_managers(managers)
        return result

    def execute_managers(self, managers):
        results = dict(changed=False)
        for manager in managers:
            result = manager.exec_module()
            for k, v in iteritems(result):
                if k == 'changed':
                    if v is True:
                        results['changed'] = True
                else:
                    results[k] = v
        return results

    def get_manager(self, type):
        vsm = VirtualServerManager(self.client)
        if type == 'virtual_server':
            return vsm
        elif type == 'virtual_address':
            self.set_name_of_virtual_address()
            result = VirtualAddressManager(self.client)
            return result

    def set_name_of_virtual_address(self):
        mgr = VirtualServerManager(self.client)
        params = mgr.read_current_from_device()
        name = params.destination_address
        self.client.module.params['name'] = name


class BaseManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state in ['present', 'enabled', 'disabled']:
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations()
        return result

    def _announce_deprecations(self):
        warnings = []
        if self.want:
            warnings += self.want._values.get('__warnings', [])
        if self.have:
            warnings += self.have._values.get('__warnings', [])
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

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def create(self):
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the virtual server")
        return True


class VirtualServerManager(BaseManager):
    def __init__(self, client):
        super(VirtualServerManager, self).__init__(client)
        self.want = VirtualServerParameters(self.client.module.params)
        self.changes = VirtualServerParameters()

    def _set_changed_options(self):
        changed = {}
        for key in VirtualServerParameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = VirtualServerParameters(changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = VirtualServerParameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                changed[k] = change
        if changed:
            self.changes = VirtualServerParameters(changed)
            return True
        return False

    def exists(self):
        result = self.client.api.tm.ltm.virtuals.virtual.exists(
            name=self.want.name,
            partition=self.want.partition
        )
        return result

    def create(self):
        required_resources = ['destination', 'port']

        self._set_changed_options()
        if self.want.destination is None:
            raise F5ModuleError(
                "'destination' must be specified when creating a virtual server"
            )
        if all(getattr(self.want, v) is None for v in required_resources):
            raise F5ModuleError(
                "You must specify both of " + ', '.join(required_resources)
            )
        return super(VirtualServerManager, self).create()

    def update_on_device(self):
        params = self.changes.api_params()
        resource = self.client.api.tm.ltm.virtuals.virtual.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.modify(**params)

    def read_current_from_device(self):
        result = self.client.api.tm.ltm.virtuals.virtual.load(
            name=self.want.name,
            partition=self.want.partition,
            requests_params=dict(
                params=dict(
                    expandSubcollections='true'
                )
            )
        )
        result = VirtualServerParameters(result.attrs)
        return result

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.ltm.virtuals.virtual.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def remove_from_device(self):
        resource = self.client.api.tm.ltm.virtuals.virtual.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if resource:
            resource.delete()


class VirtualAddressManager(BaseManager):
    def __init__(self, client):
        super(VirtualAddressManager, self).__init__(client)
        self.want = VirtualAddressParameters(self.client.module.params)
        self.have = None
        self.changes = VirtualAddressParameters()

    def _set_changed_options(self):
        changed = {}
        for key in VirtualAddressParameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = VirtualAddressParameters(changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = VirtualAddressParameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                changed[k] = change
        if changed:
            self.changes = VirtualAddressParameters(changed)
            return True
        return False

    def read_current_from_device(self):
        result = self.client.api.tm.ltm.virtual_address_s.virtual_address.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result = VirtualAddressParameters(result.attrs)
        return result

    def update_on_device(self):
        params = self.want.api_params()
        resource = self.client.api.tm.ltm.virtual_address_s.virtual_address.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.modify(**params)

    def exists(self):
        result = self.client.api.tm.ltm.virtual_address_s.virtual_address.exists(
            name=self.want.name,
            partition=self.want.partition
        )
        return result


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            state=dict(
                default='present',
                choices=['present', 'absent', 'disabled', 'enabled']
            ),
            name=dict(
                required=True,
                aliases=['vs']
            ),
            destination=dict(
                aliases=['address', 'ip']
            ),
            port=dict(
                type='int'
            ),
            profiles_both=dict(
                type='list',
                aliases=['all_profiles']
            ),
            profiles_client_side=dict(
                type='list'
            ),
            profiles_server_side=dict(
                type='list'
            ),
            irules=dict(
                type='list',
                aliases=['all_rules']
            ),
            enabled_vlans=dict(
                type='list'
            ),
            pool=dict(),
            description=dict(),
            snat=dict(),
            route_advertisement_state=dict(
                choices=['enabled', 'disabled']
            ),
            default_persistence_profile=dict()
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
