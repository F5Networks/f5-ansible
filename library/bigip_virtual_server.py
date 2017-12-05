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
---
module: bigip_virtual_server
short_description: Manage LTM virtual servers on a BIG-IP
description:
  - Manage LTM virtual servers on a BIG-IP.
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
      - Destination IP of the virtual server.
      - Required when C(state) is C(present) and virtual server does not exist.
    required: True
    aliases:
      - address
      - ip
  port:
    description:
      - Port of the virtual server. Required when C(state) is C(present)
        and virtual server does not exist.
      - If you do not want to specify a particular port, use the value C(0).
        The result is that the virtual server will listen on any port.
  profiles:
    description:
      - List of profiles (HTTP, ClientSSL, ServerSSL, etc) to apply to both sides
        of the connection (client-side and server-side).
      - If you only want to apply a particular profile to the client-side of
        the connection, specify C(client-side) for the profile's C(context).
      - If you only want to apply a particular profile to the server-side of
        the connection, specify C(server-side) for the profile's C(context).
      - If C(context) is not provided, it will default to C(all).
    suboptions:
      name:
        description:
          - Name of the profile.
          - If this is not specified, then it is assumed that the profile item is
            only a name of a profile.
          - This must be specified if a context is specified.
        required: false
      context:
        description:
          - The side of the connection on which the profile should be applied.
        choices:
          - all
          - server-side
          - client-side
        default: all
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
      - List of VLANs to be enabled. When a VLAN named C(all) is used, all
        VLANs will be allowed. VLANs can be specified with or without the
        leading partition. If the partition is not specified in the VLAN,
        then the C(partition) option of this module will be used.
      - This parameter is mutually exclusive with the C(disabled_vlans) parameter.
  disabled_vlans:
    version_added: 2.5
    description:
      - List of VLANs to be disabled. If the partition is not specified in the VLAN,
        then the C(partition) option of this module will be used.
      - This parameter is mutually exclusive with the C(enabled_vlans) parameters.
  pool:
    description:
      - Default pool for the virtual server.
  policies:
    description:
      - Specifies the policies for the virtual server
    aliases:
      - all_policies
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
    deprecated: Deprecated in 2.4. Use the C(bigip_virtual_address) module instead.
  description:
    description:
      - Virtual server description.
  fallback_persistence_profile:
    description:
      - Specifies the persistence profile you want the system to use if it
        cannot use the specified default persistence profile.
    version_added: 2.3
  partition:
    description:
      - Device partition to manage resources on.
    default: Common
    version_added: 2.5
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

EXAMPLES = r'''
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

- name: Add virtual server
  bigip_virtual_server:
    server: lb.mydomain.net
    user: admin
    password: secret
    state: present
    partition: Common
    name: my-virtual-server
    destination: 10.10.10.10
    port: 443
    pool: my-pool
    snat: Automap
    description: Test Virtual Server
    profiles:
      - http
      - fix
      - name: clientssl
        context: server-side
      - name: ilx
        context: client-side
    policies:
      - my-ltm-policy-for-asm
      - ltm-uri-policy
      - ltm-policy-2
      - ltm-policy-3
    enabled_vlans:
      - /Common/vlan2
  delegate_to: localhost

- name: Add FastL4 virtual server
  bigip_virtual_server:
    destination: 1.1.1.1
    name: fastl4_vs
    port: 80
    profiles:
      - fastL4
    state: present
'''

RETURN = r'''
---
deleted:
  description: Name of a virtual server that was deleted
  returned: changed
  type: string
  sample: my-virtual-server
'''


import netaddr
import re

