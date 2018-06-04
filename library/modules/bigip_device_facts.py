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
      - certificates
      - client-ssl-profiles
      - devices
      - device-groups
      - interfaces
      - keys
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
        - TODO: WHAT IS THIS
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
        - Valid return values can include C(none), 
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

import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.network.common.utils import to_netmask
from ansible.module_utils.parsing.convert_bool import BOOLEANS_TRUE
from ansible.module_utils.parsing.convert_bool import BOOLEANS_FALSE
from ansible.module_utils.six import iteritems
from ansible.module_utils.six import string_types

try:
    from library.module_utils.network.f5.bigip import HAS_F5SDK
    from library.module_utils.network.f5.bigip import F5Client
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


class Interfaces(object):
    """Interfaces class.

    F5 BIG-IP interfaces class.

    Attributes:
        api: iControl API instance.
        interfaces: A list of BIG-IP interface names.
    """

    def __init__(self, api, regex=None):
        self.api = api
        self.interfaces = api.Networking.Interfaces.get_list()
        if regex:
            re_filter = re.compile(regex)
            self.interfaces = filter(re_filter.search, self.interfaces)

    def get_list(self):
        return self.interfaces

    def get_active_media(self):
        return self.api.Networking.Interfaces.get_active_media(self.interfaces)

    def get_actual_flow_control(self):
        return self.api.Networking.Interfaces.get_actual_flow_control(self.interfaces)

    def get_bundle_state(self):
        return self.api.Networking.Interfaces.get_bundle_state(self.interfaces)

    def get_description(self):
        return self.api.Networking.Interfaces.get_description(self.interfaces)

    def get_dual_media_state(self):
        return self.api.Networking.Interfaces.get_dual_media_state(self.interfaces)

    def get_enabled_state(self):
        return self.api.Networking.Interfaces.get_enabled_state(self.interfaces)

    def get_if_index(self):
        return self.api.Networking.Interfaces.get_if_index(self.interfaces)

    def get_learning_mode(self):
        return self.api.Networking.Interfaces.get_learning_mode(self.interfaces)

    def get_lldp_admin_status(self):
        return self.api.Networking.Interfaces.get_lldp_admin_status(self.interfaces)

    def get_lldp_tlvmap(self):
        return self.api.Networking.Interfaces.get_lldp_tlvmap(self.interfaces)

    def get_mac_address(self):
        return self.api.Networking.Interfaces.get_mac_address(self.interfaces)

    def get_media(self):
        return self.api.Networking.Interfaces.get_media(self.interfaces)

    def get_media_option(self):
        return self.api.Networking.Interfaces.get_media_option(self.interfaces)

    def get_media_option_sfp(self):
        return self.api.Networking.Interfaces.get_media_option_sfp(self.interfaces)

    def get_media_sfp(self):
        return self.api.Networking.Interfaces.get_media_sfp(self.interfaces)

    def get_media_speed(self):
        return self.api.Networking.Interfaces.get_media_speed(self.interfaces)

    def get_media_status(self):
        return self.api.Networking.Interfaces.get_media_status(self.interfaces)

    def get_mtu(self):
        return self.api.Networking.Interfaces.get_mtu(self.interfaces)

    def get_phy_master_slave_mode(self):
        return self.api.Networking.Interfaces.get_phy_master_slave_mode(self.interfaces)

    def get_prefer_sfp_state(self):
        return self.api.Networking.Interfaces.get_prefer_sfp_state(self.interfaces)

    def get_flow_control(self):
        return self.api.Networking.Interfaces.get_requested_flow_control(self.interfaces)

    def get_sflow_poll_interval(self):
        return self.api.Networking.Interfaces.get_sflow_poll_interval(self.interfaces)

    def get_sflow_poll_interval_global(self):
        return self.api.Networking.Interfaces.get_sflow_poll_interval_global(self.interfaces)

    def get_sfp_media_state(self):
        return self.api.Networking.Interfaces.get_sfp_media_state(self.interfaces)

    def get_stp_active_edge_port_state(self):
        return self.api.Networking.Interfaces.get_stp_active_edge_port_state(self.interfaces)

    def get_stp_enabled_state(self):
        return self.api.Networking.Interfaces.get_stp_enabled_state(self.interfaces)

    def get_stp_link_type(self):
        return self.api.Networking.Interfaces.get_stp_link_type(self.interfaces)

    def get_stp_protocol_detection_reset_state(self):
        return self.api.Networking.Interfaces.get_stp_protocol_detection_reset_state(self.interfaces)






