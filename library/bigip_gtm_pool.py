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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

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
  fallback_lb_method:
    description:
      - The load balancing mode that the system tries if both the
        C(preferred_lb_method) and C(alternate_lb_method)s are unsuccessful
        in picking a pool.
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
  fallback_ip:
    description:
      - Specifies the IPv4, or IPv6 address of the server to which the system
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

import copy

GTM_POOL_TYPES = [
    'a', 'aaaa', 'cname', 'mx', 'naptr', 'srv'
]


class BigIpGtmPoolManagerBase(object):
    def __init__(self, *args, **kwargs):
        self.api = None
        self.params = kwargs
        self.changed_params = dict()

    def apply_changes(self):
        result = dict()
        changed = self.apply_to_running_config()
        result.update(**self.changed_params)
        result.update(dict(changed=changed))
        return result

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
        self.validate_fallback_ip_args()
        if self.gtm_pool_exists():
            return self.update_gtm_pool()
        else:
            return self.ensure_gtm_pool_is_present()

    def validate_fallback_ip_args(self):
        """Verify the fallback IP parameters for lb method

        The fallback IP address is required if any of the lb method parameters
        is set to 'fallback-ip'. This method raises the necessary exceptions
        if the user specified a 'fallback-ip' value for any of their lb
        methods without also specifying a valid IP address

        :return:
        """
        methods = self.get_lb_method_parameter_values()
        if not any(l == 'fallback-ip' for l in methods):
            return

        if self.params['fallback_ip'] is None:
            raise F5ModuleError(
                "You must provide a valid IP address when specifying"
                "a preferred_lb_method of type 'fallback-ip'"
            )

        try:
            str(IPAddress(self.params['fallback_ip']))
        except AddrFormatError:
            raise F5ModuleError(
                'The provided fallback address is not a valid IP address'
            )

    def get_lb_method_parameter_values(self):
        result = list()
        result.append(self.params['preferred_lb_method'])
        result.append(self.params['alternate_lb_method'])
        result.append(self.params['fallback_lb_method'])
        return result

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
            result['alternate_lb_method'] = str(pool.alternateMode)
        if hasattr(pool, 'loadBalancingMode'):
            result['preferred_lb_method'] = str(pool.loadBalancingMode)
        if hasattr(pool, 'fallbackMode'):
            result['fallback_lb_method'] = str(pool.fallbackMode)

        # In later versions of BIG-IP this parameter was changed to
        # just be an IP address. I flatten all of them to a single
        # field and let the code decide based on the format of the
        # address and the version of BIG-IP.
        if hasattr(pool, 'fallbackIpv4'):
            result['fallback_ip'] = str(pool.fallbackIpv4)
        elif hasattr(pool, 'fallbackIpv6'):
            result['fallback_ip'] = str(pool.fallbackIpv6)
        elif hasattr(pool, 'fallbackIp'):
            result['fallback_ip'] = str(pool.fallbackIp)

        if hasattr(pool, 'verifyMemberAvailability'):
            availability = str(pool.verifyMemberAvailability)
            if availability == 'enabled':
                result['verify_member_availability'] = True
            else:
                result['verify_member_availability'] = False
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
        if self.is_preferred_lb_method_changed(current):
            result['loadBalancingMode'] = self.params['preferred_lb_method']
        if self.is_alternate_lb_method_changed(current):
            result['alternateMode'] = self.params['alternate_lb_method']
        if self.is_fallback_lb_method_changed(current):
            result['fallbackMode'] = self.params['fallback_lb_method']
        if self.should_fallback_ip_be_set(current):
            fallback_ip = self.format_fallback_ip()
            result.update(fallback_ip)
        return result

    def is_preferred_lb_method_changed(self, current):
        lb_method = self.params['preferred_lb_method']
        if lb_method is None:
            return False
        if 'preferred_lb_method' not in current:
            return True
        if lb_method != current['preferred_lb_method']:
            return True
        else:
            return False

    def is_alternate_lb_method_changed(self, current):
        lb_method = self.params['alternate_lb_method']
        if lb_method is None:
            return False
        if 'alternate_lb_method' not in current:
            return True
        if lb_method != current['alternate_lb_method']:
            return True
        else:
            return False

    def is_fallback_lb_method_changed(self, current):
        lb_method = self.params['fallback_lb_method']
        if lb_method is None:
            return False
        if 'fallback_lb_method' not in current:
            return True
        if lb_method != current['fallback_lb_method']:
            return True
        else:
            return False

    def should_fallback_ip_be_set(self, current):
        fallback_ip = self.params['fallback_ip']
        if fallback_ip is None:
            return False
        if 'fallback_ip' not in current:
            return True
        if fallback_ip != current['fallback_ip']:
            return True
        else:
            return False

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

    def get_gtm_pool_creation_parameters(self):
        result = dict(
            name=self.params['name'],
            partition=self.params['partition']
        )
        if self.params['preferred_lb_method']:
            result['loadBalancingMode'] = self.params['preferred_lb_method']
        if self.params['alternate_lb_method']:
            result['alternateMode'] = self.params['alternate_lb_method']
        if self.params['fallback_lb_method']:
            result['fallbackMode'] = self.params['fallback_lb_method']
        return result

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
        return super(BigIpTypedGtmPoolManager, self).present()

    def absent(self):
        self.resource = self.select_resource_by_type()
        return super(BigIpTypedGtmPoolManager, self).absent()

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
        result = super(BigIpTypedGtmPoolManager, self)\
            .get_gtm_pool_creation_parameters()

        if self.params['fallback_ip']:
            result.update(dict(fallbackIp=self.params['fallback_ip']))
        return result

    def create_gtm_pool_on_device(self, params):
        self.resource.create(**params)

    def delete_gtm_pool_from_device(self):
        pool = self.resource.load(
            name=self.params['name'],
            partition=self.params['partition']
        )
        pool.delete()

    def format_fallback_ip(self, address):
        try:
            return dict(fallbackIp=str(IPAddress(address)))
        except AddrFormatError:
            raise F5ModuleError(
                'The provided fallback address is not a valid IP address'
            )

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
        result = super(BigIpUntypedGtmPoolManager, self) \
            .get_gtm_pool_creation_parameters()

        if self.params['fallback_ip']:
            result.update(self.format_fallback_ip())
        return result

    def create_gtm_pool_on_device(self, params):
        self.api.tm.gtm.pools.pool.create(**params)

    def delete_gtm_pool_from_device(self):
        pool = self.api.tm.gtm.pools.pool.load(
            name=self.params['name'],
            partition=self.params['partition']
        )
        pool.delete()

    def format_fallback_ip(self, address):
        try:
            address = IPAddress(address)
            if address.version == 4:
                return dict(fallbackIpv4=str(address.ip))
            elif address.version == 6:
                return dict(fallbackIpv6=str(address.ip))
        except AddrFormatError:
            raise F5ModuleError(
                'The provided fallback address is not a valid IP address'
            )


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
        self.preferred_lb_methods = [
            'round-robin', 'return-to-dns', 'ratio', 'topology',
            'static-persistence', 'global-availability',
            'virtual-server-capacity', 'least-connections',
            'lowest-round-trip-time', 'fewest-hops', 'packet-rate', 'cpu',
            'completion-rate', 'quality-of-service', 'kilobytes-per-second',
            'drop-packet', 'fallback-ip', 'virtual-server-score'
        ]
        self.alternate_lb_methods = [
            'round-robin', 'return-to-dns', 'none', 'ratio', 'topology',
            'static-persistence', 'global-availability',
            'virtual-server-capacity', 'packet-rate', 'drop-packet',
            'fallback-ip', 'virtual-server-score'
        ]
        self.fallback_lb_methods = copy.copy(self.preferred_lb_methods)
        self.fallback_lb_methods.append('none')
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
            preferred_lb_method=dict(
                type='str',
                choices=self.preferred_lb_methods,
                default=None
            ),
            fallback_lb_method=dict(
                type='str',
                choices=self.fallback_lb_methods,
                default=None
            ),
            alternate_lb_method=dict(
                type='str',
                choices=self.alternate_lb_methods,
                default=None
            ),
            fallback_ip=dict(type='str', default=None),
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
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
