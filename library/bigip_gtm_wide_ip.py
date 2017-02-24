#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
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
module: bigip_gtm_wide_ip
short_description: Manages F5 BIG-IP GTM wide ip.
description:
  - Manages F5 BIG-IP GTM wide ip.
version_added: "2.0"
options:
  lb_method:
    description:
      - Specifies the load balancing method used to select a pool in this wide
        IP. This setting is relevant only when multiple pools are configured
        for a wide IP.
    required: True
    choices:
      - round-robin
      - ratio
      - topology
      - global-availability
  name:
    description:
      - Wide IP name. This name must be formatted as a fully qualified
        domain name (FQDN). You can also use the alias C(wide_ip) but this
        is deprecated and will be removed in a future Ansible version.
    required: True
    aliases
      - wide_ip
  type:
    description:
      - Specifies the type of wide IP. GTM wide IPs need to be keyed by query
        type in addition to name, since pool members need different attributes
        depending on the response RDATA they are meant to supply. This value
        is required if you are using BIG-IP versions >= 12.0.0.
    required: False
    choices:
      - a
      - aaaa
      - cname
      - mx
      - naptr
      - srv
    version_added: 2.4
  state:
    description:
      - When C(present), ensures that the Wide IP exists and is enabled.
        When C(absent), ensures that the Wide IP has been removed. When
        C(disabled), ensures that the Wide IP exists and is disabled.
    required: False
    default: present
    choices:
      - present
      - absent
      - disabled
    version_added: 2.4
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Set lb method
  bigip_gtm_wide_ip:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      lb_method: "round-robin"
      name: "my-wide-ip.example.com"
  delegate_to: localhost
'''

RETURN = '''

