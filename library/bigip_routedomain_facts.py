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
module: bigip_routedomain_facts
short_description: Retrieve route domain attributes from a BIG-IP
description:
   - Retrieve route domain attributes from a BIG-IP
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
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds
   - Requires the requests Python package on the host. This is as easy as
     pip install requests
requirements:
    - bigsuds
    - requests
author:
    - Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = '''
- name: Get the facts for a route domain
  bigip_routedomain_facts:
      id: "1234"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''
full_name:
    description: Full name of the user
    returned: changed and success
    type: string
    sample: "John Doe"
'''

import json

PROTOCOLS=[
    'bfd','bgp','is-is','ospfv2','ospfv3','pim','rip','ripng'
]

class F5ModuleError(Exception):
    pass


class BigIpApiFactory(object):
    def factory(module):
        type = module.params.get('connection')

        if type == "rest":
            if not requests_found:
                raise Exception("The python requests module is required")
            return BigIpRestApi(check_mode=module.check_mode, **module.params)
        elif type == "soap":
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")
            return BigIpSoapApi(check_mode=module.check_mode, **module.params)

    factory = staticmethod(factory)


class BigIpCommon(object):
    def __init__(self, *args, **kwargs):
        self.result = dict(changed=False, changes=dict())
        self.params = kwargs

    def flush(self):
        if obj.exists():
            return dict(bigip=obj.facts())
        else:
            raise F5ModuleError("The route domain was not found")

class BigIpSoapApi(BigIpCommon):
    """Manipulate user accounts via SOAP
    """

    def __init__(self, *args, **kwargs):
        super(BigIpSoapApi, self).__init__(*args, **kwargs)

        self.api = bigip_api(kwargs['server'],
                             kwargs['user'],
                             kwargs['password'],
                             kwargs['validate_certs'],
                             kwargs['port'])
        self.proper_name = '/%s/%s' % (kwargs['partition'], kwargs['id'])

    def exists(self):
        exists = False
        with bigsuds.Transaction(self.api):
            # need to switch to root, set recursive query state
            current_folder = self.api.System.Session.get_active_folder()
            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder='/' + partition)

            current_query_state = self.api.System.Session.get_recursive_query_state()
            if current_query_state == 'STATE_DISABLED':
                self.api.System.Session.set_recursive_query_state('STATE_ENABLED')

            domains = self.api.Networking.RouteDomainV2.get_list()
            if self.proper_name in domains:
                exists = True

            # set everything back
            if current_query_state == 'STATE_DISABLED':
                self.api.System.Session.set_recursive_query_state('STATE_DISABLED')

            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder=current_folder)
        return exists

    def get_bw_controller_policy(self):
        return self.api.Networking.RouteDomainV2.get_bw_controller_policy(
            route_domains=[self.proper_name]
        )

    def get_connection_limit(self):
        return self.api.Networking.RouteDomainV2.get_connection_limit(
            route_domains=[self.proper_name]
        )

    def get_description(self):
        return self.api.Networking.RouteDomainV2.get_description(
            route_domains=[self.proper_name]
        )

    def get_eviction_policy(self):
        return self.api.Networking.RouteDomainV2.get_eviction_policy(
            route_domains=[self.proper_name]
        )

    def get_parent(self):
        return self.api.Networking.RouteDomainV2.get_parent(
            route_domains=[self.proper_name]
        )

    def get_route_domains(self):
        return self.api.Networking.RouteDomainV2.get_list()

    def get_routing_protocols(self):
        return self.api.Networking.RouteDomainV2.get_routing_protocols(
            route_domains=[self.proper_name]
        )

    def get_strict_isolation(self):
        return self.api.Networking.RouteDomainV2.get_strict_state(
            route_domains=[self.proper_name]
        )
    def get_vlan(self):
        return self.api.Networking.RouteDomainV2.get_vlan(
            route_domains=[self.proper_name]
        )

    def read(self):
        result = {}

        result['bandwidth_controller'] = self.get_bw_controller_policy()
        result['connection_limit'] = self.get_connection_limit()
        result['eviction_policy'] = self.get_eviction_policy()
        result['routing_protocols'] = self.get_routing_protocols()
        result['vlans'] = self.get_vlan()
        result['parent'] = self.get_parent()
        result['strict_isolation'] = self.get_strict_isolation()
        result['description'] = self.get_description()

        return result


class BigIpRestApi(BigIpCommon):
    """Get Route Domain facts via REST
    """

    def __init__(self, *args, **kwargs):
        super(BigIpRestApi, self).__init__(*args, **kwargs)

        self._headers = {
            'Content-Type': 'application/json'
        }

    def read(self):
        result = {}

        user = self.params['user']
        password = self.params['password']
        validate_certs = self.params['validate_certs']
        partition = self.params['partition']
        name = self.params['name']

        url = "%s/~%s~%s" % (self._uri, partition, name)
        resp = requests.get(url,
                            auth=(user, password),
                            verify=validate_certs)

        if resp.status_code == 200:
            res = resp.json()

            result['name'] = res['name']

            if 'apiAnonymous' in res:
                result['definition'] = res['apiAnonymous'].strip()
            else:
                result['definition'] = ''

        return result

    def exists(self):
        user = self.params['user']
        password = self.params['password']
        validate_certs = self.params['validate_certs']
        partition = self.params['partition']
        name = self.params['name']

        url = "%s/~%s~%s" % (self._uri, partition, name)
        resp = requests.get(url,
                            auth=(user, password),
                            verify=validate_certs)

        if resp.status_code != 200:
            return False
        else:
            return True

    def present(self):
        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True
            return self.create()


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        id = dict(required=True, type='int'),
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpApiFactory.factory(module)
        result = obj.flush()

        module.exit_json(**result)
    except bigsuds.ConnectionError, e:
        module.fail_json(msg="Could not connect to BIG-IP host")
    except requests.exceptions.SSLError:
        module.fail_json(msg='Certificate verification failed. Consider using validate_certs=no')
    except F5ModuleError, e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()