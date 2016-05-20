#!/usr/bin/python
# -*- coding: utf-8 -*-
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
module: bigip_sys_global
short_description: Manage BIG-IP global settings
description:
   - Manage BIG-IP global settings
version_added: "2.2"
options:
  server:
    description:
      - BIG-IP host
    required: true
  server_port:
    description:
      - BIG-IP host port
    required: false
    default: 443
  password:
    description:
      - BIG-IP password
    required: true
  state:
    description:
      - The state of the variable on the system. When C(present), guarantees
        that an existing variable is set to C(value). When C(reset) sets the
        variable back to the default value. At least one of value and state
        C(reset) are required.
    required: false
    default: present
    choices:
      - present
      - reset
  user:
    description:
      - BIG-IP username
    required: true
    aliases:
      - username
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk
requirements:
  - f5-sdk
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

try:
    from f5.bigip import ManagementRoot
    from f5.sdk_exception import F5SDKError
    HAS_F5SDK = True
except:
    HAS_F5SDK = False


CHOICES = ['enabled', 'disabled']


class BigIpSysDb():
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5SDKError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def flush(self):
        changed = False
        result = dict()
        security_banner = self.params['security_banner']

        banner_text=dict(required=False, default=None),
        gui_setup=dict(required=false, choices=CHOICES, default=None),
        lcd_display=dict(required=False, choices=CHOICES, default=None),
        mgmt_dhcp=dict(required=False, choices=CHOICES, default=None),
        net_reboot=dict(required=False, choices=CHOICES, default=None),
        quiet_boot=dict(required=False, choices=CHOICES, default=None),
        console_timeout=dict(required=False, type='int', default=None),

        current = self.read()

        if self.params['check_mode']:
            if security_banner:
                if security_banner != current['guiSecurityBanner']:
                    changed = True

            if banner_text is not None:
                # Comparing to 'None' because an empty string is valid
                if banner_text != current['guiSecurityBannerText']:
                    changed = True

        else:
            if state == "present":
                changed = self.present()

            if not self.params['check_mode']:
                current = self.read()
                result.update(current)

        result.update(dict(changed=changed))
        return result

    def read(self):
        settings = self.api.tm.sys.global_settings.load()
        return settings

    def present(self):
        current = self.read()

        if current['value'] == self.params['value']:
            return False

        current.update(self.params['value'])
        current.refresh()

        if current['value'] == self.params['value']:
            raise F5ModuleError(
                "Failed to set the DB variable"
            )
        return True


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        security_banner=dict(required=False, choices=CHOICES, default=None),
        banner_text=dict(required=False, default=None),
        gui_setup=dict(required=false, choices=CHOICES, default=None),
        lcd_display=dict(required=False, choices=CHOICES, default=None),
        mgmt_dhcp=dict(required=False, choices=CHOICES, default=None),
        net_reboot=dict(required=False, choices=CHOICES, default=None),
        quiet_boot=dict(required=False, choices=CHOICES, default=None),
        console_timeout=dict(required=False, type='int', default=None),
        state=dict(default='present', choices=['present'])
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpSysGlobal(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5SDKError, e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
