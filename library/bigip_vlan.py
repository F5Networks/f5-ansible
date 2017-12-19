#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_vlan
short_description: Manage VLANs on a BIG-IP system
description:
  - Manage VLANs on a BIG-IP system
version_added: "2.2"
options:
  description:
    description:
      - The description to give to the VLAN.
  tagged_interfaces:
    description:
      - Specifies a list of tagged interfaces and trunks that you want to
        configure for the VLAN. Use tagged interfaces or trunks when
        you want to assign a single interface or trunk to multiple VLANs.
    aliases:
      - tagged_interface
  untagged_interfaces:
    description:
      - Specifies a list of untagged interfaces and trunks that you want to
        configure for the VLAN.
    aliases:
      - untagged_interface
  name:
    description:
      - The VLAN to manage. If the special VLAN C(ALL) is specified with
        the C(state) value of C(absent) then all VLANs will be removed.
    required: True
  state:
    description:
      - The state of the VLAN on the system. When C(present), guarantees
        that the VLAN exists with the provided attributes. When C(absent),
        removes the VLAN from the system.
    default: present
    choices:
      - absent
      - present
  tag:
    description:
      - Tag number for the VLAN. The tag number can be any integer between 1
        and 4094. The system automatically assigns a tag number if you do not
        specify a value.
  mtu:
    description:
      - Specifies the maximum transmission unit (MTU) for traffic on this VLAN.
        When creating a new VLAN, if this parameter is not specified, the default
        value used will be C(1500).
      - This number must be between 576 to 9198.
    version_added: 2.5
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - Requires BIG-IP versions >= 12.0.0
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
  - Wojciech Wypior (@wojtek0806)
'''

EXAMPLES = r'''
- name: Create VLAN
  bigip_vlan:
      name: "net1"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost

- name: Set VLAN tag
  bigip_vlan:
      name: "net1"
      password: "secret"
      server: "lb.mydomain.com"
      tag: "2345"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost

- name: Add VLAN 2345 as tagged to interface 1.1
  bigip_vlan:
      tagged_interface: 1.1
      name: "net1"
      password: "secret"
      server: "lb.mydomain.com"
      tag: "2345"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost

- name: Add VLAN 1234 as tagged to interfaces 1.1 and 1.2
  bigip_vlan:
      tagged_interfaces:
          - 1.1
          - 1.2
      name: "net1"
      password: "secret"
      server: "lb.mydomain.com"
      tag: "1234"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost
'''

RETURN = r'''
description:
    description: The description set on the VLAN
    returned: changed
    type: string
    sample: foo VLAN
interfaces:
    description: Interfaces that the VLAN is assigned to
    returned: changed
    type: list
    sample: ['1.1','1.2']
partition:
    description: The partition that the VLAN was created on
    returned: changed
    type: string
    sample: Common
tag:
    description: The ID of the VLAN
    returned: changed
    type: int
    sample: 2345
