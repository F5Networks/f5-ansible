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

DOCUMENTATION = '''
---
module: bigip_provision
short_description: Manage BIG-IP module provisioning
description:
  - Manage BIG-IP module provisioning. This module will only provision at the
    standard levels of Dedicated, Nominal, and Minimum.
version_added: "2.3"
options:
  module:
    description:
      - The module to provision in BIG-IP.
    required: true
    choices:
      - afm
      - am
      - sam
      - asm
      - avr
      - fps
      - gtm
      - lc
      - ltm
      - pem
      - swg
  level:
    description:
      - Sets the provisioning level for the requested modules. Changing the
        level for one module may require modifying the level of another module.
        For example, changing one module to C(dedicated) requires setting all
        others to C(none). Setting the level of a module to C(none) means that
        the module is not run.
    required: false
    default: nominal
    choices:
      - dedicated
      - nominal
      - minimum
  state:
    description:
      - The state of the provisioned module on the system. When C(present),
        guarantees that the specified module is provisioned at the requested
        level provided that there are sufficient resources on the device (such
        as physical RAM) to support the provisioned module. When C(absent),
        deprovision the module.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
  - This module only works reliably on BIG-IP versions >= 13.1.
  - After you provision something you should
requirements:
  - f5-sdk >= 2.2.3
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Provision PEM at "nominal" level
  bigip_provision:
      server: "lb.mydomain.com"
      module: "pem"
      level: "nominal"
      password: "secret"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost

- name: Provision a dedicated SWG. This will unprovision every other module
  bigip_provision:
      server: "lb.mydomain.com"
      module: "swg"
      password: "secret"
      level: "dedicated"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost
'''


import time


# This is a temporary placeholder for folks that dont yet have
# Ansible 2.4
try:
    from f5.bigip import ManagementRoot as BigIpMgmt
    from f5.bigip.contexts import TransactionContextManager as BigIpTxContext
    from f5.bigiq import ManagementRoot as BigIqMgmt
    from f5.iworkflow import ManagementRoot as iWorkflowMgmt
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

from ansible.module_utils.basic import env_fallback
from ansible.module_utils.basic import *
from ansible.module_utils.six import iteritems


F5_COMMON_ARGS = dict(
    server=dict(
        type='str',
        required=True,
        fallback=(env_fallback, ['F5_SERVER'])
    ),
    user=dict(
        type='str',
        required=True,
        fallback=(env_fallback, ['F5_USER'])
    ),
    password=dict(
        type='str',
        aliases=['pass', 'pwd'],
        required=True,
        no_log=True,
        fallback=(env_fallback, ['F5_PASSWORD'])
    ),
    validate_certs=dict(
        default='yes',
        type='bool',
        fallback=(env_fallback, ['F5_VALIDATE_CERTS'])
    ),
    server_port=dict(
        type='int',
        default=443,
        required=False,
        fallback=(env_fallback, ['F5_SERVER_PORT'])
    ),
    state=dict(
        type='str',
        default='present',
        choices=['present', 'absent']
    ),
    partition=dict(
        type='str',
        default='Common',
        fallback=(env_fallback, ['F5_PARTITION'])
    )
)


class AnsibleF5Client(object):
    def __init__(self, argument_spec=None, supports_check_mode=False,
                 mutually_exclusive=None, required_together=None,
                 required_if=None, required_one_of=None,
                 f5_product_name='bigip'):

        merged_arg_spec = dict()
        merged_arg_spec.update(F5_COMMON_ARGS)
        if argument_spec:
            merged_arg_spec.update(argument_spec)
            self.arg_spec = merged_arg_spec

        mutually_exclusive_params = []
        if mutually_exclusive:
            mutually_exclusive_params += mutually_exclusive

        required_together_params = []
        if required_together:
            required_together_params += required_together

        self.module = AnsibleModule(
            argument_spec=merged_arg_spec,
            supports_check_mode=supports_check_mode,
            mutually_exclusive=mutually_exclusive_params,
            required_together=required_together_params,
            required_if=required_if,
            required_one_of=required_one_of
        )

        self.check_mode = self.module.check_mode
        self._connect_params = self._get_connect_params()

        try:
            self.api = self._get_mgmt_root(
                f5_product_name, **self._connect_params
            )
        except iControlUnexpectedHTTPError as exc:
            self.fail(str(exc))

    def fail(self, msg):
        self.module.fail_json(msg=msg)

    def _get_connect_params(self):
        params = dict(
            user=self.module.params['user'],
            password=self.module.params['password'],
            server=self.module.params['server'],
            server_port=self.module.params['server_port'],
            validate_certs=self.module.params['validate_certs']
        )
        return params

    def _get_mgmt_root(self, type, **kwargs):
        if type == 'bigip':
            return BigIpMgmt(
                kwargs['server'],
                kwargs['user'],
                kwargs['password'],
                port=kwargs['server_port'],
                token='tmos'
            )
        elif type == 'iworkflow':
            return iWorkflowMgmt(
                kwargs['server'],
                kwargs['user'],
                kwargs['password'],
                port=kwargs['server_port'],
                token='local'
            )
        elif type == 'bigiq':
            return BigIqMgmt(
                kwargs['server'],
                kwargs['user'],
                kwargs['password'],
                port=kwargs['server_port'],
                token='local'
            )