from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError
from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
from ansible.module_utils.six import iteritems
from collections import defaultdict
from collections import namedtuple


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

    def _fqdn_name(self, value):
        if value is not None and not value.startswith('/'):
            return '/{0}/{1}'.format(self.partition, value)
        return value

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
        'sourceAddressTranslation': 'snat',
        'fallbackPersistence': 'fallback_persistence_profile',
        'persist': 'default_persistence_profile',
        'vlansEnabled': 'vlans_enabled',
        'vlansDisabled': 'vlans_disabled',
        'profilesReference': 'profiles',
        'policiesReference': 'policies',
        'rules': 'irules'
    }

    api_attributes = [
        'description',
        'destination',
        'disabled',
        'enabled',
        'fallbackPersistence',
        'persist',
        'policies',
        'pool',
        'profiles',
        'rules',
        'sourceAddressTranslation',
        'vlans',
        'vlansEnabled',
        'vlansDisabled'
    ]

    updatables = [
        'description',
        'default_persistence_profile',
        'destination',
        'disabled',
        'disabled_vlans',
        'enabled',
        'enabled_vlans',
        'fallback_persistence_profile',
        'irules',
        'pool',
        'policies',
        'port',
        'profiles',
        'snat',
    ]

    returnables = [
        'description',
        'default_persistence_profile',
        'destination',
        'disabled',
        'disabled_vlans',
        'enabled',
        'enabled_vlans',
        'fallback_persistence_profile',
        'irules',
        'pool',
        'policies',
        'port',
        'profiles',
        'snat'
    ]

    def __init__(self, params=None):
        super(VirtualServerParameters, self).__init__(params)
        self.profiles_mutex = [
            'sip', 'sipsession', 'iiop', 'rtsp', 'http', 'diameter',
            'diametersession', 'radius', 'ftp', 'tftp', 'dns', 'pptp', 'fix'
        ]

    def is_valid_ip(self, value):
        try:
            netaddr.IPAddress(value)
            return True
        except (netaddr.core.AddrFormatError, ValueError):
            return False

    def _format_port_for_destination(self, ip, port):
        addr = netaddr.IPAddress(ip)
        if addr.version == 6:
            if port == 0:
                result = '.any'
            else:
                result = '.{0}'.format(port)
        else:
            result = ':{0}'.format(port)
        return result

    def _format_destination(self, address, port, route_domain):
        if port is None:
            if route_domain is None:
                result = '{0}'.format(
                    self._fqdn_name(address)
                )
            else:
                result = '{0}%{1}'.format(
                    self._fqdn_name(address),
                    route_domain
                )
        else:
            port = self._format_port_for_destination(address, port)
            if route_domain is None:
                result = '{0}{1}'.format(
                    self._fqdn_name(address),
                    port
                )
            else:
                result = '{0}%{1}{2}'.format(
                    self._fqdn_name(address),
                    route_domain,
                    port
                )
        return result


