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
  banner_text:
    description:
      - Specifies the text to present in the advisory banner.
    required: false
    default: None
  console_timeout:
    description:
      - Specifies the number of seconds of inactivity before the system logs
        off a user that is logged on.
    required: false
    default: None
  gui_setup:
    description:
      - C(enable) or C(disabled) the Setup utility in the browser-based
        Configuration utility
    required: false
    default: None
    choices:
      - enabled
      - disabled
  lcd_display:
    description:
      - Specifies, when C(enabled), that the system menu displays on the
        LCD screen on the front of the unit. This setting has no effect
        when used on the VE platform.
    required: false
    default: None
    choices:
      - enabled
      - disabled
  mgmt_dhcp:
    description:
      - Specifies whether or not to enable DHCP client on the management
        interface
    required: false
    default: None
    choices:
      - enabled
      - disabled
  net_reboot:
    description:
      - Specifies, when C(enabled), that the next time you reboot the system,
        the system boots to an ISO image on the network, rather than an
        internal media drive.
    choices:
      - enabled
      - disabled
    required: false
    default: None
  quiet_boot:
    description:
      - Specifies, when C(enabled), that the system suppresses informational
        text on the console during the boot cycle. When C(disabled), the
        system presents messages and informational text on the console during
        the boot cycle.
  security_banner:
    description:
      - Specifies whether the system displays an advisory message on the
        login screen.
    choices:
      - enabled
      - disabled
    required: false
    default: None
  state:
    description:
      - The state of the variable on the system. When C(present), guarantees
        that an existing variable is set to C(value).
    required: false
    default: present
    choices:
      - present
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
- name: Disable the setup utility
  bigip_sys_global:
      gui_setup: "disabled"
      password: "secret"
      server: "lb.mydomain.com"
      user: "admin"
      state: "present"
  delegate_to: localhost
'''

RETURN = '''
banner_text:
    description: The new text to present in the advisory banner.
    returned: changed
    type: string
    sample: "This is a corporate device. Do not touch."
console_timeout:
    description: >
      The new number of seconds of inactivity before the system
      logs off a user that is logged on.
    returned: changed
    type: integer
    sample: 600
gui_setup:
    description: The new setting for the Setup utility.
    returned: changed
    type: string
    sample: enabled
lcd_display:
    description: The new setting for displaying the system menu on the LCD.
    returned: changed
    type: string
    sample: enabled
mgmt_dhcp:
    description: >
      The new setting for whether the mgmt interface should DHCP
      or not
    returned: changed
    type: string
    sample: enabled
net_reboot:
    description: >
      The new setting for whether the system should boot to an ISO on the
      network or not
    returned: changed
    type: string
    sample: enabled
quiet_boot:
    description: >
      The new setting for whether the system should suppress information to
      the console during boot or not.
    returned: changed
    type: string
    sample: enabled
security_banner:
    description: >
      The new setting for whether the system should display an advisory message
      on the login screen or not
    returned: changed
    type: string
    sample: enabled
'''

try:
    from f5.bigip import ManagementRoot
    from icontrol.session import iControlUnexpectedHTTPError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


CHOICES = ['enabled', 'disabled']


class BigIpSysGlobal(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5SDKError("The python f5-sdk module is required")

        # The params that change in the module
        self.cparams = dict()

        # Stores the params that are sent to the module
        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def flush(self):
        result = dict()
        changed = False

        try:
            changed = self.update()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        result.update(**self.cparams)
        result.update(dict(changed=changed))
        return result

    def read(self):
        """Read information and transform it

        The values that are returned by BIG-IP in the f5-sdk can have encoding
        attached to them as well as be completely missing in some cases.

        Therefore, this method will transform the data from the BIG-IP into a
        format that is more easily consumable by the rest of the class and the
        parameters that are supported by the module.
        """
        p = dict()
        r = self.api.tm.sys.global_settings.load()

        if hasattr(r, 'guiSecurityBanner'):
            p['security_banner'] = str(r.guiSecurityBanner)
        if hasattr(r, 'guiSecurityBannerText'):
            p['banner_text'] = str(r.guiSecurityBannerText)
        if hasattr(r, 'guiSetup'):
            p['gui_setup'] = str(r.guiSetup)
        if hasattr(r, 'lcdDisplay'):
            p['lcd_display'] = str(r.lcdDisplay)
        if hasattr(r, 'mgmtDhcp'):
            p['mgmt_dhcp'] = str(r.mgmtDhcp)
        if hasattr(r, 'netReboot'):
            p['net_reboot'] = str(r.netReboot)
        if hasattr(r, 'quietBoot'):
            p['quiet_boot'] = str(r.quietBoot)
        if hasattr(r, 'consoleInactivityTimeout'):
            p['console_timeout'] = int(r.consoleInactivityTimeout)
        return p

    def update(self):
        changed = False
        current = self.read()
        params = dict()

        security_banner = self.params['security_banner']
        banner_text = self.params['banner_text']
        gui_setup = self.params['gui_setup']
        lcd_display = self.params['lcd_display']
        mgmt_dhcp = self.params['mgmt_dhcp']
        net_reboot = self.params['net_reboot']
        quiet_boot = self.params['quiet_boot']
        console_timeout = self.params['console_timeout']
        check_mode = self.params['check_mode']

        if security_banner:
            if 'security_banner' in current:
                if security_banner != current['security_banner']:
                    params['guiSecurityBanner'] = security_banner
            else:
                params['guiSecurityBanner'] = security_banner

        if banner_text:
            if 'banner_text' in current:
                if banner_text != current['banner_text']:
                    params['guiSecurityBannerText'] = banner_text
            else:
                params['guiSecurityBannerText'] = banner_text

        if gui_setup:
            if 'gui_setup' in current:
                if gui_setup != current['gui_setup']:
                    params['guiSetup'] = gui_setup
            else:
                params['guiSetup'] = gui_setup

        if lcd_display:
            if 'lcd_display' in current:
                if lcd_display != current['lcd_display']:
                    params['lcdDisplay'] = lcd_display
            else:
                params['lcdDisplay'] = lcd_display

        if mgmt_dhcp:
            if 'mgmt_dhcp' in current:
                if mgmt_dhcp != current['mgmt_dhcp']:
                    params['mgmtDhcp'] = mgmt_dhcp
            else:
                params['mgmtDhcp'] = mgmt_dhcp

        if net_reboot:
            if 'net_reboot' in current:
                if net_reboot != current['net_reboot']:
                    params['netReboot'] = net_reboot
            else:
                params['netReboot'] = net_reboot

        if quiet_boot:
            if 'quiet_boot' in current:
                if quiet_boot != current['quiet_boot']:
                    params['quietBoot'] = quiet_boot
            else:
                params['quietBoot'] = quiet_boot

        if console_timeout:
            if 'console_timeout' in current:
                if console_timeout != current['console_timeout']:
                    params['consoleInactivityTimeout'] = console_timeout
            else:
                params['consoleInactivityTimeout'] = console_timeout

        if params:
            changed = True
            if check_mode:
                return changed
            self.cparams = camel_dict_to_snake_dict(params)
        else:
            return changed

        r = self.api.tm.sys.global_settings.load()
        r.update(**params)
        r.refresh()

        return changed


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        security_banner=dict(required=False, choices=CHOICES, default=None),
        banner_text=dict(required=False, default=None),
        gui_setup=dict(required=False, choices=CHOICES, default=None),
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
        obj = BigIpSysGlobal(check_mode=module.check_mode, **module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import camel_dict_to_snake_dict
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
