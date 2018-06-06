#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# Copyright (c) 2013 Matt Hite <mhite@hotmail.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_device_facts
short_description: Collect facts from F5 BIG-IP devices
description:
  - Collect facts from F5 BIG-IP devices.
version_added: 2.7
options:
  gather_subset:
    description:
      - When supplied, this argument will restrict the facts returned to a given subset.
      - Can specify a list of values to include a larger subset.
      - Values can also be used with an initial C(!) to specify that a specific subset
        should not be collected.
    required: True
    choices:
      - internal-data-groups
      - client-ssl-profiles
      - devices
      - device-groups
      - interfaces
      - ssl-certs
      - ssl-keys
      - nodes
      - ltm-pools
      - provision-info
      - irules
      - self-ips
      - software-volumes
      - system-info
      - traffic-groups
      - trunks
      - virtual-addresses
      - virtual-servers
      - vlans
    aliases: ['include']
notes:
  - Requires the netaddr Python package on the host. This is as easy as pip
    install netaddr.
requirements:
  - netaddr
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Collect BIG-IP facts
  bigip_facts:
    server: lb.mydomain.com
    user: admin
    password: secret
    gather_subset:
      - interface
      - vlans
  delegate_to: localhost

- name: Collect all BIG-IP facts
  bigip_facts:
    server: lb.mydomain.com
    user: admin
    password: secret
    gather_subset:
      - all
  delegate_to: localhost

- name: Collect all BIG-IP facts except trunks
  bigip_facts:
    server: lb.mydomain.com
    user: admin
    password: secret
    gather_subset:
      - all
      - "!trunks"
  delegate_to: localhost
