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
module: bigip_node
short_description: Manages F5 BIG-IP LTM nodes
description:
  - Manages F5 BIG-IP LTM nodes via iControl SOAP API.
version_added: "1.4"
options:
  state:
    description:
      - Specifies the current state of the node. C(enabled) (All traffic
        allowed), specifies that system sends traffic to this node regardless
        of the node's state. C(disabled) (Only persistent or active connections
        allowed), Specifies that the node can handle only persistent or
        active connections. C(offline) (Only active connections allowed),
        Specifies that the node can handle only active connections. In all
        cases except C(absent), the node will be created if it does not yet
        exist.
    required: true
    default: present
    choices:
      - present
      - absent
      - enabled
      - disabled
      - offline
  name:
    description:
      - Specifies the name of the node.
    required: False
    default: None
  availability_requirement:
    description:
      - Specifies, if you activate more than one health monitor, the number
        of health monitors that must receive successful responses in order
        for the node to be considered available. The default is C(all).
    version_added: "2.2"
    default: C(and_list)
    required: False
    choices:
      - all
      - at_least
    aliases:
      - monitor_type
  quorum:
    description:
      - Monitor quorum value when C(monitor_type) is C(at_least).
    version_added: "2.2"
    required: False
    default: None
  monitors:
    description:
      - Specifies the health monitors that the system currently uses to
        monitor this node.
    version_added: "2.2"
    required: False
    default: None
  host:
    description:
      - Node IP. Required when C(state) is present and node does not exist.
        Error when C(state) is equal to C(absent).
    required: true
    default: None
    aliases:
      - address
      - ip
  description:
    description:
      - Specifies descriptive text that identifies the node.
    required: False
    default: None
notes:
  - Requires BIG-IP software version >= 11
  - Requires the f5-sdk Python package on the host. This is as easy as
    pip install f5-sdk
  - Requires the netaddr Python package on the host. This is as easy as
    pip install netaddr
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add node
  bigip_node:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "present"
      partition: "Common"
      host: "10.20.30.40"
      name: "10.20.30.40"
  delegate_to: localhost

- name: Add node with a single 'ping' monitor
  bigip_node:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "present"
      partition: "Common"
      host: "10.20.30.40"
      name: "mytestserver"
      monitors:
          - /Common/icmp
  delegate_to: localhost

- name: Modify node description
  bigip_node:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "present"
      partition: "Common"
      name: "10.20.30.40"
      description: "Our best server yet"
  delegate_to: localhost

- name: Delete node
  bigip_node:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "absent"
      partition: "Common"
      name: "10.20.30.40"
  delegate_to: localhost

- name: Force node offline
  bigip_node:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "disabled"
      partition: "Common"
      name: "10.20.30.40"
  delegate_to: localhost
'''

RETURN = '''
members:
    description:
      - List of members that are part of the SNAT pool.
    returned: changed and success
    type: list
    sample: "['10.10.10.10']"
