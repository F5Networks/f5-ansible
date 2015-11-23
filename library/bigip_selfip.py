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
module: bigip_selfip
short_description: Manage Self-IPs on a BIG-IP system
description:
   - Manage Self-IPs on a BIG-IP system
version_added: "2.0"
options:
  address:
    description:
      - The IP addresses for the new self IP
    required: true
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: rest
    choices: [ "rest", "icontrol" ]
  floating_state:
    description:
      - The floating attributes of the self IPs.
    default: disabled
    required: false
    choices:
      - enabled
      - disabled
  name:
    description:
      - The self IP to create
    required: false
    default: Value of C(address)
  netmask:
    description:
      - The netmasks for the self IP
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  server:
    description:
      - BIG-IP host
    required: true
  state:
    description:
      - The state of the variable on the system. When C(present), guarantees
        that the Self-IP exists with the provided attributes. When C(absent),
        removes the floating IP from the system.
    required: false
    default: present
    choices:
      - absent
      - present
  traffic_group:
    description:
      - The traffic group for the self IP addresses in an active-active,
        redundant load balancer configuration
    required: false
  user:
    description:
      - BIG-IP username
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
  vlan:
    description:
      - The VLAN that the new self IPs will be on
    required: true

notes:
   - Requires the bigsuds Python package on the host if using the iControl
     interface. This is as easy as pip install bigsuds
   - Requires the netaddr Python package on the host