'''

RETURN = r'''
irules:
  description: iRule related facts.
  returned: when C(irules) is specified in C(gather_subset).
  type: complex
  contains:
    full_path:
      description:
        - Full name of the resource as known to BIG-IP.
      returned: changed
      type: string
      sample: /Common/irul1
    name:
      description:
        - Relative name of the resource in BIG-IP.
      returned: changed
      type: string
      sample: irule1
    ignore_verification:
      description:
        - Whether the verification of the iRule should be ignored or not.
      returned: changed
      type: bool
      sample: no
    checksum:
      description:
        - Checksum of the iRule as calculated by BIG-IP.
      returned: changed
      type: string
      sample: d41d8cd98f00b204e9800998ecf8427e
    definition:
      description:
        - The actual definition of the iRule.
      returned: changed
      type: string
      sample: when HTTP_REQUEST {\n HTTP::redirect https://[getfield...
    signature:
      description:
        - The calculated signature of the iRule.
      returned: changed
      type: string
      sample: WsYy2M6xMqvosIKIEH/FSsvhtWMe6xKOA6i7f...
  sample: hash/dictionary of values
vlans:
  description: List of VLAN facts.
  returned: when C(vlans) is specified in C(gather_subset).
  type: complex
  contains:
    type:
      description: The action type.
      returned: changed
      type: string
      sample: forward
    pool:
      description: Pool for forward to.
      returned: changed
      type: string
      sample: foo-pool
  sample: hash/dictionary of values
software_volumes:
  description: List of software volumes.
  returned: when C(software-volumes) is specified in C(gather_subset).
  type: complex
  contains:
    active:
      description:
        - Whether the volume is currently active or not.
        - An active volume contains the currently running version of software.
      returned: changed
      type: bool
      sample: yes
    base_build:
      description:
        - Base build version of the software installed in the volume.
        - When a hotfix is installed, this refers to the base version of software
          that the hotfix requires.
      returned: changed
      type: string
      sample: 0.0.6
    build:
      description:
        - Build version of the software installed in the volume.
      returned: changed
      type: string
      sample: 0.0.6
    full_path:
      description:
        - Full name of the resource as known to BIG-IP.
      returned: changed
      type: string
      sample: HD1.1
    name:
      description:
        - Relative name of the resource in BIG-IP.
        - This usually matches the C(full_name).
      returned: changed
      type: string
      sample: HD1.1
    product:
      description:
        - The F5 product installed in this slot.
        - This should always be BIG-IP.
      returned: changed
      type: string
      sample: BIG-IP
    status:
      description:
        - Status of the software installed, or being installed, in the volume.
        - When C(complete), indicates that the software has completed installing.
      returned: changed
      type: string
      sample: complete
    version:
      description:
        - Version of software installed in the volume, excluding the C(build) number.
      returned: changed
      type: string
      sample: 13.1.0.4
  sample: hash/dictionary of values
ltm_pools:
  description: List of LTM (Local Traffic Manager) pools.
  returned: when C(ltm-pools) is specified in C(gather_subset).
  type: complex
  contains:
    allow_nat:
      description:
        - Whether NATs are automatically enabled or disabled for any connections using this pool.
      returned: changed
      type: bool
      sample: yes
    allow_snat:
      description:
        - Whether SNATs are automatically enabled or disabled for any connections using this pool.
      returned: changed
      type: bool
      sample: yes
    client_ip_tos:
      description:
        - Whether the system sets a Type of Service (ToS) level within a packet sent to the client,
          based on the targeted pool.
        - Values can range from C(0) to C(255), or be set to C(pass-through) or C(mimic).
      returned: changed
      type: string
      sample: pass-through
    client_link_qos:
      description:
        - Whether the system sets a Quality of Service (QoS) level within a packet sent to the client,
          based on the targeted pool.
        - Values can range from C(0) to C(7), or be set to C(pass-through).
      returned: changed
      type: string
      sample: pass-through
    description:
      description:
        - Description of the pool.
      returned: changed
      type: string
      sample: my pool
    full_path:
      description:
        - Full name of the resource as known to BIG-IP.
      returned: changed
      type: string
      sample: /Common/pool1
    ignore_persisted_weight:
      description:
        - Do not count the weight of persisted connections on pool members when making load balancing decisions.
      returned: changed
      type: bool
      sample: no
    lb_method:
      description:
        - Load balancing method used by the pool.
      returned: changed
      type: string
      sample: round-robin
    metadata:
      description:
        - Dictionary of arbitrary key/value pairs set on the pool.
      returned: changed
      type: complex
      sample: hash/dictionary of values
    minimum_active_members:
      description:
        - Whether the system load balances traffic according to the priority number assigned to the pool member.
        - This parameter is identical to C(priority_group_activation) and is just an alias for it.
      returned: changed
      type: int
      sample: 2
    minimum_up_members:
      description:
        - The minimum number of pool members that must be up.
      returned: changed
      type: int
      sample: 1
    minimum_up_members_action:
      description:
        - The action to take if the C(minimum_up_members_checking) is enabled and the number of active pool
          members falls below the number specified in C(minimum_up_members).
      returned: changed
      type: string
      sample: failover
    minimum_up_members_checking:
      description:
        - Enables or disables the C(minimum_up_members) feature.
      returned: changed
      type: bool
      sample: no
    name:
      description:
        - Relative name of the resource in BIG-IP.
      returned: changed
      type: string
      sample: pool1
    priority_group_activation:
      description:
        - Whether the system load balances traffic according to the priority number assigned to the pool member.
        - This parameter is identical to C(minimum_active_members) and is just an alias for it.
      returned: changed
      type: int
      sample: 2
    queue_depth_limit:
      description:
        - The maximum number of connections that may simultaneously be queued to go to any member of this pool.
      returned: changed
      type: int
      sample: 3
    queue_on_connection_limit:
      description:
        - Enable or disable queuing connections when pool member or node connection limits are reached.
      returned: changed
      type: bool
      sample: yes
    queue_time_limit:
      description:
        - Specifies the maximum time, in milliseconds, a connection will remain enqueued.
      returned: changed
      type: int
      sample: 0
    reselect_tries:
      description:
        - The number of times the system tries to contact a pool member after a passive failure.
      returned: changed
      type: int
      sample: 0
    server_ip_tos:
      description:
        - The Type of Service (ToS) level to use when sending packets to a server.
      returned: changed
      type: string
      sample: pass-through
    server_link_qos:
      description:
        - The Quality of Service (QoS) level to use when sending packets to a server.
      returned: changed
      type: string
      sample: pass-through
    service_down_action:
      description:
        - The action to take if the service specified in the pool is marked down.
      returned: changed
      type: string
      sample: none
    slow_ramp_time:
      description:
        - The ramp time for the pool.
        - This provides the ability to cause a pool member that has just been enabled,
          or marked up, to receive proportionally less traffic than other members in the pool.
      returned: changed
      type: int
      sample: 10
    members:
      description: List of LTM (Local Traffic Manager) pools.
      returned: when members exist in the pool.
      type: complex
      contains:
        address:
          description: IP address of the pool member.
          returned: changed
          type: string
          sample: 1.1.1.1
        connection_limit:
          description: The maximum number of concurrent connections allowed for a pool member.
          returned: changed
          type: int
          sample: 0
        description:
          description: The description of the pool member.
          returned: changed
          type: string
          sample: pool member 1
        dynamic_ratio:
          description:
            - A range of numbers that you want the system to use in conjunction with the ratio load balancing method.
          returned: changed
          type: int
          sample: 1
        ephemeral:
          description:
            - Whether the node backing the pool member is ephemeral or not.
          returned: changed
          type: bool
          sample: yes
        fqdn_autopopulate:
          description:
            - Whether the node should scale to the IP address set returned by DNS.
          returned: changed
          type: bool
          sample: yes
        full_path:
          description:
            - Full name of the resource as known to BIG-IP.
            - Includes the port in the name
          returned: changed
          type: string
          sample: "/Common/member:80"
        inherit_profile:
          description:
            - Whether the pool member inherits the encapsulation profile from the parent pool.
          returned: changed
          type: bool
          sample: no
        logging:
          description:
            - Whether the monitor applied should log its actions.
          returned: changed
          type: bool
          sample: no
        monitors:
          description:
            - Monitors active on the pool member. Monitor names are in their "full_path" form.
          returned: changed
          type: list
          sample: ['/Common/http']
        name:
          description:
            - Relative name of the resource in BIG-IP.
          returned: changed
          type: string
          sample: "member:80"
        partition:
          description:
            - Partition that the member exists on.
          returned: changed
          type: string
          sample: Common
        priority_group:
          description:
            - The priority group within the pool for this pool member.
          returned: changed
          type: int
          sample: 0
        encapsulation_profile:
          description:
            - The encapsulation profile to use for the pool member.
          returned: changed
          type: string
          sample: ip4ip4
        rate_limit:
          description:
            - The maximum number of connections per second allowed for a pool member.
          returned: changed
          type: bool
          sample: no
        ratio:
          description:
            - The weight of the pool for load balancing purposes.
          returned: changed
          type: int
          sample: 1
        session:
          description:
            - Enables or disables the pool member for new sessions.
          returned: changed
          type: string
          sample: monitor-enabled
        state:
          description:
            - Controls the state of the pool member, overriding any monitors.
          returned: changed
          type: string
          sample: down
  sample: hash/dictionary of values
nodes:
  description: Node related facts.
  returned: when C(nodes) is specified in C(gather_subset).
  type: complex
  contains:
    full_path:
      description:
        - Full name of the resource as known to BIG-IP.
      returned: changed
      type: string
      sample: /Common/5.6.7.8
    name:
      description:
        - Relative name of the resource in BIG-IP.
      returned: changed
      type: string
      sample: 5.6.7.8
    ratio:
      description:
        - Fixed size ratio used for node during C(Ratio) load balancing.
      returned: changed
      type: int
      sample: 10
    description:
      description:
        - Description of the node.
      returned: changed
      type: string
      sample: My node
    connection_limit:
      description:
        - Maximum number of connections that node can handle.
      returned: changed
      type: int
      sample: 100
    address:
      description:
        - IP address of the node.
      returned: changed
      type: string
      sample: 2.3.4.5
    dynamic_ratio:
      description:
        - Dynamic ratio number for the node used when doing C(Dynamic Ratio) load balancing.
      returned: changed
      type: int
      sample: 200
    rate_limit:
      description:
        - Maximum number of connections per second allowed for node.
      returned: changed
      type: int
      sample: 1000
    monitor_status:
      description:
        - Status of the node as reported by the monitor(s) associated with it.
        - This value is also used in determining node C(state).
      returned: changed
      type: string
      sample: down
    session_status:
      description:
        - This value is also used in determining node C(state).
      returned: changed
      type: string
      sample: enabled
    availability_status:
      description:
        - The availability of the node.
      returned: changed
      type: string
      sample: offline
    enabled_status:
      description:
        - The enabled-ness of the node.
      returned: changed
      type: string
      sample: enabled
    status_reason:
      description:
        - If there is a problem with the status of the node, that problem is reported here.
      returned: changed
      type: string
      sample: /Common/https_443 No successful responses received...
    monitor_rule:
      description:
        - A string representation of the full monitor rule.
      returned: changed
      type: string
      sample: /Common/https_443 and /Common/icmp
    monitors:
      description:
        - A list of the monitors identified in the C(monitor_rule).
      returned: changed
      type: list
      sample: ['/Common/https_443', '/Common/icmp']
    monitor_type:
      description:
        - The C(monitor_type) field related to the C(bigip_node) module, for this nodes
          monitors.
      returned: changed
      type: string
      sample: and_list
  sample: hash/dictionary of values
provision_info:
  description: Module provisioning related information.
  returned: when C(provision-info) is specified in C(gather_subset).
  type: complex
  contains:
    full_path:
      description:
        - Full name of the resource as known to BIG-IP.
      returned: changed
      type: string
      sample: asm
    name:
      description:
        - Relative name of the resource in BIG-IP.
      returned: changed
      type: string
      sample: asm
    cpu_ratio:
      description:
        - Ratio of CPU allocated to this module.
        - Only relevant if C(level) was specified as C(custom). Otherwise, this value
          will be reported as C(0).
      returned: changed
      type: int
      sample: 0
    disk_ratio:
      description:
        - Ratio of disk allocated to this module.
        - Only relevant if C(level) was specified as C(custom). Otherwise, this value
          will be reported as C(0).
      returned: changed
      type: int
      sample: 0
    memory_ratio:
      description:
        - Ratio of memory allocated to this module.
        - Only relevant if C(level) was specified as C(custom). Otherwise, this value
          will be reported as C(0).
      returned: changed
      type: int
      sample: 0
    level:
      description:
        - Provisioned level of the module on BIG-IP.
        - Valid return values can include C(none), C(minimum), C(nominal), C(dedicated)
          and C(custom).
      returned: changed
      type: int
      sample: 0
  sample: hash/dictionary of values
self_ips:
  description: Self-IP related facts.
  returned: when C(self-ips) is specified in C(gather_subset).
  type: complex
  contains:
    full_path:
      description:
        - Full name of the resource as known to BIG-IP.
      returned: changed
      type: string
      sample: /Common/self1
    name:
      description:
        - Relative name of the resource in BIG-IP.
      returned: changed
      type: string
      sample: self1
    description:
      description:
        - Description of the Self-IP.
      returned: changed
      type: string
      sample: My self-ip
    netmask:
      description:
        - Netmask portion of the IP address. In dotted notation.
      returned: changed
      type: string
      sample: 255.255.255.0
    netmask_cidr:
      description:
        - Netmask portion of the IP address. In CIDR notation.
      returned: changed
      type: int
      sample: 24
    floating:
      description:
        - Whether the Self-IP is a floating address or not.
      returned: changed
      type: bool
      sample: yes
    traffic_group:
      description:
        - Traffic group the Self-IP is associated with.
      returned: changed
      type: string
      sample: /Common/traffic-group-local-only
    service_policy:
      description:
        - Service policy assigned to the Self-IP.
      returned: changed
      type: string
      sample: /Common/service1
    vlan:
      description:
        - VLAN associated with the Self-IP.
      returned: changed
      type: string
      sample: /Common/vlan1
    allow_access_list:
      description:
        - List of protocols and optionally their ports that are allowed to access the
          Self-IP. Also known as port-lockdown in the web interface.
        - Items in the list are in the format of "protocol:port". Some items may not
          have a port associated with them and in those cases the port is C(0).
      returned: changed
      type: list
      sample: ['tcp:80', 'egp:0']
    traffic_group_inherited:
      description:
        - Whether or not the traffic group is inherited.
      returned: changed
      type: bool
      sample: no
  sample: hash/dictionary of values
trunks:
  description: Trunk related facts.
  returned: when C(trunks) is specified in C(gather_subset).
  type: complex
  contains:
    full_path:
      description:
        - Full name of the resource as known to BIG-IP.
      returned: changed
      type: string
      sample: /Common/trunk1
    name:
      description:
        - Relative name of the resource in BIG-IP.
      returned: changed
      type: string
      sample: trunk1
    description:
      description:
        - Description of the Trunk.
      returned: changed
      type: string
      sample: My trunk
    media_speed:
      description:
        - Speed of the media attached to the trunk.
      returned: changed
      type: int
      sample: 10000
    lacp_mode:
      description:
        - The operation mode for LACP.
      returned: changed
      type: string
      sample: passive
    lacp_enabled:
      description:
        - Whether LACP is enabled or not.
      returned: changed
      type: bool
      sample: yes
    stp_enabled:
      description:
        - Whether Spanning Tree Protocol (STP) is enabled or not.
      returned: changed
      type: bool
      sample: yes
    operational_member_count:
      description:
        - Number of working members associated with the trunk.
      returned: changed
      type: int
      sample: 1
    media_status:
      description:
        - Whether the media that is part of the trunk is up or not.
      returned: changed
      type: bool
      sample: yes
    link_selection_policy:
      description:
        - The LACP policy that the trunk uses to determine which member link can handle
          new traffic.
      returned: changed
      type: string
      sample: maximum-bandwidth
    lacp_timeout:
      description:
        - The rate at which the system sends the LACP control packets.
      returned: changed
      type: int
      sample: 10
    interfaces:
      description:
        - The list of interfaces that are part of the trunk.
      returned: changed
      type: list
      sample: ['1.2', '1.3']
    distribution_hash:
      description:
        - The basis for the has that the system uses as the frame distribution algorithm.
        - The system uses this hash to determine which interface to use for forwarding
          traffic.
      returned: changed
      type: string
      sample: src-dst-ipport
    configured_member_count:
      description:
        - The number of configured members that are associated with the trunk.
      returned: changed
      type: int
      sample: 1
'''

import datetime
import math
import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.network.common.utils import to_netmask
from ansible.module_utils.parsing.convert_bool import BOOLEANS_TRUE
from ansible.module_utils.parsing.convert_bool import BOOLEANS_FALSE
from ansible.module_utils.six import iteritems
from ansible.module_utils.six import string_types
from collections import namedtuple

try:
    from library.module_utils.network.f5.bigip import HAS_F5SDK
    from library.module_utils.network.f5.bigip import F5Client
    from library.module_utils.network.f5.bigip import F5RestClient
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import cleanup_tokens
    from library.module_utils.network.f5.common import f5_argument_spec
    from library.module_utils.network.f5.common import fq_name
    try:
        from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
        from f5.utils.responses.handlers import Stats
    except ImportError:
        HAS_F5SDK = False
except ImportError:
    from ansible.module_utils.network.f5.bigip import HAS_F5SDK
    from ansible.module_utils.network.f5.bigip import F5Client
    from ansible.module_utils.network.f5.bigip import F5RestClient
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import AnsibleF5Parameters
    from ansible.module_utils.network.f5.common import cleanup_tokens
    from ansible.module_utils.network.f5.common import f5_argument_spec
    from ansible.module_utils.network.f5.common import fq_name
    try:
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
        from f5.utils.responses.handlers import Stats
    except ImportError:
        HAS_F5SDK = False

try:
    import netaddr
    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False


def parseStats(entry):
    if 'description' in entry:
        return entry['description']
    elif 'value' in entry:
        return entry['value']
    elif 'entries' in entry or 'nestedStats' in entry and 'entries' in entry['nestedStats']:
        if 'entries' in entry:
            entries = entry['entries']
        else:
            entries = entry['nestedStats']['entries']
        result = None

        for name in entries:
            entry = entries[name]
            if 'https://localhost' in name:
                name = name.split('/')
                name = name[-1]
                if result and isinstance(result, list):
                    result.append(parseStats(entry))
                elif result and isinstance(result, dict):
                    result[name] = parseStats(entry)
                else:
                    try:
                        int(name)
                        result = list()
                        result.append(parseStats(entry))
                    except ValueError:
                        result = dict()
                        result[name] = parseStats(entry)
            else:
                if '.' in name:
                    names = name.split('.')
                    key = names[0]
                    value = names[1]
                    if not result[key]:
                        result[key] = {}
                    result[key][value] = parseStats(entry)
                else:
                    if result and isinstance(result, list):
                        result.append(parseStats(entry))
                    elif result and isinstance(result, dict):
                        result[name] = parseStats(entry)
                    else:
                        try:
                            int(name)
                            result = list()
                            result.append(parseStats(entry))
                        except ValueError:
                            result = dict()
                            result[name] = parseStats(entry)
        return result


class BaseManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = kwargs.get('client', None)
        self.kwargs = kwargs

    def read_stats_from_device(self, resource):
        stats = Stats(resource.stats.load())
        return stats.stat

    def exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        return results


class Parameters(AnsibleF5Parameters):
    @property
    def gather_subset(self):
        if isinstance(self._values['gather_subset'], string_types):
            self._values['gather_subset'] = [self._values['gather_subset']]
        elif not isinstance(self._values['gather_subset'], list):
            raise F5ModuleError(
                "The specified gather_subset must be a list."
            )
        self._values['gather_subset'].sort()
        return self._values['gather_subset']


class BaseParameters(Parameters):
    @property
    def enabled(self):
        if self._values['enabled'] is None:
            return None
        elif self._values['enabled'] in BOOLEANS_TRUE:
            return True
        else:
            return False

    @property
    def disabled(self):
        if self._values['disabled'] is None:
            return None
        elif self._values['disabled'] in BOOLEANS_TRUE:
            return True
        else:
            return False

    def flatten_boolean(self, key, resource):
        truthy = list(BOOLEANS_TRUE) + ['enabled']
        falsey = list(BOOLEANS_FALSE) + ['disabled']
        if resource[key] in truthy:
            resource[key] = 'yes'
        elif resource[key] in falsey:
            resource[key] = 'no'

    def _remove_internal_keywords(self, resource):
        resource.pop('kind', None)
        resource.pop('generation', None)
        resource.pop('selfLink', None)
        resource.pop('isSubcollection', None)
        resource.pop('fullPath', None)

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result


class ClientSslProfilesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'alertTimeout': 'alert_timeout',
        'allowNonSsl': 'allow_non_ssl',
        'authenticateDepth': 'authenticate_depth',
        'authenticate': 'authenticate_frequency',
        'caFile': 'ca_file',
        'cacheSize': 'cache_size',
        'cacheTimeout': 'cache_timeout',
        'cert': 'certificate_file',
        'chain': 'chain_file',
        'clientCertCa': 'client_certificate_ca_file',
        'crlFile': 'crl_file',
        'defaultsFrom': 'parent',
        'modSslMethods': 'modssl_methods',
        'peerCertMode': 'peer_certification_mode',
        'sniRequire': 'sni_require',
        'strictResume': 'strict_resume',
        'mode': 'profile_mode_enabled',
        'renegotiateMaxRecordDelay': 'renegotiation_maximum_record_delay',
        'renegotiatePeriod': 'renegotiation_period',
        'serverName': 'server_name',
        'sessionTicket': 'session_ticket',
        'sniDefault': 'sni_default',
        'uncleanShutdown': 'unclean_shutdown',
        'retainCertificate': 'retain_certificate',
        'secureRenegotiation': 'secure_renegotiation_mode',
        'handshakeTimeout': 'handshake_timeout',
        'certExtensionIncludes': 'forward_proxy_certificate_extension_include',
        'certLifespan': 'forward_proxy_certificate_lifespan',
        'certLookupByIpaddrPort': 'forward_proxy_lookup_by_ipaddr_port',
        'sslForwardProxy': 'forward_proxy_enabled',
        'proxyCaPassphrase': 'forward_proxy_ca_passphrase',
        'proxyCaCert': 'forward_proxy_ca_certificate_file',
        'proxyCaKey': 'forward_proxy_ca_key_file'
    }

    returnables = [
        'full_path',
        'name',
        'alert_timeout',
        'allow_non_ssl',
        'authenticate_depth',
        'authenticate_frequency',
        'ca_file',
        'cache_size',
        'cache_timeout',
        'certificate_file',
        'chain_file',
        'ciphers',
        'client_certificate_ca_file',
        'crl_file',
        'parent',
        'description',
        'modssl_methods',
        'peer_certification_mode',
        'sni_require',
        'sni_default',
        'strict_resume',
        'profile_mode_enabled',
        'renegotiation_maximum_record_delay',
        'renegotiation_period',
        'renegotiation',
        'server_name',
        'session_ticket',
        'unclean_shutdown',
        'retain_certificate',
        'secure_renegotiation_mode',
        'handshake_timeout',
        'forward_proxy_certificate_extension_include',
        'forward_proxy_certificate_lifespan',
        'forward_proxy_lookup_by_ipaddr_port',
        'forward_proxy_enabled',
        'forward_proxy_ca_passphrase',
        'forward_proxy_ca_certificate_file',
        'forward_proxy_ca_key_file'
    ]

    @property
    def alert_timeout(self):
        if self._values['alert_timeout'] is None:
            return None
        if self._values['alert_timeout'] == 'indefinite':
            return 0
        return int(self._values['alert_timeout'])

    @property
    def renegotiation_maximum_record_delay(self):
        if self._values['renegotiation_maximum_record_delay'] is None:
            return None
        if self._values['renegotiation_maximum_record_delay'] == 'indefinite':
            return 0
        return int(self._values['renegotiation_maximum_record_delay'])

    @property
    def renegotiation_period(self):
        if self._values['renegotiation_period'] is None:
            return None
        if self._values['renegotiation_period'] == 'indefinite':
            return 0
        return int(self._values['renegotiation_period'])

    @property
    def handshake_timeout(self):
        if self._values['handshake_timeout'] is None:
            return None
        if self._values['handshake_timeout'] == 'indefinite':
            return 0
        return int(self._values['handshake_timeout'])

    @property
    def allow_non_ssl(self):
        if self._values['allow_non_ssl'] is None:
            return None
        if self._values['allow_non_ssl'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def forward_proxy_enabled(self):
        if self._values['forward_proxy_enabled'] is None:
            return None
        if self._values['forward_proxy_enabled'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def renegotiation(self):
        if self._values['renegotiation'] is None:
            return None
        if self._values['renegotiation'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def forward_proxy_lookup_by_ipaddr_port(self):
        if self._values['forward_proxy_lookup_by_ipaddr_port'] is None:
            return None
        if self._values['forward_proxy_lookup_by_ipaddr_port'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def unclean_shutdown(self):
        if self._values['unclean_shutdown'] is None:
            return None
        if self._values['unclean_shutdown'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def session_ticket(self):
        if self._values['session_ticket'] is None:
            return None
        if self._values['session_ticket'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def retain_certificate(self):
        if self._values['retain_certificate'] is None:
            return None
        if self._values['retain_certificate'] == 'true':
            return 'yes'
        return 'no'

    @property
    def server_name(self):
        if self._values['server_name'] in [None, 'none']:
            return None
        return self._values['server_name']

    @property
    def forward_proxy_ca_certificate_file(self):
        if self._values['forward_proxy_ca_certificate_file'] in [None, 'none']:
            return None
        return self._values['forward_proxy_ca_certificate_file']

    @property
    def forward_proxy_ca_key_file(self):
        if self._values['forward_proxy_ca_key_file'] in [None, 'none']:
            return None
        return self._values['forward_proxy_ca_key_file']

    @property
    def authenticate_frequency(self):
        if self._values['authenticate_frequency'] is None:
            return None
        return self._values['authenticate_frequency']

    @property
    def ca_file(self):
        if self._values['ca_file'] is [None, 'none']:
            return None
        return self._values['ca_file']

    @property
    def certificate_file(self):
        if self._values['certificate_file'] is [None, 'none']:
            return None
        return self._values['certificate_file']

    @property
    def chain_file(self):
        if self._values['chain_file'] is [None, 'none']:
            return None
        return self._values['chain_file']

    @property
    def client_certificate_ca_file(self):
        if self._values['client_certificate_ca_file'] is [None, 'none']:
            return None
        return self._values['client_certificate_ca_file']

    @property
    def crl_file(self):
        if self._values['crl_file'] is [None, 'none']:
            return None
        return self._values['crl_file']

    @property
    def ciphers(self):
        if self._values['ciphers'] is [None, 'none']:
            return None
        return self._values['ciphers'].split(' ')

    @property
    def modssl_methods(self):
        if self._values['modssl_methods'] is None:
            return None
        if self._values['modssl_methods'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def strict_resume(self):
        if self._values['strict_resume'] is None:
            return None
        if self._values['strict_resume'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def profile_mode_enabled(self):
        if self._values['profile_mode_enabled'] is None:
            return None
        if self._values['profile_mode_enabled'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def sni_require(self):
        if self._values['sni_require'] is None:
            return None
        if self._values['sni_require'] == 'false':
            return 'no'
        return 'yes'

    @property
    def sni_default(self):
        if self._values['sni_default'] is None:
            return None
        if self._values['sni_default'] == 'false':
            return 'no'
        return 'yes'


class ClientSslProfilesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(ClientSslProfilesFactManager, self).__init__(**kwargs)
        self.want = ClientSslProfilesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(client_ssl_profiles=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = ClientSslProfilesParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.ltm.profile.client_ssls.get_collection()
        return result


class DeviceGroupsParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'autoSync': 'autosync_enabled',
        'asmSync': 'asm_sync_enabled',
        'devicesReference': 'devices',
        'fullLoadOnSync': 'full_load_on_sync',
        'incrementalConfigSyncSizeMax': 'incremental_config_sync_size_maximum',
        'networkFailover': 'network_failover_enabled'
    }

    returnables = [
        'full_path',
        'name',
        'autosync_enabled',
        'description',
        'devices',
        'full_load_on_sync',
        'incremental_config_sync_size_maximum',
        'network_failover_enabled',
        'type',
        'asm_sync_enabled'
    ]

    @property
    def network_failover_enabled(self):
        if self._values['network_failover_enabled'] is None:
            return None
        if self._values['network_failover_enabled'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def asm_sync_enabled(self):
        if self._values['asm_sync_enabled'] is None:
            return None
        if self._values['asm_sync_enabled'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def autosync_enabled(self):
        if self._values['autosync_enabled'] is None:
            return None
        if self._values['autosync_enabled'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def full_load_on_sync(self):
        if self._values['full_load_on_sync'] is None:
            return None
        if self._values['full_load_on_sync'] == 'true':
            return 'yes'
        return 'no'

    @property
    def devices(self):
        if self._values['devices'] is None or 'items' not in self._values['devices']:
            return None
        result = [x['fullPath'] for x in self._values['devices']['items']]
        result.sort()
        return result


class DeviceGroupsFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(DeviceGroupsFactManager, self).__init__(**kwargs)
        self.want = DeviceGroupsParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(device_groups=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = DeviceGroupsParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.cm.device_groups.get_collection(
            requests_params=dict(
                params='expandSubcollections=true'
            )
        )
        return result


class DevicesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'activeModules': 'active_modules',
        'baseMac': 'base_mac_address',
        'chassisId': 'chassis_id',
        'chassisType': 'chassis_type',
        'configsyncIp': 'configsync_address',
        'failoverState': 'failover_state',
        'managementIp': 'management_address',
        'marketingName': 'marketing_name',
        'multicastIp': 'multicast_address',
        'optionalModules': 'optional_modules',
        'platformId': 'platform_id',
        'mirrorIp': 'primary_mirror_address',
        'mirrorSecondaryIp': 'secondary_mirror_address',
        'version': 'software_version',
        'timeLimitedModules': 'timelimited_modules',
        'timeZone': 'timezone',
        'unicastAddress': 'unicast_addresses'
    }

    returnables = [
        'full_path',
        'name',
        'active_modules',
        'base_mac_address',
        'build',
        'chassis_id',
        'chassis_type',
        'comment',
        'configsync_address',
        'contact',
        'description',
        'edition',
        'failover_state',
        'hostname',
        'location',
        'management_address',
        'marketing_name',
        'multicast_address',
        'optional_modules',
        'platform_id',
        'primary_mirror_address',
        'product',
        'secondary_mirror_address',
        'software_version',
        'timelimited_modules',
        'timezone',
        'unicast_addresses'
    ]

    @property
    def active_modules(self):
        if self._values['active_modules'] is None:
            return None
        result = {}
        for x in self._values['active_modules']:
            parts = x.split('|')
            name = parts[0]
            result[name] = parts[2:]
        return result

    @property
    def configsync_address(self):
        if self._values['configsync_address'] in [None, 'none']:
            return None
        return self._values['configsync_address']

    @property
    def primary_mirror_address(self):
        if self._values['primary_mirror_address'] in [None, 'any6']:
            return None
        return self._values['primary_mirror_address']

    @property
    def secondary_mirror_address(self):
        if self._values['secondary_mirror_address'] in [None, 'any6']:
            return None
        return self._values['secondary_mirror_address']

    @property
    def unicast_addresses(self):
        if self._values['unicast_addresses'] is None:
            return None
        result = []

        for addr in self._values['unicast_addresses']:
            tmp = {}
            for key in ['effectiveIp', 'effectivePort', 'ip', 'port']:
                if key in addr:
                    renamed_key = self.convert(key)
                    tmp[renamed_key] = addr.get(key, None)
            if tmp:
                result.append(tmp)
        if result:
            return result

    def convert(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class DevicesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(DevicesFactManager, self).__init__(**kwargs)
        self.want = DevicesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(devices=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = DevicesParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.cm.devices.get_collection()
        return result


class InterfacesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'mediaActive': 'active_media_type',
        'flowControl': 'flow_control',
        'bundleSpeed': 'bundle_speed',
        'ifIndex': 'if_index',
        'macAddress': 'mac_address',
        'mediaSfp': 'media_sfp',
        'lldpTlvmap': 'lldp_tlvmap',
        'lldpAdmin': 'lldp_admin',
        'preferPort': 'prefer_port',
        'stpAutoEdgePort': 'stp_auto_edge_port',
        'stp': 'stp_enabled',
        'stpLinkType': 'stp_link_type'
    }

    returnables = [
        'full_path',
        'name',
        'active_media_type',
        'flow_control',
        'description',
        'bundle',
        'bundle_speed',
        'enabled',
        'if_index',
        'mac_address',
        'media_sfp',
        'lldp_tlvmap',
        'lldp_admin',
        'mtu',
        'prefer_port',
        'sflow_poll_interval',
        'sflow_poll_interval_global',
        'stp_auto_edge_port',
        'stp_enabled',
        'stp_link_type'
    ]

    @property
    def stp_enabled(self):
        if self._values['stp_enabled'] is None:
            return None
        elif self._values['stp_enabled'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def sflow_poll_interval_global(self):
        if self._values['sflow'] is None:
            return None
        if 'pollIntervalGlobal' in self._values['sflow']:
            return self._values['sflow']['pollIntervalGlobal']

    @property
    def sflow_poll_interval(self):
        if self._values['sflow'] is None:
            return None
        if 'pollInterval' in self._values['sflow']:
            return self._values['sflow']['pollInterval']

    @property
    def mac_address(self):
        if self._values['mac_address'] in [None, 'none']:
            return None
        return self._values['mac_address']

    @property
    def enabled(self):
        if self._values['enabled'] is None:
            return None
        elif self._values['enabled'] is True:
            return 'yes'
        return 'no'


class InterfacesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(InterfacesFactManager, self).__init__(**kwargs)
        self.want = InterfacesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(interfaces=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = InterfacesParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.net.interfaces.get_collection()
        return result


class InternalDataGroupsParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path'
    }

    returnables = [
        'full_path',
        'name',
        'type',
        'records'
    ]


class InternalDataGroupsFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(InternalDataGroupsFactManager, self).__init__(**kwargs)
        self.want = InternalDataGroupsParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(internal_data_groups=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = InternalDataGroupsParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.ltm.data_group.internals.get_collection()
        return result


class IrulesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'ignoreVerification': 'ignore_verification',
    }

    returnables = [
        'full_path',
        'name',
        'ignore_verification',
        'checksum',
        'definition',
        'signature'
    ]

    @property
    def checksum(self):
        if self._values['apiAnonymous'] is None:
            return None
        pattern = r'definition-checksum\s(?P<checksum>\w+)'
        matches = re.search(pattern, self._values['apiAnonymous'])
        if matches:
            return matches.group('checksum')

    @property
    def definition(self):
        if self._values['apiAnonymous'] is None:
            return None
        pattern = r'(definition-(checksum|signature)\s[\w=\/+]+)'
        result = re.sub(pattern, '', self._values['apiAnonymous']).strip()
        if result:
            return result

    @property
    def signature(self):
        if self._values['apiAnonymous'] is None:
            return None
        pattern = r'definition-signature\s(?P<signature>[\w=\/+]+)'
        matches = re.search(pattern, self._values['apiAnonymous'])
        if matches:
            return matches.group('signature')

    @property
    def ignore_verification(self):
        if self._values['ignore_verification'] is None:
            return 'no'
        return 'yes'


class IrulesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(IrulesFactManager, self).__init__(**kwargs)
        self.want = IrulesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(irules=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = IrulesParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.ltm.rules.get_collection()
        return result


class LtmPoolsParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'allowNat': 'allow_nat',
        'allowSnat': 'allow_snat',
        'ignorePersistedWeight': 'ignore_persisted_weight',
        'ipTosToClient': 'client_ip_tos',
        'ipTosToServer': 'server_ip_tos',
        'linkQosToClient': 'client_link_qos',
        'linkQosToServer': 'server_link_qos',
        'loadBalancingMode': 'lb_method',
        'minActiveMembers': 'minimum_active_members',
        'minUpMembers': 'minimum_up_members',
        'minUpMembersAction': 'minimum_up_members_action',
        'minUpMembersChecking': 'minimum_up_members_checking',
        'queueDepthLimit': 'queue_depth_limit',
        'queueOnConnectionLimit': 'queue_on_connection_limit',
        'queueTimeLimit': 'queue_time_limit',
        'reselectTries': 'reselect_tries',
        'serviceDownAction': 'service_down_action',
        'slowRampTime': 'slow_ramp_time',
        'monitor': 'monitors',
    }

    returnables = [
        'full_path',
        'name',
        'allow_nat',
        'allow_snat',
        'description',
        'ignore_persisted_weight',
        'client_ip_tos',
        'server_ip_tos',
        'client_link_qos',
        'server_link_qos',
        'lb_method',
        'minimum_active_members',
        'minimum_up_members',
        'minimum_up_members_action',
        'minimum_up_members_checking',
        'monitors',
        'queue_depth_limit',
        'queue_on_connection_limit',
        'queue_time_limit',
        'reselect_tries',
        'service_down_action',
        'slow_ramp_time',
        'priority_group_activation',
        'members',
        'metadata'
    ]

    @property
    def ignore_persisted_weight(self):
        self.flatten_boolean('ignore_persisted_weight', self._values)
        return self._values['ignore_persisted_weight']

    @property
    def minimum_up_members_checking(self):
        self.flatten_boolean('minimum_up_members_checking', self._values)
        return self._values['minimum_up_members_checking']

    @property
    def queue_on_connection_limit(self):
        self.flatten_boolean('queue_on_connection_limit', self._values)
        return self._values['queue_on_connection_limit']

    @property
    def priority_group_activation(self):
        """Returns the TMUI value for "Priority Group Activation"

        This value is identified as ``minActiveMembers`` in the REST API, so this
        is just a convenience key for users of Ansible (where the ``bigip_virtual_server``
        parameter is called ``priority_group_activation``.

        Returns:
            int: Priority number assigned to the pool members.
        """
        return self._values['minimum_active_members']

    @property
    def metadata(self):
        """Returns metadata associated with a pool

        An arbitrary amount of metadata may be associated with a pool. You typically
        see this used in situations where the user wants to annotate a resource, maybe
        in cases where an automation system is responsible for creating the resource.

        The metadata in the API is always stored as a list of dictionaries. We change
        this to be a simple dictionary before it is returned to the user.

        Returns:
            dict: A dictionary of key/value pairs where the key is the metadata name
                  and the value is the metadata value.
        """
        if self._values['metadata'] is None:
            return None
        result = dict([(k['name'], k['value']) for k in self._values['metadata']])
        return result

    @property
    def members(self):
        if not self._values['members']:
            return None
        result = []
        for member in self._values['members']:
            member['connection_limit'] = member.pop('connectionLimit', None)
            member['dynamic_ratio'] = member.pop('dynamicRatio', None)
            member['full_path'] = member.pop('fullPath', None)
            member['inherit_profile'] = member.pop('inheritProfile', None)
            member['priority_group'] = member.pop('priorityGroup', None)
            member['rate_limit'] = member.pop('rateLimit', None)

            if 'fqdn' in member and 'autopopulate' in member['fqdn']:
                if member['fqdn']['autopopulate'] == 'enabled':
                    member['fqdn_autopopulate'] = 'yes'
                elif member['fqdn']['autopopulate'] == 'disabled':
                    member['fqdn_autopopulate'] = 'no'
                del member['fqdn']

            for key in ['ephemeral', 'inherit_profile', 'logging', 'rate_limit']:
                self.flatten_boolean(key, member)

            if 'profiles' in member:
                # Even though the ``profiles`` is a list, there is only ever 1
                member['encapsulation_profile'] = [x['name'] for x in member['profiles']][0]
                del member['profiles']

            if 'monitor' in member:
                monitors = member.pop('monitor')
                if monitors is not None:
                    try:
                        member['monitors'] = re.findall(r'/[\w-]+/[^\s}]+', monitors)
                    except Exception:
                        member['monitors'] = [monitors.strip()]

            session = member.pop('session')
            state = member.pop('state')

            if state in ['user-up', 'unchecked', 'fqdn-up-no-addr'] and session in ['user-enabled']:
                member['state'] = 'present'
            elif state in ['user-down'] and session in ['user-disabled']:
                member['state'] = 'forced_offline'
            elif state in ['down'] and session in ['monitor-enabled']:
                member['state'] = 'offline'
            else:
                member['state'] = 'disabled'
            self._remove_internal_keywords(member)
            member = dict([(k, v) for k, v in iteritems(member) if v is not None])
            result.append(member)
        return result

    @property
    def monitors(self):
        if self._values['monitors'] is None:
            return None
        try:
            result = re.findall(r'/[\w-]+/[^\s}]+', self._values['monitors'])
            return result
        except Exception:
            return [self._values['monitors'].strip()]


class LtmPoolsFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(LtmPoolsFactManager, self).__init__(**kwargs)
        self.want = LtmPoolsParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(ltm_pools=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            attrs = resource.attrs
            members = resource.members_s.get_collection()
            attrs['members'] = [member.attrs for member in members]
            params = LtmPoolsParameters(params=attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        """Read the LTM pools collection from the device

        Note that sub-collection expansion does not work with LTM pools. Therefore,
        one needs to query the ``members`` endpoint separately and add that to the
        list of ``attrs`` before the full set of attributes is sent to the ``Parameters``
        class.

        Returns:
             list: List of ``Pool`` objects
        """
        result = self.client.api.tm.ltm.pools.get_collection()
        return result


class NodesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'connectionLimit': 'connection_limit',
        'dynamicRatio': 'dynamic_ratio',
        'rateLimit': 'rate_limit',
        'monitor': 'monitors'
    }

    returnables = [
        'full_path',
        'name',
        'ratio',
        'description',
        'connection_limit',
        'address',
        'dynamic_ratio',
        'rate_limit',
        'monitor_status',
        'session_status',
        'availability_status',
        'enabled_status',
        'status_reason',
        'monitor_rule',
        'monitors',
        'monitor_type'
    ]

    @property
    def monitors(self):
        if self._values['monitors'] is None:
            return []
        try:
            result = re.findall(r'/\w+/[^\s}]+', self._values['monitors'])
            return result
        except Exception:
            return [self._values['monitors']]

    @property
    def monitor_type(self):
        if self._values['monitors'] is None:
            return None
        pattern = r'min\s+\d+\s+of'
        matches = re.search(pattern, self._values['monitors'])
        if matches:
            return 'm_of_n'
        else:
            return 'and_list'

    @property
    def rate_limit(self):
        if self._values['rate_limit'] is None:
            return None
        elif self._values['rate_limit'] == 'disabled':
            return 0
        else:
            return int(self._values['rate_limit'])

    @property
    def monitor_status(self):
        return self._values['stats']['monitorStatus']['description']

    @property
    def session_status(self):
        return self._values['stats']['sessionStatus']['description']

    @property
    def availability_status(self):
        return self._values['stats']['status_availabilityState']['description']

    @property
    def enabled_status(self):
        return self._values['stats']['status_enabledState']['description']

    @property
    def status_reason(self):
        return self._values['stats']['status_statusReason']['description']

    @property
    def monitor_rule(self):
        return self._values['stats']['monitorRule']['description']


class NodesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(NodesFactManager, self).__init__(**kwargs)
        self.want = NodesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(nodes=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            attrs = resource.attrs
            attrs['stats'] = Stats(resource.stats.load()).stat
            params = NodesParameters(params=attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.ltm.nodes.get_collection()
        return result


class ProvisionInfoParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'cpuRatio': 'cpu_ratio',
        'diskRatio': 'disk_ratio',
        'memoryRatio': 'memory_ratio',
    }

    returnables = [
        'full_path',
        'name',
        'cpu_ratio',
        'disk_ratio',
        'memory_ratio',
        'level'
    ]


class ProvisionInfoFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(ProvisionInfoFactManager, self).__init__(**kwargs)
        self.want = ProvisionInfoParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(provision_info=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = ProvisionInfoParameters(params=resource)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.sys.provision.get_collection()
        return result


class SelfIpsParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'trafficGroup': 'traffic_group',
        'servicePolicy': 'service_policy',
        'allowService': 'allow_access_list',
        'inheritedTrafficGroup': 'traffic_group_inherited'
    }

    returnables = [
        'full_path',
        'name',
        'address',
        'description',
        'netmask',
        'netmask_cidr',
        'floating',
        'traffic_group',
        'service_policy',
        'vlan',
        'allow_access_list',
        'traffic_group_inherited'
    ]

    @property
    def address(self):
        parts = self._values['address'].split('/')
        return parts[0]

    @property
    def netmask(self):
        parts = self._values['address'].split('/')
        return to_netmask(parts[1])

    @property
    def netmask_cidr(self):
        parts = self._values['address'].split('/')
        return int(parts[1])

    @property
    def traffic_group_inherited(self):
        if self._values['traffic_group_inherited'] is None:
            return None
        elif self._values['traffic_group_inherited'] in [False, 'false']:
            # BIG-IP appears to store this as a string. This is a bug, so we handle both
            # cases here.
            return 'no'
        else:
            return 'yes'

    @property
    def floating(self):
        if self._values['floating'] is None:
            return None
        elif self._values['floating'] == 'disabled':
            return 'no'
        else:
            return 'yes'


class SelfIpsFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(SelfIpsFactManager, self).__init__(**kwargs)
        self.want = SelfIpsParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(self_ips=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = SelfIpsParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.net.selfips.get_collection()
        return result


class SoftwareVolumesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'basebuild': 'base_build',
    }

    returnables = [
        'full_path',
        'name',
        'active',
        'base_build',
        'build',
        'product',
        'status',
        'version',
        'install_volume',
    ]

    @property
    def install_volume(self):
        if self._values['media'] is None:
            return None
        return self._values['media'].get('name', None)

    @property
    def active(self):
        if self._values['active'] is True:
            return 'yes'
        return 'no'


class SoftwareVolumesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(SoftwareVolumesFactManager, self).__init__(**kwargs)
        self.want = SoftwareVolumesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(software_volumes=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = SoftwareVolumesParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.sys.software.volumes.get_collection()
        return result


class SslCertificatesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'keyType': 'key_type',
        'certificateKeySize': 'key_size',
        'systemPath': 'system_path',
        'checksum': 'sha1_checksum',
        'lastUpdateTime': 'last_update_time',
        'isBundle': 'is_bundle',
        'expirationString': 'expiration_date',
        'expirationDate': 'expiration_timestamp',
        'createTime': 'create_time'
    }

    returnables = [
        'full_path',
        'name',
        'key_type',
        'key_size',
        'system_path',
        'sha1_checksum',
        'subject',
        'last_update_time',
        'issuer',
        'is_bundle',
        'fingerprint',
        'expiration_date',
        'expiration_timestamp',
        'create_time',
    ]

    @property
    def sha1_checksum(self):
        if self._values['sha1_checksum'] is None:
            return None
        parts = self._values['sha1_checksum'].split(':')
        return parts[2]

    @property
    def is_bundle(self):
        if self._values['sha1_checksum'] is None:
            return None
        if self._values['is_bundle'] in BOOLEANS_TRUE:
            return 'yes'
        return 'no'


class SslCertificatesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(SslCertificatesFactManager, self).__init__(**kwargs)
        self.want = SslCertificatesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(ssl_certs=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = SslCertificatesParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.sys.file.ssl_certs.get_collection()
        return result


class SslKeysParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'keyType': 'key_type',
        'keySize': 'key_size',
        'securityType': 'security_type',
        'systemPath': 'system_path',
        'checksum': 'sha1_checksum'
    }

    returnables = [
        'full_path',
        'name',
        'key_type',
        'key_size',
        'security_type',
        'system_path',
        'sha1_checksum'
    ]

    @property
    def sha1_checksum(self):
        if self._values['sha1_checksum'] is None:
            return None
        parts = self._values['sha1_checksum'].split(':')
        return parts[2]


class SslKeysFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(SslKeysFactManager, self).__init__(**kwargs)
        self.want = SslKeysParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(ssl_keys=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = SslKeysParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.sys.file.ssl_keys.get_collection()
        return result


class SystemInfoParameters(BaseParameters):
    api_map = {

    }

    returnables = [
        'base_mac_address',
        'marketing_name',
        'time',
        'hardware_information',
        'product_information',
        'package_edition',
        'package_version',
        'product_code',
        'product_version',
        'system_information',
        'uptime'
    ]

    @property
    def product_information(self):
        """Return product information

        This is maintained here for legacy purposes.

        Returns a dictionary of product related information where the keys in
        the dictionary are mapped to the stats returned from the /mgmt/tm/sys/version
        API.

        Note that the list of product features, previously reported by the SOAP API
        is no longer available in the REST API and has been removed from this module.

        Returns:
            A dict of product information such as the version and code.
        """
        result = dict(
            package_edition=self._values['Edition'],
            package_version='Build {0} - {1}'.format(
                self._values['Build'], self._values['Date']
            ),
            product_code=self._values['Product'],
            product_version=self._values['Version'],
        )

        if 'version_info' not in self._values:
            return result
        if 'Built' in self._values['version_info']:
            result['product_built'] = int(self._values['version_info']['Built'])
        if 'Changelist' in self._values['version_info']:
            result['product_changelist'] = int(self._values['version_info']['Changelist'])
        if 'JobID' in self._values['version_info']:
            result['product_jobid'] = int(self._values['version_info']['JobID'])
        return result

    @property
    def system_information(self):
        """Return system information

        This is maintained here for legacy purposes.

        Returns a dictionary of product related information where the keys in
        the dictionary are mapped to the stats returned from the /mgmt/tm/sys/hardware
        API.

        Returns:
            A dict of system information such as the version and code.
        """
        if self._values['system-info'] is None:
            return None

        result = dict(
            chassis_serial=self._values['system-info'][0]['bigipChassisSerialNum'],
            host_board_part_revision=self._values['system-info'][0]['hostBoardPartRevNum'],
            host_board_serial=self._values['system-info'][0]['hostBoardSerialNum'],
            platform=self._values['system-info'][0]['platform'],
            switch_board_part_revision=self._values['system-info'][0]['switchBoardPartRevNum'],
            switch_board_serial=self._values['system-info'][0]['switchBoardSerialNum'],
        )
        return result

    @property
    def package_edition(self):
        return self._values['Edition']

    @property
    def package_version(self):
        return 'Build {0} - {1}'.format(self._values['Build'], self._values['Date'])

    @property
    def product_code(self):
        return self._values['Product']

    @property
    def product_version(self):
        return self._values['Version']

    @property
    def hardware_information(self):
        if self._values['hardware-version'] is None:
            return None
        self._transform_name_attribute(self._values['hardware-version'])
        result = [v for k, v in iteritems(self._values['hardware-version'])]
        return result

    def _transform_name_attribute(self, entry):
        if isinstance(entry, dict):
            for k, v in iteritems(entry):
                if k == 'tmName':
                    entry['name'] = entry.pop('tmName')
                self._transform_name_attribute(v)
        elif isinstance(entry, list):
            for k in entry:
                if k == 'tmName':
                    entry['name'] = entry.pop('tmName')
                self._transform_name_attribute(k)
        else:
            return

    @property
    def time(self):
        if self._values['fullDate'] is None:
            return None
        date = datetime.datetime.strptime(self._values['fullDate'], "%Y-%m-%dT%H:%M:%SZ")
        result = dict(
            day=date.day,
            hour=date.hour,
            minute=date.minute,
            month=date.month,
            second=date.second,
            year=date.year
        )
        return result

    @property
    def marketing_name(self):
        if self._values['platform'] is None:
            return None
        return self._values['platform'][0]['marketingName']

    @property
    def base_mac_address(self):
        if self._values['platform'] is None:
            return None
        return self._values['platform'][0]['baseMac']


class SystemInfoFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(SystemInfoFactManager, self).__init__(**kwargs)
        self.want = SystemInfoParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(system_info=facts)
        return result

    def _exec_module(self):
        facts = self.read_facts()
        results = facts.to_return()
        return results

    def read_facts(self):
        collection = self.read_collection_from_device()
        params = SystemInfoParameters(params=collection)
        return params

    def read_collection_from_device(self):
        result = dict()
        tmp = self.read_hardware_info_from_device()
        if tmp:
            result.update(tmp)

        tmp = self.read_clock_info_from_device()
        if tmp:
            result.update(tmp)

        tmp = self.read_version_info_from_device()
        if tmp:
            result.update(tmp)

        tmp = self.read_uptime_info_from_device()
        if tmp:
            result.update(tmp)

        tmp = self.read_version_file_info_from_device()
        if tmp:
            result.update(tmp)

        return result

    def read_version_file_info_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/util/bash".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        args = dict(
            command='run',
            utilCmdArgs='-c "cat /VERSION"'
        )
        resp = self.client.api.post(uri, json=args)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        try:
            pattern = r'^(?P<key>(Product|Build|Sequence|BaseBuild|Edition|Date|Built|Changelist|JobID))\:(?P<value>.*)'
            result = response['commandResult'].strip()
        except KeyError:
            return None

        if 'No such file or directory' in result:
            return None

        lines = response['commandResult'].split("\n")
        result = dict()
        for line in lines:
            if not line:
                continue
            matches = re.match(pattern, line)
            if matches:
                result[matches.group('key')] = matches.group('value').strip()

        if result:
            return dict(
                version_info=result
            )

    def read_uptime_info_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/util/bash".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        args = dict(
            command='run',
            utilCmdArgs='-c "cat /proc/uptime"'
        )
        resp = self.client.api.post(uri, json=args)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        try:
            parts = response['commandResult'].strip().split(' ')
            return dict(
                uptime=math.floor(float(parts[0]))
            )
        except KeyError:
            pass

    def read_hardware_info_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/sys/hardware".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        result = parseStats(response)
        return result

    def read_clock_info_from_device(self):
        """Parses clock info from the REST API

        The clock stat returned from the REST API (at the time of 13.1.0.7)
        is similar to the following.

        {
            "kind": "tm:sys:clock:clockstats",
            "selfLink": "https://localhost/mgmt/tm/sys/clock?ver=13.1.0.4",
            "entries": {
                "https://localhost/mgmt/tm/sys/clock/0": {
                    "nestedStats": {
                        "entries": {
                            "fullDate": {
                                "description": "2018-06-05T13:38:33Z"
                            }
                        }
                    }
                }
            }
        }

        Parsing this data using the ``parseStats`` method, yields a list of
        the clock stats in a format resembling that below.

        [{'fullDate': '2018-06-05T13:41:05Z'}]

        Therefore, this method cherry-picks the first entry from this list
        and returns it. There can be no other items in this list.

        Returns:
            A dict mapping keys to the corresponding clock stats. For
            example:

            {'fullDate': '2018-06-05T13:41:05Z'}

            There should never not be a clock stat, unless by chance it
            is removed from the API in the future, or changed to a different
            API endpoint.

        Raises:
            F5ModuleError: A non-successful HTTP code was returned or a JSON
                           response was not found.
        """
        uri = "https://{0}:{1}/mgmt/tm/sys/clock".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        result = parseStats(response)
        return result[0]

    def read_version_info_from_device(self):
        """Parses version info from the REST API

        The version stat returned from the REST API (at the time of 13.1.0.7)
        is similar to the following.

        {
            "kind": "tm:sys:version:versionstats",
            "selfLink": "https://localhost/mgmt/tm/sys/version?ver=13.1.0.4",
            "entries": {
                "https://localhost/mgmt/tm/sys/version/0": {
                    "nestedStats": {
                        "entries": {
                            "Build": {
                                "description": "0.0.6"
                            },
                            "Date": {
                                "description": "Tue Mar 13 20:10:42 PDT 2018"
                            },
                            "Edition": {
                                "description": "Point Release 4"
                            },
                            "Product": {
                                "description": "BIG-IP"
                            },
                            "Title": {
                                "description": "Main Package"
                            },
                            "Version": {
                                "description": "13.1.0.4"
                            }
                        }
                    }
                }
            }
        }

        Parsing this data using the ``parseStats`` method, yields a list of
        the clock stats in a format resembling that below.

        [{'Build': '0.0.6', 'Date': 'Tue Mar 13 20:10:42 PDT 2018',
          'Edition': 'Point Release 4', 'Product': 'BIG-IP', 'Title': 'Main Package',
          'Version': '13.1.0.4'}]

        Therefore, this method cherry-picks the first entry from this list
        and returns it. There can be no other items in this list.

        Returns:
            A dict mapping keys to the corresponding clock stats. For
            example:

            {'Build': '0.0.6', 'Date': 'Tue Mar 13 20:10:42 PDT 2018',
             'Edition': 'Point Release 4', 'Product': 'BIG-IP', 'Title': 'Main Package',
             'Version': '13.1.0.4'}

            There should never not be a version stat, unless by chance it
            is removed from the API in the future, or changed to a different
            API endpoint.

        Raises:
            F5ModuleError: A non-successful HTTP code was returned or a JSON
                           response was not found.
        """
        uri = "https://{0}:{1}/mgmt/tm/sys/version".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if 'code' in response and response['code'] == 400:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)
        result = parseStats(response)
        return result[0]


class TrafficGroupsParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'autoFailbackEnabled': 'auto_failback_enabled',
        'autoFailbackTime': 'auto_failback_time',
        'haLoadFactor': 'ha_load_factor',
        'haOrder': 'ha_order',
        'isFloating': 'is_floating',
        'mac': 'mac_masquerade_address'
    }

    returnables = [
        'full_path',
        'name',
        'description',
        'auto_failback_enabled',
        'auto_failback_time',
        'ha_load_factor',
        'ha_order',
        'is_floating',
        'mac_masquerade_address'
    ]

    @property
    def auto_failback_time(self):
        if self._values['auto_failback_time'] is None:
            return None
        return int(self._values['auto_failback_time'])

    @property
    def auto_failback_enabled(self):
        if self._values['auto_failback_enabled'] is None:
            return None
        elif self._values['auto_failback_enabled'] == 'false':
            # Yes, the REST API stores this as a string
            return 'no'
        return 'yes'

    @property
    def is_floating(self):
        if self._values['is_floating'] is None:
            return None
        elif self._values['is_floating'] == 'true':
            # Yes, the REST API stores this as a string
            return 'yes'
        return 'no'

    @property
    def mac_masquerade_address(self):
        if self._values['mac_masquerade_address'] in [None, 'none']:
            return None
        return self._values['mac_masquerade_address']


class TrafficGroupsFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(TrafficGroupsFactManager, self).__init__(**kwargs)
        self.want = TrafficGroupsParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(traffic_groups=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            attrs = resource.attrs
            attrs['stats'] = Stats(resource.stats.load()).stat
            params = TrafficGroupsParameters(params=attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.cm.traffic_groups.get_collection()
        return result


class TrunksParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'media': 'media_speed',
        'lacpMode': 'lacp_mode',
        'lacp': 'lacp_state',
        'lacpTimeout': 'lacp_timeout',
        'stp': 'stp_enabled',
        'workingMbrCount': 'operational_member_count',
        'linkSelectPolicy': 'link_selection_policy',
        'distributionHash': 'distribution_hash',
        'cfgMbrCount': 'configured_member_count'
    }

    returnables = [
        'full_path',
        'name',
        'description',
        'media_speed',
        'lacp_mode',        # 'active' or 'passive'
        'lacp_enabled',
        'stp_enabled',
        'operational_member_count',
        'media_status',
        'link_selection_policy',
        'lacp_timeout',
        'interfaces',
        'distribution_hash',
        'configured_member_count'
    ]

    @property
    def lacp_enabled(self):
        if self._values['lacp_enabled'] is None:
            return None
        elif self._values['lacp_enabled'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def stp_enabled(self):
        if self._values['stp_enabled'] is None:
            return None
        elif self._values['stp_enabled'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def media_status(self):
        # This is in the 'description' key instead of the more common
        # 'value' key. I'm not sure why this is, but it is.
        return self._values['stats']['status']['description']


class TrunksFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(TrunksFactManager, self).__init__(**kwargs)
        self.want = TrunksParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(trunks=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            attrs = resource.attrs
            attrs['stats'] = Stats(resource.stats.load()).stat
            params = TrunksParameters(params=attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.net.trunks.get_collection()
        return result


class VirtualAddressesParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'arp': 'arp_enabled',
        'autoDelete': 'auto_delete_enabled',
        'connectionLimit': 'connection_limit',
        'icmpEcho': 'icmp_echo',
        'mask': 'netmask',
        'routeAdvertisement': 'route_advertisement',
        'trafficGroup': 'traffic_group',
        'inheritedTrafficGroup': 'inherited_traffic_group'
    }

    returnables = [
        'full_path',
        'name',
        'address',
        'arp_enabled',
        'auto_delete_enabled',
        'connection_limit',
        'description',
        'enabled',
        'icmp_echo',
        'floating',
        'netmask',
        'route_advertisement',
        'traffic_group',
        'spanning',
        'inherited_traffic_group'
    ]

    @property
    def spanning(self):
        if self._values['spanning'] is None:
            return None
        elif self._values['spanning'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def arp_enabled(self):
        if self._values['arp_enabled'] is None:
            return None
        elif self._values['arp_enabled'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def route_advertisement(self):
        if self._values['route_advertisement'] is None:
            return None
        elif self._values['route_advertisement'] == 'disabled':
            return 'no'
        return 'yes'

    @property
    def auto_delete_enabled(self):
        if self._values['auto_delete_enabled'] is None:
            return None
        elif self._values['auto_delete_enabled'] == 'true':
            return 'yes'
        return 'no'

    @property
    def inherited_traffic_group(self):
        if self._values['inherited_traffic_group'] is None:
            return None
        elif self._values['inherited_traffic_group'] == 'true':
            return 'yes'
        return 'no'

    @property
    def icmp_echo(self):
        if self._values['icmp_echo'] is None:
            return None
        elif self._values['icmp_echo'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def floating(self):
        if self._values['floating'] is None:
            return None
        elif self._values['floating'] == 'enabled':
            return 'yes'
        return 'no'


class VirtualAddressesFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(VirtualAddressesFactManager, self).__init__(**kwargs)
        self.want = VirtualAddressesParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(virtual_addresses=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = VirtualAddressesParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.ltm.virtual_address_s.get_collection()
        return result


class VirtualServersParameters(BaseParameters):
    api_map = {
        'fullPath': 'full_path',
        'autoLasthop': 'auto_lasthop',
        'bwcPolicy': 'bw_controller_policy',
        'cmpEnabled': 'cmp_enabled',
        'connectionLimit': 'connection_limit',
        'fallbackPersistence': 'fallback_persistence_profile',
        'persist': 'persistence_profile',
        'translatePort': 'translate_port',
        'translateAddress': 'translate_address',
        'lastHopPool': 'last_hop_pool',
        'nat64': 'nat64_enabled',
        'sourcePort': 'source_port_behavior',
        'ipIntelligencePolicy': 'ip_intelligence_policy',
        'ipProtocol': 'protocol',
        'pool': 'default_pool',
        'rateLimitMode': 'rate_limit_mode',
        'rateLimitSrcMask': 'rate_limit_source_mask',
        'rateLimitDstMask': 'rate_limit_destination_mask',
        'rateLimit': 'rate_limit',
        'sourceAddressTranslation': 'snat_type',
        'gtmScore': 'gtm_score',
        'rateClass': 'rate_class',
        'source': 'source_address',
        'auth': 'authentication_profile',
        'mirror': 'connection_mirror_enabled',
        'rules': 'irules',
        'securityLogProfiles': 'security_log_profiles',
        'profilesReference': 'profiles'
    }

    returnables = [
        'full_path',
        'name',
        'auto_lasthop',
        'bw_controller_policy',
        'cmp_enabled',
        'connection_limit',
        'description',
        'enabled',
        'fallback_persistence_profile',
        'persistence_profile',
        'translate_port',
        'translate_address',
        'vlans',
        'destination',
        'last_hop_pool',
        'nat64_enabled',
        'source_port_behavior',
        'ip_intelligence_policy',
        'protocol',
        'default_pool',
        'rate_limit_mode',
        'rate_limit_source_mask',
        'rate_limit',
        'snat_type',
        'snat_pool',
        'gtm_score',
        'rate_class',
        'rate_limit_destination_mask',
        'source_address',
        'authentication_profile',
        'connection_mirror_enabled',
        'irules',
        'security_log_profiles',
        'type',
        'profiles',
        'destination_address',
        'destination_port'
    ]

    @property
    def destination_address(self):
        if self._values['destination'] is None:
            return None
        tup = self.destination_tuple
        return tup.ip

    @property
    def destination_port(self):
        if self._values['destination'] is None:
            return None
        tup = self.destination_tuple
        return tup.port

    @property
    def type(self):
        """Attempt to determine the current server type

        This check is very unscientific. It turns out that this information is not
        exactly available anywhere on a BIG-IP. Instead, we rely on a semi-reliable
        means for determining what the type of the virtual server is. Hopefully it
        always works.

        There are a handful of attributes that can be used to determine a specific
        type. There are some types though that can only be determined by looking at
        the profiles that are assigned to them. We follow that method for those
        complicated types; message-routing, fasthttp, and fastl4.

        Because type determination is an expensive operation, we cache the result
        from the operation.

        Returns:
            string: The server type.
        """
        if self._values['l2Forward'] is True:
            result = 'forwarding-l2'
        elif self._values['ipForward'] is True:
            result = 'forwarding-ip'
        elif self._values['stateless'] is True:
            result = 'stateless'
        elif self._values['reject'] is True:
            result = 'reject'
        elif self._values['dhcpRelay'] is True:
            result = 'dhcp'
        elif self._values['internal'] is True:
            result = 'internal'
        elif self.has_fasthttp_profiles:
            result = 'performance-http'
        elif self.has_fastl4_profiles:
            result = 'performance-l4'
        elif self.has_message_routing_profiles:
            result = 'message-routing'
        else:
            result = 'standard'
        return result

    @property
    def profiles(self):
        """Returns a list of profiles from the API

        The profiles are formatted so that they are usable in this module and
        are able to be compared by the Difference engine.

        Returns:
             list (:obj:`list` of :obj:`dict`): List of profiles.

             Each dictionary in the list contains the following three (3) keys.

             * name
             * context
             * fullPath

        Raises:
            F5ModuleError: If the specified context is a value other that
                ``all``, ``serverside``, or ``clientside``.
        """
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
    def has_message_routing_profiles(self):
        if self.profiles is None:
            return None
        current = self._read_current_message_routing_profiles_from_device()
        result = [x['name'] for x in self.profiles if x['name'] in current]
        if len(result) > 0:
            return True
        return False

    @property
    def has_fastl4_profiles(self):
        if self.profiles is None:
            return None
        current = self._read_current_fastl4_profiles_from_device()
        result = [x['name'] for x in self.profiles if x['name'] in current]
        if len(result) > 0:
            return True
        return False

    @property
    def has_fasthttp_profiles(self):
        """Check if ``fasthttp`` profile is in API profiles

        This method is used to determine the server type when doing comparisons
        in the Difference class.

        Returns:
             bool: True if server has ``fasthttp`` profiles. False otherwise.
        """
        if self.profiles is None:
            return None
        current = self._read_current_fasthttp_profiles_from_device()
        result = [x['name'] for x in self.profiles if x['name'] in current]
        if len(result) > 0:
            return True
        return False

    def _read_current_message_routing_profiles_from_device(self):
        collection1 = self.client.api.tm.ltm.profile.diameters.get_collection()
        collection2 = self.client.api.tm.ltm.profile.sips.get_collection()
        result = [x.name for x in collection1]
        result += [x.name for x in collection2]
        return result

    def _read_current_fastl4_profiles_from_device(self):
        collection = self.client.api.tm.ltm.profile.fastl4s.get_collection()
        result = [x.name for x in collection]
        return result

    def _read_current_fasthttp_profiles_from_device(self):
        collection = self.client.api.tm.ltm.profile.fasthttps.get_collection()
        result = [x.name for x in collection]
        return result

    @property
    def security_log_profiles(self):
        if self._values['security_log_profiles'] is None:
            return None
        result = list(set([x.strip('"') for x in self._values['security_log_profiles']]))
        result.sort()
        return result

    @property
    def snat_type(self):
        if self._values['snat_type'] is None:
            return None
        if 'type' in self._values['snat_type']:
            if self._values['snat_type']['type'] == 'pool':
                return self._values['snat_type']['pool']

    @property
    def snat_type(self):
        if self._values['snat_type'] is None:
            return None
        if 'type' in self._values['snat_type']:
            if self._values['snat_type']['type'] == 'automap':
                return 'automap'
            elif self._values['snat_type']['type'] == 'none':
                return 'none'
            elif self._values['snat_type']['type'] == 'pool':
                return 'snat'

    @property
    def connection_mirror_enabled(self):
        if self._values['connection_mirror_enabled'] is None:
            return None
        elif self._values['connection_mirror_enabled'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def rate_limit(self):
        if self._values['rate_limit'] is None:
            return None
        elif self._values['rate_limit'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def nat64_enabled(self):
        if self._values['nat64_enabled'] is None:
            return None
        elif self._values['nat64_enabled'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def enabled(self):
        if self._values['enabled'] is None:
            return None
        elif self._values['enabled'] is True:
            return 'yes'
        return 'no'

    @property
    def translate_port(self):
        if self._values['translate_port'] is None:
            return None
        elif self._values['translate_port'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def translate_address(self):
        if self._values['translate_address'] is None:
            return None
        elif self._values['translate_address'] == 'enabled':
            return 'yes'
        return 'no'

    @property
    def persistence_profile(self):
        """Return persistence profile in a consumable form

        I don't know why the persistence profile is stored this way, but below is the
        general format of it.

            "persist": [
                {
                    "name": "msrdp",
                    "partition": "Common",
                    "tmDefault": "yes",
                    "nameReference": {
                        "link": "https://localhost/mgmt/tm/ltm/persistence/msrdp/~Common~msrdp?ver=13.1.0.4"
                    }
                }
            ],

        As you can see, this is quite different from something like the fallback
        persistence profile which is just simply

            /Common/fallback1

        This method makes the persistence profile look like the fallback profile.

        Returns:
             string: The persistence profile configured on the virtual.
        """
        if self._values['persistence_profile'] is None:
            return None
        profile = self._values['persistence_profile'][0]
        result = fq_name(profile['partition'], profile['name'])
        return result

    @property
    def destination_tuple(self):
        Destination = namedtuple('Destination', ['ip', 'port', 'route_domain'])

        # Remove the partition
        if self._values['destination'] is None:
            result = Destination(ip=None, port=None, route_domain=None)
            return result
        destination = re.sub(r'^/[a-zA-Z0-9_.-]+/', '', self._values['destination'])

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

    def is_valid_ip(self, value):
        try:
            netaddr.IPAddress(value)
            return True
        except (netaddr.core.AddrFormatError, ValueError):
            return False


class VirtualServersFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(VirtualServersFactManager, self).__init__(**kwargs)
        self.want = VirtualServersParameters(client=self.client, params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(virtual_servers=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = VirtualServersParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.ltm.virtuals.get_collection(
            requests_params=dict(
                params=dict(
                    expandSubcollections='true'
                )
            )
        )
        return result


class VlansParameters(BaseParameters):
    api_map = {
        'autoLasthop': 'auto_lasthop',
        'cmpHash': 'cmp_hash_algorithm',
        'failsafeAction': 'failsafe_action',
        'failsafe': 'failsafe_state',
        'failsafeTimeout': 'failsafe_timeout',
        'ifIndex': 'if_index',
        'learning': 'learning_mode',
        'interfacesReference': 'interfaces',
        'sourceChecking': 'source_check_state',
        'fullPath': 'full_path'
    }

    returnables = [
        'full_path',
        'name',
        'auto_lasthop',
        'cmp_hash_algorithm',
        'description',
        'failsafe_action',
        'failsafe_state',
        'failsafe_timeout',
        'if_index',
        'learning_mode',
        'interfaces',  # (deprecated) Replaces the "members" return value
        'mtu',
        'sflow_poll_interval',
        'sflow_poll_interval_global',  # SOAP values are deprecated (ex. SFLOW_GLOBAL_YES)
        'sflow_sampling_rate',
        'sflow_sampling_rate_global',
        'source_check_state',
        'true_mac_address',
        'vlan_id',
        # (deprecated) MAC masquerade addresses are now configured on traffic groups.
        # (missing; ask Don) def get_dynamic_forwarding(self): return self.api.Networking.VLAN.get_dynamic_forwarding(self.vlans)
    ]

    @property
    def interfaces(self):
        if self._values['interfaces'] is None:
            return None
        if 'items' not in self._values['interfaces']:
            return None
        result = []
        for item in self._values['interfaces']['items']:
            tmp = dict(
                name=item['name'],
                full_path=item['fullPath']
            )
            if 'tagged' in item:
                tmp['tagged'] = True
            else:
                tmp['tagged'] = False
            result.append(tmp)
        return result

    @property
    def sflow_poll_interval(self):
        return int(self._values['sflow']['pollInterval'])

    @property
    def sflow_poll_interval_global(self):
        if self._values['sflow']['pollIntervalGlobal'] in BOOLEANS_TRUE:
            return True
        return False

    @property
    def sflow_sampling_rate(self):
        return int(self._values['sflow']['samplingRate'])

    @property
    def sflow_sampling_rate_global(self):
        if self._values['sflow']['samplingRateGlobal'] in BOOLEANS_TRUE:
            return True
        return False

    @property
    def source_check_state(self):
        if self._values['source_check_state'] == 'enabled':
            return True
        return False

    @property
    def true_mac_address(self):
        # Who made this field a "description"!?
        return self._values['stats']['macTrue']['description']

    @property
    def vlan_id(self):
        # We can't agree on field names...SMH
        return self._values['stats']['id']['value']


class VlansFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(VlansFactManager, self).__init__(**kwargs)
        self.want = VlansParameters(params=self.module.params)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(vlans=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            attrs = resource.attrs
            attrs['stats'] = Stats(resource.stats.load()).stat
            params = VlansParameters(params=attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.net.vlans.get_collection(
            requests_params=dict(
                params='expandSubcollections=true'
            )
        )
        return result


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = kwargs.get('client', None)
        self.kwargs = kwargs
        self.want = Parameters(params=self.module.params)
        self.managers = {
            'internal-data-groups': InternalDataGroupsFactManager,
            'client-ssl-profiles': ClientSslProfilesFactManager,
            'devices': DevicesFactManager,
            'device-groups': DeviceGroupsFactManager,
            'interfaces': InterfacesFactManager,
            'ssl-certs': SslCertificatesFactManager,
            'ssl-keys': SslKeysFactManager,
            'nodes': NodesFactManager,
            'ltm-pools': LtmPoolsFactManager,
            'provision-info': ProvisionInfoFactManager,
            'irules': IrulesFactManager,
            'self-ips': SelfIpsFactManager,
            'software-volumes': SoftwareVolumesFactManager,
            'system-info': SystemInfoFactManager,
            'traffic-groups': TrafficGroupsFactManager,
            'trunks': TrunksFactManager,
            'virtual-addresses': VirtualAddressesFactManager,
            'virtual-servers': VirtualServersFactManager,
            'vlans': VlansFactManager
        }

    def exec_module(self):
        if 'all' in self.want.gather_subset:
            managers = list(self.managers.keys()) + self.want.gather_subset
            managers.remove('all')
            self.want.update({'gather_subset': managers})
        res = self.check_valid_gather_subset(self.want.gather_subset)
        if res:
            invalid = ','.join(res)
            raise F5ModuleError(
                "The specified 'gather_subset' options are invalid: {0}".format(invalid)
            )

        # Remove the excluded entries from the list of possible facts
        exclude = [x[1:] for x in self.want.gather_subset if x[0] == '!']
        include = [x for x in self.want.gather_subset if x[0] != '!']
        result = [x for x in include if x not in exclude]

        managers = []
        for name in result:
            manager = self.get_manager(name)
            if manager:
                managers.append(manager)

        if not managers:
            result = dict(
                changed=False
            )
            return result

        result = self.execute_managers(managers)
        if result:
            result['changed'] = True
        else:
            result['changed'] = False
        return result

    def check_valid_gather_subset(self, includes):
        """Check that the specified subset is valid

        The ``gather_subset`` parameter is specified as a "raw" field which means that
        any Python type could technically be provided

        :param includes:
        :return:
        """
        keys = self.managers.keys()
        result = []
        for x in includes:
            if x not in keys:
                if x[0] == '!':
                    if x[1:] not in keys:
                        result.append(x)
                else:
                    result.append(x)
        return result

    def execute_managers(self, managers):
        results = dict()
        for manager in managers:
            result = manager.exec_module()
            results.update(result)
        return results

    def get_manager(self, which):
        result = {}
        manager = self.managers.get(which, None)
        if manager:
            kwargs = dict()
            kwargs.update(self.kwargs)

            if manager == SystemInfoFactManager:
                # Replace the API layer for the SystemInfoFactManager
                #
                # This is being done because there is no API for talking to the
                # /mgmt/tm/sys/hardware API in the f5-sdk.
                #
                # Longer term, all of the classes in this module should use the
                # F5RestClient object and drop the usage of the f5-sdk.

                client = F5RestClient(**self.module.params)
                kwargs['client'] = client
            result = manager(**kwargs)
        return result


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = False
        argument_spec = dict(
            gather_subset=dict(
                type='list',
                required=True,
                aliases=['include']
            ),
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    if not HAS_F5SDK:
        module.fail_json(msg="The python f5-sdk module is required")
    if not HAS_NETADDR:
        module.fail_json(msg="The python netaddr module is required")

    try:
        client = F5Client(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        module.exit_json(**results)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
