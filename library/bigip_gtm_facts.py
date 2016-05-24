#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2015, Michael Perzel
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
module: bigip_gtm_facts
short_description: "Collect facts from F5 BIG-IP GTM devices"
description:
    - "Collect facts from F5 BIG-IP GTM devices"
version_added: "2.2"
author: 'Michael Perzel'
notes:
    - "Requires BIG-IP software version >= 11.4"
    - "F5 developed module 'bigsuds' required (see http://devcentral.f5.com)"
    - "Best run as a local_action in your playbook"
    - "Tested with manager and above account privilege level"
requirements:
    - bigsuds
    - re
options:
    server:
        description:
            - BIG-IP host
        required: true
        default: null
        choices: []
        aliases: []
    user:
        description:
            - BIG-IP username
        required: true
        default: null
        choices: []
        aliases: []
    password:
        description:
            - BIG-IP password
        required: true
        default: null
        choices: []
        aliases: []
    include:
        description:
            - Fact category to collect
        required: true
        choices: ['pool','wide_ip','virtual_server']
        aliases: []
    fact_filter:
        description:
            - Perform regex filter of response
        required: false
        default: None
        aliases: []
'''

RETURN = '''
bigip_gtm_facts:
    description: Details about GTM wide ip, pool, virtual servers
    returned: success
    type: dictionary
    contains:
        wide_ip:
            description: Contains the lb method for the wide ip and the pools that are within the wide ip
            returned: when include contains wide_ip
            type: dictionary
            sample: '{"wide_ip": {"/Common/test.example.com": {"lb_method": "LB_METHOD_ROUND_ROBIN", "pool": [{"order": 0, "pool_name": "/Common/MN-test.example.com", "ratio": 1}, {"order": 1, "pool_name": "/Common/VA-test.example.com", "ratio": 1}]}}}'
        pool:
            description: Contains the pool object status and enabled status
            returned: when include contains pool
            type: dictionary
            sample: '{"pool": {"/Common/VA-test.example.com": {"member": [{"name": "VA-test_example_com", "server": "/Common/VA-Server"}], "object_status": {"availability_status": "AVAILABILITY_STATUS_RED", "enabled_status": "ENABLED_STATUS_DISABLED", "status_description": "No enabled pool members available: disabled directly"}}}}'
        virtual_server:
            description: Contains the virtual server enabled and availability status, and address
            returned: when include contains virtual_server
            type: dictionary
            sample: '{"virtual_server": {"/Common/MN-LTM": {"mn-test_example_com": {"address": {"address": "192.168.1.1", "port": 80}, "enabled_state": "STATE_ENABLED", "object_status": {"availability_status": "AVAILABILITY_STATUS_GREEN", "enabled_status": "ENABLED_STATUS_ENABLED", "status_description": " Monitor /Common/bigip from 192.168.0.1 : UP"}}, "va-test_example_com": {"address": {"address": "192.168.1.2", "port": 80}, "enabled_state": "STATE_ENABLED", "object_status": {"availability_status": "AVAILABILITY_STATUS_GREEN", "enabled_status": "ENABLED_STATUS_ENABLED", "status_description": " Monitor /Common/bigip from 192.168.0.1 : UP"}}}}}'
'''

EXAMPLES = '''
  - name: Get pool facts
    local_action: >
      bigip_gtm_facts
      server=192.168.0.1
      user=admin
      password=mysecret
      include=pool
      fact_filter=my_pool