class VirtualServerApiParameters(VirtualServerParameters):
    @property
    def destination(self):
        if self._values['destination'] is None:
            return None
        destination = self.destination_tuple
        result = self._format_destination(destination.ip, destination.port, destination.route_domain)
        return result

    @property
    def destination_tuple(self):
        Destination = namedtuple('Destination', ['ip', 'port', 'route_domain'])

        # Remove the partition
        if self._values['destination'] is None:
            result = Destination(ip=None, port=None, route_domain=None)
            return result
        destination = re.sub(r'^/[a-zA-Z_.-]+/', '', self._values['destination'])

        if self.is_valid_ip(destination):
            result = Destination(
                ip=destination,
                port=None,
                route_domain=None
            )
            return result

        # Covers the following examples
        #
        # /Common/2700:bc00:1f10:101::6%2.80
        # 2700:bc00:1f10:101::6%2.80
        # 1.1.1.1%2:80
        # /Common/1.1.1.1%2:80
        # /Common/2700:bc00:1f10:101::6%2.any
        #
        pattern = r'(?P<ip>[^%]+)%(?P<route_domain>[0-9]+)[:.](?P<port>[0-9]+|any)'
        matches = re.search(pattern, destination)
        if matches:
            try:
                port = int(matches.group('port'))
            except ValueError:
                # Can be a port of "any". This only happens with IPv6
                port = matches.group('port')
                if port == 'any':
                    port = 0
            ip = matches.group('ip')
            if not self.is_valid_ip(ip):
                raise F5ModuleError(
                    "The provided destination is not a valid IP address"
                )
            result = Destination(
                ip=matches.group('ip'),
                port=port,
                route_domain=int(matches.group('route_domain'))
            )
            return result

        pattern = r'(?P<ip>[^%]+)%(?P<route_domain>[0-9]+)'
        matches = re.search(pattern, destination)
        if matches:
            ip = matches.group('ip')
            if not self.is_valid_ip(ip):
                raise F5ModuleError(
                    "The provided destination is not a valid IP address"
                )
            result = Destination(
                ip=matches.group('ip'),
                port=None,
                route_domain=int(matches.group('route_domain'))
            )
            return result

        parts = destination.split('.')
        if len(parts) == 4:
            # IPv4
            ip, port = destination.split(':')
            if not self.is_valid_ip(ip):
                raise F5ModuleError(
                    "The provided destination is not a valid IP address"
                )
            result = Destination(
                ip=ip,
                port=int(port),
                route_domain=None
            )
            return result
        elif len(parts) == 2:
            # IPv6
            ip, port = destination.split('.')
            try:
                port = int(port)
            except ValueError:
                # Can be a port of "any". This only happens with IPv6
                if port == 'any':
                    port = 0
                pass
            if not self.is_valid_ip(ip):
                raise F5ModuleError(
                    "The provided destination is not a valid IP address"
                )
            result = Destination(
                ip=ip,
                port=port,
                route_domain=None
            )
            return result
        else:
            result = Destination(ip=None, port=None, route_domain=None)
            return result

    @property
    def port(self):
        destination = self.destination_tuple
        self._values['port'] = destination.port
        return destination.port

    @property
    def route_domain(self):
        destination = self.destination_tuple
        self._values['route_domain'] = destination.route_domain
        return destination.route_domain

    @property
    def profiles(self):
        if 'items' not in self._values['profiles']:
            return None
        result = []
        for item in self._values['profiles']['items']:
            context = item['context']
            name = item['name']
            if context in ['all', 'serverside', 'clientside']:
                result.append(dict(name=name, context=context, fullPath=item['fullPath']))
            else:
                raise F5ModuleError(
                    "Unknown profile context found: '{0}'".format(context)
                )
        return result

    @property
    def policies(self):
        if 'items' not in self._values['policies']:
            return None
        result = []
        for item in self._values['policies']['items']:
            name = item['name']
            partition = item['partition']
            result.append(dict(name=name, partition=partition))
        return result

    @property
    def default_persistence_profile(self):
        if self._values['default_persistence_profile'] is None:
            return None
        # These persistence profiles are always lists when we get them
        # from the REST API even though there can only be one. We'll
        # make it a list again when we get to the Difference engine.
        return self._values['default_persistence_profile'][0]


