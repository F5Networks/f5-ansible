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
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


CHOICES = ['enabled', 'disabled']


class BigIpSysDb(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5SDKError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def flush(self):
        changed = self.update()
        current = self.read()
        result.update(**current)

        result.update(dict(changed=changed))
        return result

    def read(self):
        settings = self.api.tm.sys.global_settings.load()
        return settings

    def update(self):
        changed = False
        current = self.read()

        if self.params['security_banner']:
            if self.params['security_banner'] != current['guiSecurityBanner']:
                changed = True
        else:
            del self.params['security_banner']

        if self.params['banner_text']:
            if self.params['banner_text'] != current['guiSecurityBannerText']:
                changed = True
        else:
            del self.params['banner_text']

        if self.params['gui_setup']:
            if self.params['gui_setup'] != current['guiSetup']:
                changed = True
        else:
            del self.params['guiSetup']

        if self.params['lcd_display']:
            if self.params['lcd_display'] != current['lcdDisplay']:
                changed = True
        else:
            del self.params['lcd_display']

        if self.params['mgmt_dhcp']:
            if self.params['mgmt_dhcp'] != current['mgmtDhcp']:
                changed = True
        else:
            del self.params['mgmt_dhcp']

        if self.params['net_reboot']:
            if self.params['net_reboot'] != current['netReboot']:
                changed = True
        else:
            del self.params['net_reboot']

        if self.params['quiet_boot']:
            if self.params['quiet_boot'] != current['quietBoot']:
                changed = True
        else:
            del self.params['quiet_boot']

        if self.params['console_timeout']:
            if self.params['console_timeout'] != current['consoleInactivityTimeout']:
                changed = True
        else:
            del self.params['console_timeout']

        if self.params['check_mode']:
            return changed

        r = self.api.tm.sys.sshd.load()
        r.update(**self.params)

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
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
