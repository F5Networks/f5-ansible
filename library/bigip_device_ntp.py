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
module: bigip_device_ntp
short_description: Manage NTP servers on a BIG-IP
description:
   - Manage NTP servers on a BIG-IP
version_added: "2.1"
options:
  append:
    description:
      - If C(yes), will only add NTP servers, not set them to just the list
        in C(ntp_servers) or the value of C(ntp_server).
    choices:
      - yes
      - no
    default: no
  server:
    description:
      - BIG-IP host
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  ntp_server:
    description:
      - A single NTP server to set on the device. At least one of C(ntp_servers)
        or C(ntp_server) are required.
    required: false
    default: None
  ntp_servers:
    description:
      - A list of NTP servers to set on the device. At least one of C(ntp_servers)
        or C(ntp_server) are required.
    required: false
    default: []
  state:
    description:
      - The state of the NTP servers on the system. When C(present), guarantees
        that the NTP servers are set on the system. When C(absent), removes the
        specified NTP servers from the device configuration.
    required: false
    default: present
    choices:
      - absent
      - present
  timezone:
    description:
      - The timezone to set for NTP lookups
    default: UTC
    required: false
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
   - Requires the requests Python package on the host. This is as easy as pip
     install requests

requirements: [ "requests", "bigsuds" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
- name: Set the boot.quiet DB variable on the BIG-IP
  bigip_sysdb:
      server: "big-ip"
      key: "boot.quiet"
      value: "disable"
  delegate_to: localhost
"""

import json
import socket

try:
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True


class BigIpCommon(object):
    def __init__(self, user, password, server, ntp_servers=[], timezone=None,
                 append=False, validate_certs=True):

        self._username = user
        self._password = password
        self._hostname = server

        if isinstance(ntp_servers, list):
            self._ntp_servers = ntp_servers
        else:
            self._ntp_servers = [ntp_servers]

        self._timezone = timezone
        self._append = append
        self._validate_certs = validate_certs


class BigIpRest(BigIpCommon):
    """Handles talking to the REST API

    The data structure that is returned by the API looks like this

    {
      "kind": "tm:sys:ntp:ntpstate",
      "selfLink": "https://localhost/mgmt/tm/sys/ntp?ver=12.0.0",
      "servers": [
        "pool.ntp.org",
        "time.ntp.org"
      ],
      "timezone": "America/Los_Angeles",
      "restrictReference": {
        "link": "https://localhost/mgmt/tm/sys/ntp/restrict?ver=12.0.0",
        "isSubcollection": true
      }
    }
    """

    def __init__(self, user, password, server, ntp_servers=[], timezone=None,
                 append=False, validate_certs=True):

        super(BigIpRest, self).__init__(user, password, server, ntp_servers,
                                        timezone, append, validate_certs)

        self._uri = 'https://%s/mgmt/tm/sys/ntp' % (self._hostname)
        self._headers = {
            'Content-Type': 'application/json'
        }

    def read(self):
        resp = requests.get(self._uri,
                            auth=(self._username, self._password),
                            verify=self._validate_certs)

        if resp.status_code != 200:
            return {}
        else:
            return resp.json()

    def present(self):
        changed = False
        payload = dict()
        current = self.read()

        # NTP servers can be set independently
        if self._ntp_servers and self._append:
            if 'servers' in current:
                current_servers = current['servers']
                if not set(self._ntp_servers).issubset(set(current_servers)):
                    current_servers += self._ntp_servers
                    ntp_servers = list(set(current_servers))
                    changed = True
            else:
                ntp_servers = self._ntp_servers
                changed = True
        elif self._ntp_servers:
            if 'servers' in current and current['servers'] != self._ntp_servers:
                ntp_servers = self._ntp_servers
                changed = True
            elif 'servers' not in current:
                ntp_servers = self._ntp_servers
                changed = True

        if changed:
            payload['servers'] = ntp_servers

        # Timezone can be set independently
        if self._timezone:
            if 'timezone' in current and current['timezone'] != self._timezone:
                payload['timezone'] = self._timezone
                changed = True

        if not changed:
            return changed

        resp = requests.patch(self._uri,
                              auth=(self._username, self._password),
                              data=json.dumps(payload),
                              verify=self._validate_certs)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def absent(self):
        changed = False
        payload = dict()
        current = self.read()

        if self._ntp_servers and 'servers' in current:
            servers = current['servers']
            new_servers = [x for x in servers if x not in self._ntp_servers]

            if servers != new_servers:
                payload['servers'] = new_servers
                changed = True

        if not changed:
            return changed

        resp = requests.patch(self._uri,
                              auth=(self._username, self._password),
                              data=json.dumps(payload),
                              verify=self._validate_certs)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def save(self):
        payload = dict(command='save')
        uri = 'https://%s/mgmt/tm/sys/config' % (self._hostname)
        resp = requests.post(uri,
                             auth=(self._username, self._password),
                             data=json.dumps(payload),
                             verify=self._validate_certs)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            append=dict(default='no', type='bool'),
            server=dict(required=True),
            password=dict(required=True),
            ntp_server=dict(required=False, type='str', default=None),
            ntp_servers=dict(required=False, type='list', default=[]),
            state=dict(default='present', choices=['absent', 'present']),
            timezone=dict(default='UTC', required=False),
            user=dict(required=True, aliases=['username']),
            validate_certs=dict(default='yes', type='bool'),
        ),
        required_one_of=[
            ['ntp_server', 'ntp_servers', 'timezone']
        ],
        mutually_exclusive=[
            ['ntp_server', 'ntp_servers']
        ]
    )

    append = module.params.get('append')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')
    timezone = module.params.get('timezone')
    ntp_server = module.params.get('ntp_server')
    ntp_servers = module.params.get('ntp_servers')
    validate_certs = module.params.get('validate_certs')

    try:
        if ntp_server:
            ntp_servers = ntp_server

        if append and not ntp_servers:
            module.fail_json(msg='The append parameter requires at least one NTP server')

        if not requests_found:
            raise Exception("The python requests module is required")

        obj = BigIpRest(username, password, hostname, ntp_servers, timezone,
                        append, validate_certs)

        if state == "present":
            if obj.present():
                changed = True
        elif state == "absent":
            if not ntp_servers:
                module.fail_json(msg='State absent is only relevant when removing NTP servers')

            if obj.absent():
                changed = True
    except socket.timeout, e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except Exception, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