class VirtualServerModuleParameters(VirtualServerParameters):
    @property
    def destination(self):
        addr = self._values['destination'].split("%")[0]
        if not self.is_valid_ip(addr):
            raise F5ModuleError(
                "The provided destination is not a valid IP address"
            )
        result = self._format_destination(addr, self.port, self.route_domain)
        return result

    @property
    def port(self):
        if self._values['port'] is None:
            return None
        if self._values['port'] in ['*', 'any']:
            return 0
        self._check_port()
        return int(self._values['port'])

    def _check_port(self):
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
            result = self._fqdn_name(irule)
            results.append(result)
        return results

    @property
    def profiles(self):
        if self._values['profiles'] is None:
            return None
        result = []
        for profile in self._values['profiles']:
            tmp = dict()
            if isinstance(profile, dict):
                tmp.update(profile)
                self._handle_profile_context(tmp)
                if 'name' not in profile:
                    tmp['name'] = profile
                tmp['fullPath'] = self._fqdn_name(tmp['name'])
                self._handle_clientssl_profile_nuances(tmp)
            else:
                tmp['name'] = profile
                tmp['context'] = 'all'
                tmp['fullPath'] = self._fqdn_name(tmp['name'])
                self._handle_clientssl_profile_nuances(tmp)
            result.append(tmp)
        mutually_exclusive = [x['name'] for x in result if x in self.profiles_mutex]
        if len(mutually_exclusive) > 1:
            raise F5ModuleError(
                "Profiles {0} are mutually exclusive".format(
                    ', '.join(self.profiles_mutex).strip()
                )
            )
        return result

    def _handle_profile_context(self, tmp):
        if 'context' not in tmp:
            tmp['context'] = 'all'
        else:
            if 'name' not in tmp:
                raise F5ModuleError(
                    "A profile name must be specified when a context is specified."
                )
        tmp['context'] = tmp['context'].replace('server-side', 'serverside')
        tmp['context'] = tmp['context'].replace('client-side', 'clientside')

    def _handle_clientssl_profile_nuances(self, profile):
        if profile['name'] != 'clientssl':
            return
        if profile['context'] != 'clientside':
            profile['context'] = 'clientside'

    @property
    def policies(self):
        if self._values['policies'] is None:
            return None
        result = []
        policies = [self._fqdn_name(p) for p in self._values['policies']]
        policies = set(policies)
        for policy in policies:
            parts = policy.split('/')
            if len(parts) != 3:
                raise F5ModuleError(
                    "The specified policy '{0}' is malformed".format(policy)
                )
            tmp = dict(
                name=parts[2],
                partition=parts[1]
            )
            result.append(tmp)
        return result

    @property
    def pool(self):
        if self._values['pool'] is None:
            return None
        return self._fqdn_name(self._values['pool'])

    @property
    def vlans_enabled(self):
        if self._values['enabled_vlans'] is None:
            return None
        elif self._values['vlans_enabled'] is False:
            # This is a special case for "all" enabled VLANs
            return False
        if self._values['disabled_vlans'] is None:
            return True
        return False

    @property
    def vlans_disabled(self):
        if self._values['disabled_vlans'] is None:
            return None
        elif self._values['vlans_disabled'] is True:
            # This is a special case for "all" enabled VLANs
            return True
        elif self._values['enabled_vlans'] is None:
            return True
        return False

    @property
    def enabled_vlans(self):
        if self._values['enabled_vlans'] is None:
            return None
        elif any(x.lower() for x in self._values['enabled_vlans'] if x == 'all'):
            return [self._fqdn_name('all')]
        results = list(set([self._fqdn_name(x) for x in self._values['enabled_vlans']]))
        return results

    @property
    def disabled_vlans(self):
        if self._values['disabled_vlans'] is None:
            return None
        elif any(x.lower() for x in self._values['disabled_vlans'] if x == 'all'):
            raise F5ModuleError(
                "You cannot disable all VLANs. You must name them individually."
            )
        results = list(set([self._fqdn_name(x) for x in self._values['disabled_vlans']]))
        return results

    @property
    def vlans(self):
        disabled = self.disabled_vlans
        if disabled:
            return self.disabled_vlans
        return self.enabled_vlans

    @property
    def state(self):
        if self._values['state'] == 'present':
            return 'enabled'
        return self._values['state']

    @property
    def snat(self):
        if self._values['snat'] is None:
            return None
        lowercase = self._values['snat'].lower()
        if lowercase in ['automap', 'none']:
            return dict(type=lowercase)
        snat_pool = self._fqdn_name(self._values['snat'])
        return dict(pool=snat_pool, type='snat')

    @property
    def default_persistence_profile(self):
        if self._values['default_persistence_profile'] is None:
            return None
        profile = self._fqdn_name(self._values['default_persistence_profile'])
        parts = profile.split('/')
        if len(parts) != 3:
            raise F5ModuleError(
                "The specified 'default_persistence_profile' is malformed"
            )
        result = dict(
            name=parts[2],
            partition=parts[1]
        )
        return result

    @property
    def fallback_persistence_profile(self):
        if self._values['fallback_persistence_profile'] is None:
            return None
        result = self._fqdn_name(self._values['fallback_persistence_profile'])
        return result