requirements: [ "bigsuds", "netaddr", "requests" ]
author: Tim Rupp <caphrim007@gmail.com> (@caphrim007)
'''

EXAMPLES = """
"""

import json
import socket
import netaddr
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

SHARED_CONFIG_DEFAULT_TRAFFIC_GROUP = 'traffic-group-local-only'
CONNECTION_TIMEOUT = 30
OBJ_PREFIX = 'uuid_'

def strip_domain_address(ip_address):
    """ Strip domain from ip address """
    mask_index = ip_address.find('/')
    if mask_index > 0:
        return ip_address[:mask_index].split('%')[0] + ip_address[mask_index:]
    else:
        return ip_address.split('%')[0]


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


class SelfIPCreationException(Exception):
    """SelfIPCreationException"""
    pass


class SelfIPDeleteException(Exception):
    """SelfIPDeleteException"""
    pass


class SelfIPQueryException(Exception):
    """SelfIPQueryException"""
    pass


class SelfIPUpdateException(Exception):
    """SelfIPUpdateException"""
    pass


class RouteUpdateException(Exception):
    """RouteUpdateException"""
    pass


class RouteQueryException(Exception):
    """RouteQueryException"""
    pass


class BigIpCommon(object):
    def __init__(self, module):
        self._username = module.params.get('user')
        self._password = module.params.get('password')
        self._hostname = module.params.get('server')

        self._self_ip = module.params.get('name')
        self._address = module.params.get('address')
        self._floating_state = module.params.get('floating_state')
        self._vlan = module.params.get('vlan')
        self._netmask = module.params.get('netmask')
        self._traffic_group = module.params.get('traffic_group')

        self._validate_certs = module.params.get('validate_certs')

        if self._floating_state == 'enabled':
            self._floating_state = 'STATE_ENABLED'
        else:
            self._floating_state = 'STATE_DISABLED'

        if not self._self_ip:
            self._self_ip = self._address

        self._formatted_name = "/Common/%s" % (self._self_ip.replace('/','_'))

        # Check if we can connect to the device
        sock = socket.create_connection((self._hostname,443), 60)
        sock.close()

class BigIpIControl(BigIpCommon):
    def __init__(self, module):
        super(BigIpIControl, self).__init__(module)

        self.api = bigsuds.BIGIP(
            hostname=self._hostname,
            username=self._username,
            password=self._password,
            debug=True
        )

    def read(self):
        try:
            response = self.api.Networking.SelfIPV2.get_list()
        except bigsuds.ServerError:
            return {}

        return response

    @property
    def self_ip(self):
        return self._self_ip

    @property
    def address(self):
        try:
            return self.api.Networking.SelfIPV2.get_address([self._self_ip])
        except:
            return None

    @property
    def floating_state(self):
        return self.api.Networking.SelfIPV2.get_floating_state([self._self_ip])

    @floating_state.setter
    def floating_state(self, val):
        self.api.Networking.SelfIPV2.set_floating_state(
            self_ips=[self._self_ip],
            states=[val]
        )

    @property
    def netmask(self):
        return self.api.Networking.SelfIPV2.get_netmask([self._self_ip])

    @netmask.setter
    def netmask(self, val):
        self.api.Networking.SelfIPV2.set_netmask(
            self_ips=[self._self_ip],
            netmasks=[val]
        )

    @property
    def traffic_group(self):
        return self.api.Networking.SelfIPV2.get_traffic_group([self._self_ip])

    @traffic_group.setter
    def traffic_group(self, val):
        self.api.Networking.SelfIPV2.set_traffic_group(
            self_ips=[self._self_ip],
            traffic_groups=[val]
        )

    @property
    def vlan(self):
        return self.api.Networking.SelfIPV2.get_vlan([self._self_ip])

    @vlan.setter
    def vlan(self, val):
        self.api.Networking.SelfIPV2.set_vlan(
            self_ips=[self._self_ip],
            vlan_names=[val]
        )

    def _create(self):
        self.api.Networking.SelfIPV2.create(
            self_ips=[self._self_ip],
            vlan_names=[self._vlan],
            addresses=[self._address],
            netmasks=[self._netmask],
            traffic_groups=[self._traffic_group],
            floating_states=[self._floating_state]
        )

    def absent(self):
        current = self.read()

        if self._formatted_name not in current:
            return False

        self.api.Networking.SelfIPV2.delete_self_ip(
            self_ips=[self._self_ip]
        )
        return True

    def present(self):
        changed = False
        current = self.read()

        if self._formatted_name in current:
            return False

        if self._address:
            if not self.address:
                self._create()
            elif self.address != self._address:
                # There is no set address, so we need to delete the address
                # and then create a new one
                self._delete()
                self._create()

                # Creating the new address means we can skip the remaining
                # steps because they would be redundant
                return True

        if self._vlan:
            if self.vlan != self._vlan:
                self.vlan = self._vlan
                changed = True

        if self._floating_state:
            if self.floating_state != self._floating_state:
                self.floating_state = self._floating_state
                changed = True

        if self._netmask:
            if self.netmask != self._netmask:
                self.netmask = self._netmask
                changed = True

        if self._traffic_group:
            if self.traffic_group != self._traffic_group:
                self.traffic_group = self._traffic_group
                changed = True

        return changed


class BigIpRest(BigIpCommon):
    def __init__(self, module):
        super(BigIpRest, self).__init__(module)

        self._uri = 'https://%s/mgmt/tm' % self._hostname

        self.api = self._get_icr_session(
            self._hostname, self._username, self._password,
            validate_certs=self._validate_certs
        )

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
        if self._vlan:
            ips = self.get_selfips(vlan=self._vlan)
            if self._self_ip in ips:
                self.delete_by_vlan_name(vlan_name=self._vlan)
                changed = True
            else:
                changed = False
        else:
            ips = self.get_selfip_list()
            if self._self_ip in ips:
                self.delete(name=self._self_ip)
                changed = True
            else:
                changed = False
        return changed

    def present(self):
        changed = False

        if self._address:
            if not self.get_addr(self._self_ip):
                self.create(self._self_ip, self._address, self._netmask,
                    self._vlan, self._floating_state, self._traffic_group
                )
            elif self.address != self._address:
                # There is no set address, so we need to delete the address
                # and then create a new one
                self._delete(self._self_ip)
                self.create(self._self_ip, self._address, self._netmask,
                    self._vlan, self._floating_state, self._traffic_group
                )

                # Creating the new address means we can skip the remaining
                # steps because they would be redundant
                return True

        if self._vlan:
            if self.get_vlan(self._self_ip) != self._vlan:
                self.set_vlan(self._self_ip, self._vlan)
                changed = True

        if self._netmask:
            if self.get_mask(self._self_ip) != self._netmask:
                self.set_mask(self._self_ip, self._netmask)
                changed = True

        if self._traffic_group:
            if self.get_traffic_group(self._self_ip) != self._traffic_group:
                self.set_traffic_group(self._self_ip, self._traffic_group)
                changed = True

        return changed

    def create(self, name=None, ip_address=None, netmask=None,
               vlan_name=None, floating=False, traffic_group=None,
               folder='Common'):
        """ Create selfip """
        if name:
            folder = str(folder).replace('/', '')
            if not traffic_group:
                if floating:
                    traffic_group = \
                        SHARED_CONFIG_DEFAULT_FLOATING_TRAFFIC_GROUP
                else:
                    traffic_group = SHARED_CONFIG_DEFAULT_TRAFFIC_GROUP
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if not netmask:
                netmask = '32'
                payload['address'] = ip_address + '/' + str(netmask)
            else:
                if ':' in str(netmask):
                    net = netaddr.IPNetwork('::/' + str(netmask))
                else:
                    net = netaddr.IPNetwork('1.1.1.1/' + str(netmask))
                payload['address'] = ip_address + '/' + str(net.prefixlen)
            if floating:
                payload['floating'] = 'enabled'
            else:
                payload['floating'] = 'disabled'
            payload['trafficGroup'] = traffic_group
            if not vlan_name.startswith('/Common'):
                payload['vlan'] = '/' + folder + '/' + vlan_name
            else:
                payload['vlan'] = vlan_name

            request_url = self._uri + '/net/self/'
            response = self.api.post(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)

            if response.status_code < 400:
                return True
            elif response.status_code == 409:
                return True
            elif response.status_code == 400 and \
                response.text.find("must be one of the vlans "
                                   "in the associated route domain") > 0:
                self.add_vlan_to_domain(name=vlan_name, folder=folder)

                # bridge creation was halted before it was added to route
                # domain. Attempting to add to route domain and retrying
                # SelfIP creation.
                response = self.api.post(
                    request_url, data=json.dumps(payload),
                    timeout=CONNECTION_TIMEOUT)
                if response.status_code < 400:
                    return True
                elif response.status_code == 409:
                    return True
                else:
                    raise SelfIPCreationException(response.text)
            else:
                raise SelfIPCreationException(response.text)
        return False

    def add_vlan_to_domain(self, name=None, folder='Common'):
        """ Add VLANs to Domain """
        folder = str(folder).replace('/', '')
        existing_vlans = self.get_vlans_in_domain(folder=folder)
        if not name in existing_vlans:
            existing_vlans.append(name)
            vlans = dict()
            vlans['vlans'] = existing_vlans
            request_url = self._uri + '/net/route-domain/'
            request_url += '~' + folder + '~' + folder
            response = self.api.put(
                request_url, data=json.dumps(vlans),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise RouteUpdateException(response.text)
        return False

    def get_vlans_in_domain(self, folder='Common'):
        """ Get VLANs in Domain """
        folder = str(folder).replace('/', '')
        request_url = self._uri + \
            '/net/route-domain?$select=name,partition,vlans'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.api.get(request_url, timeout=CONNECTION_TIMEOUT)

        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                vlans = []
                folder = str(folder).replace('/', '')
                for route_domain in response_obj['items']:
                    if route_domain['name'] == folder:
                        if 'vlans' in route_domain:
                            for vlan in route_domain['vlans']:
                                vlans.append(vlan)
                return vlans
            return []
        else:
            if response.status_code != 404:
                raise RouteQueryException(response.text)
        return []

    def delete(self, name=None, folder='Common'):
        """ Delete selfip """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            response = self.api.delete(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                raise SelfIPDeleteException(response.text)
            else:
                return True
        return False

    def delete_by_vlan_name(self, vlan_name=None, folder='Common'):
        """ Delete selfip by vlan name """
        if vlan_name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self'
            request_url += '?$select=vlan,selfLink,floating'
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
                    float_to_delete = []
                    nonfloat_to_delete = []
                    for selfip in return_obj['items']:
                        name = os.path.basename(selfip['vlan'])
                        if vlan_name == name or \
                           vlan_name == strip_folder_and_prefix(name):
                            if selfip['floating'] == 'enabled':
                                float_to_delete.append(
                                    self.icr_link(selfip['selfLink']))
                            else:
                                nonfloat_to_delete.append(
                                    self.icr_link(selfip['selfLink']))
                    for selfip in float_to_delete:
                        del_res = self.api.delete(
                            selfip, timeout=CONNECTION_TIMEOUT)
                        if del_res.status_code > 399 and\
                           del_res.status_code != 404:
                            raise SelfIPDeleteException(del_res.text)
                    for selfip in nonfloat_to_delete:
                        del_res = self.api.delete(
                            selfip, timeout=CONNECTION_TIMEOUT)
                        if del_res.status_code > 399 and\
                           del_res.status_code != 404:
                            raise SelfIPDeleteException(del_res.text)
                return True
            else:
                raise SelfIPQueryException(response.text)
        return False

    def get_selfips(self, folder='Common', vlan=None):
        """ Get selfips """
        folder = str(folder).replace('/', '')
        request_url = self._uri + '/net/self/'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '?$filter=' + request_filter
        response = self.api.get(
            request_url, timeout=CONNECTION_TIMEOUT)
        return_list = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for selfip in return_obj['items']:
                    if vlan and selfip['vlan'] != vlan:
                        continue
                    selfip['name'] = strip_folder_and_prefix(selfip['name'])
                    return_list.append(selfip)
        elif response.status_code != 404:
            raise SelfIPQueryException(response.text)
        return return_list

    def get_selfip_list(self, folder='Common'):
        """ Get selfips """
        folder = str(folder).replace('/', '')
        request_url = self._uri + '/net/self/'
        request_url += '?$select=name'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.api.get(
            request_url, timeout=CONNECTION_TIMEOUT)
        return_list = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for selfip in return_obj['items']:
                    return_list.append(strip_folder_and_prefix(selfip['name']))
        elif response.status_code != 404:
            raise SelfIPQueryException(response.text)
        return return_list

    def get_addr(self, name=None, folder='Common'):
        """ Get selfip addr """
        folder = str(folder).replace('/', '')
        if name:
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=address'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return self._strip_mask(return_obj['address'])
            elif response.status_code != 404:
                raise SelfIPQueryException(response.text)
        return None

    def get_mask(self, name=None, folder='Common'):
        """ Get selfip netmask """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=address'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                try:
                    net = netaddr.IPNetwork(
                        strip_domain_address(return_obj['address']))
                    return str(net.netmask)
                except Exception:
                    pass
            elif response.status_code != 404:
                raise SelfIPQueryException(response.text)
        return None

    def set_mask(self, name=None, netmask=None, folder='Common'):
        """ Set selfip netmask """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=address'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                try:
                    address = self._strip_mask(return_obj['address'])
                    net = netaddr.IPNetwork(
                        strip_domain_address(address) + '/' + netmask)
                    payload = dict()
                    payload['address'] = address + '/' + str(net.prefixlen)
                    request_url = self._uri + '/net/self/'
                    request_url += '~' + folder + '~' + name
                    response = self.api.put(
                        request_url, data=json.dumps(payload),
                        timeout=CONNECTION_TIMEOUT)
                    if response.status_code < 400:
                        return True
                    else:
                        raise SelfIPUpdateException(response.text)
                except Exception:
                    pass
            else:
                raise SelfIPQueryException(response.text)
        return False

    def get_vlan(self, name=None, folder='Common'):
        """ Get selfip vlan """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=vlan'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'vlan' in return_obj:
                    return strip_folder_and_prefix(return_obj['vlan'])
            else:
                raise SelfIPQueryException(response.text)
        return None

    def set_vlan(self, name=None, vlan_name=None, folder='Common'):
        """ Set selfip vlan """
        if name and vlan_name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['vlan'] = vlan_name
            response = self.api.put(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise SelfIPUpdateException(response.text)
        return False

    def set_description(self, name=None, description=None, folder='Common'):
        """ Set selfip description """
        if name and description:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['description'] = description
            response = self.api.put(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise SelfIPUpdateException(response.text)
        return False

    def get_description(self, name=None, folder='Common'):
        """ Get selfip description """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=description'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return return_obj['description']
            else:
                raise SelfIPQueryException(response.text)
        return None

    def set_traffic_group(self, name=None, traffic_group=None,
                          folder='Common'):
        """ Set selfip traffic group """
        if name and traffic_group:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['trafficGroup'] = traffic_group
            response = self.api.put(
                request_url, data=json.dumps(payload),
                timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                raise SelfIPUpdateException(response.text)
        return False

    def get_traffic_group(self, name=None, folder='Common'):
        """ Get selfip traffic group """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=trafficGroup'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return return_obj['trafficGroup']
            else:
                raise SelfIPQueryException(response.text)
        return None

    def exists(self, name=None, folder='Common'):
        """ Does selfip exist? """
        folder = str(folder).replace('/', '')
        request_url = self._uri + '/net/self/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.api.get(
            request_url, timeout=CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            request_url = self._uri + '/net/self/'
            request_url += '~' + folder + '~' + strip_folder_and_prefix(name)
            request_url += '?$select=name'
            response = self.api.get(
                request_url, timeout=CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                raise SelfIPQueryException(response.text)
        else:
            raise SelfIPQueryException(response.text)
        return False

    def _strip_mask(self, ip_address):
        """ strip mask """
        mask_index = ip_address.find('/')
        if mask_index > 0:
            ip_address = ip_address[:mask_index]
        return ip_address


def main():
    changed = False
    icontrol = False

    module = AnsibleModule(
        argument_spec = dict(
            address=dict(required=True, default=None),
            connection=dict(default='rest', choices=['icontrol', 'rest']),
            floating_state=dict(required=False, default='disabled'),
            name=dict(required=False, default=None),
            netmask=dict(required=True),
            password=dict(required=True),
            server=dict(required=True),
            state=dict(default='present', choices=['absent', 'present']),
            traffic_group=dict(required=True),
            user=dict(required=True),
            validate_certs=dict(default='yes', type='bool'),
            vlan=dict(required=True)
        )
    )

    connection = module.params.get('connection')
    hostname = module.params.get('server')
    password = module.params.get('password')
    username = module.params.get('user')
    state = module.params.get('state')
    vlan = module.params.get('vlan')

    try:
        if connection == 'icontrol':
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            icontrol = test_icontrol(username, password, hostname)
            if icontrol:
                obj = BigIpIControl(module)
        elif connection == 'rest':
            if not requests_found:
                raise Exception("The python requests module is required")

            obj = BigIpRest(module)

        if state == "present":
            if obj.present():
                changed = True
        elif state == "absent":
            if obj.absent():
                changed = True
    except bigsuds.ConnectionError, e:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % hostname)
    except bigsuds.ServerError, e:
        error = str(e)

        if '17236104' in error:
            mesg = "The requested object name (%s) is invalid" % name
            module.fail_json(msg=mesg)
        elif '17236599' in error:
            mesg = "The requested vlan, vlangroup or tunnel (%s) was not found" % vlan
            module.fail_json(msg=mesg)
        elif '17236821' in error:
            mesg = "Self IP %s is declared as a floating address but there is no non-floating address defined for this network" % obj.self_ip
            module.fail_json(msg=mesg)
        else:
            module.fail_json(msg="An unknown error occurred")
    except socket.timeout, e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except Exception, e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
