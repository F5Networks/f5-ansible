#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016 F5 Networks Inc.
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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

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
      - Virtual server name
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
  all_profiles:
    description:
      - List of all Profiles (HTTP, ClientSSL, ServerSSL, etc) that must be
        used by the virtual server
    required: false
    default: None
  all_rules:
    version_added: "2.2"
    description:
      - List of rules to be applied in priority order
    required: false
    default: None
  enabled_vlans:
    version_added: "2.2"
    description:
      - List of vlans to be enabled. When a VLAN named C(ALL) is used, all
        VLANs will be allowed.
    required: false
    default: None
  pool:
    description:
      - Default pool for the virtual server
    required: false
    default: None
  snat:
    description:
      - Source network address policy
    required: false
    choices:
      - None
      - Automap
      - Name of a SNAT pool (eg "/Common/snat_pool_name") to enable SNAT with the specific pool
    default: None
  default_persistence_profile:
    description:
      - Default Profile which manages the session persistence
    required: false
    default: None
  route_advertisement_state:
    description:
      - Enable route advertisement for destination
    required: false
    default: disabled
    version_added: "2.3"
  description:
    description:
      - Virtual server description
    required: false
    default: None
notes:
  - Requires BIG-IP software version >= 11
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
requirements:
  - bigsuds
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
      partition: MyPartition
      name: myvirtualserver
      destination: "{{ ansible_default_ipv4['address'] }}"
      port: 443
      pool: "{{ mypool }}"
      snat: Automap
      description: Test Virtual Server
      all_profiles:
          - http
          - clientssl
      enabled_vlans:
          - /Common/vlan2
  delegate_to: localhost

- name: Modify Port of the Virtual Server
  bigip_virtual_server:
      server: lb.mydomain.net
      user: admin
      password: secret
      state: present
      partition: MyPartition
      name: myvirtualserver
      port: 8080
  delegate_to: localhost

- name: Delete virtual server
  bigip_virtual_server:
      server: lb.mydomain.net
      user: admin
      password: secret
      state: absent
      partition: MyPartition
      name: myvirtualserver
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

try:
    from distutils.version import LooseVersion
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


STATES = {
    'enabled': 'STATE_ENABLED',
    'disabled': 'STATE_DISABLED'
}

STATUSES = {
    'enabled': 'SESSION_STATUS_ENABLED',
    'disabled': 'SESSION_STATUS_DISABLED',
    'offline': 'SESSION_STATUS_FORCED_DISABLED'
}


