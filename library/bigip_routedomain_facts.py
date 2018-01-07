#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_routedomain_facts
short_description: Retrieve route domain attributes from a BIG-IP
description:
  - Retrieve route domain attributes from a BIG-IP
version_added: "2.2"
options:
  server:
    description:
      - BIG-IP host
    required: True
  password:
    description:
      - BIG-IP password
    required: True
  id:
    description:
      - The unique identifying integer representing the route domain.
    required: True
  partition:
    description:
      - The partition the route domain resides on
    default: Common
  user:
    description:
      - BIG-IP username
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    default: yes
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Get the facts for a route domain
  bigip_routedomain_facts:
    id: 1234
    password: secret
    server: lb.mydomain.com
    user: admin
  delegate_to: localhost
'''

RETURN = r'''
bwc_policy:
  description: Bandwidth controller for the route domain
  returned: changed
  type: string
  sample: /Common/foo
connection_limit:
  description: Maximum number of concurrent connections allowed for the route domain
  returned: changed
  type: integer
  sample: 0
description:
  description: Descriptive text that identifies the route domain
  returned: changed
  type: string
  sample: The foo route domain
evict_policy:
  description: Eviction policy to use with this route domain
  returned: changed
  type: string
  sample: /Common/default-eviction-policy
id:
  description: ID of the route domain
  returned: changed
  type: integer
  sample: 1234
service_policy:
  description: Service policy to associate with the route domain
  returned: changed
  type: string
  sample: /Common/abc
strict:
  description: Whether the system enforces cross-routing restrictions
  returned: changed
  type: string
  sample: enabled
routing_protocol:
  description: Dynamic routing protocols for the system to use in the route domain
  returned: changed
  type: list
  sample: ["BGP", "OSPFv2"]
vlans:
  description: VLANs for the system to use in the route domain
  returned: changed
  type: list
  sample: ["/Common/abc", "/Common/xyz"]
'''

try:
    from f5.bigip import ManagementRoot
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


class BigIpRouteDomainFacts(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def flush(self):
        result = dict()

        rds = self.api.tm.net.route_domains
        rd = rds.route_domain.load(name=kwargs['id'],
                                   partition=kwargs['partition'])

        result['id'] = rd.id
        result['name'] = rd.name
        result['parent'] = rd.parent

        if hasattr(r, 'bwcPolicy'):
            result['bwc_policy'] = rd.bwcPolicy
        if hasattr(r, 'connectionLimit'):
            result['connection_limit'] = rd.connectionLimit
        if hasattr(r, 'description'):
            result['description'] = rd.description
        if hasattr(r, 'flowEvictionPolicy'):
            result['evict_policy'] = rd.flowEvictionPolicy
        if hasattr(r, 'servicePolicy'):
            result['service_policy'] = rd.servicePolicy
        if hasattr(r, 'strict'):
            result['strict'] = rd.strict
        if hasattr(r, 'routingProtocol'):
            result['routing_protocol'] = rd.routingProtocol
        if hasattr(r, 'vlans'):
            result['vlans'] = rd.vlans
        return result


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        id=dict(required=True),
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpRouteDomainFacts(**module.params)
        result = obj.flush()

        module.exit_json(changed=True, bigip=result)
    except F5ModuleError as e:
        module.fail_json(msg=e.message)

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