class AddressClasses(object):
    """Address group/class class.

    F5 BIG-IP address group/class class.

    Attributes:
        api: iControl API instance.
        address_classes: List of address classes.
    """

    def __init__(self, api, regex=None):
        self.api = api
        self.address_classes = api.LocalLB.Class.get_address_class_list()
        if regex:
            re_filter = re.compile(regex)
            self.address_classes = filter(re_filter.search, self.address_classes)

    def get_list(self):
        return self.address_classes

    def get_address_class(self):
        key = self.api.LocalLB.Class.get_address_class(self.address_classes)
        value = self.api.LocalLB.Class.get_address_class_member_data_value(key)
        result = list(map(zip, [x['members'] for x in key], value))
        return result

    def get_description(self):
        return self.api.LocalLB.Class.get_description(self.address_classes)




class SystemInfo(object):
    """System information class.

    F5 BIG-IP system information class.

    Attributes:
        api: iControl API instance.
    """

    def __init__(self, api):
        self.api = api

    def get_base_mac_address(self):
        return self.api.System.SystemInfo.get_base_mac_address()

    def get_blade_temperature(self):
        return self.api.System.SystemInfo.get_blade_temperature()

    def get_chassis_slot_information(self):
        return self.api.System.SystemInfo.get_chassis_slot_information()

    def get_globally_unique_identifier(self):
        return self.api.System.SystemInfo.get_globally_unique_identifier()

    def get_group_id(self):
        return self.api.System.SystemInfo.get_group_id()

    def get_hardware_information(self):
        return self.api.System.SystemInfo.get_hardware_information()

    def get_marketing_name(self):
        return self.api.System.SystemInfo.get_marketing_name()

    def get_product_information(self):
        return self.api.System.SystemInfo.get_product_information()

    def get_pva_version(self):
        return self.api.System.SystemInfo.get_pva_version()

    def get_system_id(self):
        return self.api.System.SystemInfo.get_system_id()

    def get_system_information(self):
        return self.api.System.SystemInfo.get_system_information()

    def get_time(self):
        return self.api.System.SystemInfo.get_time()

    def get_time_zone(self):
        return self.api.System.SystemInfo.get_time_zone()

    def get_uptime(self):
        return self.api.System.SystemInfo.get_uptime()



def generate_interface_dict(f5, regex):
    interfaces = Interfaces(f5.get_api(), regex)
    fields = ['active_media', 'actual_flow_control', 'bundle_state',
              'description', 'dual_media_state', 'enabled_state', 'if_index',
              'learning_mode', 'lldp_admin_status', 'lldp_tlvmap',
              'mac_address', 'media', 'media_option', 'media_option_sfp',
              'media_sfp', 'media_speed', 'media_status', 'mtu',
              'phy_master_slave_mode', 'prefer_sfp_state', 'flow_control',
              'sflow_poll_interval', 'sflow_poll_interval_global',
              'sfp_media_state', 'stp_active_edge_port_state',
              'stp_enabled_state', 'stp_link_type',
              'stp_protocol_detection_reset_state']
    return generate_dict(interfaces, fields)








def generate_address_class_dict(f5, regex):
    address_classes = AddressClasses(f5.get_api(), regex)
    fields = ['address_class', 'description']
    return generate_dict(address_classes, fields)


def generate_system_info_dict(f5):
    system_info = SystemInfo(f5.get_api())
    fields = ['base_mac_address',
              'blade_temperature', 'chassis_slot_information',
              'globally_unique_identifier', 'group_id',
              'hardware_information',
              'marketing_name',
              'product_information', 'pva_version', 'system_id',
              'system_information', 'time',
              'time_zone', 'uptime']
    return generate_simple_dict(system_info, fields)
















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
        result = {}

        for name in entries:
            entry = entries[name]
            if 'https://localhost' in name:
                name = name.split('/')
                name = name[-1]
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
    include_map = {
        'address_class': 'internal-data-groups',
        'certificate': 'certificates',
        'client_ssl_profile': 'client-ssl-profiles',
        'device': 'devices',
        'device_group': 'device-groups',
        'interface': 'interfaces',
        'key': 'keys',
        'node': 'nodes',
        'pool': 'pools',
        'provision': 'provision-info',
        'rule': 'irules',
        'self_ip': 'self-ips',
        'software': 'software-images',
        'system_info': 'system-info',
        'traffic_group': 'traffic-groups',
        'trunk': 'trunks',
        'virtual_address': 'virtual-addresses',
        'virtual_server': 'virtual-servers',
        'vlan': 'vlans',
    }

    @property
    def include(self):
        if isinstance(self._values['include'], string_types):
            self._values['include'] = [self._values['include']]
        elif not isinstance(self._values['include'], list):
            raise F5ModuleError(
                "The specified gather_subset must be a list."
            )
        self._values['include'].sort()
        return self._values['include']


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






