'''

import re


class F5(object):
    def __init__(self, host, user, password, validate_certs, session=False):
        self.api = bigip_api(host, user, password, validate_certs)
        if session:
            self.start_session()

    def get_api(self):
        return self.api


class Pools(object):
    def __init__(self, api, regex=None):
        self.api = api
        self.pool_names = api.GlobalLB.Pool.get_list()
        if regex:
            re_filter = re.compile(regex)
            self.pool_names = filter(re_filter.search, self.pool_names)

    def get_list(self):
        return self.pool_names

    def get_object_status(self):
        return self.api.GlobalLB.Pool.get_object_status(self.pool_names)

    def get_lb_method(self):
        return self.api.GlobalLB.Pool.get_lb_method(self.pool_names)

    def get_member(self):
        return self.api.GlobalLB.Pool.get_member_v2(self.pool_names)


class VirtualServers(object):
    def __init__(self, api, regex=None):
        self.api = api
        self.virtual_servers = api.GlobalLB.VirtualServerV2.get_list()
        if regex:
            self.virtual_servers = [d for d in self.virtual_servers if regex in d['server'] or regex in d['name']]

    def get_list(self):
        return self.virtual_servers

    def get_enabled_state(self):
        return self.api.GlobalLB.VirtualServerV2.get_enabled_state(self.virtual_servers)

    def get_object_status(self):
        return self.api.GlobalLB.VirtualServerV2.get_object_status(self.virtual_servers)

    def get_address(self):
        return self.api.GlobalLB.VirtualServerV2.get_address(self.virtual_servers)


class WideIps(object):
    def __init__(self, api, regex=None):
        self.api = api
        self.wide_ips = api.GlobalLB.WideIP.get_list()
        if regex:
            re_filter = re.compile(regex)
            self.wide_ips = filter(re_filter.search, self.wide_ips)

    def get_list(self):
        return self.wide_ips

    def get_lb_method(self):
        return self.api.GlobalLB.WideIP.get_lb_method(self.wide_ips)

    def get_pool(self):
        return self.api.GlobalLB.WideIP.get_wideip_pool(self.wide_ips)


def generate_pool_dict(f5, regex):
    pools = Pools(f5.get_api(), regex)
    fields = ['member', 'object_status']
    return generate_dict(pools, fields)


def generate_wide_ip_dict(f5, regex):
    wide_ips = WideIps(f5.get_api(), regex)
    fields = ['lb_method', 'pool']
    return generate_dict(wide_ips, fields)


def generate_virtual_server_dict(f5, regex):
    virtual_servers = VirtualServers(f5.get_api(), regex)
    fields = ['enabled_state', 'object_status',
              'ltm_virtual_server', 'statistics', 'address']
    attributes = {}
    lists = []
    supported_fields = []
    servers = {}
    for i, j in enumerate(virtual_servers.get_list()):
        for field in fields:
            try:
                api_response = getattr(virtual_servers, "get_" + field)()
            except Exception:  # Removed specific exceptions
                pass
            else:
                lists.append(api_response)
                supported_fields.append(field)
        temp = {}
        temp.update([(item[0], item[1][i]) for item in zip(supported_fields, lists)])
        attributes = temp
        if j['server'] not in servers:
            names = {j['name']: attributes}
            servers.update({j['server']: names})
        else:
            names = servers[j['server']]
            names.update({j['name']: attributes})
            servers.update({j['server']: names})
    return servers


def generate_dict(api_obj, fields):
    result_dict = {}
    lists = []
    supported_fields = []
    if api_obj.get_list():
        for field in fields:
            try:
                api_response = getattr(api_obj, "get_" + field)()
            except Exception:  # Removed specific exceptions
                pass
            else:
                lists.append(api_response)
                supported_fields.append(field)
        for i, j in enumerate(api_obj.get_list()):
            temp = {}
            temp.update([(item[0], item[1][i]) for item in zip(supported_fields, lists)])
            result_dict[j] = temp
    return result_dict


def main():
    argument_spec = f5_argument_spec()

    valid_includes = ['pool', 'wide_ip', 'virtual_server']

    meta_args = dict(
        include=dict(type='list', required=True),
        fact_filter=dict(type='str', required=False)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    if not bigsuds_found:
        module.fail_json(msg="the python bigsuds module is required")

    server = module.params['server']
    user = module.params['user']
    password = module.params['password']
    validate_certs = module.params['validate_certs']

    fact_filter = module.params['fact_filter']
    include = map(lambda x: x.lower(), module.params['include'])

    include_test = map(lambda x: x in valid_includes, include)
    if not all(include_test):
        module.fail_json(msg="value of include must be one or more of: %s, got: %s" % (",".join(valid_includes), ",".join(include)))

    facts = {}

    if fact_filter:
        regex = fact_filter
    else:
        regex = None

    try:
        if len(include) > 0:
            f5 = F5(server, user, password, validate_certs)
            if 'pool' in include:
                facts['pool'] = generate_pool_dict(f5, regex)
            if 'virtual_server' in include:
                facts['virtual_server'] = generate_virtual_server_dict(f5, regex)
            if 'wide_ip' in include:
                facts['wide_ip'] = generate_wide_ip_dict(f5, regex)
            result = {'ansible_facts': facts}
    except Exception as e:
        module.fail_json(msg="received exception: %s" % e)

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