class VirtualServerChanges(VirtualServerParameters):
    @property
    def destination(self):
        return self._values['destination']

    @property
    def vlans(self):
        if self._values['vlans'] is None:
            return None
        elif len(self._values['vlans']) == 0:
            return []
        elif any(x for x in self._values['vlans'] if x.lower() in ['/common/all', 'all']):
            return []
        return self._values['vlans']


class VirtualAddressChanges(VirtualAddressParameters):
    pass


class Difference(object):
    def __init__(self, want, have=None):
        self.have = have
        self.want = want

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            result = self.__default(param)
            return result

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)

            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1

    @property
    def destination(self):
        addr_tuple = [self.want.destination, self.want.port, self.want.route_domain]
        if all(x for x in addr_tuple if x is None):
            return None

        have = self.have.destination_tuple

        if self.want.port is None:
            self.want.update({'port': have.port})
        if self.want.route_domain is None:
            self.want.update({'route_domain': have.route_domain})
        if self.want.destination_address is None:
            self.want.destination_address = have.ip

        want = self.want._format_destination(
            self.want.destination_address, self.want.port, self.want.route_domain
        )
        if want != self.have.destination:
            return self.want._fqdn_name(want)

    @property
    def vlans(self):
        if self.want.vlans is None:
            return None
        elif self.want.vlans == [] and self.have.vlans is None:
            return None
        elif self.want.vlans == self.have.vlans:
            return None

        # Specifically looking for /all because the vlans return value will be
        # an FQDN list. This means that "all" will be returned as "/partition/all",
        # ex, /Common/all.
        #
        # We do not want to accidentally match values that would end with the word
        # "all", like "vlansall". Therefore we look for the forward slash because this
        # is a path delimiter.
        elif any(x.lower().endswith('/all') for x in self.want.vlans):
            if self.have.vlans is None:
                return None
            else:
                return []
        else:
            return self.want.vlans

    def _update_vlan_status(self, result):
        if self.want.vlans_disabled is not None:
            if self.want.vlans_disabled != self.have.vlans_disabled:
                result['vlans_disabled'] = self.want.vlans_disabled
                result['vlans_enabled'] = not self.want.vlans_disabled
        elif self.want.vlans_enabled is not None:
            if any(x.lower().endswith('/all') for x in self.want.vlans):
                if self.have.vlans_enabled is True:
                    result['vlans_disabled'] = True
                    result['vlans_enabled'] = False
            elif self.want.vlans_enabled != self.have.vlans_enabled:
                result['vlans_disabled'] = not self.want.vlans_enabled
                result['vlans_enabled'] = self.want.vlans_enabled

    @property
    def enabled_vlans(self):
        return self.vlan_status

    @property
    def disabled_vlans(self):
        return self.vlan_status

    @property
    def vlan_status(self):
        result = dict()
        vlans = self.vlans
        if vlans is not None:
            result['vlans'] = vlans
        self._update_vlan_status(result)
        return result

    @property
    def port(self):
        result = self.destination
        if result is not None:
            return dict(
                destination=result
            )

    @property
    def profiles(self):
        if self.want.profiles is None:
            return None
        want = set([(p['name'], p['context'], p['fullPath']) for p in self.want.profiles])
        have = set([(p['name'], p['context'], p['fullPath']) for p in self.have.profiles])
        if len(have) == 0:
            return self.want.profiles
        elif len(have) == 1:
            if want != have:
                return self.want.profiles
        else:
            if not any(x[0] == 'tcp' for x in want):
                have = set([x for x in have if x[0] != 'tcp'])
            if not any(x[0] == 'udp' for x in want):
                have = set([x for x in have if x[0] != 'udp'])
            if not any(x[0] == 'sctp' for x in want):
                have = set([x for x in have if x[0] != 'sctp'])
            want = set([(p[2], p[1]) for p in want])
            have = set([(p[2], p[1]) for p in have])
            if want != have:
                return self.want.profiles

    @property
    def default_persistence_profile(self):
        if self.want.default_persistence_profile is None:
            return None
        w_name = self.want.default_persistence_profile.get('name', None)
        w_partition = self.want.default_persistence_profile.get('partition', None)
        h_name = self.want.default_persistence_profile.get('name', None)
        h_partition = self.want.default_persistence_profile.get('partition', None)
        if w_name != h_name or w_partition != h_partition:
            return [self.want.default_persistence_profile]

    @property
    def policies(self):
        if self.want.policies is None:
            return None
        if not self.have.policies:
            return self.want.policies
        want = set([(p['name'], p['partition']) for p in self.want.policies])
        have = set([(p['name'], p['partition']) for p in self.have.policies])
        if not want == have:
            return self.want.policies

    @property
    def snat(self):
        if self.want.snat is None:
            return None
        if self.want.snat['type'] != self.have.snat['type']:
            result = dict(snat=self.want.snat)
            return result

        if self.want.snat.get('pool', None) is None:
            return None

        if self.want.snat['pool'] != self.have.snat['pool']:
            result = dict(snat=self.want.snat)
            return result


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
        destination = params.destination_tuple
        self.client.module.params['name'] = destination.ip


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

        # This must be changed back to a list to make a valid REST API
        # value. The module manipulates this as a normal dictionary
        if self.want.default_persistence_profile is not None:
            self.want.update({'default_persistence_profile': [self.want.default_persistence_profile]})

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
            raise F5ModuleError("Failed to delete the resource")
        return True


