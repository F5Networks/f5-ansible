#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bigip_data_group
short_description: Manage data groups on a BIG-IP
description:
  - Allows for managing data groups on a BIG-IP. Data groups provide a way to store collections
    of values on a BIG-IP for later use in things such as LTM rules, iRules, and ASM policies.
version_added: "1.0.0"
options:
  name:
    description:
      - Specifies the name of the data group.
    type: str
    required: True
  description:
    description:
      - The description of the data group.
    type: str
  type:
    description:
      - The type of records in this data group.
      - This parameter is important because it causes the BIG-IP to store your data
        in different ways to optimize access to it. For example, it would be wrong
        to specify a list of records containing IP addresses, but label them as a C(string)
        type.
      - This value cannot be changed once the data group is created.
    type: str
    choices:
      - address
      - addr
      - ip
      - string
      - integer
      - int
    default: string
  internal:
    description:
      - The type of this data group.
      - You should only consider setting this value in cases where you know exactly what
        you are doing, B(or), you are working with a pre-existing internal data group.
      - Be aware that if you deliberately force this parameter to C(yes), and you have a
        either a large number of records or a large total records size, this large amount
        of data will be reflected in your BIG-IP configuration. This can lead to B(long)
        system configuration load times due to parsing and verifying the large
        configuration.
      - There is a limit of either 4 megabytes or 65,000 records (whichever is more restrictive)
        for uploads when this parameter is C(yes).
      - This value cannot be changed once the data group is created.
    type: bool
    default: no
  external_file_name:
    description:
      - When creating a new data group, this specifies the file name you want to give an
        external data group file on the BIG-IP.
      - This parameter is ignored when C(internal) is C(yes).
      - This parameter can be used to select an existing data group file to use with an
        existing external data group.
      - If this value is not provided, it will be given the value specified in C(name) and,
        therefore, match the name of the data group.
      - This value may only contain letters, numbers, underscores, dashes, or a period.
    type: str
  records:
    description:
      - Specifies the records you want to add to a data group.
      - If you have a large number of records, we recommend you use C(records_src)
        instead of typing all those records here.
      - The technical limit of either the number of records, or the total size of all
        records. Varies with the size of the total resources on your system; in particular,
        RAM.
      - When C(internal) is C(no), at least one record must be specified in either C(records)
        or C(records_src).
      - "When C(type) is: C(ip), C(address), C(addr) if the addresses use a non-default route domain,
        they must be explicit about it, meaning they must contain a route domain notation C(%) e.g. 10.10.1.1%11.
        This is true regardless if the data group resides in a partition or not."
    type: list
    elements: raw
    suboptions:
      key:
        description:
          - The key describing the record in the data group.
          - The key will be used for validation of the C(type) parameter to this module.
        type: str
        required: True
      value:
        description:
          - The value of the key describing the record in the data group.
        type: raw
  records_src:
    description:
      - Path to a file with records in it.
      - The file should be well-formed. This means it includes records, one per line,
        that resemble the following format "key separator value". For example, C(foo := bar).
      - BIG-IP is strict about this format, but this module is a bit more lax. It will allow
        you to include arbitrary amounts (including none) of empty space on either side of
        the separator. For an illustration of this, see the Examples section.
      - Record keys are limited in length to no more than 65520 characters.
      - Values of record keys are limited in length to no more than 65520 characters.
      - The total number of records you can have in your BIG-IP is limited by the memory
        of the BIG-IP itself.
      - The format of this content is slightly different depending on whether you specify
        a C(type) of C(address), C(integer), or C(string). See the examples section for
        examples of the different types of payload formats that are expected in your data
        group file.
      - When C(internal) is C(no), at least one record must be specified in either C(records)
        or C(records_src).
    type: path
  separator:
    description:
      - When specifying C(records_src), this is the string of characters that will
        be used to break apart entries in the C(records_src) into key/value pairs.
      - By default, the value of this parameter is C(:=).
      - This value cannot be changed once it is set.
      - This parameter is only relevant when C(internal) is C(no). It will be ignored
        otherwise.
    type: str
    default: ":="
  delete_data_group_file:
    description:
      - When C(yes), ensures the remote data group file is deleted.
      - This parameter is only relevant when C(state) is C(absent) and C(internal) is C(no).
    type: bool
    default: no
  partition:
    description:
      - Device partition to manage resources on.
    type: str
    default: Common
  state:
    description:
      - When C(state) is C(present), ensures the data group exists.
      - When C(state) is C(absent), ensures the data group is removed.
      - The use of state in this module refers to the entire data group, not its members.
    type: str
    choices:
      - present
      - absent
    default: present
notes:
  - This module does NOT support atomic updates of data group members in a type C(internal) data group.
  - Addition/Deletion of data group members in a type C(external) data group should be done through Ansible modules only,
    if changes are made manually, the Ansible module will not detect those changes.
