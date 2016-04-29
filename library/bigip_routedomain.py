#!/usr/bin/python
# -*- coding: utf-8 -*-
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

DOCUMENTATION = '''
---
module: bigip_routedomain
short_description: Manage route domains on a BIG-IP
description:
   - Manage route domains on a BIG-IP
version_added: "2.2"
options:
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: smart
    choices:
      - rest
      - soap
  server:
    description:
      - BIG-IP host
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  id:
    description:
      - The unique identifying integer representing the route domain.
    required: true
  partition:
    description:
      - The partition to create the route domain on
    required: false
    default: Common
  user:
    description:
      - BIG-IP username
    required: true
  state:
    description:
      - Whether the route domain should exist or not
    required: false
    default: present
    choices:
      - present
      - absent
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
   - Requires the f5-sdk Python package on the host. This is as easy as
     pip install f5-sdk
requirements:
    - f5-sdk
author:
    - Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = '''
- name: Create a route domain
  bigip_routedomain:
      id: "1234"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost

- name: Set VLANs on the route domain
  bigip_routedomain:
      id: "1234"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
      vlans:
          - net1
          - foo
  delegate_to: localhost
'''

RETURN = '''
'''

PROTOCOLS = [
    'bfd', 'bgp', 'is-is', 'ospfv2', 'ospfv3', 'pim', 'rip', 'ripng'
]

PROTOCOL_MAP = {
    'bfd': "BFD",
    'bgp': "BGP",
    'is-is': "IS-IS",
    'ospfv2': "OSPFv2",
    'ospfv3': "OSPFv3",
    'pim': "PIM",
    'rip': "RIP",
    'ripng': "RIPng"
}

STRICTS = ['enabled', 'disabled']


class F5ModuleError(Exception):
    pass


class BigIpRouteDomain(object):
    def __init__(self, *args, **kwargs):
        if not f5sdk_found:
            raise F5ModuleError("The python f5-sdk module is required")

        if type(kwargs['vlans']) is str:
            kwargs['vlans'] = [kwargs['vlans']]

        if type(kwargs['routing_protocol']) is str:
            kwargs['routing_protocol'] = [kwargs['routing_protocol']]

        self.params = kwargs
        self.api = BigIP(kwargs['server'],
                         kwargs['user'],
                         kwargs['password'],
                         port=kwargs['server_port'])

    def absent(self):
        if not self.exists():
            return False

        if self.params['check_mode']:
            return True

        self.api.net.route_domains.route_domain.delete(
            name=self.params['id']
        )

        if self.exists():
            raise F5ModuleError("Failed to delete the self IP")
        else:
            return True

    def present(self):
        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True
            return self.create()

    def create(self):
        config = dict()
        config['id'] = self.params['id']
        if self.params['description'] is not None:
            config['description'] = self.params['description']
        if self.params['strict'] is not None:
            config['strict'] = self.params['strict']
        if self.params['parent'] is not None:
            parent = '%s/%s' % (self.params['partition'],
                                self.params['parent'])
            config['parent'] = parent
        if self.params['bwc_policy'] is not None:
            policy = '%s/%s' % (self.params['partition'],
                                self.params['bwc_policy'])
            config['bwcPolicy'] = policy
        if self.params['vlans'] is not None:
            configs['vlans'] = []
            for vlan in self.params['vlans']:
                vname = '%s/%s' % (self.params['partition'],
                                   vlan)
                configs['vlans'].append(vname)
        if self.params['routing_protocol'] is not None:
            configs['routingProtocol'] = []
            for rp in self.params['routing_protocol']:
                rp_name = '%s/%s' % (self.params['partition'],
                                     rp)
                configs['routingProtocol'].append(rp_name)
        if self.params['connection_limit'] is not None:
            config['connectionLimit'] = self.params['connection_limit']
        if self.params['flow_eviction_policy'] is not None:
            policy = '%s/%s' % (self.params['partition'],
                                self.params['flow_eviction_policy'])
            config['flowEvictionPolicy'] = policy
        if self.params['service_policy'] is not None:
            policy = '%s/%s' % (self.params['partition'],
                                self.params['service_policy'])
            config['servicePolicy'] = policy

        self.api.net.route_domains.route_domain.create(**config)
        exists = self.api.net.route_domains.route_domain.exists(
            name=self.params['name']
        )
        if exists:
            return True
        else:
            raise F5ModuleError(
                "An error occurred while creating the route domain"
            )

    def delete(self):
        self.api.net.route_domains.route_domain.delete(
            name=self.params['name']
        )

    def exists(self):
        return self.api.net.route_domains.route_domain.exists(
            name=self.params['name']
        )

    def flush(self):
        current = self.read()

        if self.params['check_mode']:
            if value == current:
                changed = False
            else:
                changed = True
        else:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
            current = self.read()
            result.update(current)

        result.update(dict(changed=changed))
        return result


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        id=dict(required=True, type='int'),
        description=dict(required=False, default=None),
        strict=dict(required=False, default=None, choices=STRICTS),
        parent=dict(required=False, type='int', default=None),
        vlans=dict(required=False, default=None),
        routing_protocol=dict(required=False, default=None),
        bwc_policy=dict(required=False, type='str', default=None),
        connection_limit=dict(required=False, type='int', default=None),
        flow_eviction_policy=dict(required=False, type='str', default=None),
        service_policy=dict(required=False, type='str', default=None)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpRouteDomain(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError, e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
