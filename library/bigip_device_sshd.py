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
module: bigip_device_sshd
short_description: Manage the SSHD settings of a BIG-IP
description:
  - Manage the SSHD settings of a BIG-IP
version_added: "2.2"
options:
  banner:
    description:
      - Whether to enable the banner or not
    required: false
    choices:
      - enabled
      - disabled
  banner_text:
    description:
      - Specifies the text to include on the pre-login banner that displays
        when a user attempts to login to the system using SSH
    required: false
  inactivity_timeout:
    description:
      - Specifies the number of seconds before inactivity causes an SSH
        session to log out
    required: false
  log_level:
    description:
      - Specifies the minimum SSHD message level to include in the system log
    choices:
      - debug
      - debug1
      - debug2
      - debug3
      - error
      - fatal
      - info
      - quiet
      - verbose
  login:
    description:
      - Specifies, when checked C(enabled), that the system accepts SSH
        communications
    required: false
  password:
    description:
      - BIG-IP password
    required: true
  port:
    description:
      - Port that you want the SSH daemon to run on
    required: false
  server:
    description:
      - BIG-IP host
    required: true
  server_port:
    description:
      - BIG-IP server port
    required: false
    default: 443
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
  - Requires the f5-sdk Python package on the host This is as easy as pip
    install f5-sdk
requirements:
  - f5-sdk
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Set the banner for the SSHD service from a string
  bigip_device_sshd:
      banner: "enabled"
      banner_text: "banner text goes here"
      password: "admin"
      server: "bigip.localhost.localdomain"
      user: "admin"
  delegate_to: localhost

- name: Set the banner for the SSHD service from a file
  bigip_device_sshd:
      banner: "enabled"
      banner_text: "{{ lookup('file', '/path/to/file') }}"
      password: "admin"
      server: "bigip.localhost.localdomain"
      user: "admin"
  delegate_to: localhost

- name: Set the SSHD service to run on port 2222
  bigip_device_sshd:
      password: "admin"
      port: 2222
      server: "bigip.localhost.localdomain"
      user: "admin"
  delegate_to: localhost
'''

try:
    from f5.bigip import ManagementRoot
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

CHOICES = ['enabled', 'disabled']
LEVELS = ['debug', 'debug1', 'debug2', 'debug3', 'error', 'fatal', 'info',
          'quiet', 'verbose']


class F5ModuleError(Exception):
    pass


class BigIpDeviceSshd(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'])

    def update(self):
        changed = False
        current = self.read()

        if self.params['allow']:
            if self.params['allow'] != current['allow']:
                changed = True
        else:
            del self.params['allow']

        if self.params['banner']:
            if self.params['banner'] != current['banner']:
                changed = True
        else:
            del self.params['banner']

        if self.params['banner_text']:
            if self.params['banner_text'] != current['banner_text']:
                changed = True
        else:
            del self.params['banner_text']

        if self.params['inactivity_timeout']:
            if self.params['inactivity_timeout'] != current['inactivity_timeout']:
                changed = True
        else:
            del self.params['inactivity_timeout']

        if self.params['log_level']:
            if self.params['log_level'] != current['log_level']:
                changed = True
        else:
            del self.params['log_level']

        if self.params['login']:
            if self.params['login'] != current['login']:
                changed = True
        else:
            del self.params['login']

        if self.params['port']:
            if self.params['port'] != current['port']:
                changed = True
        else:
            del self.params['port']

        if self.params['check_mode']:
            return changed

        r = self.api.tm.sys.sshd.load()
        r.update(**self.params)

        return True

    def read(self):
        r = self.api.tm.sys.sshd.load()
        return r

    def flush(self):
        changed = self.update()
        current = self.read()
        result.update(**current)

        result.update(dict(changed=changed))
        return result


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        allow=dict(required=False, default=None),
        banner=dict(required=False, default=None, choices=CHOICES),
        banner_text=dict(required=False, default=None),
        inactivity_timeout=dict(required=False, default=None, type='int'),
        log_level=dict(required=False, default=None, choices=LEVELS),
        login=dict(required=False, default=None, choices=CHOICES),
        port=dict(required=False, default=None, type='int'),
        state=dict(default='present', choices=['present'])
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpDeviceSshd(**module.params)
        result = obj.flush()

        module.exit_json(**result)
    except F5ModuleError as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