'''

from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import AnsibleF5Parameters
from ansible.module_utils.f5_utils import HAS_F5SDK
from ansible.module_utils.f5_utils import F5ModuleError
from ansible.module_utils.six import iteritems
from collections import defaultdict

try:
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    api_map = {}
    updatables = [
        'tagged_interfaces', 'untagged_interfaces', 'tag',
        'description', 'mtu'
    ]

    returnables = [
        'description', 'partition', 'tag', 'interfaces',
        'tagged_interfaces', 'untagged_interfaces', 'mtu'
    ]

    api_attributes = [
        'description', 'interfaces', 'tag', 'mtu'
    ]

    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        if params:
            self.update(params=params)

    def update(self, params=None):
        if params:
            for k, v in iteritems(params):
                if self.api_map is not None and k in self.api_map:
                    map_key = self.api_map[k]
                else:
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have
                        # an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if api_attribute in self.api_map:
                result[api_attribute] = getattr(
                    self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ApiParameters(Parameters):
    @property
    def tagged_interfaces(self):
        if self._values['interfaces'] is None:
            return None
        result = [str(x.name) for x in self._values['interfaces'] if x.tagged is True]
        result = sorted(result)
        return result

    @property
    def untagged_interfaces(self):
        if self._values['interfaces'] is None:
            return None
        result = [str(x.name) for x in self._values['interfaces'] if x.untagged is True]
        result = sorted(result)
        return result


class ModuleParameters(Parameters):
    @property
    def untagged_interfaces(self):
        if self._values['untagged_interfaces'] is None:
            return None
        if self._values['untagged_interfaces'] is None:
            return None
        if len(self._values['untagged_interfaces']) == 1 and self._values['untagged_interfaces'][0] == '':
            return ''
        result = sorted([str(x) for x in self._values['untagged_interfaces']])
        return result

    @property
    def tagged_interfaces(self):
        if self._values['tagged_interfaces'] is None:
            return None
        if self._values['tagged_interfaces'] is None:
            return None
        if len(self._values['tagged_interfaces']) == 1 and self._values['tagged_interfaces'][0] == '':
            return ''
        result = sorted([str(x) for x in self._values['tagged_interfaces']])
        return result

    @property
    def mtu(self):
        if self._values['mtu'] is None:
            return None
        if int(self._values['mtu']) < 576 or int(self._values['mtu']) > 9198:
            raise F5ModuleError(
                "The mtu value must be between 576 - 9198"
            )
        return int(self._values['mtu'])


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class UsableChanges(Changes):
    pass


class ReportableChanges(Changes):
    @property
    def tagged_interfaces(self):
        if self._values['interfaces'] is None:
            return None
        result = [str(x['name']) for x in self._values['interfaces'] if 'tagged' in x and x['tagged'] is True]
        result = sorted(result)
        return result

    @property
    def untagged_interfaces(self):
        if self._values['interfaces'] is None:
            return None
        result = [str(x['name']) for x in self._values['interfaces'] if 'untagged' in x and x['untagged'] is True]
        result = sorted(result)
        return result


class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            return self.__default(param)

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1

    @property
    def untagged_interfaces(self):
        result = []
        if self.want.untagged_interfaces is None:
            return None
        elif self.want.untagged_interfaces == '' and self.have.untagged_interfaces is None:
            return None
        elif self.want.untagged_interfaces == '' and len(self.have.untagged_interfaces) > 0:
            pass
        elif not self.have.untagged_interfaces:
            result = dict(
                interfaces=[dict(name=x, untagged=True) for x in self.want.untagged_interfaces]
            )
        elif set(self.want.untagged_interfaces) != set(self.have.untagged_interfaces):
            result = dict(
                interfaces=[dict(name=x, untagged=True) for x in self.want.untagged_interfaces]
            )
        else:
            return None
        return result

    @property
    def tagged_interfaces(self):
        result = []
        if self.want.tagged_interfaces is None:
            return None
        elif self.want.tagged_interfaces == '' and self.have.tagged_interfaces is None:
            return None
        elif self.want.tagged_interfaces == '' and len(self.have.tagged_interfaces) > 0:
            pass
        elif not self.have.tagged_interfaces:
            result = dict(
                interfaces=[dict(name=x, tagged=True) for x in self.want.tagged_interfaces]
            )
        elif set(self.want.tagged_interfaces) != set(self.have.tagged_interfaces):
            result = dict(
                interfaces=[dict(name=x, tagged=True) for x in self.want.tagged_interfaces]
            )
        else:
            return None
        return result


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.want = ModuleParameters(params=self.client.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = UsableChanges(changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = UsableChanges(changed)
            return True
        return False

    def exec_module(self):
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

        reportable = ReportableChanges(self.changes.to_return())
        changes = reportable.to_return()
        result.update(**changes)
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

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        return True

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the VLAN")
        return True

    def create(self):
        if self.want.mtu is None:
            self.want.update({'mtu': 1500})
        if self.want.untagged_interfaces is not None:
            interfaces = [dict(name=x, untagged=True) for x in self.want.untagged_interfaces]
            self.want.update({'interfaces': interfaces})
        elif self.want.tagged_interfaces is not None:
            interfaces = [dict(name=x, tagged=True) for x in self.want.tagged_interfaces]
            self.want.update({'interfaces': interfaces})
        self._set_changed_options()
        if self.client.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.net.vlans.vlan.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def update_on_device(self):
        params = self.changes.api_params()
        resource = self.client.api.tm.net.vlans.vlan.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.modify(**params)

    def exists(self):
        return self.client.api.tm.net.vlans.vlan.exists(
            name=self.want.name,
            partition=self.want.partition
        )

    def remove_from_device(self):
        resource = self.client.api.tm.net.vlans.vlan.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if resource:
            resource.delete()

    def read_current_from_device(self):
        resource = self.client.api.tm.net.vlans.vlan.load(
            name=self.want.name, partition=self.want.partition
        )
        interfaces = resource.interfaces_s.get_collection()
        result = resource.attrs
        result['interfaces'] = interfaces
        return ApiParameters(result)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            name=dict(
                required=True,
            ),
            tagged_interfaces=dict(
                type='list',
                aliases=['tagged_interface']
            ),
            untagged_interfaces=dict(
                type='list',
                aliases=['untagged_interface']
            ),
            description=dict(),
            tag=dict(
                type='int'
            ),
            mtu=dict(type='int')
        )
        self.f5_product_name = 'bigip'


def cleanup_tokens(client):
    try:
        resource = client.api.shared.authz.tokens_s.token.load(
            name=client.api.icrs.token
        )
        resource.delete()
    except Exception:
        pass


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name,
        mutually_exclusive=[
            ['tagged_interfaces', 'untagged_interfaces']
        ]
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        cleanup_tokens(client)
        client.module.exit_json(**results)
    except F5ModuleError as e:
        cleanup_tokens(client)
        client.module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
