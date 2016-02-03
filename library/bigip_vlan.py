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
#
# Based on work by Kevin Maloney and Rick Masters

DOCUMENTATION = '''
---
module: bigip_vlan
short_description: Manage VLANs on a BIG-IP system
description:
   - Manage VLANs on a BIG-IP system
version_added: "2.0"
options:
  description:
    description:
      - The description to give to the VLAN
    required: false
    default: None
  interface:
    description:
      - The interface to create the VLAN on when C(state) is C(present)
  interfaces:
    description:
      - Specifies a list of tagged or untagged interfaces and trunks that you
        want to configure for the VLAN. Use tagged interfaces or trunks when
        you want to assign a single interface or trunk to multiple VLANs.
    required: false
    dfault: None
  name:
    description:
      - The VLAN to manage. If the special VLAN C(ALL) is specified with
        the C(state) value of C(absent) then all VLANs will be removed.
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  route_domain:
    description:
      - The route domain that the VLAN is associated with if something other
        than Common
    required: false
    default: None
  server:
    description:
      - BIG-IP host
    required: true
  state:
    description:
      - The state of the VLAN on the system. When C(present), guarantees
        that the VLAN exists with the provided attributes. When C(absent),
        removes the VLAN from the system.
    required: false
    default: present
    choices:
      - absent
      - present
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
  vlan_id:
    description:
      - The ID (tag) of the VLAN
    required: true
    aliases:
      - tag
notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds

requirements: [ "bigsuds", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
"""

import json
import socket
import os

try:
    import bigsuds
except ImportError:
    bigsuds_found = False
else:
    bigsuds_found = True

try:
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True

CONNECTION_TIMEOUT = 30
OBJ_PREFIX = 'uuid_'
BIGIP_VE_PLATFORM_ID = 'Z100'


class VLANCreationException(Exception):
    """VLANCreationException"""
    pass


class VLANDeleteException(Exception):
    """VLANDeleteException"""
    pass


class VLANQueryException(Exception):
    """VLANQueryException"""
    pass


class VLANUpdateException(Exception):
    """VLANUpdateException"""
    pass


class SystemQueryException(Exception):
    """SystemQueryException"""
    pass


class RouteQueryException(Exception):
    """RouteQueryException"""
    pass


class RouteUpdateException(Exception):
    """RouteUpdateException"""
    pass


def strip_folder_and_prefix(path):
    """ Strip folder and prefix """
    if isinstance(path, list):
        for i in range(len(path)):
            if path[i].find('~') > -1:
                path[i] = path[i].replace('~', '/')
            if path[i].startswith('/Common'):
                path[i] = path[i].replace(OBJ_PREFIX, '')
            else:
                path[i] = \
                    os.path.basename(str(path[i])).replace(OBJ_PREFIX, '')
        return path
    else:
        if path.find('~') > -1:
            path = path.replace('~', '/')
        if path.startswith('/Common'):
            return str(path).replace(OBJ_PREFIX, '')
        else:
            return os.path.basename(str(path)).replace(OBJ_PREFIX, '')


def test_icontrol(username, password, hostname):
    api = bigsuds.BIGIP(
        hostname=hostname,
        username=username,
        password=password,
        debug=True
    )

    try:
        response = api.Management.LicenseAdministration.get_license_activation_status()
        if 'STATE' in response:
            return True
        else:
            return False
    except:
        return False


class BigIpCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._hostname = module.params.get('server')

        self._name = module.params.get('name')
        self._description = module.params.get('description')
        self._interface = module.params.get('interface')
        self._route_domain = module.params.get('route_domain')
        self._vlan_id = module.params.get('vlan_id')

        self._validate_certs = module.params.get('validate_certs')

        if not self._validate_certs:
            requests.packages.urllib3.disable_warnings()


class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm' % self._hostname
        self.systeminfo = None
        self.api = self._get_icr_session(
            self._hostname, self._username, self._password,
            validate_certs=self._validate_certs
        )
        self.icontrol = BigIpIControl(module)

    def icr_link(self, selfLink):
        """ Create iControl REST link """
        return selfLink.replace('https://localhost/mgmt/tm', self._uri)

    def _get_icr_session(self, hostname, username, password, validate_certs=False, timeout=None):
        """ Get iControl REST Session """
        icr_session = requests.session()
        icr_session.auth = (username, password)
        icr_session.verify = validate_certs
        icr_session.headers.update({'Content-Type': 'application/json'})
        if timeout:
            socket.setdefaulttimeout(timeout)
        else:
            socket.setdefaulttimeout(CONNECTION_TIMEOUT)

        return icr_session

    def absent(self):
        if self._name == 'ALL':
            vlans = self.get_vlans()
            if len(vlans) == 0:
                return False
            else:
                self.delete_all()
                return True
        elif self.exists(name=self._name):
            self.delete(name=self._name)
            return True
        else:
            return False

    def present(self):
        changed = False

        if not self.exists(self._name):
            if self._route_domain:
                route_domain_id = self.get_domain(self._route_domain)
            else:
                route_domain_id = 0

            self.create(name=self._name,
                        vlanid=self._vlan_id,
                        interface=self._interface,
                        description=self._description,
                        route_domain_id=route_domain_id
                        )
            return True

        if self._vlan_id:
            if self.get_id(self._name) != int(self._vlan_id):
                self.set_id(name=self._name, vlanid=self._vlan_id)
                changed = True

        if self._interface:
            if self.get_interface(self._name) != self._interface:
                self.set_interface(name=self._name, interface=self._interface)
                changed = True

        if self._description:
            if self.get_description(self._name) != self._description:
                self.set_description(name=self._name, description=self._description)
                changed = True

        return changed

    def create(self, name=None, vlanid=None, interface=None,
               folder='Common', description=None, route_domain_id=0):
        """ Create vlan.
            route_domain_id is an int  """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if vlanid:
                payload['tag'] = vlanid
                if interface:
                    payload['interfaces'] = [{'name': interface,
                                              'tagged': True}]
            else:
                payload['tag'] = 0
                if interface:
                    payload['interfaces'] = [{'name': interface,
                                              'untagged': True}]
            if description:
                payload['description'] = description
            request_url = self._uri + '/net/vlan/'
            response = self.api.post(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                if not folder == 'Common':
                    self.add_vlan_to_domain_by_id(
                        name=name, folder=folder,
                        route_domain_id=route_domain_id)
                return True
            elif response.status_code == 409:
                return True
            else:
                raise VLANCreationException(response.text)
        return False

    def delete(self, name=None, folder='Common'):
        """ Delete vlan """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            response = self.api.delete(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                raise VLANDeleteException(response.text)
            else:
                return True
        return False

    def delete_all(self, folder='Common'):
        """ Delete vlans """
        folder = str(folder).replace('/', '')
        request_url = self._uri + '/net/vlan/'
        request_url += '?$select=name,selfLink'
        request_filter = 'partition eq ' + folder
        request_url += '&$filter=' + request_filter
        response = self.api.get(
            request_url, timeout=CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for item in response_obj['items']:
                    response = self.api.delete(
                        self.icr_link(item['selfLink']),
                        timeout=CONNECTION_TIMEOUT)
                    if response.status_code > 400 and \
                       response.status_code != 404:
                        raise VLANDeleteException(response.text)
        elif response.status_code == 404:
            return True
        else:
            raise VLANQueryException(response.text)

    def get_vlans(self, folder='Common'):
        """ Get vlans """
        request_url = self._uri + '/net/vlan/'
        request_url += '?$select=name'
        if folder:
            folder = str(folder).replace('/', '')
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.api.get(
            request_url, timeout=CONNECTION_TIMEOUT)
        return_list = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for vlan in return_obj['items']:
                    return_list.append(strip_folder_and_prefix(vlan['name']))
        elif response.status_code != 404:
            raise VLANQueryException(response.text)
        return return_list

    def get_id(self, name=None, folder='Common'):
        """ Get vlan id """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=tag'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return return_obj['tag']
            elif response.status_code != 404:
                raise VLANQueryException(response.text)
        return 0

    def set_id(self, name=None, vlanid=0, folder='Common'):
        """ Set vlan id """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['tag'] = vlanid
            response = self.api.put(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise VLANUpdateException(response.text)
        return False

    def get_interface(self, name=None, folder='Common'):
        """ Get vlan interface by name """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            request_url += '/interfaces?$select=name'
            if folder:
                request_filter = 'partition eq ' + folder
                request_url += '&$filter=' + request_filter
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for interface in return_obj['items']:
                        return interface['name']
            elif response.status_code == 404:
                return None
            else:
                raise VLANQueryException(response.text)
        return None

    def set_interface(self, name=None, interface='1.1', folder='Common'):
        """ Set vlan interface """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            if self.get_platform().startswith(BIGIP_VE_PLATFORM_ID):
                payload['interfaces'] = [{'name': interface, 'untagged': True}]
            else:
                payload['interfaces'] = [{'name': interface, 'untagged': True}]
            response = self.api.put(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise VLANUpdateException(response.text)
        return False

    def set_description(self, name=None, description=None, folder='Common'):
        """ Set vlan description """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['description'] = description
            response = self.api.put(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise VLANUpdateException(response.text)
        return False

    def get_description(self, name=None, folder='Common'):
        """ Get vlan description """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + \
                '/net/vlan?$select=name,description'
            if folder:
                request_filter = 'partition eq ' + folder
                request_url += '&$filter=' + request_filter
            else:
                folder = 'Common'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for vlan in return_obj['items']:
                        vlan_name = os.path.basename(vlan['name'])
                        if vlan_name == name:
                            if 'description' in vlan:
                                return vlan['description']
                        if vlan_name == \
                           strip_folder_and_prefix(name):
                            if 'description' in vlan:
                                return vlan['description']
            elif response.status_code != 404:
                raise VLANQueryException(response.text)
        return None

    def exists(self, name=None, folder='Common'):
        """ Does vlan exist? """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=name'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                raise VLANQueryException(response.text)
        return False

    def get_platform(self):
        """ Get platform """
        if not self.systeminfo:
            try:
                self.systeminfo = self.icontrol.api.System.SystemInfo.get_system_information()
            except Exception as exc:
                raise SystemQueryException(exc.message)
        return self.systeminfo['product_category']

    def add_vlan_to_domain_by_id(
            self, name=None, folder='Common', route_domain_id=0):
        """ Add VLANs to Domain """
        folder = str(folder).replace('/', '')
        existing_vlans = self.get_vlans_in_domain_by_id(
            folder=folder, route_domain_id=route_domain_id)
        route_domain = self.get_domain_by_id(
            folder=folder, route_domain_id=route_domain_id)
        if not route_domain:
            raise RouteUpdateException("Cannot get route domain %s" % route_domain_id)
        if name not in existing_vlans:
            existing_vlans.append(name)
            vlans = dict()
            vlans['vlans'] = existing_vlans
            request_url = self._uri + '/net/route-domain/'
            request_url += '~' + folder + '~' + route_domain['name']
            response = self.api.put(
                request_url, data=json.dumps(vlans),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise RouteUpdateException(response.text)
        return False

    def get_vlans_in_domain_by_id(self, folder='/Common', route_domain_id=0):
        """ Get VLANs in Domain """
        route_domain = self.get_domain_by_id(
            folder=folder, route_domain_id=route_domain_id)
        vlans = []
        if 'vlans' in route_domain:
            for vlan in route_domain['vlans']:
                vlans.append(vlan)
        return vlans

    def get_domain_by_id(self, folder='/Common', route_domain_id=0):
        """ Get VLANs in Domain """
        folder = str(folder).replace('/', '')
        request_url = self._uri + \
            '/net/route-domain?$select=id,name,partition,vlans'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.api.get(request_url, timeout=CONNECTION_TIMEOUT)

        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for route_domain in response_obj['items']:
                    if int(route_domain['id']) == route_domain_id:
                        return route_domain
            return None
        else:
            if response.status_code != 404:
                raise RouteQueryException(response.text)
        return None

    def get_domain(self, folder='Common'):
        """ Get route domain """
        folder = str(folder).replace('/', '')
        if folder == 'Common':
            return 0
        if folder in self.domain_index:
            return self.domain_index[folder]
        else:
            request_url = self._uri + '/net/route-domain/'
            request_url += '~' + folder + '~' + folder
            request_url += '?$select=id'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'id' in response_obj:
                    self.domain_index[folder] = int(response_obj['id'])
                    return self.domain_index[folder]
            elif response.status_code != 404:
                raise RouteQueryException(response.text)
            return 0


def main():
    changed = False

    module = AnsibleModule(
        argument_spec=dict(
            description=dict(required=False, default=None),
            interface=dict(required=False, default=None),
            interfaces=dict(required=False, default=None),
            name=dict(required=True, default=None),
            password=dict(required=True),
            route_domain=dict(required=False, default=None),
            server=dict(required=True),
            state=dict(default='present', choices=['absent', 'present']),
            user=dict(required=True, aliases=['username']),
            validate_certs=dict(default='yes', type='bool'),
            vlan_id=dict(required=False, default=None, aliases=['tag']),
        ),
        mutually_exclusive=[
            ['interface', 'interfaces']
        ]
    )

    state = module.params.get('state')

    try:
        if not requests_found:
            raise Exception("The python requests module is required")

        if not bigsuds_found:
            raise Exception("The python bigsuds module is required")

        obj = BigIpRest(module)

        if state == "present":
            if obj.present():
                changed = True
        elif state == "absent":
            if obj.absent():
                changed = True
    except socket.timeout, e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except VLANUpdateException, e:
        response_obj = json.loads(str(e))
        module.fail_json(msg=response_obj['message'])
    except MemoryError, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