class AnsibleF5Parameters(object):
    def __init__(self, params=None):
        self._partition = None
        if params is None:
            return
        for key, value in iteritems(params):
            setattr(self, key, value)

    @property
    def partition(self):
        if self._partition is None:
            return 'Common'
        return self._partition.strip('/')

    @partition.setter
    def partition(self, value):
        self._partition = value

    @classmethod
    def from_api(cls, params):
        for key,value in iteritems(cls.param_api_map):
            params[key] = params.pop(value, None)
        p = cls(params)
        return p

    def __getattr__(self, item):
        return None

    def api_params(self):
        result = self._api_params_from_map()
        return self._filter_none(result)

    def _filter_none(self, params):
        result = dict()
        for k, v in iteritems(params):
            if v is None:
                continue
            result[k] = v
        return result

    def _api_params_from_map(self):
        result = dict()
        pmap = self.__class__.param_api_map
        for k,v in iteritems(pmap):
            value = getattr(self, k)
            result[v] = value
        return result

    def _params_from_map(self):
        result = dict()
        pmap = self.__class__.param_api_map
        for k,v in iteritems(pmap):
            value = getattr(self, k)
            result[k] = value
        return result

    def to_dict(self):
        result = self._params_from_map()
        return self._filter_none(result)


class Parameters(AnsibleF5Parameters):
    param_api_map = dict(
        level='level'
    )

    def __init__(self, params=None):
        self._level = None
        super(Parameters, self).__init__(params)

    @property
    def level(self):
        if self._level is None:
            return None
        return str(self._level)

    @level.setter
    def level(self, value):
        self._level = value

class ModuleManager(object):
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
                changed = self.update()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        #result.update(**self.changes.to_dict())
        result.update(dict(changed=changed))
        return result

    def exists(self):
        provision = self.client.api.tm.sys.provision
        resource = getattr(provision, self.want.module)
        resource = resource.load()
        result = resource.to_dict()
        result.pop('_meta_data', None)
        if str(result.level) == 'none':
            return False
        return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.client.check_mode:
            return True
        self.update_on_device()
        self.wait_for_module_provisioning()
        return True

    def should_update(self):
        if self.want.level != self.have.level:
            self.changes.level = self.want.level
            return True
        return False

    def update_on_device(self):
        params = self.want.api_params()
        provision = self.client.api.tm.sys.provision
        resource = getattr(provision, self.want.module)
        resource = resource.load()
        resource.update(**params)

    def read_current_from_device(self):
        provision = self.client.api.tm.sys.provision
        resource = getattr(provision, str(self.want.module))
        resource = resource.load()
        result = resource.to_dict()
        result.pop('_meta_data', None)
        return Parameters.from_api(result)

    def absent(self, ):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        self.wait_for_module_provisioning()
        if self.exists():
            raise F5ModuleError("Failed to deprovision the module")
        return True

    def remove_from_device():
        provision = self.client.api.tm.sys.provision
        resource = getattr(provision, self.want.module)
        resource = resource.load()
        resource.update({'level': self.want.level})

    def wait_for_module_provisioning(self):
        # To prevent things from running forever, the hack is to check
        # for mprov's status twice. If mprov is finished, then in most
        # cases (not ASM) the provisioning is probably ready.
        nops = 0

        # Sleep a little to let provisioning settle and begin properly
        time.sleep(5)

        while nops < 2:
            if not self._is_mprov_running_on_device():
                nops += 1
            time.sleep(5)

    def _is_mprov_running_on_device(self):
        output = self.client.api.tm.util.bash.exec_cmd(
            'run',
            utilCmdArgs='-c "ps aux | grep \'[m]prov\'"'
        )
        if hasattr(output, 'commandResult'):
            return True
        return False


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            module=dict(
                required=True,
                choices=[
                    'afm', 'am', 'sam', 'asm', 'avr', 'fps',
                    'gtm', 'lc', 'ltm', 'pem', 'swg'
                ]
            ),
            level=dict(
                default='nominal',
                choices=['nominal', 'dedicated', 'minimal']
            ),
            state=dict(
                default='present',
                choices=['present', 'absent']
            )
        )
        self.mutually_exclusive = [
            ['parameters', 'parameters_src']
        ]
        self.f5_product_name = 'bigip'


def main():
    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        mutually_exclusive=spec.mutually_exclusive,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    mm = ModuleManager(client)
    results = mm.exec_module()
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