class VirtualServerManager(BaseManager):
    def __init__(self, client):
        super(VirtualServerManager, self).__init__(client)
        self.have = None
        self.want = VirtualServerModuleParameters(self.client.module.params)
        self.changes = VirtualServerChanges()

    def _set_changed_options(self):
        changed = {}
        for key in VirtualServerParameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = VirtualServerChanges(changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = VirtualServerParameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = VirtualServerChanges(changed)
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
        if self.want.enabled_vlans is not None:
            if any(x for x in self.want.enabled_vlans if x.lower() in ['/common/all', 'all']):
                self.want.update(
                    dict(
                        enabled_vlans=[],
                        vlans_disabled=True,
                        vlans_enabled=False
                    )
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
        params = result.attrs
        params.update(dict(kind=result.to_dict().get('kind', None)))
        result = VirtualServerApiParameters(params)
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
        self.changes = VirtualAddressChanges()

    def _set_changed_options(self):
        changed = {}
        for key in VirtualAddressParameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = VirtualAddressChanges(changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = VirtualAddressParameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = VirtualAddressChanges(changed)
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
            profiles=dict(
                type='list',
                aliases=['all_profiles'],
                options=dict(
                    name=dict(required=False),
                    context=dict(default='all', choices=['all', 'server-side', 'client-side'])
                )
            ),
            policies=dict(
                type='list',
                aliases=['all_policies']
            ),
            irules=dict(
                type='list',
                aliases=['all_rules']
            ),
            enabled_vlans=dict(
                type='list'
            ),
            disabled_vlans=dict(
                type='list'
            ),
            pool=dict(),
            description=dict(),
            snat=dict(),
            route_advertisement_state=dict(
                choices=['enabled', 'disabled']
            ),
            default_persistence_profile=dict(),
            fallback_persistence_profile=dict()
        )
        self.f5_product_name = 'bigip'
        self.mutually_exclusive = [
            ['enabled_vlans', 'disabled_vlans']
        ]


def cleanup_tokens(client):
    try:
        resource = client.api.shared.authz.tokens_s.token.load(
            name=client.api.icrs.token
        )
        resource.delete()
    except Exception:
        pass


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name,
        mutually_exclusive=spec.mutually_exclusive
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        cleanup_tokens(client)
        client.module.exit_json(**results)
    except F5ModuleError as e:
        cleanup_tokens(client)
        client.module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
