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
short_description: Manage LTM virtual servers on a BIG-IP
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
    required: false
    default: present
    choices:
      - present
      - absent
      - enabled
      - disabled
  name:
    description:
      - Virtual server name.
    required: true
    aliases:
      - vs
  destination:
    description:
      - Destination IP of the virtual server (only host is currently
        supported). Required when state=present and vs does not exist.
    required: true
    aliases:
      - address
      - ip
  port:
    description:
      - Port of the virtual server. Required when C(state) is C(present)
        and virtual server does not exist.
    required: false
    default: None
  profiles:
    description:
      - List of all Profiles (HTTP, ClientSSL, ServerSSL, etc) that must be
        used by the virtual server. The module will delegate to the device
        whether the specified profile list is valid or not.
    aliases:
      - all_profiles
    required: false
    default: None
  irules:
    version_added: "2.2"
    description:
      - List of rules to be applied in priority order.
    aliases:
      - all_rules
    required: false
    default: None
  enabled_vlans:
    version_added: "2.2"
    description:
      - List of VLANs to be enabled. When a VLAN named C(ALL) is used, all
        VLANs will be allowed. VLANs can be specified with or without the
        leading partition. If the partition is not specified in the VLAN,
        then the `partition` option of this module will be used.
    required: false
    default: None
  pool:
    description:
      - Default pool for the virtual server.
    required: false
    default: None
  snat:
    description:
      - Source network address policy.
    required: false
    choices:
      - None
      - Automap
      - Name of a SNAT pool (eg "/Common/snat_pool_name") to enable SNAT with the specific pool
    default: None
  default_persistence_profile:
    description:
      - Default Profile which manages the session persistence.
    required: false
    default: None
  route_advertisement_state:
    description:
      - Enable route advertisement for destination.
    required: false
    default: None
    choices:
      - enabled
      - disabled
    version_added: "2.3"
  description:
    description:
      - Virtual server description.
    required: false
    default: None
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

from ansible.module_utils.f5_utils import *


class Parameters(AnsibleF5Parameters):
    api_map = {
        'sourceAddressTranslation': 'snat'
    }

    api_attributes = [
        'destination', 'enabled', 'disabled', 'pool', 'port',
        'vlans', 'persist', 'sourceAddressTranslation', 'profiles',
        'vlansEnabled', 'vlansDisabled'
    ]

    updatables = [
        'destination', 'enabled', 'disabled', 'pool', 'port',
        'irules', 'profiles', 'vlans', 'default_persistence_profile'
    ]

    returnables = [
        'cache', 'forwarders', 'name_servers', 'search', 'ip_version'
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
        if self._values['pool'].startswith('/'+self.partition):
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
            if vlan.startswith('/'+self.partition):
                results.append(vlan)
            else:
                vlan = '/{0}/{1}'.format(self.partition, vlan)
                results.append(vlan)
        return results

    @enabled_vlans.setter
    def enabled_vlans(self, value):
        self._values['vlans'] = value

    @property
    def description(self):
        if self._values['description'] is None:
            return None
        return str(self._values['description'])

    @property
    def destination(self):
        if self._values['destination'] is None:
            return None
        destination = self._values['destination']
        try:
            ip = netaddr.IPAddress(destination)
        except netaddr.core.AddrFormatError:
            raise F5ModuleError(
                "The provided destination is not a valid IP address"
            )
        return '/{0}/{1}:{2}'.format(
            self.partition, self._values['destination'], self.port
        )

    @destination.setter
    def destination(self, value):
        matches = re.search(r'.*\/(?P<destination>.*):(?P<port>\d+)', value)
        if matches:
            self._values['destination'] = matches.group('destination')
            self._values['port'] = matches.group('port')
        else:
            self._values['destination'] = value

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
    def route_advertisement_state(self):
        if self._values['route_advertisement_state'] is None:
            return None
        return str(self._values['route_advertisement_state'])

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
            name=str(item['name'])
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
            if state in ['present', 'enabled', 'disabled']:
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
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
        return Parameters(result.attrs)

    def exists(self):
        return self.client.api.tm.ltm.virtuals.virtual.exists(
            name=self.have.name,
            partition=self.have.partition
        )

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def update_virtual_server_on_device(self, params):
        resource = api.tm.ltm.virtuals.virtual.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.modify(**params)

    def create(self):
        required_resources = ['destination', 'port']

        self._set_changed_options()
        if self.want.destination is None:
            raise F5ModuleError(
                'destination must be specified when creating a static route'
            )
        if all(getattr(self.want, v) is None for v in required_resources):
            raise F5ModuleError(
                "You must specify both of "
                + ', '.join(required_resources)
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

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.ltm.virtuals.virtual.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the virtual server")
        return True

    def remove_from_device(self):
        resource = self.client.api.tm.ltm.virtuals.virtual.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent', 'disabled', 'enabled']
            ),
            name=dict(
                type='str',
                required=True,
                aliases=['vs']
            ),
            destination=dict(
                type='str',
                aliases=['address', 'ip'],
                default=None
            ),
            port=dict(
                type='int',
                default=None
            ),
            profiles_both=dict(
                type='list',
                default=None,
                aliases=['all_profiles']
            ),
            profiles_client_side=dict(
                type='list',
                default=None
            ),
            profiles_server_side=dict(
                type='list',
                default=None
            ),
            irules=dict(
                type='list',
                default=None,
                aliases=['all_rules']
            ),
            enabled_vlans=dict(
                type='list',
                default=None
            ),
            pool=dict(
                type='str',
                default=None
            ),
            description=dict(
                type='str',
                default=None
            ),
            snat=dict(
                type='str',
                default=None
            ),
            route_advertisement_state=dict(
                type='str',
                default=None,
                choices=['enabled', 'disabled']
            ),
            default_persistence_profile=dict(
                type='str',
                default=None
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