'''

import re

try:
    from f5.bigip.contexts import TransactionContextManager
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

try:
    import bigsuds
    HAS_BIGSUDS = True
except ImportError:
    HAS_BIGSUDS = False

try:
    from netaddr import IPAddress, AddrFormatError
    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False


class F5Connector(object):
    __instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance:
            return self.__instance
        else:
            if HAS_F5SDK:
                self.__instance = F5RestConnector(**kwargs)
            elif HAS_BIGSUDS:
                self.__instance = F5SoapConnector(**kwargs)
            else:
                raise F5ModuleError(
                    "No API connector was found"
                )


class F5RestConnector(object):
    def __init__(self, *args, **kwargs):
        self.api = ManagementRoot(
            kwargs['server'],
            kwargs['username'],
            kwargs['password'],
            port=kwargs['server_port'],
            token=True
        )


class F5SoapConnector(object):
    def __init__(self, *args, **kwargs):
        self.api = bigsuds.BIGIP(
            hostname=kwargs['server'],
            username=kwargs['username'],
            password=kwargs['password'],
            verify=kwargs['validate_certs'],
            port=kwargs['server_port']
        )


class BigIpNodeCreator(object):
    def __call__(self, *args, **kwargs):
        self.api.tm.ltm.nodes.node.create(
            name=node.name,
            partition=node.partition,
            monitor=node.monitor,
            description=node.description,
            state=node.cache
        )


class BigIpNodeUpdater(object):
    def __call__(self, *args, **kwargs):
        tx = self.client.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            req = api.tm.ltm.nodes.node.load(
                name=node.name,
                partition=node.partition
            )
            req.modify(**kwargs)


class BigIpNodeDeleter(object):
    def __call__(self, *args, **kwargs):
        tx = self.api.tm.transactions.transaction
        with TransactionContextManager(tx) as api:
            req = api.tm.ltm.nodes.node.load(
                name=node.name, partition=node.partition
            )
            req.delete()


class BigIpNodeLoader(object):
    def __call__(self, *args, **kwargs):
        return F5Connector.tm.ltm.nodes.node.load(
            name=node.name, partition=node.partition
        )


class ModuleConfig(object):

    def __init__(self):
        # Initial parameter values
        self.states = [
            'absent', 'present', 'enabled', 'disabled', 'offline'
        ]
        self.monitor_type_choices = ['all', 'at_least']
        self.host_choices = ['address', 'ip']

        # Initial Ansible Module parameter values
        self.supports_check_mode = True
        self.required_together=[
            ['availability_requirement', 'monitors'],
            ['quorum', 'monitors']
        ]
        self.required_if = [
            'availability_requirement', 'at_least', ['quorum']
        ]

    def init_meta_args(self, **kwargs):
        args = dict(
            name=dict(required=True),
            host=dict(aliases=kwargs['host_choices']),
            description=dict(),
            availability_requirement=dict(
                choices=kwargs['monitor_type_choices']
            ),
            quorum=dict(type='int'),
            monitors=dict(type='list'),
            state=dict(
                choices=kwargs['states'],
                default='present'
            )
        )
        return args

    def init_argument_spec(self, meta_args=None):
        argument_spec = f5_argument_spec()
        if meta_args:
            argument_spec.update(meta_args)
        return argument_spec

    def create(self):
        meta_args = self.init_meta_args(
            host_choices=self.host_choices,
            monitor_type_choices=self.monitor_type_choices,
            states=self.states
        )
        argument_spec = self.init_argument_spec(meta_args)
        return AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=self.supports_check_mode,
            required_together=self.required_together,
            required_if=self.required_if
        )


class DeviceState(object):
    def __init__(self, **kwargs):
        self._values = dict(
            state=None,
            session=None
        )
        self._valid_sessions = [
            'user-disabled', 'user-enabled'
        ]
        self._valid_states = [
            'user-down'
        ]
        state = kwargs.pop('state', None)
        session = kwargs.pop('session', None)
        self.update(state=state, session=session)

    def update(self, state=None, session=None):
        if session in self._valid_sessions or session is None:
            self._values['session'] = session
        if state in self._valid_states or state is None:
            self._values['state'] = state

    def from_param_state(cls, param_state):
        pass


class ParamState(object):
    def __init__(self):
        self._values = dict(
            state=None
        )
        self._valid_states = [
            'offline','enabled','disabled'
        ]

    def update(self, state=None):
        if state in self._valid_states or state is None:
            self._values['state'] = state
        """
        if state == 'offline':
            self._values['session'] = 'user-disabled'
            self._values['state'] = 'user-down'
        elif state == 'enabled':
            self._values['session'] = 'user-enabled'
            self._values['state'] = None
        elif state == 'disabled':
            self._values['session'] = 'user-disabled'
            self._values['state'] = None
        """

    @classmethod
    def as_device_state(cls, param_state):
        device_state = cls()
        device_state.update()


class MonitorAdapter(object):

    def __init__(self, **kwargs):
        self.pattern = r'^min\s(\d+)\s+of'
        self._quorum = None
        self._requirements = None
        self._monitors = None
        self.quorum = kwargs.pop('quorum', None)
        self.requirements = kwargs.pop('requirements', None)

    @property
    def requirements(self):
        return self._value

    @requirements.setter
    def requirements(self, value):
        matches = re.match(self.pattern, value)
        if matches:
            if matches:
                self._requirements = "at_least"
            else:
                self._requirements = "all"

    @property
    def quorum(self):
        return self._quorum

    @quorum.setter
    def quorum(self, value):
        try:
            self._quorum = int(value)
        except (TypeError) as ex:
            matches = re.match(self.pattern, value)
            if matches:
                self._quorum = int(matches.group(1))

    @property
    def monitors(self):
        return self._monitors

    @monitors.setter
    def monitors(self, value):
        self._monitors = value


class BigIpNode(object):

    def __init__(self, **kwargs):
        self.address = kwargs.pop('address', None)
        self.description = kwargs.pop('description', None)
        self.monitor = kwargs.pop('monitor', None)
        self.name = kwargs.pop('name', None)
        self.partition = kwargs.pop('partition', None)
        self.state = kwargs.pop('state', None)

    @classmethod
    def from_device(cls, name, partition):
        device = BigIpNodeLoader()
        settings = device()

    def from_params(self):
        pass


class BigIpNodeFacade(object):
    def __init__(self, *args, **kwargs):
        self.changed_params = dict()
        self.params = kwargs
        self.api = None

    def apply_changes(self):
        result = dict()
        try:
            if self.config['state'] == 'absent':
                changed = self.absent()
            else:
                changed = self.present()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))
        result.update(**changed)
        result.update(dict(changed=changed))
        return result

    def present(self):
        if self.node_exists():
            return self.update_node()
        else:
            return self.ensure_node_is_present()

    def absent(self):
        changed = False
        if self.node_exists():
            changed = ensure_node_is_absent()
        return changed

    def update_node(self, node):
        params = self.set_changed_parameters()
        if params:
            self.changed_params = camel_dict_to_snake_dict(params)
            if self.params['check_mode']:
                return True
        else:
            return False
        self.update_node_on_device(node)
        return True

    def ensure_node_is_absent(self, node, check_mode):
        if check_mode:
            return True
        self.delete_node_from_device(name, partition)
        if self.node_exists(name, partition):
            raise F5ModuleError("Failed to delete the node")
        return True

    def ensure_node_is_present(self, node):
        if self.params['host'] is None:
            F5ModuleError(
                "host parameter required when state is equal to present"
            )
        params = self.get_node_creation_parameters()
        self.changed_params = camel_dict_to_snake_dict(params)
        if self.params['check_mode']:
            return True
        self.create_node_on_device(params)
        if self.node_exists():
            return True
        else:
            raise F5ModuleError("Failed to create the node")

    def format_node_information(self, node):
        result = dict(
            name=str(node.name),
            state=format_current_state(node.session, node.cache)
        )
        if hasattr(node, 'monitor'):
            result['monitors'] = self.format_current_monitors(node.monitor)
            result['quorum'] = self.format_current_quorum(node.monitor)
            result['availability_req'] = self.format_current_availability_req(node.monitor)
        return result

    def set_changed_parameters(self):
        result = dict()
        params = self.get_supplied_parameters()
        current = self.read_node_information()
        if self.is_description_changed(current, params['description']):
            result['description'] = params['description']
        if self.is_state_changed(current):
            result.update(**self.get_changed_state())
        if (self.are_monitors_changed(current) or
                self.is_quorum_changed(current) or
                self.is_availability_req_changed(current)):
            result['monitor'] = self.format_monitor_parameter()
        return result

    def are_monitors_changed(self, current):
        if self.params['monitors'] is None:
            return False
        if 'monitors' not in current:
            return True
        if set(self.params['monitors']) != set(current['monitors']):
            return True
        else:
            return False

    def is_description_changed(self, current, description):
        if description is None:
            return False
        if 'description' not in current:
            return True
        if description != current['description']:
            return True
        else:
            return False

    def is_state_changed(self, current):
        if self.params['state'] != current['state']:
            return True
        else:
            return False

    def is_availability_req_changed(self, current):
        if self.params['availability_req'] is None:
            return False
        if 'availability_req' not in current:
            return True
        if self.params['availability_req'] != current['availability_req']:
            return True
        else:
            return False

    def get_node_creation_parameters(self):
        result = dict(
            name=self.params['name'],
            address=self.params['host'],
            partition=self.params['partition']
        )
        if self.params['description']:
            result['description'] = self.params['description']
        if self.params['monitors']:
            result['monitor'] = self.format_monitor_parameter()
        return result

    def format_monitor_parameter(self):
        if len(self.params['monitors']) == 1:
            return 'default'
        return self.format_monitor_param_with_quorum()

    def format_monitor_param_with_quorum(self):
        monitors = self.params['monitors']
        quorum = self.params['quorum']
        partition = self.params['partition']
        availability = self.params['availability_requirement']
        if quorum > len(monitors):
            raise F5ModuleError(
                "The quorum number cannot exceed the number of monitors"
            )
        tmp = ['/{0}/{1}'.format(partition, x) for x in monitors]
        if availability == 'at_least':
            return "min {0} of {1}".format(quorum,' '.join(tmp))
        else:
            return ' and '.join(tmp)


def main():
    if not HAS_NETADDR:
        raise F5ModuleError("The python netaddr module is required")

    config = ModuleConfig()
    module = config.create()

    try:
        obj = BigIpNodeFacade(
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