class VirtualServers(object):

    def get_name(self):
        return [x[x.rfind('/') + 1:] for x in self.virtual_servers]

    def get_actual_hardware_acceleration(self):
        return self.api.LocalLB.VirtualServer.get_actual_hardware_acceleration(self.virtual_servers)

    def get_authentication_profile(self):
        return self.api.LocalLB.VirtualServer.get_authentication_profile(self.virtual_servers)

    def get_auto_lasthop(self):
        return self.api.LocalLB.VirtualServer.get_auto_lasthop(self.virtual_servers)

    def get_bw_controller_policy(self):
        return self.api.LocalLB.VirtualServer.get_bw_controller_policy(self.virtual_servers)

    def get_clone_pool(self):
        return self.api.LocalLB.VirtualServer.get_clone_pool(self.virtual_servers)

    def get_cmp_enable_mode(self):
        return self.api.LocalLB.VirtualServer.get_cmp_enable_mode(self.virtual_servers)

    def get_connection_limit(self):
        return self.api.LocalLB.VirtualServer.get_connection_limit(self.virtual_servers)

    def get_connection_mirror_state(self):
        return self.api.LocalLB.VirtualServer.get_connection_mirror_state(self.virtual_servers)

    def get_default_pool_name(self):
        return self.api.LocalLB.VirtualServer.get_default_pool_name(self.virtual_servers)

    def get_description(self):
        return self.api.LocalLB.VirtualServer.get_description(self.virtual_servers)

    def get_destination(self):
        return self.api.LocalLB.VirtualServer.get_destination_v2(self.virtual_servers)

    def get_enabled_state(self):
        return self.api.LocalLB.VirtualServer.get_enabled_state(self.virtual_servers)

    def get_enforced_firewall_policy(self):
        return self.api.LocalLB.VirtualServer.get_enforced_firewall_policy(self.virtual_servers)

    def get_fallback_persistence_profile(self):
        return self.api.LocalLB.VirtualServer.get_fallback_persistence_profile(self.virtual_servers)

    def get_fw_rule(self):
        return self.api.LocalLB.VirtualServer.get_fw_rule(self.virtual_servers)

    def get_gtm_score(self):
        return self.api.LocalLB.VirtualServer.get_gtm_score(self.virtual_servers)

    def get_last_hop_pool(self):
        return self.api.LocalLB.VirtualServer.get_last_hop_pool(self.virtual_servers)

    def get_nat64_state(self):
        return self.api.LocalLB.VirtualServer.get_nat64_state(self.virtual_servers)

    def get_object_status(self):
        return self.api.LocalLB.VirtualServer.get_object_status(self.virtual_servers)

    def get_persistence_profile(self):
        return self.api.LocalLB.VirtualServer.get_persistence_profile(self.virtual_servers)

    def get_profile(self):
        return self.api.LocalLB.VirtualServer.get_profile(self.virtual_servers)

    def get_protocol(self):
        return self.api.LocalLB.VirtualServer.get_protocol(self.virtual_servers)

    def get_rate_class(self):
        return self.api.LocalLB.VirtualServer.get_rate_class(self.virtual_servers)

    def get_rate_limit(self):
        return self.api.LocalLB.VirtualServer.get_rate_limit(self.virtual_servers)

    def get_rate_limit_destination_mask(self):
        return self.api.LocalLB.VirtualServer.get_rate_limit_destination_mask(self.virtual_servers)

    def get_rate_limit_mode(self):
        return self.api.LocalLB.VirtualServer.get_rate_limit_mode(self.virtual_servers)

    def get_rate_limit_source_mask(self):
        return self.api.LocalLB.VirtualServer.get_rate_limit_source_mask(self.virtual_servers)

    def get_related_rule(self):
        return self.api.LocalLB.VirtualServer.get_related_rule(self.virtual_servers)

    def get_rule(self):
        return self.api.LocalLB.VirtualServer.get_rule(self.virtual_servers)

    def get_security_log_profile(self):
        return self.api.LocalLB.VirtualServer.get_security_log_profile(self.virtual_servers)

    def get_snat_pool(self):
        return self.api.LocalLB.VirtualServer.get_snat_pool(self.virtual_servers)

    def get_snat_type(self):
        return self.api.LocalLB.VirtualServer.get_snat_type(self.virtual_servers)

    def get_source_address(self):
        return self.api.LocalLB.VirtualServer.get_source_address(self.virtual_servers)

    def get_source_address_translation_lsn_pool(self):
        return self.api.LocalLB.VirtualServer.get_source_address_translation_lsn_pool(self.virtual_servers)

    def get_source_address_translation_snat_pool(self):
        return self.api.LocalLB.VirtualServer.get_source_address_translation_snat_pool(self.virtual_servers)

    def get_source_address_translation_type(self):
        return self.api.LocalLB.VirtualServer.get_source_address_translation_type(self.virtual_servers)

    def get_source_port_behavior(self):
        return self.api.LocalLB.VirtualServer.get_source_port_behavior(self.virtual_servers)

    def get_staged_firewall_policy(self):
        return self.api.LocalLB.VirtualServer.get_staged_firewall_policy(self.virtual_servers)

    def get_translate_address_state(self):
        return self.api.LocalLB.VirtualServer.get_translate_address_state(self.virtual_servers)

    def get_translate_port_state(self):
        return self.api.LocalLB.VirtualServer.get_translate_port_state(self.virtual_servers)

    def get_type(self):
        return self.api.LocalLB.VirtualServer.get_type(self.virtual_servers)

    def get_vlan(self):
        return self.api.LocalLB.VirtualServer.get_vlan(self.virtual_servers)

    def get_wildmask(self):
        return self.api.LocalLB.VirtualServer.get_wildmask(self.virtual_servers)