'''

import re

from ansible.module_utils.f5_utils import *


class Parameters(AnsibleF5Parameters):
    param_api_map = dict(
        lb_method='poolLbMode',
        state='state',
        name='name'
    )

    @property
    def lb_method(self):
        deprecated = [
            'return_to_dns', 'null', 'ratio', 'topology', 'static_persist',
            'vs_capacity', 'least_conn', 'lowest_rtt', 'lowest_hops',
            'packet_rate', 'cpu', 'hit_ratio', 'qos', 'bps', 'drop_packet',
            'explicit_ip', 'connection_rate', 'vs_score'
        ]
        if self._values['lb_method'] is None:
            return None
        lb_method = str(self._values['lb_method'])
        if lb_method in deprecated:
            raise F5ModuleError(
                "The provided lb_method is not supported"
            )
        elif lb_method == 'global_availability':
            if self._values['__warnings'] is None:
                self._values['__warnings'] = []
            self._values['__warnings'].append(
                [
                    dict(
                        msg='The provided lb_method is deprecated',
                        version='2.4'
                    )
                ]
            )
            lb_method = 'global-availability'
        elif lb_method == 'round_robin':
            if self._values['__warnings'] is None:
                self._values['__warnings'] = []
            self._values['__warnings'].append(
                [
                    dict(
                        msg='The provided lb_method is deprecated',
                        version='2.4'
                    )
                ]
            )
            lb_method = 'round-robin'
        return lb_method

    @lb_method.setter
    def lb_method(self, value):
        self._values['lb_method'] = value

    @property
    def type(self):
        type_map = dict(
            a='a_s',
            aaaa='aaaas',
            cname='cnames',
            mx='mxs',
            naptr='naptrs',
            srv='srvs'
        )
        wideip_type = self._values['type']
        return type_map[wideip_type]

    @type.setter
    def type(self):
        self._values['type'] = value

    @property
    def name(self):
        if not re.search(r'.*\..*\..*', self._values['name']):
            raise F5ModuleError(
                "The provided name must be a valid FQDN"
            )
        return self._values['name']

    @name.setter
    def name(self, value):
        self._value['name'] = value


class ModuleManager(object):
    def __init__(self, client):
        self.client = client

    def exec_module(self):
        if self.version_is_less_than_12():
            manager = self.get_manager('untyped')
        else:
            manager = self.get_manager('typed')
        return manager.exec_module()

    def get_manager(self, type):
        if type == 'typed':
            return TypedManager(self.client)
        elif type =='untyped':
            return UntypedManager(self.client)

    def version_is_less_than_12(self):
        version = self.client.api.tmos_version
        if LooseVersion(version) < LooseVersion('12.0.0'):
            return True
        else:
            return False


class BaseManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def exec_module(self):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.changes.to_return())
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
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

    def should_update(self):
        updateable = Parameters.param_api_map.keys()
        for key in updateable:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    self.changes._values[key] = getattr(self.want, key)
                    return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the Wide IP")
        return True


class UntypedManager(BaseManager):
    def exists(self):
        return self.client.api.tm.gtm.wideips.wideip.exists(
            name=self.want.name,
            partition=self.want.partition
        )

    def create(self):
        updateable = Parameters.param_api_map.keys()
        for key in updateable:
            if getattr(self.want, key) is not None:
                self.changes._values[key] = getattr(self.want, key)
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def update_on_device(self):
        params = self.want.api_params()
        result = self.client.api.tm.gtm.wideips.wipeip.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result.modify(**params)

    def read_current_from_device(self):
        result = self.client.api.tm.gtm.wideips.wideip.load(
            name=self.want.name,
            partition=self.want.partition
        ).to_dict()
        result.pop('_meta_data', None)
        return Parameters.from_api(result)

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.gtm.wideips.wideip.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def remove_from_device(self):
        result = self.client.api.tm.gtm.wideips.wideip.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if result:
            result.delete()


class TypedManager(BaseManager):
    def exists(self):
        wideips = self.client.api.tm.gtm.wideips
        resource = getattr(wideips, self.want.type)
        return resource.exists(
            name=self.want.name,
            partition=self.want.partition
        )

    def create(self):
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def update_on_device(self):
        params = self.want.api_params()
        wideips = self.client.api.tm.gtm.wideips
        resource = getattr(wideips, self.want.type)
        result = resource.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result.modify(**params)

    def read_current_from_device(self):
        wideips = self.client.api.tm.gtm.wideips
        resource = getattr(wideips, self.want.type)
        result = resource.load(
            name=self.want.name,
            partition=self.want.partition
        ).to_dict()
        result.pop('_meta_data', None)
        return Parameters.from_api(result)

    def create_on_device(self):
        params = self.want.api_params()
        wideips = self.client.api.tm.gtm.wideips
        resource = getattr(wideips, self.want.type)
        resource.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def remove_from_device(self):
        wideips = self.client.api.tm.gtm.wideips
        resource = getattr(wideips, self.want.type)
        result = resource.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if result:
            result.delete()


class ArgumentSpec(object):
    def __init__(self):
        deprecated = [
            'return_to_dns', 'null', 'round_robin', 'ratio', 'topology',
            'static_persist', 'global_availability', 'vs_capacity',
            'least_conn', 'lowest_rtt', 'lowest_hops', 'packet_rate',
            'cpu', 'hit_ratio', 'qos', 'bps', 'drop_packet', 'explicit_ip',
            'connection_rate', 'vs_score'
        ]
        supported = [
            'round-robin', 'topology', 'ratio', 'global-availability'
        ]
        lb_method_choices = deprecated + supported
        self.supports_check_mode = True
        self.argument_spec = dict(
            lb_method=dict(
                required=True,
                choices=lb_method_choices
            ),
            name=dict(
                required=True,
                aliases=['wide_ip']
            ),
            type=dict(
                required=False,
                default=None,
                choices=[
                    'a','aaaa','cname','mx','naptr','srv'
                ]
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.f5_product_name = 'bigip'


def main():
    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    mm = ModuleManager(client)
    results = mm.exec_module()
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
