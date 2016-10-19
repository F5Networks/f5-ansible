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

DOCUMENTATION = '''
---
module: bigip_gtm_pool
short_description: Manages F5 BIG-IP GTM pools.
description:
    - Manages F5 BIG-IP GTM pools.
version_added: "2.3"
options:
  state:
    description:
        - Pool member state. When C(present), ensures that the pool is
          created and enabled. When C(absent), ensures that the pool is
          removed from the system. When C(enabled) or C(disabled), ensures
          that the pool is enabled or disabled (respectively) on the remote
          device.
    required: true
    choices:
      - present
      - absent
      - enabled
      - disabled
  preferred_lb_method:
    description:
      - The load balancing mode that the system tries first.
    required: False
    default: None
    choices:
      - round-robin
      - return-to-dns
      - ratio
      - topology
      - static-persistence
      - global-availability
      - virtual-server-capacity
      - least-connections
      - lowest-round-trip-time
      - fewest-hops
      - packet-rate
      - cpu
      - completion-rate
      - quality-of-service
      - kilobytes-per-second
      - drop-packet
      - fallback-ip
      - virtual-server-score
  alternate_lb_method:
    description:
      - The load balancing mode that the system tries if the
        C(preferred_lb_method) is unsuccessful in picking a pool.
    required: False
    default: None
    choices:
      - round-robin
      - return-to-dns
      - none
      - ratio
      - topology
      - static-persistence
      - global-availability
      - virtual-server-capacity
      - packet-rate
      - drop-packet
      - fallback-ip
      - virtual-server-score
  fallback_ipv4
  fallback_ipv6:
    description:
      - Specifies the IPv4 address of the server to which the system
        directs requests when it cannot use one of its pools to do so.
        Note that the system uses the fallback IP only if you select the
        C(fallback_ip) load balancing method.
    required: False
    default: None
  type:
    description:
      - The type of GTM pool that you want to create. On BIG-IP releases
        prior to version 12, this parameter is not supported.
    choices:
      - a
      - aaaa
      - cname
      - mx
      - naptr
      - srv
  name:
    description:
      - Name of the GTM pool.
    required: true
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as
    pip install f5-sdk
  - Requires the netaddr Python package on the host. This is as easy as
    pip install netaddr
extends_documentation_fragment: f5
requirements:
  - f5-sdk
  - netaddr
author:
  - Tim Rupp (@caphrim007)
'''

RETURN = '''
changed:
    description: Denotes if the F5 configuration was updated
    returned: always
    type: bool
'''

EXAMPLES = '''
  - name: Disable pool
    bigip_gtm_pool:
        server: "lb.mydomain.com"
        user: "admin"
        password: "secret"
        state: "disabled"
        pool: "my_pool"
    delegate_to: localhost
'''

try:
    from distutils.version import LooseVersion
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

try:
    from netaddr import IPAddress, AddrFormatError
    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False

GTM_POOL_TYPES = [
    'a', 'aaaa', 'cname', 'mx', 'naptr', 'srv'
]