extends_documentation_fragment: f5networks.f5_modules.f5
author:
  - Tim Rupp (@caphrim007)
  - Wojciech Wypior (@wojtek0806)
  - Greg Crosby (@crosbygw)
'''

EXAMPLES = r'''
- name: Create a data group of addresses
  bigip_data_group:
    name: foo
    internal: yes
    records:
      - key: 0.0.0.0/32
        value: External_NAT
      - key: 10.10.10.10
        value: No_NAT
    type: address
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost

- name: Create a data group of strings
  bigip_data_group:
    name: foo
    internal: yes
    records:
      - key: caddy
        value: ""
      - key: cafeteria
        value: ""
      - key: cactus
        value: ""
    type: string
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost

- name: Create a data group of IP addresses from a file
  bigip_data_group:
    name: foo
    records_src: /path/to/dg-file
    type: address
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost

- name: Update an existing internal data group of strings
  bigip_data_group:
    name: foo
    internal: yes
    records:
      - key: caddy
        value: ""
      - key: cafeteria
        value: ""
      - key: cactus
        value: ""
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
  delegate_to: localhost

- name: Show the data format expected for records_content - address 1
  copy:
    dest: /path/to/addresses.txt
    content: |
      network 10.0.0.0 prefixlen 8 := "Network1",
      network 172.16.0.0 prefixlen 12 := "Network2",
      network 192.168.0.0 prefixlen 16 := "Network3",
      network 2402:9400:1000:0:: prefixlen 64 := "Network4",
      host 192.168.20.1 := "Host1",
      host 172.16.1.1 := "Host2",
      host 172.16.1.1 := "Host3",
      host 2001:0db8:85a3:0000:0000:8a2e:0370:7334 := "Host4",
      host 2001:0db8:85a3:0000:0000:8a2e:0370:7334 := "Host5"

- name: Show the data format expected for records_content - address 2
  copy:
    dest: /path/to/addresses.txt
    content: |
      10.0.0.0/8 := "Network1",
      172.16.0.0/12 := "Network2",
      192.168.0.0/16 := "Network3",
      2402:9400:1000:0::/64 := "Network4",
      192.168.20.1 := "Host1",
      172.16.1.1 := "Host2",
      172.16.1.1/32 := "Host3",
      2001:0db8:85a3:0000:0000:8a2e:0370:7334 := "Host4",
      2001:0db8:85a3:0000:0000:8a2e:0370:7334/128 := "Host5"

- name: Show the data format expected for records_content - string
  copy:
    dest: /path/to/strings.txt
    content: |
      a := alpha,
      b := bravo,
      c := charlie,
      x := x-ray,
      y := yankee,
      z := zulu,

- name: Show the data format expected for records_content - integer
  copy:
    dest: /path/to/integers.txt
    content: |
      1 := bar,
      2 := baz,
      3,
      4,
