#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# Copyright (c) 2015 Etienne Carriere <etienne.carriere@gmail.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from collections import defaultdict

try:
    from f5.bigip import ManagementRoot as BigIpMgmt
    from f5.bigip.contexts import TransactionContextManager as BigIpTxContext
    from f5.bigiq import ManagementRoot as BigIqMgmt
    from f5.iworkflow import ManagementRoot as iWorkflowMgmt
    from icontrol.exceptions import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.six import iteritems


F5_COMMON_ARGS = dict(
    server=dict(
        required=True,
        fallback=(env_fallback, ['F5_SERVER'])
    ),
    user=dict(
        required=True,
        fallback=(env_fallback, ['F5_USER'])
    ),
    password=dict(
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
        fallback=(env_fallback, ['F5_SERVER_PORT'])
    ),
    state=dict(
        default='present',
        choices=['present', 'absent']
    ),
    partition=dict(
        default='Common',
        fallback=(env_fallback, ['F5_PARTITION'])
    )
)


class F5AnsibleModule(object):
    def __init__(self, argument_spec=None, supports_check_mode=False,
                 mutually_exclusive=None, required_together=None,
                 required_if=None, required_one_of=None, add_file_common_args=False,
                 f5_product_name='bigip'):

        self.f5_product_name = f5_product_name

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
            required_one_of=required_one_of,
            add_file_common_args=add_file_common_args
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

    def reconnect(self):
        """Attempts to reconnect to a device

        The existing token from a ManagementRoot can become invalid if you,
        for example, upgrade the device (such as is done in the *_software
        module.

        This method can be used to reconnect to a remote device without
        having to re-instantiate the ArgumentSpec and AnsibleF5Client classes
        it will use the same values that were initially provided to those
        classes

        :return:
        :raises iControlUnexpectedHTTPError
        """
        self.api = self._get_mgmt_root(
            self.f5_product_name, **self._connect_params
        )


class AnsibleF5Parameters(object):
    def __init__(self, params=None):
        self._values = defaultdict(lambda: None)
        if params:
            for k, v in iteritems(params):
                if self.api_map is not None and k in self.api_map:
                    dict_to_use = self.api_map
                    map_key = self.api_map[k]
                else:
                    dict_to_use = self._values
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    def __getattr__(self, item):
        # Ensures that properties that weren't defined, and therefore stashed
        # in the `_values` dict, will be retrievable.
        return self._values[item]

    @property
    def partition(self):
        if self._values['partition'] is None:
            return 'Common'
        return self._values['partition'].strip('/')

    @partition.setter
    def partition(self, value):
        self._values['partition'] = value

    def _filter_params(self, params):
        return dict((k, v) for k, v in iteritems(params) if v is not None)


class F5ModuleError(Exception):
    pass