def generate_vs_dict(f5, regex):
    fields = ['', 'authentication_profile',
              '', '', '',
              '', '', 'connection_mirror_state',
              'default_pool_name', '', '',
              '', 'enforced_firewall_policy',
              '', 'fw_rule', 'gtm_score',
              'last_hop_pool', 'nat64_state', 'object_status',
              '', 'profile', 'protocol',
              'rate_class', 'rate_limit', 'rate_limit_destination_mask',
              'rate_limit_mode', 'rate_limit_source_mask', 'related_rule',
              'rule', 'security_log_profile', 'snat_pool', 'snat_type',
              'source_address', 'source_address_translation_lsn_pool',
              'source_address_translation_snat_pool',
              'source_address_translation_type', 'source_port_behavior',
              'staged_firewall_policy', 'translate_address_state',
              'type', '', 'wildmask',
              '']
    return generate_dict(virtual_servers, fields)




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
        'translateAddress': 'translate_address'
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
        'destination'
    ]

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


class VirtualServersFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.module = kwargs.get('module', None)
        super(VirtualServersFactManager, self).__init__(**kwargs)
        self.want = VirtualServersParameters(params=self.module.params)

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
            params = VirtualServersParameters(params=resource.attrs)
            results.append(params)
        return results

    def read_collection_from_device(self):
        result = self.client.api.tm.ltm.virtuals.get_collection()
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
        'interfaces', # (deprecated) Replaces the "members" return value
        'mtu',
        'sflow_poll_interval',
        'sflow_poll_interval_global', # SOAP values are deprecated (ex. SFLOW_GLOBAL_YES)
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
            #'internal-data-groups': InternalDataGroupsFactManager,
            'client-ssl-profiles': ClientSslProfilesFactManager,
            'devices': DevicesFactManager,
            'device-groups': DeviceGroupsFactManager,
            #'interfaces': InterfacesFactManager,
            'ssl-certs': SslCertificatesFactManager,
            'ssl-keys': SslKeysFactManager,
            'nodes': NodesFactManager,
            'ltm-pools': LtmPoolsFactManager,
            'provision-info': ProvisionInfoFactManager,
            'irules': IrulesFactManager,
            'self-ips': SelfIpsFactManager,
            'software-volumes': SoftwareVolumesFactManager,
            #'system-info': SystemInfoFactManager,
            'traffic-groups': TrafficGroupsFactManager,
            'trunks': TrunksFactManager,
            'virtual-addresses': VirtualAddressesFactManager,
            'virtual-servers': VirtualServersFactManager,
            'vlans': VlansFactManager
        }

    def exec_module(self):
        if 'all' in self.want.include:
            managers = list(self.managers.keys())
            self.want.update({'includes': managers})
        else:
            res = self.check_valid_gather_subset(self.want.include)
            if res:
                invalid = ','.join(res)
                raise F5ModuleError(
                    "The specified 'gather_subset' options are invalid: {0}"
                        .format(invalid)
                )

        managers = []
        for name in self.want.include:
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
        if 'all' in includes:
            return []
        invalid = [x for x in includes if x not in self.managers.keys()]
        return invalid

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
            result = manager(**self.kwargs)
        return result


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = False
        argument_spec = dict(
            include=dict(
                type='list',
                required=True,
                aliases=['gather_subset']
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
