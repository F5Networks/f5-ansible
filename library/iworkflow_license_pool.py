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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
module: iworkflow_license_pool
short_description: Manage license pools in iWorkflow.
description:
  - Manage license pools in iWorkflow.
version_added: 2.4
options:
  name:
    description:
      - Name of the license pool to create.
    required: True
  state:
    description:
      - Whether the license pool should exist, or not. A state of C(present)
        will attempt to activate the license pool if C(accept_eula) is set
        to C(yes).
    required: False
    default: present
    choices:
      - present
      - absent
  base_key:
    description:
      - Key that the license server uses to verify the functionality that
        you are entitled to license. This option is required if you are
        creating a new license.
    required: False
    default: None
  accept_eula:
    description:
      - Specifies that you accept the EULA that is part of iWorkflow. Note
        that this is required to activate the license pool. If this is not
        specified, or it is set to C(no), then the pool will remain in a state
        of limbo until you choose to accept the EULA. This option is required
        when updating a license. It is also suggested that you provide it when
        creating a license, but if you do not, the license will remain
        inactive and you will have to run this module again with this option
        set to C(yes) to activate it.
    required: False
    default: 'no'
    choices:
      - yes
      - no
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
requirements:
    - f5-sdk >= 2.3.0
    - iWorkflow >= 2.1.0
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Create license pool
  iworkflow_license_pool:
      accept_eula: "yes"
      name: "my-lic-pool"
      base_key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
      state: "present"
      server: "iwf.mydomain.com"
      password: "secret"
      user: "admin"
      validate_certs: "no"
  delegate_to: localhost
'''

RETURN = '''
'''

import time

from ansible.module_utils.basic import BOOLEANS
from ansible.module_utils.f5_utils import (
    AnsibleF5Client,
    AnsibleF5Parameters,
    F5ModuleError,
    HAS_F5SDK,
    iControlUnexpectedHTTPError
)


class Parameters(AnsibleF5Parameters):
    api_map = {
        'baseRegKey': 'base_key'
    }
    returnables = []
    api_attributes = [
        'baseRegKey', 'state'
    ]
    updatables = []

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result

    @property
    def name(self):
        if self._values['name'] is None:
            return None
        name = str(self._values['name']).strip()
        if name == '':
            raise F5ModuleError(
                "You must specify a name for this module"
            )
        return name


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(changed)

    def _update_changed_options(self):
        changed = {}
        for key in Parameters.updatables:
            if getattr(self.want, key) is not None:
                attr1 = getattr(self.want, key)
                attr2 = getattr(self.have, key)
                if attr1 != attr2:
                    changed[key] = attr1
        if changed:
            self.changes = Parameters(changed)
            return True
        return False

    def _pool_is_licensed(self):
        if self.have.state == 'LICENSED':
            return True
        return False

    def _pool_is_unlicensed_eula_unaccepted(self, current):
        if current.state != 'LICENSED' and not self.want.accept_eula:
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

        result.update(**self.changes.to_return())
        result.update(dict(changed=changed))
        return result

    def exists(self):
        collection = self.client.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.want.name)
            )
        )
        if len(collection) == 1:
            return True
        elif len(collection) == 0:
            return False
        else:
            raise F5ModuleError(
                "Multiple license pools with the provided name were found!"
            )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def should_update(self):
        if self._pool_is_licensed():
            return False
        if self._pool_is_unlicensed_eula_unaccepted():
            return False
        return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def update_on_device(self):
        collection = self.client.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.want.name)
            )
        )
        resource = collection.pop()
        resource.modify(
            state='RELICENSE',
            method='AUTOMATIC'
        )
        return self._wait_for_license_pool_state_to_activate(resource)

    def create(self):
        self._set_changed_options()
        if self.client.check_mode:
            return True
        if self.want.base_key is None:
            raise F5ModuleError(
                "You must specify a 'base_key' when creating a license pool"
            )
        self.create_on_device()
        return True

    def read_current_from_device(self):
        collection = self.client.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.want.name)
            )
        )
        resource = collection.pop()
        result = resource.attrs
        return Parameters(result)

    def create_on_device(self):
        resource = self.client.api.cm.shared.licensing.pools_s.pool.create(
            name=self.want.name,
            baseRegKey=self.want.base_key,
            method="AUTOMATIC"
        )
        return self._wait_for_license_pool_state_to_activate(resource)

    def _wait_for_license_pool_state_to_activate(self, pool):
        error_values = ['EXPIRED', 'FAILED']
        # Wait no more than 5 minutes
        for x in range(1, 30):
            pool.refresh()
            if pool.state == 'LICENSED':
                return True
            elif pool.state == 'WAITING_FOR_EULA_ACCEPTANCE':
                pool.modify(
                    eulaText=pool.eulaText,
                    state='ACCEPTED_EULA'
                )
            elif pool.state in error_values:
                raise F5ModuleError(pool.errorText)
            time.sleep(10)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.client.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the license pool")
        return True

    def remove_from_device(self):
        collection = self.client.api.cm.shared.licensing.pools_s.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(self.want.name)
            )
        )
        resource = collection.pop()
        if resource:
            resource.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            accept_eula=dict(
                type='bool',
                default='no',
                choices=BOOLEANS
            ),
            base_key=dict(
                required=False,
                no_log=True
            ),
            name=dict(
                required=True
            ),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']
            )
        )
        self.f5_product_name = 'iworkflow'


def main():
    if not HAS_F5SDK:
        raise F5ModuleError("The python f5-sdk module is required")

    spec = ArgumentSpec()

    client = AnsibleF5Client(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        f5_product_name=spec.f5_product_name
    )

    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
