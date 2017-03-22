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
module: bigip_service
short_description: Manage BIG-IP service states
description:
  - Manage BIG-IP service states
version_added: "2.2"
options:
  server:
    description:
      - BIG-IP host
    required: true
  name:
    description:
      - Name of the service
    choices:
      - big3d
      - gtmd
      - named
      - ntpd
      - snmpd
      - sshd
      - zrd
      - websso
    required: true
  password:
    description:
      - BIG-IP password
    required: true
    default: admin
  state:
    description:
      - C(started)/C(stopped) are idempotent actions that will not run commands
        unless necessary. C(restarted) will always bounce the service.
    required: false
    default: None
    choices:
      - started
      - stopped
      - restarted
  user:
    description:
      - BIG-IP username
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: yes
    choices:
      - yes
      - no
notes:
  - Requires the bigsuds Python package on the host if using the iControl
    interface. This is as easy as pip install bigsuds
requirements:
  - bigsuds
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Restart the BIG-IP sshd service
  bigip_service:
      server: "big-ip"
      name: "sshd"
      user: "admin"
      password: "admin"
      state: "restarted"
  delegate_to: localhost
'''

import socket
import time

try:
    import bigsuds
except ImportError:
    bigsuds_found = False
else:
    bigsuds_found = True


class BigIpCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._hostname = module.params.get('server')

        self._service = module.params.get('name')
        self._timeout = module.params.get('timeout')
        self._validate_certs = module.params.get('validate_certs')


class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )

        # We do not support all services because disabling/stopping some of
        # them would break the system
        service_map = {
            'big3d': 'SERVICE_BIG3D',
            'gtmd': 'SERVICE_GTMD',
            'named': 'SERVICE_NAMED',
            'ntpd': 'SERVICE_NTPD',
            'snmpd': 'SERVICE_SNMPD',
            'sshd': 'SERVICE_SSHD',
            'zrd': 'SERVICE_ZRD',
            'websso': 'SERVICE_WEBSSO'
        }

        service = service_map[self._service]
        self._service = service

    def is_supported_service(self):
        services = self.api.System.Services.get_list()
        if self._service in services:
            return True
        else:
            return False

    def get_service_status(self):
        result = self.api.System.Services.get_service_status([self._service])
        if result[0]['status'] == 'SERVICE_STATUS_UP':
            return 'started'
        elif result[0]['status'] == 'SERVICE_STATUS_DOWN':
            return 'stopped'

    def _wait_for_service(self, state):
        timeout = time.time() + int(self._timeout)
        while True:
            status = self.get_service_status()

            if time.time() > timeout:
                break
            elif status == state:
                break
            else:
                time.sleep(1)

    def started(self):
        try:
            self.api.System.Services.set_service(
                services=[self._service],
                service_action='SERVICE_ACTION_START'
            )
            changed = True
        except Exception:
            raise Exception('Failed to start the service')
        self._wait_for_service('started')

        return changed

    def stopped(self):
        try:
            self.api.System.Services.set_service(
                services=[self._service],
                service_action='SERVICE_ACTION_STOP'
            )
            changed = True
        except Exception:
            raise Exception('Failed to stop the service')
        self._wait_for_service('stopped')

        return changed

    def restarted(self):
        try:
            self.api.System.Services.set_service(
                services=[self._service],
                service_action='SERVICE_ACTION_RESTART'
            )
            changed = True
        except Exception:
            raise Exception('Failed to restart the service')

        self._wait_for_service('started')

        return changed


def main():
    changed = False

    service_choices = [
        'big3d', 'gtmd', 'named', 'ntpd', 'snmpd', 'sshd', 'zrd', 'websso'
    ]

    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(default='icontrol', choices=['icontrol', 'rest']),
            server=dict(required=True),
            name=dict(required=True, choices=service_choices),
            password=dict(default='admin'),
            state=dict(default=None, choices=['started', 'stopped', 'restarted']),
            user=dict(required=True),
            validate_certs=dict(default='yes', type='bool', choices=['yes', 'no']),
            timeout=dict(default='60')
        )
    )

    connection = module.params.get('connection')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')

    try:
        if connection == 'icontrol':
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            icontrol = test_icontrol(username, password, hostname)
            if icontrol:
                obj = BigIpIControl(module)
        elif connection == 'rest':
            if not requests_found:
                raise Exception("The REST connection is not currently supported")

        if not obj.is_supported_service():
            module.fail_json(msg="The specified service is not supported on this platform")

        status = obj.get_service_status()

        if state == "started" and status != 'started':
            if obj.started():
                changed = True
        elif state == "stopped" and status != 'stopped':
            if obj.stopped():
                changed = True
        elif state == "restarted":
            if obj.restarted():
                changed = True
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except socket.timeout:
        module.fail_json(msg="Timed out connecting to the BIG-IP")

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