class BigIpVirtualServerManager(object):
    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = None

    def apply_changes(self):
        result = dict()
        changed = False

        try:
            self.api = self.connect_to_bigip(**self.params)

            if self.params['state'] == "present":
                changed = self.present()
            elif self.params['state'] == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.changed_params)
        result.update(dict(changed=changed))
        return result

    def present(self):
        if self.virtual_server_exists():
            return self.update_virtual_server()
        else:
            return self.ensure_virtual_server_is_present()

    def absent(self):
        changed = False
        if self.virtual_server_exists():
            changed = self.ensure_virtual_server_is_absent()
        return changed

    def connect_to_bigip(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

    def read_virtual_server_information(self):
        server = self.load_virtual_server()
        return self.format_virtual_server_information(server)

    def format_virtual_server_information(self, server):
        result = dict()
        result['name'] = str(server.name)
        if hasattr(user, 'description'):
            result['full_name'] = str(user.description)
        if hasattr(user, 'shell'):
            result['shell'] = str(user.shell)
        return result

    def load_virtual_server(self):
        return self.api.tm.ltm.virtuals.virtual.load(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def virtual_server_exists(self):
        return self.api.tm.ltm.virtuals.virtual.__exists(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def update_virtual_server(self):
        params = self.get_changed_parameters()
        if params:
            self.changed_params = camel_dict_to_snake_dict(params)
            if self.params['check_mode']:
                return True
        else:
            return False
        params['name'] = self.params['name']
        params['partition'] = self.params['partition']
        self.update_virtual_server_on_device(params)
        return True

    def update_virtual_server_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            server = api.tm.ltm.virtuals.virtual.load(
                name=self.params['name'],
                partition=self.params['partition']
            )
            server.modify(**params)

    def get_changed_parameters(self):
        result = dict()
        current = self.read_virtual_server_information()
        if self.is_description_changed(current):
            result['description'] = self.params['full_name']
        if self.is_password_changed():
            result['password'] = self.params['password_credential']
        if self.is_shell_changed(current):
            result['shell'] = self.params['shell']
        return result

    def is_port_changed(self, current):
        port = self.params['port']
        if full_name is None:
            return False
        if 'full_name' not in current:
            return True
        if full_name != current['full_name']:
            return True
        else:
            return False

    def ensure_virtual_server_is_present(self):
        params = self.get_virtual_server_creation_parameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.create_virtual_server_on_device(params)
        if self.virtual_server_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the virtual server")

    def get_virtual_server_creation_parameters(self):
        result = dict(
            name=self.params['username_credential'],
            partition=self.params['partition']
        )

        if self.params['port'] is not None:
            if self.params['port'] < 1:
                raise F5ModuleError(
                    "Valid ports must be in range 1 - 65535"
                )
            elif self.params['port'] > 65535:
                raise F5ModuleError(
                    "Valid ports must be in range 1 - 65535"
                )
            result['port'] = self.params['port']

    def create_virtual_server_on_device(self, params):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            api.tm.ltm.virtuals.virtual.create(**params)

    def ensure_virtual_server_is_absent(self):
        if self.params['check_mode']:
            return True
        self.delete_virtual_server_from_device()
        if self.virtual_server_exists():
            raise F5ModuleError("Failed to delete the virtual server")
        return True

    def delete_virtual_server_from_device(self):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            server = api.tm.ltm.virtuals.virtual.load(
                name=self.params['name'],
                partition=self.params['partition']
            )
            server.delete()










def vs_create(api, name, destination, port, pool):
    _profiles = [[{'profile_context': 'PROFILE_CONTEXT_TYPE_ALL', 'profile_name': 'tcp'}]]
    created = False
    # a bit of a hack to handle concurrent runs of this module.
    # even though we've checked the vs doesn't exist,
    # it may exist by the time we run create_vs().
    # this catches the exception and does something smart
    # about it!
    try:
        api.LocalLB.VirtualServer.create(
            definitions=[{'name': [name], 'address': [destination], 'port': port, 'protocol': 'PROTOCOL_TCP'}],
            wildmasks=['255.255.255.255'],
            resources=[{'type': 'RESOURCE_TYPE_POOL', 'default_pool_name': pool}],
            profiles=_profiles)
        created = True
        return created
    except bigsuds.OperationFailed as e:
        if "already exists" not in str(e):
            raise Exception('Error on creating Virtual Server : %s' % e)



def get_rules(api, name):
    return api.LocalLB.VirtualServer.get_rule(
        virtual_servers=[name]
    )[0]


def set_rules(api, name, rules_list):
    updated = False
    if rules_list is None:
        return False
    rules_list = list(enumerate(rules_list))
    try:
        current_rules = map(lambda x: (x['priority'], x['rule_name']), get_rules(api, name))
        to_add_rules = []
        for i, x in rules_list:
            if (i, x) not in current_rules:
                to_add_rules.append({'priority': i, 'rule_name': x})
        to_del_rules = []
        for i, x in current_rules:
            if (i, x) not in rules_list:
                to_del_rules.append({'priority': i, 'rule_name': x})
        if len(to_del_rules) > 0:
            api.LocalLB.VirtualServer.remove_rule(
                virtual_servers=[name],
                rules=[to_del_rules]
            )
            updated = True
        if len(to_add_rules) > 0:
            api.LocalLB.VirtualServer.add_rule(
                virtual_servers=[name],
                rules=[to_add_rules]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting rules : %s' % e)


def get_profiles(api, name):
    return api.LocalLB.VirtualServer.get_profile(
        virtual_servers=[name]
    )[0]


def set_profiles(api, name, profiles_list):
    updated = False
    try:
        if profiles_list is None:
            return False
        current_profiles = list(map(lambda x: x['profile_name'], get_profiles(api, name)))
        to_add_profiles = []
        for x in profiles_list:
            if x not in current_profiles:
                to_add_profiles.append({'profile_context': 'PROFILE_CONTEXT_TYPE_ALL', 'profile_name': x})
        to_del_profiles = []
        for x in current_profiles:
            if (x not in profiles_list) and (x != "/Common/tcp"):
                to_del_profiles.append({'profile_context': 'PROFILE_CONTEXT_TYPE_ALL', 'profile_name': x})
        if len(to_del_profiles) > 0:
            api.LocalLB.VirtualServer.remove_profile(
                virtual_servers=[name],
                profiles=[to_del_profiles]
            )
            updated = True
        if len(to_add_profiles) > 0:
            api.LocalLB.VirtualServer.add_profile(
                virtual_servers=[name],
                profiles=[to_add_profiles]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting profiles : %s' % e)


def get_vlan(api, name):
    return api.LocalLB.VirtualServer.get_vlan(
        virtual_servers=[name]
    )[0]


def set_enabled_vlans(api, name, vlans_enabled_list):
    updated = False
    to_add_vlans = []
    try:
        if vlans_enabled_list is None:
            return updated
        current_vlans = get_vlan(api, name)

        # Set allowed list back to default ("all")
        #
        # This case allows you to undo what you may have previously done.
        # The default case is "All VLANs and Tunnels". This case will handle
        # that situation.
        if 'ALL' in vlans_enabled_list:
            # The user is coming from a situation where they previously
            # were specifying a list of allowed VLANs
            if len(current_vlans['vlans']) > 0 or \
               current_vlans['state'] is "STATE_ENABLED":
                api.LocalLB.VirtualServer.set_vlan(
                    virtual_servers=[name],
                    vlans=[{'state': 'STATE_DISABLED', 'vlans': []}]
                )
                updated = True
        else:
            if current_vlans['state'] is "STATE_DISABLED":
                to_add_vlans = vlans_enabled_list
            else:
                for vlan in vlans_enabled_list:
                    if vlan not in current_vlans['vlans']:
                        updated = True
                        to_add_vlans = vlans_enabled_list
                        break
            if updated:
                api.LocalLB.VirtualServer.set_vlan(
                    virtual_servers=[name],
                    vlans=[{
                        'state': 'STATE_ENABLED',
                        'vlans': [to_add_vlans]
                    }]
                )

        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting enabled vlans : %s' % e)


def set_snat(api, name, snat):
    updated = False
    try:
        current_state = get_snat_type(api, name)
        current_snat_pool = get_snat_pool(api, name)
        if snat is None:
            return updated
        elif snat == 'None' and current_state != 'SRC_TRANS_NONE':
            api.LocalLB.VirtualServer.set_source_address_translation_none(
                virtual_servers=[name]
            )
            updated = True
        elif snat == 'Automap' and current_state != 'SRC_TRANS_AUTOMAP':
            api.LocalLB.VirtualServer.set_source_address_translation_automap(
                virtual_servers=[name]
            )
            updated = True
        elif snat_settings_need_updating(snat, current_state, current_snat_pool):
            api.LocalLB.VirtualServer.set_source_address_translation_snat_pool(
                virtual_servers=[name],
                pools=[snat]
            )
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting snat : %s' % e)


def get_snat_type(api, name):
    return api.LocalLB.VirtualServer.get_source_address_translation_type(
        virtual_servers=[name]
    )[0]


def get_snat_pool(api, name):
    return api.LocalLB.VirtualServer.get_source_address_translation_snat_pool(
        virtual_servers=[name]
    )[0]


def snat_settings_need_updating(snat, current_state, current_snat_pool):
    if snat == 'None' or snat == 'Automap':
        return False
    elif snat and current_state != 'SRC_TRANS_SNATPOOL':
        return True
    elif snat and current_state == 'SRC_TRANS_SNATPOOL' and current_snat_pool != snat:
        return True
    else:
        return False


def get_pool(api, name):
    return api.LocalLB.VirtualServer.get_default_pool_name(
        virtual_servers=[name]
    )[0]


def set_pool(api, name, pool):
    updated = False
    try:
        current_pool = get_pool(api, name)
        if pool is not None and (pool != current_pool):
            api.LocalLB.VirtualServer.set_default_pool_name(
                virtual_servers=[name],
                default_pools=[pool]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting pool : %s' % e)


def get_destination(api, name):
    return api.LocalLB.VirtualServer.get_destination_v2(
        virtual_servers=[name]
    )[0]


def set_destination(api, name, destination):
    updated = False
    try:
        current_destination = get_destination(api, name)
        if destination is not None and destination != current_destination['address']:
            api.LocalLB.VirtualServer.set_destination_v2(
                virtual_servers=[name],
                destinations=[{'address': destination, 'port': current_destination['port']}]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting destination : %s' % e)


def set_port(api, name, port):
    updated = False
    try:
        current_destination = get_destination(api, name)
        if port is not None and port != current_destination['port']:
            api.LocalLB.VirtualServer.set_destination_v2(
                virtual_servers=[name],
                destinations=[{'address': current_destination['address'], 'port': port}]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting port : %s' % e)


def get_state(api, name):
    return api.LocalLB.VirtualServer.get_enabled_state(
        virtual_servers=[name]
    )[0]


def set_state(api, name, state):
    updated = False
    try:
        current_state = get_state(api, name)
        # We consider that being present is equivalent to enabled
        if state == 'present':
            state = 'enabled'
        if STATES[state] != current_state:
            api.LocalLB.VirtualServer.set_enabled_state(
                virtual_servers=[name],
                states=[STATES[state]]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting state : %s' % e)


def get_description(api, name):
    return api.LocalLB.VirtualServer.get_description(
        virtual_servers=[name]
    )[0]


def set_description(api, name, description):
    updated = False
    try:
        current_description = get_description(api, name)
        if description is not None and current_description != description:
            api.LocalLB.VirtualServer.set_description(
                virtual_servers=[name],
                descriptions=[description]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting description : %s ' % e)


def get_persistence_profiles(api, name):
    return api.LocalLB.VirtualServer.get_persistence_profile(
        virtual_servers=[name]
    )[0]


def set_default_persistence_profiles(api, name, persistence_profile):
    updated = False
    if persistence_profile is None:
        return updated
    try:
        current_persistence_profiles = get_persistence_profiles(api, name)
        default = None
        for profile in current_persistence_profiles:
            if profile['default_profile']:
                default = profile['profile_name']
                break
        if default is not None and default != persistence_profile:
            api.LocalLB.VirtualServer.remove_persistence_profile(
                virtual_servers=[name],
                profiles=[[{'profile_name': default, 'default_profile': True}]]
            )
        if default != persistence_profile:
            api.LocalLB.VirtualServer.add_persistence_profile(
                virtual_servers=[name],
                profiles=[[{'profile_name': persistence_profile, 'default_profile': True}]]
            )
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting default persistence profile : %s' % e)


def get_route_advertisement_status(api, address):
    result = api.LocalLB.VirtualAddressV2.get_route_advertisement_state(virtual_addresses=[address]).pop(0)
    result = result.split("STATE_")[-1].lower()
    return result


def set_route_advertisement_state(api, destination, partition, route_advertisement_state):
    updated = False

    try:
        state = "STATE_%s" % route_advertisement_state.strip().upper()
        address = fq_name(partition, destination,)
        current_route_advertisement_state=get_route_advertisement_status(api,address)
        if current_route_advertisement_state != route_advertisement_state:
            api.LocalLB.VirtualAddressV2.set_route_advertisement_state(virtual_addresses=[address], states=[state])
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception('Error on setting profiles : %s' % e)



class BigIpVirtualServerModuleConfig(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.states = ['present', 'absent', 'disabled', 'enabled']

        self.initialize_meta_args()
        self.initialize_argument_spec()

    def initialize_meta_args(self):
        args = dict(
            state=dict(
                type='str',
                default='present',
                choices=self.states
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
            port=dict(type='int', default=None),
            all_profiles=dict(type='list', default=None),
            all_rules=dict(type='list', default=None),
            enabled_vlans=dict(type='list', default=None),
            pool=dict(type='str', default=None),
            description=dict(type='str', default=None),
            snat=dict(type='str', default=None),
            route_advertisement_state=dict(
                type='str',
                default=None,
                choices=['enabled', 'disabled']
            ),
            default_persistence_profile=dict(type='str', default=None)
        )
        self.meta_args = args

    def initialize_argument_spec(self):
        self.argument_spec = f5_argument_spec()
        self.argument_spec.update(self.meta_args)

    def create(self):
        return AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=self.supports_check_mode
        )


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    config = BigIpVirtualServerModuleConfig()
    module = config.create()

    try:
        obj = BigIpVirtualServerManager(
            check_mode=module.check_mode, **module.params
        )
        result = obj.apply_changes()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import camel_dict_to_snake_dict
from ansible.module_utils.f5 import *


if __name__ == '__main__':
    main()











"""

def main():
    name = fq_name(partition, module.params['name'])
    all_profiles = fq_list_names(partition, module.params['all_profiles'])
    all_rules = fq_list_names(partition, module.params['all_rules'])

    enabled_vlans = module.params['enabled_vlans']
    if enabled_vlans is None or 'ALL' in enabled_vlans:
        all_enabled_vlans = enabled_vlans
    else:
        all_enabled_vlans = fq_list_names(partition, enabled_vlans)

    pool = fq_name(partition, module.params['pool'])
    default_persistence_profile = fq_name(partition, module.params['default_persistence_profile'])





        else:
            update = False
            if not vs_exists(api, name):
                if (not destination) or (not port):
                    module.fail_json(msg="both destination and port must be supplied to create a VS")
                if not module.check_mode:
                    do stuff
                else:
                    # check-mode return value
                    result = {'changed': True}
            else:
                update = True
            if update:
                # VS exists
                if not module.check_mode:
                    do stuff
                else:
                    # check-mode return value
                    result = {'changed': True}
"""