'''

RETURN = r'''
# only common fields returned
'''

import hashlib
import os
import re
from datetime import datetime

from ansible.module_utils.six import iteritems
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import (
    AnsibleModule, env_fallback
)

from ipaddress import (
    ip_network, ip_interface
)

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from ..module_utils.bigip import F5RestClient
from ..module_utils.common import (
    F5ModuleError, AnsibleF5Parameters, f5_argument_spec, transform_name
)
from ..module_utils.compare import (
    cmp_str_with_none
)
from ..module_utils.icontrol import (
    upload_file, tmos_version
)
from ..module_utils.ipaddress import is_valid_ip_interface
from ..module_utils.teem import send_teem

LINE_LIMIT = 65000
SIZE_LIMIT_BYTES = 4000000


def zero_length(content):
    content.seek(0, os.SEEK_END)
    length = content.tell()
    content.seek(0)
    if length == 0:
        return True
    return False


def size_exceeded(content):
    records = content
    records.seek(0, os.SEEK_END)
    size = records.tell()
    records.seek(0)
    if size > SIZE_LIMIT_BYTES:
        return True
    return False


def lines_exceeded(content):
    result = False
    for i, line in enumerate(content):
        if i > LINE_LIMIT:
            result = True
    content.seek(0)
    return result


class RecordsEncoder(object):
    def __init__(self, record_type=None, separator=None):
        self._record_type = record_type
        self._separator = separator
        self._network_pattern = re.compile(r'^network\s+(?P<addr>[^ ]+)\s+prefixlen\s+(?P<prefix>\d+)\s+.*')
        self._rd_net_prefix_ptrn = re.compile(
            r'^network\s+(?P<addr>[^%]+)%(?P<rd>[0-9]+)\s+prefixlen\s+(?P<prefix>\d+)\s+.*'
        )
        self._host_pattern = re.compile(r'^host\s+(?P<addr>[^%]+)\s+.*')
        self._rd_host_ptrn = re.compile(r'^host\s+(?P<addr>[^%]+)%(?P<rd>[0-9]+)\s+.*')
        self._ipv4_cidr_ptrn = re.compile(r'^(?P<addr>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|'
                                          r'2[0-4][0-9]|[01]?[0-9][0-9]?))/(?P<cidr>(3[0-2]|2[0-9]|1[0-9]|[0-9]))')
        self._ipv4_cidr_ptrn_rd = re.compile(r'^(?P<addr>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|'
                                             r'2[0-4][0-9]|[01]?[0-9][0-9]?))%(?P<rd>[0-9]+)/'
                                             r'(?P<cidr>(3[0-2]|2[0-9]|1[0-9]|[0-9]))')
        self._ipv6_cidr_ptrn = re.compile(r'^(?P<addr>^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:)'
                                          r'{1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}'
                                          r'(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|'
                                          r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}'
                                          r'(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:'
                                          r'((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}'
                                          r'|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.)'
                                          r'{3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:'
                                          r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}'
                                          r'[0-9]){0,1}[0-9])))/(?P<cidr>((1(1[0-9]|2[0-8]))|([0-9][0-9])|([0-9])))')
        self._ipv6_cidr_ptrn_rd = re.compile(r'^(?P<addr>^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|'
                                             r'([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
                                             r'([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|'
                                             r'([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|'
                                             r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|'
                                             r'([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|'
                                             r'[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|'
                                             r':)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}'
                                             r'|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|'
                                             r'1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|'
                                             r'([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.)'
                                             r'{3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))%(?P<rd>[0-9]+)'
                                             r'/(?P<cidr>((1(1[0-9]|2[0-8]))|([0-9][0-9])|([0-9])))')

    def encode(self, record):
        if isinstance(record, dict):
            return self.encode_dict(record)
        else:
            return self.encode_string(record)

    def encode_dict(self, record):
        if self._record_type == 'ip':
            return self.encode_address_from_dict(record)
        elif self._record_type == 'integer':
            return self.encode_integer_from_dict(record)
        else:
            return self.encode_string_from_dict(record)

    def encode_rd_address(self, record, match, ipv6=False):
        if is_valid_ip_interface(match.group('addr')):
            key = ip_interface(u"{0}/{1}".format(match.group('addr'), match.group('cidr')))
        else:
            raise F5ModuleError(
                "When specifying an 'address' type, the value to the left of the separator must be an IP."
            )
        if key and 'value' in record:
            if ipv6 and key.network.prefixlen == 128:
                return self.encode_host(str(key.ip) + '%' + match.group('rd'), record['value'])
            else:
                if not ipv6 and key.network.prefixlen == 32:
                    return self.encode_host(str(key.ip) + '%' + match.group('rd'), record['value'])
            return self.encode_network(
                str(key.network.network_address) + '%' + match.group('rd'), key.network.prefixlen, record['value']
            )
        elif key:
            if ipv6 and key.network.prefixlen == 128:
                return self.encode_host(
                    str(key.ip) + '%' + match.group('rd'), str(key.ip) + '%' + match.group('rd')
                )
            else:
                if not ipv6 and key.network.prefixlen == 32:
                    return self.encode_host(
                        str(key.ip) + '%' + match.group('rd'), str(key.ip) + '%' + match.group('rd')
                    )
            return self.encode_network(
                str(key.network.network_address) + '%' + match.group('rd'), key.network.prefixlen,
                str(key.network.network_address) + '%' + match.group('rd')
            )

    def encode_address_from_dict(self, record):
        rd_match = re.match(self._ipv4_cidr_ptrn_rd, record['key'])
        if rd_match:
            return self.encode_rd_address(record, rd_match)
        rd_match = re.match(self._ipv6_cidr_ptrn_rd, record['key'])
        if rd_match:
            return self.encode_rd_address(record, rd_match, ipv6=True)
        if is_valid_ip_interface(record['key']):
            key = ip_interface(u"{0}".format(str(record['key'])))
        else:
            raise F5ModuleError(
                "When specifying an 'address' type, the value to the left of the separator must be an IP."
            )
        ipv4_match = re.match(self._ipv4_cidr_ptrn, record['key'])
        ipv6_match = re.match(self._ipv6_cidr_ptrn, record['key'])

        if key and 'value' in record:
            if (ipv6_match and key.network.prefixlen == 128) or (ipv4_match and key.network.prefixlen == 32):
                return self.encode_host(str(key.ip), record['value'])
            else:
                return self.encode_network(
                    str(key.network.network_address), key.network.prefixlen, record['value']
                )
        elif key:
            if (ipv6_match and key.network.prefixlen == 128) or (ipv4_match and key.network.prefixlen == 32):
                return self.encode_host(str(key.ip), str(key.ip))
            else:
                return self.encode_network(
                    str(key.network.network_address), key.network.prefixlen, str(key.network.network_address)
                )

    def encode_integer_from_dict(self, record):
        try:
            int(record['key'])
        except ValueError:
            raise F5ModuleError(
                "When specifying an 'integer' type, the value to the left of the separator must be a number."
            )
        if 'key' in record and 'value' in record:
            return '{0} {1} {2}'.format(record['key'], self._separator, record['value'])
        elif 'key' in record:
            return str(record['key'])

    def encode_string_from_dict(self, record):
        if 'key' in record and 'value' in record:
            return '{0} {1} {2}'.format(record['key'], self._separator, record['value'])
        elif 'key' in record:
            return '{0} {1} ""'.format(record['key'], self._separator)

    def encode_string(self, record):
        record = record.strip().strip(',')
        if self._record_type == 'ip':
            return self.encode_address_from_string(record)
        elif self._record_type == 'integer':
            return self.encode_integer_from_string(record)
        else:
            return self.encode_string_from_string(record)

    def encode_address_from_string(self, record):
        if self._network_pattern.match(record):
            # network 192.168.0.0 prefixlen 16 := "Network3"
            # network 2402:9400:1000:0:: prefixlen 64 := "Network4"
            return record
        elif self._host_pattern.match(record):
            # host 172.16.1.1/32 := "Host3"
            # host 2001:0db8:85a3:0000:0000:8a2e:0370:7334 := "Host4"
            return record
        elif self._rd_net_prefix_ptrn.match(record) or self._rd_host_ptrn.match(record):
            # network 192.168.0.0%11/16 := "Network3"
            # network 2402:9400:1000:0::%11/64 := "Network4"
            # host 192.168.1.1%11/32 := "Host3"
            # host 2001:0db8:85a3:0000:0000:8a2e:0370:7334%11 := "Host4"
            return record
        elif self._ipv4_cidr_ptrn_rd.match(record) or self._ipv6_cidr_ptrn_rd.match(record):
            # 10.0.0.0%12/8
            # 2402:6940::%12/32 := "Network2"
            # 192.168.1.1%12/32 := "Host1"
            # 2402:9400:1000::%12/128
            parts = [r.strip() for r in record.split(self._separator)]
            if parts[0] == '':
                return
            pattern = re.compile(r'(?P<addr>[^%]+)%(?P<rd>[0-9]+)/(?P<prefix>[0-9]+)')
            match = pattern.match(parts[0])
            addr = u"{0}/{1}".format(match.group('addr'), match.group('prefix'))
            if not is_valid_ip_interface(addr):
                raise F5ModuleError(
                    "When specifying an 'address' type, the value to the left of the separator must be an IP."
                )
            key = ip_interface(addr)
            ipv4_match = re.match(self._ipv4_cidr_ptrn, addr)
            ipv6_match = re.match(self._ipv6_cidr_ptrn, addr)
            if len(parts) == 2:
                if (ipv4_match and key.network.prefixlen == 32) or (ipv6_match and key.network.prefixlen == 128):
                    return self.encode_host(str(key.ip) + '%' + str(match.group('rd')), parts[1])
                else:
                    return self.encode_network(
                        str(key.network.network_address) + '%' + str(match.group('rd')),
                        key.network.prefixlen, parts[1]
                    )
            elif len(parts) == 1 and parts[0] != '':
                if (ipv4_match and key.network.prefixlen == 32) or (ipv6_match and key.network.prefixlen == 128):
                    return self.encode_host(
                        str(key.ip) + '%' + str(match.group('rd')), str(key.ip) + '%' + str(match.group('rd'))
                    )
                return self.encode_network(
                    str(key.network.network_address) + '%' + str(match.group('rd')),
                    key.network.prefixlen, str(key.network.network_address) + '%' + str(match.group('rd'))
                )
        else:
            # 192.168.0.0/16 := "Network3"
            # 2402:9400:1000:0::/64 := "Network4"
            # 10.0.0.0/8
            # 2402:6940::/32 := "Network2"
            # 192.168.1.1/32 := "Host1"
            # 2402:9400:1000::/128
            parts = [r.strip() for r in record.split(self._separator)]
            if parts[0] == '':
                return
            if len(re.split(' ', parts[0])) == 1:
                if not is_valid_ip_interface(parts[0]):
                    raise F5ModuleError(
                        "When specifying an 'address' type, the value to the left of the separator must be an IP."
                    )
                key = ip_interface(u"{0}".format(str(parts[0])))
                ipv4_match = re.match(self._ipv4_cidr_ptrn, str(parts[0]))
                ipv6_match = re.match(self._ipv6_cidr_ptrn, str(parts[0]))

                if len(parts) == 2:
                    if (ipv4_match and key.network.prefixlen == 32) or (ipv6_match and key.network.prefixlen == 128):
                        return self.encode_host(str(key.ip), parts[1])
                    else:
                        return self.encode_network(str(key.network.network_address), key.network.prefixlen, parts[1])
                elif len(parts) == 1 and parts[0] != '':
                    if (ipv4_match and key.network.prefixlen == 32) or (ipv6_match and key.network.prefixlen == 128):
                        return self.encode_host(str(key.ip), str(key.ip))
                    return self.encode_network(
                        str(key.network.network_address), key.network.prefixlen, str(key.network.network_address)
                    )
            else:
                return str(parts[0])

    def encode_host(self, key, value):
        return 'host {0} {1} {2}'.format(str(key), self._separator, str(value))

    def encode_network(self, key, prefixlen, value):
        return 'network {0} prefixlen {1} {2} {3}'.format(
            str(key), str(prefixlen), self._separator, str(value)
        )

    def encode_integer_from_string(self, record):
        parts = record.split(self._separator)
        if len(parts) == 1 and parts[0] == '':
            return None
        try:
            int(parts[0])
        except ValueError:
            raise F5ModuleError(
                "When specifying an 'integer' type, the value to the left of the separator must be a number."
            )
        if len(parts) == 2:
            return '{0} {1} {2}'.format(parts[0], self._separator, parts[1])
        elif len(parts) == 1:
            return str(parts[0])

    def encode_string_from_string(self, record):
        parts = record.split(self._separator)
        if len(parts) == 2:
            return '{0} {1} {2}'.format(parts[0], self._separator, parts[1])
        elif len(parts) == 1 and parts[0] != '':
            return '{0} {1} ""'.format(parts[0], self._separator)


class RecordsDecoder(object):
    def __init__(self, record_type=None, separator=None):
        self._record_type = record_type
        self._separator = separator
        self._net_prefix_pattern = re.compile(r'^network\s+(?P<addr>[^ ]+)\s+prefixlen\s+(?P<prefix>\d+)\s+.*')
        self._rd_net_prefix_ptrn = re.compile(r'^network\s+(?P<addr>[^%]+)%(?P<rd>[0-9]+)'
                                              r'\s+prefixlen\s+(?P<prefix>\d+)\s+.*')
        self._host_pattern = re.compile(r'^host\s+(?P<addr>[^ ,]+)\s?.*')
        self._net_pattern = re.compile(r'^^network\s+(?P<addr>[^ ,]+)\s?.*')
        self._rd_host_ptrn = re.compile(r'^host\s+(?P<addr>[^%]+)%(?P<rd>[0-9]+)\s+.*')

    def decode(self, record):
        record = record.strip().strip(',')
        if self._record_type == 'ip':
            return self.decode_address_from_string(record)
        else:
            return self.decode_from_string(record)

    def decode_address_from_string(self, record):
        matches = self._rd_net_prefix_ptrn.match(record)
        if matches:
            # network 192.168.0.0%11 prefixlen 16 := "Network3",
            # network 2402:9400:1000:0::%11 prefixlen 64 := "Network4",
            value = record.split(self._separator)[1].strip().strip('"')
            addr = "{0}%{1}/{2}".format(matches.group('addr'), matches.group('rd'), matches.group('prefix'))
            result = dict(name=addr, data=value)
            return result
        matches = self._net_prefix_pattern.match(record)
        if matches:
            # network 192.168.0.0 prefixlen 16 := "Network3",
            # network 2402:9400:1000:0:: prefixlen 64 := "Network4",
            key = u"{0}/{1}".format(matches.group('addr'), matches.group('prefix'))
            addr = ip_network(key)
            value = record.split(self._separator)[1].strip().strip('"')
            result = dict(name=str(addr), data=value)
            return result
        matches = self._net_pattern.match(record)
        if matches:
            # network 192.168.2.0/24,
            # network 2402:9400:1000:0:: prefixlen 64 := "Network4",
            key = u"{0}".format(matches.group('addr'))
            addr = ip_network(key)
            if len(record.split(self._separator)) > 1:
                value = record.split(self._separator)[1].strip().strip('"')
                result = dict(name=str(addr), data=value)
                return result
            return str(record)
        matches = self._rd_host_ptrn.match(record)
        if matches:
            # host 172.16.1.1%11/32 := "Host3"
            # host 2001:0db8:85a3:0000:0000:8a2e:0370:7334%11 := "Host4"
            host = ip_interface(u"{0}".format(matches.group('addr')))
            addr = "{0}%{1}/{2}".format(matches.group('addr'), matches.group('rd'), str(host.network.prefixlen))
            value = record.split(self._separator)[1].strip().strip('"')
            result = dict(name=addr, data=value)
            return result
        matches = self._host_pattern.match(record)
        if matches:
            # host 172.16.1.1/32 := "Host3"
            # host 2001:0db8:85a3:0000:0000:8a2e:0370:7334 := "Host4"
            key = matches.group('addr')
            addr = ip_interface(u"{0}".format(str(key)))
            if len(record.split(self._separator)) > 1:
                value = record.split(self._separator)[1].strip().strip('"')
                result = dict(name=str(addr), data=value)
                return result
            return str(record)

        raise F5ModuleError(
            'The value "{0}" is not an address'.format(record)
        )

    def decode_from_string(self, record):
        parts = record.split(self._separator)
        if len(parts) == 2:
            return dict(name=parts[0].strip(), data=parts[1].strip().strip('"'))
        else:
            return dict(name=parts[0].strip(), data="")


class Parameters(AnsibleF5Parameters):
    api_map = {
        'externalFileName': 'external_file_name',
    }

    api_attributes = [
        'records',
        'type',
        'description',
    ]

    returnables = [
        'type',
        'records',
        'description',
    ]

    updatables = [
        'records',
        'checksum',
        'description',
    ]

    @property
    def type(self):
        if self._values['type'] in ['address', 'addr', 'ip']:
            return 'ip'
        elif self._values['type'] in ['integer', 'int']:
            return 'integer'
        elif self._values['type'] in ['string']:
            return 'string'

    @property
    def records_src(self):
        try:
            self._values['records_src'].seek(0)
            return self._values['records_src']
        except AttributeError:
            pass

        if self._values['records_src']:
            records = open(self._values['records_src'])
        else:
            records = self._values['records']

        if records is None:
            return None

        # There is a 98% chance that the user will supply a data group that is < 1MB.
        # 99.917% chance it is less than 10 MB. This is well within the range of typical
        # memory available on a system.
        #
        # If this changes, this may need to be changed to use temporary files instead.
        self._values['records_src'] = StringIO()

        self._write_records_to_file(records)
        return self._values['records_src']

    def _write_records_to_file(self, records):
        bucket_size = 1000000
        bucket = []
        encoder = RecordsEncoder(record_type=self.type, separator=self.separator)
        for record in records:
            result = encoder.encode(record)
            if result:
                bucket.append(to_text(result + ",\n"))
                if len(bucket) == bucket_size:
                    self._values['records_src'].writelines(bucket)
                    bucket = []
        self._values['records_src'].writelines(bucket)
        self._values['records_src'].seek(0)


class ApiParameters(Parameters):
    @property
    def checksum(self):
        if self._values['checksum'] is None:
            return None
        result = self._values['checksum'].split(':')[2]
        return result

    @property
    def records(self):
        cleaned_records_list = []
        if self._values['records'] is None:
            return None
        for record in self._values['records']:
            clean_record = {}
            for k, v in record.items():
                clean_record[k] = re.sub('\\\\', '', v)
            cleaned_records_list.append(clean_record)
        return cleaned_records_list

    @property
    def records_list(self):
        return self._values['records']

    @property
    def description(self):
        if self._values['description'] in [None, 'none']:
            return None
        return self._values['description']


class ModuleParameters(Parameters):
    @property
    def description(self):
        if self._values['description'] is None:
            return None
        elif self._values['description'] in ['none', '']:
            return ''
        return self._values['description']

    @property
    def checksum(self):
        if self._values['checksum']:
            return self._values['checksum']
        if self.records_src is None:
            return None
        result = hashlib.sha1()
        records = self.records_src
        while True:
            data = records.read(4096)
            if not data:
                break
            result.update(data.encode('utf-8'))
        result = result.hexdigest()
        self._values['checksum'] = result
        return result

    @property
    def external_file_name(self):
        if self._values['external_file_name'] is None:
            name = self.name
        else:
            name = self._values['external_file_name']
        if re.search(r'[^a-zA-Z0-9-_.]', name):
            raise F5ModuleError(
                "'external_file_name' may only contain letters, numbers, underscores, dashes, or a period."
            )
        return name

    @property
    def records(self):
        results = []
        if self.records_src is None:
            return None
        decoder = RecordsDecoder(record_type=self.type, separator=self.separator)
        for record in self.records_src:
            result = decoder.decode(record)
            if result:
                results.append(result)
        return results

    @property
    def records_list(self):
        if self._values['records'] is None:
            return None
        return self.records


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class UsableChanges(Changes):
    pass


class ReportableChanges(Changes):
    pass


class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            return self.__default(param)

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1

    def _compare_records(self):
        want = self.want.records
        have = self.have.records
        if want == [] and have is None:
            return None
        if want is None:
            return None
        w = []
        h = []

        for x in want:
            tmp = tuple((str(k), str(v)) for k, v in iteritems(x))
            w.append(tmp)
        for x in have:
            tmp = tuple((str(k), str(v)) for k, v in iteritems(x))
            h.append(tmp)

        if set(w) == set(h):
            return None
        else:
            return want

    @property
    def records(self):
        # External data groups are compared by their checksum, not their records. This
        # is because the BIG-IP does not store the actual records in the API. It instead
        # stores the checksum of the file. External DGs have the possibility of being huge
        # and we would never want to do a comparison of such huge files.
        #
        # Therefore, comparison is no-op if the DG being worked with is an external DG.
        if self.want.internal is False:
            return None
        if self.have.records is None and self.want.records == []:
            return None
        if self.have.records is None:
            return self.want.records
        result = self._compare_records()
        return result

    @property
    def type(self):
        return None

    @property
    def checksum(self):
        if self.want.internal:
            return None
        if self.want.checksum is None:
            return None
        if self.want.checksum != self.have.checksum:
            return True

    @property
    def description(self):
        return cmp_str_with_none(self.want.description, self.have.description)


class BaseManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.want = ModuleParameters(params=self.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def exec_module(self):
        start = datetime.now().isoformat()
        version = tmos_version(self.client)
        changed = False
        result = dict()
        state = self.want.state

        if state == "present":
            changed = self.present()
        elif state == "absent":
            changed = self.absent()

        reportable = ReportableChanges(params=self.changes.to_return())
        changes = reportable.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        send_teem(start, self.client, self.module, version)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def _set_changed_options(self):
        changed = {}
        for key in ApiParameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = UsableChanges(params=changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = ApiParameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = UsableChanges(params=changed)
            return True
        return False

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        return True


class InternalManager(BaseManager):
    def create(self):
        self._set_changed_options()
        if size_exceeded(self.want.records_src) or lines_exceeded(self.want.records_src):
            raise F5ModuleError(
                "The size of the provided data (or file) is too large for an internal data group."
            )
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def exists(self):
        errors = [401, 403, 409, 500, 501, 502, 503, 504]
        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/internal/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status == 404 or 'code' in response and response['code'] == 404:
            return False
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True

        if resp.status in errors or 'code' in response and response['code'] in errors:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def create_on_device(self):
        params = self.changes.api_params()
        params['name'] = self.want.name
        params['partition'] = self.want.partition
        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/internal/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(resp.content)

    def update_on_device(self):
        params = self.changes.api_params()
        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/internal/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(resp.content)

    def remove_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/internal/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        response = self.client.api.delete(uri)

        if response.status in [200, 201]:
            return True
        raise F5ModuleError(response.content)

    def read_current_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/internal/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return ApiParameters(params=response)
        raise F5ModuleError(resp.content)


class ExternalManager(BaseManager):
    def absent(self):
        result = False
        if self.exists():
            result = self.remove()
        if self.external_file_exists() and self.want.delete_data_group_file:
            result = self.remove_data_group_file_from_device()
        return result

    def create(self):
        if zero_length(self.want.records_src):
            raise F5ModuleError(
                "An external data group cannot be empty."
            )
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.changes.records_src and zero_length(self.want.records_src):
            raise F5ModuleError(
                "An external data group cannot be empty."
            )
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def exists(self):
        errors = [401, 403, 409, 500, 501, 502, 503, 504]
        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/external/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status == 404 or 'code' in response and response['code'] == 404:
            return False
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True

        if resp.status in errors or 'code' in response and response['code'] in errors:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def external_file_exists(self):
        errors = [401, 403, 409, 500, 501, 502, 503, 504]
        uri = "https://{0}:{1}/mgmt/tm/sys/file/data-group/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.external_file_name)
        )
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status == 404 or 'code' in response and response['code'] == 404:
            return False
        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True

        if resp.status in errors or 'code' in response and response['code'] in errors:
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def upload_file_to_device(self, content, name):
        url = 'https://{0}:{1}/mgmt/shared/file-transfer/uploads'.format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        try:
            upload_file(self.client, url, content, name)
        except F5ModuleError:
            raise F5ModuleError(
                "Failed to upload the file."
            )

    def _upload_to_file(self, name, type, remote_path, update=False):
        self.upload_file_to_device(self.want.records_src, name)
        if update:
            uri = "https://{0}:{1}/mgmt/tm/sys/file/data-group/{2}".format(
                self.client.provider['server'],
                self.client.provider['server_port'],
                transform_name(self.want.partition, name)
            )
            params = {'sourcePath': 'file:{0}'.format(remote_path)}
            resp = self.client.api.patch(uri, json=params)

            try:
                response = resp.json()
            except ValueError as ex:
                raise F5ModuleError(str(ex))

        else:
            uri = "https://{0}:{1}/mgmt/tm/sys/file/data-group/".format(
                self.client.provider['server'],
                self.client.provider['server_port'],
            )
            params = dict(
                name=name,
                type=type,
                sourcePath='file:{0}'.format(remote_path),
                partition=self.want.partition
            )
            resp = self.client.api.post(uri, json=params)

            try:
                response = resp.json()
            except ValueError as ex:
                raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return response['name']
        raise F5ModuleError(resp.content)

    def remove_file_on_device(self, remote_path):
        uri = "https://{0}:{1}/mgmt/tm/util/unix-rm/".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
        )
        args = dict(
            command='run',
            utilCmdArgs=remote_path
        )
        resp = self.client.api.post(uri, json=args)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(response.content)

    def create_on_device(self):
        name = self.want.external_file_name
        remote_path = '/var/config/rest/downloads/{0}'.format(name)
        external_file = self._upload_to_file(name, self.want.type, remote_path, update=False)

        params = dict(
            name=self.want.name,
            partition=self.want.partition,
            externalFileName=external_file,
        )
        if self.want.description:
            params['description'] = self.want.description

        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/external/".format(
            self.client.provider['server'],
            self.client.provider['server_port']
        )
        resp = self.client.api.post(uri, json=params)

        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status not in [200, 201] or 'code' in response and response['code'] not in [200, 201]:
            raise F5ModuleError(response.content)

        self.remove_file_on_device(remote_path)

    def update_on_device(self):
        params = {}

        if self.want.records_src is not None:
            name = self.want.external_file_name
            remote_path = '/var/config/rest/downloads/{0}'.format(name)
            external_file = self._upload_to_file(name, self.have.type, remote_path, update=True)
            params['externalFileName'] = external_file
        if self.changes.description is not None:
            params['description'] = self.changes.description

        if not params:
            return

        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/external/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )

        resp = self.client.api.patch(uri, json=params)

        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            return True
        raise F5ModuleError(resp.content)

    def remove_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/external/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        response = self.client.api.delete(uri)

        # Remove the remote data group file if asked to
        if self.want.delete_data_group_file:
            self.remove_data_group_file_from_device()

        if response.status in [200, 201]:
            return True
        raise F5ModuleError(response.content)

    def remove_data_group_file_from_device(self):
        uri = "https://{0}:{1}/mgmt/tm/sys/file/data-group/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.external_file_name)
        )
        response = self.client.api.delete(uri)

        if response.status in [200, 201]:
            return True
        raise F5ModuleError(response.content)

    def read_current_from_device(self):
        """Reads the current configuration from the device

        For an external data group, we are interested in two things from the
        current configuration

        * ``checksum``
        * ``type``

        The ``checksum`` will allow us to compare the data group value we have
        with the data group value being provided.

        The ``type`` will allow us to do validation on the data group value being
        provided (if any).

        Returns:
             ExternalApiParameters: Attributes of the remote resource.
        """

        uri = "https://{0}:{1}/mgmt/tm/ltm/data-group/external/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(self.want.partition, self.want.name)
        )
        resp_dg = self.client.api.get(uri)

        try:
            response_dg = resp_dg.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp_dg.status not in [200, 201] or 'code' in response_dg and response_dg['code'] not in [200, 201]:
            raise F5ModuleError(resp_dg.content)

        external_file = os.path.basename(response_dg['externalFileName'])
        external_file_partition = os.path.dirname(response_dg['externalFileName']).strip('/')

        uri = "https://{0}:{1}/mgmt/tm/sys/file/data-group/{2}".format(
            self.client.provider['server'],
            self.client.provider['server_port'],
            transform_name(external_file_partition, external_file)
        )
        resp = self.client.api.get(uri)

        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))

        if resp.status in [200, 201] or 'code' in response and response['code'] in [200, 201]:
            result = ApiParameters(params=response)
            result.update({'description': response_dg.get('description', None)})
            return result
        raise F5ModuleError(resp.content)


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.module = kwargs.get('module')

    def exec_module(self):
        if self.module.params['internal']:
            manager = self.get_manager('internal')
        else:
            manager = self.get_manager('external')
        return manager.exec_module()

    def get_manager(self, type):
        if type == 'internal':
            return InternalManager(**self.kwargs)
        elif type == 'external':
            return ExternalManager(**self.kwargs)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            name=dict(required=True),
            type=dict(
                choices=['address', 'addr', 'ip', 'string', 'integer', 'int'],
                default='string'
            ),
            delete_data_group_file=dict(
                type='bool',
                default='no'
            ),
            internal=dict(type='bool', default='no'),
            records=dict(
                type='list',
                elements='raw',
                options=dict(
                    key=dict(required=True),
                    value=dict(type='raw')
                )
            ),
            records_src=dict(type='path'),
            external_file_name=dict(),
            separator=dict(default=':='),
            description=dict(),
            state=dict(choices=['absent', 'present'], default='present'),
            partition=dict(
                default='Common',
                fallback=(env_fallback, ['F5_PARTITION'])
            )
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)
        self.mutually_exclusive = [
            ['records', 'records_src']
        ]


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        mutually_exclusive=spec.mutually_exclusive
    )

    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