class BigIpGtmPoolManagerBase(object):
    def __init__(self, *args, **kwargs):
        self.api = None
        self.changed_params = dict()

    def apply_changes(self):
        result = dict()

        changed = self.apply_to_running_config()
        if changed:
            self.save_running_config()

        result.update(**self.changed_params)
        result.update(dict(changed=changed))
        return result

    def apply_to_running_config(self):
        try:
            self.api = self.connect_to_bigip(**self.params)
            if self.params['state'] == "present":
                return self.present()
            elif self.params['state'] == "absent":
                return self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

    def present(self):
        if self.gtm_pool_exists():
            return self.update_gtm_pool()
        else:
            return self.ensure_gtm_pool_is_present()

    def absent(self):
        changed = False
        if self.gtm_pool_exists():
            changed = self.ensure_gtm_pool_is_absent()
        return changed

    def read_gtm_pool_information(self):
        pool = self.load_gtm_pool()
        return self.format_gtm_pool_information(pool)

    def format_gtm_pool_information(self, pool):
        """Ensure that the pool information is in a standard format

        The SDK provides information back in a format that may change with
        the version of BIG-IP being worked with. Therefore, we need to make
        sure that the data is formatted in a way that our module expects it.

        Additionally, this takes care of minor variations between Python 2
        and Python 3.

        :param pool:
        :return:
        """
        result = dict()
        result['name'] = str(pool.name)
        if hasattr(pool, 'alternateMode'):
            result['alternate_mode'] = str(pool.alternateMode)
        return result

    def update_gtm_pool(self):
        params = self.get_changed_parameters()
        if params:
            self.changed_params = camel_dict_to_snake_dict(params)
            if self.params['check_mode']:
                return True
        else:
            return False
        params['name'] = self.params['name']
        params['partition'] = self.params['partition']
        self.update_gtm_pool_on_device(params)
        return True

    def save_running_config(self):
        self.api.tm.sys.config.exec_cmd('save')

    def get_changed_parameters(self):
        result = dict()
        current = self.read_gtm_pool_information()
        if self.are_members_changed(current):
            result['members'] = self.get_new_member_list(current['members'])
        return result

    def ensure_gtm_pool_is_present(self):
        params = self.get_gtm_pool_creation_parameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.create_gtm_pool_on_device(params)
        if self.gtm_pool_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the GTM pool")

    def ensure_gtm_pool_is_absent(self):
        if self.params['check_mode']:
            return True
        self.delete_gtm_pool_from_device()
        if self.gtm_pool_exists():
            raise F5ModuleError("Failed to delete the GTM pool")
        return True

    def connect_to_bigip(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

class BigIpTypedGtmPoolManager(BigIpGtmPoolManagerBase):
    def __init__(self, *args, **kwargs):
        super(BigIpTypedGtmPoolManager, self).__init__()
        self.params = kwargs
        self.resource = None

    def select_resource_by_type(self):
        type = self.params['type']

        if type == 'a':
            collection_name = 'a_s'
        elif type == 'aaaa':
            collection_name = 'aaaas'
        elif type == 'cname':
            collection_name = 'cnames',
        elif type == 'mx':
            collection_name = 'mxs',
        elif type == 'naptr':
            collection_name = 'naptrs',
        elif type == 'srv':
            collection_name = 'srvs'
        else:
            raise F5ModuleError(
                "Specified GTM pool type is invalid"
            )

        collection = getattr(self.api.tm.gtm.pools, collection_name)
        return getattr(collection, type)

    def present(self):
        if self.params['type'] is None:
            raise F5ModuleError(
                "A pool 'type' must be specified"
            )
        elif self.params['type'] not in GTM_POOL_TYPES:
            raise F5ModuleError(
                "The specified pool type is invalid"
            )

        self.resource = self.select_resource_by_type()
        super(BigIpTypedGtmPoolManager, self).present()

    def load_gtm_pool(self):
        return self.resource.load(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def gtm_pool_exists(self):
        return self.resource.exists(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def update_gtm_pool_on_device(self, params):
        r = self.resource.load(
            name=self.params['name'],
            partition=self.params['partition']
        )
        r.modify(**params)

    def get_gtm_pool_creation_parameters(self):
        members = self.get_formatted_members_list()
        return dict(
            name=self.params['name'],
            partition=self.params['partition'],
            members=members
        )

    def create_gtm_pool_on_device(self, params):
        self.resource.create(**params)

    def delete_gtm_pool_from_device(self):
        pool = self.resource.load(
            name=self.params['name'],
            partition=self.params['partition']
        )
        pool.delete()

class BigIpUntypedGtmPoolManager(BigIpGtmPoolManagerBase):
    def __init__(self, *args, **kwargs):
        super(BigIpUntypedGtmPoolManager, self).__init__()
        self.params = kwargs

    def load_gtm_pool(self):
        return self.api.tm.gtm.pools.pool.load(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def gtm_pool_exists(self):
        return self.api.tm.gtm.pools.pool.exists(
            name=self.params['name'],
            partition=self.params['partition']
        )

    def update_gtm_pool_on_device(self, params):
        r = self.api.tm.gtm.pools.pool.load(
            name=self.params['name'],
            partition=self.params['partition']
        )
        r.modify(**params)

    def get_gtm_pool_creation_parameters(self):
        members = self.get_formatted_members_list()
        return dict(
            name=self.params['name'],
            partition=self.params['partition'],
            members=members
        )

    def create_gtm_pool_on_device(self, params):
        self.api.tm.gtm.pools.pool.create(**params)

    def delete_gtm_pool_from_device(self):
        pool = self.api.tm.gtm.pools.pool.load(
            name=self.params['name'],
            partition=self.params['partition']
        )
        pool.delete()

class BigIpGtmPoolManager(object):
    def __init__(self, *args, **kwargs):
        self.params = kwargs
        self.api = None

    def apply_changes(self):
        self.api = self.connect_to_bigip(**self.params)
        if self.is_version_less_than_12():
            manager = BigIpUnTypedGtmPoolManager(**self.params)
        else:
            manager = BigIpTypedGtmPoolManager(**self.params)
        return manager.apply_changes()

    def is_version_less_than_12(self):
        """Checks to see if the TMOS version is less than 12

        Anything less than BIG-IP 12.x does not support typed pools.

        :return:
        """
        version = self.api.tmos_version
        if LooseVersion(version) < LooseVersion('12.0.0'):
            return True
        else:
            return False

    def connect_to_bigip(self, **kwargs):
        return ManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])


class BigIpGtmPoolModuleConfig(object):
    def __init__(self):
        self.argument_spec = dict()
        self.meta_args = dict()
        self.supports_check_mode = True
        self.states = ['absent', 'present', 'enabled', 'disabled']
        self.lb_methods = [
            'round-robin', 'return-to-dns', 'ratio', 'topology',
            'static-persistence', 'global-availability',
            'virtual-server-capacity', 'least-connections',
            'lowest-round-trip-time', 'fewest-hops', 'packet-rate', 'cpu',
            'completion-rate', 'quality-of-service', 'kilobytes-per-second',
            'drop-packet', 'fallback-ip', 'virtual-server-score'
        ]
        self.types = GTM_POOL_TYPES
        self.initialize_meta_args()
        self.initialize_argument_spec()

    def initialize_meta_args(self):
        args = dict(
            name=dict(required=True),
            state=dict(
                default='present',
                choices=self.states,
            ),
            lb_method=dict(
                type='str',
                choices=self.lb_methods,
                default=None
            ),
            type=dict(
                type='str',
                choices=self.types,
                default=None
            )
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

    if not HAS_NETADDR:
        raise F5ModuleError("The python netaddr module is required")

    config = BigIpGtmPoolModuleConfig()
    module = config.create()

    try:
        obj = BigIpGtmPoolManager(
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
