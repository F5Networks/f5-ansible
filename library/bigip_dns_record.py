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
module: bigip_dns_record
short_description: Manage DNS resource records on a BIG-IP
description:
  - Manage DNS resource records on a BIG-IP
version_added: "2.2"
options:
  user:
    description:
      - BIG-IP username
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  server:
    description:
      - BIG-IP host
    required: true
    default: localhost
  state:
    description:
      - Whether the record should exist.  When C(absent), removes
        the record.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the bigsuds Python package on the remote host. This is as easy as
    pip install bigsuds
requirements:
  - bigsuds
  - distutils
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add an A record to organization.com zone
  bigip_dns_record:
      user="admin"
      password="secret"
      hostname="lb.mydomain.com"
      type="A"
      zone="organization.com"
      state="present"
      options:
          hostname: "elliot.organization.com"
          ip_address: "10.1.1.1"
  delegate_to: localhost

- name: Add an A record to organization.com zone
  local_action:
      module: bigip_dns_record
      user: "admin"
      password: "admin"
      hostname: "lb.mydomain.com"
      type: "A"
      zone: "organization.com"
      state: "present"
      ttl: "10"
      options:
          domain_name: "elliot.organization.com"
          ip_address: "10.1.1.1"
'''

from distutils.version import StrictVersion
import re


VERSION_PATTERN = 'BIG-IP_v(?P<version>\d+\.\d+\.\d+)'
RECORDS = [
    'A', 'AAAA', 'CNAME', 'DNAME', 'DS',
    'HINFO', 'MX', 'NAPTR', 'NS', 'PTR',
    'SOA', 'SRV', 'TXT'
]


class BigIpCommon(object):
    def __init__(self, *args, **kwargs):
        self.result = dict(changed=False, changes=dict())
        self.params = kwargs

    def flush(self):
        result = dict()
        state = self.params['state']

        if state == "present":
            changed = self.present()

            if not self.params['check_mode']:
                current = self.read()
                result.update(current)
        else:
            changed = self.absent()

        result.update(dict(changed=changed))
        return result


def get_resource_record(module):
    rtype = module.params['type']

    if rtype == 'A':
        return AResourceRecord(module)
    elif rtype == 'CNAME':
        return AResourceRecord(module)


class ResourceRecordException(Exception):
    pass


class ResourceRecord(object):
    REQUIRED_BIGIP_VERSION = '9.0.3'

    def __init__(self, module):
        self.module = module

        self.username = module.params['username']
        self.password = module.params['password']
        self.hostname = module.params['hostname']
        self.type = module.params['type']
        self.ttl = module.params['ttl']
        self.view = module.params['view']
        self.zone = module.params['zone']
        self.options = module.params['options']

        if not self.zone.endswith('.'):
            self.zone += '.'

        self.view_zones = [{
            'view_name': self.view,
            'zone_name': self.zone
        }]

        self.client = bigsuds.BIGIP(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            debug=True
        )

        self.check_required_params()
        self.check_version()

    def check_version(self):
        response = self.client.System.SystemInfo.get_version()
        match = re.search(VERSION_PATTERN, response)
        version = match.group('version')

        v1 = StrictVersion(version)
        v2 = StrictVersion(self.REQUIRED_BIGIP_VERSION)

        if v1 < v2:
            raise ResourceRecordException('The BIG-IP version %s does not support this record type' % version)

    def check_required_params(self):
        params = self.options.keys()

        for param in self.REQUIRED_PARAMS:
            if param not in params:
                raise ResourceRecordException('Required param %s not specified' % param)


class AResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'ip_address'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'ip_address': self.options['ip_address'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_a(
                view_zones=self.view_zones,
                a_records=records,
                sync_ptrs=[1]
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class AaaaResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'ip_address'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'ip_address': self.options['ip_address'],
            'ttl': self.ttl
        }]]

        self.client.Management.ResourceRecord.add_aaaa(
            view_zones=self.view_zones,
            aaaa_records=records,
            sync_ptrs=[1]
        )


class CnameResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'cname'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'cname': self.options['cname'],
            'ttl': self.ttl
        }]]

        self.client.Management.ResourceRecord.add_cname(
            view_zones=self.view_zones,
            cname_records=records
        )


class DnameResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'label'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'label': self.options['label'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_dname(
                view_zones=self.view_zones,
                dname_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class DsResourceRecord(ResourceRecord):
    REQUIRED_BIGIP_VERSION = '11.4.0'

    REQUIRED_PARAMS = [
        'domain_name', 'key_tag', 'algorithm', 'digest_type', 'digest'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'key_tag': self.options['label'],
            'algorithm': self.options['algorithm'],
            'digest_type': self.options['digest_type'],
            'digest': self.options['digest'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_ds(
                view_zones=self.view_zones,
                ds_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class HinfoResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'hardware', 'os'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'hardware': self.options['hardware'],
            'os': self.options['os'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_hinfo(
                view_zones=self.view_zones,
                hinfo_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class MxResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'preference', 'mail'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'preference': self.options['preference'],
            'mail': self.options['mail'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_mx(
                view_zones=self.view_zones,
                mx_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class NaptrResourceRecord(ResourceRecord):
    REQUIRED_BIGIP_VERSION = '11.4.0'

    REQUIRED_PARAMS = [
        'domain_name', 'order', 'preference', 'flags', 'service', 'regexp',
        'replacement'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'order': self.options['order'],
            'preference': self.options['preference'],
            'flags': self.options['flags'],
            'service': self.options['service'],
            'regexp': self.options['regexp'],
            'replacement': self.options['replacement'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_naptr(
                view_zones=self.view_zones,
                naptr_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class NsResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'host_name'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'host_name': self.options['host_name'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_ns(
                view_zones=self.view_zones,
                ns_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class PtrResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'ip_address', 'dname'
    ]

    def create_record(self):
        records = [[{
            'ip_address': self.options['ip_address'],
            'dname': self.options['dname'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_ptr(
                view_zones=self.view_zones,
                ptr_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class SoaResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'primary', 'email', 'serial', 'refresh', 'retry',
        'expire', 'neg_ttl'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'primary': self.options['primary'],
            'email': self.options['email'],
            'serial': self.options['serial'],
            'refresh': self.options['refresh'],
            'retry': self.options['retry'],
            'expire': self.options['expire'],
            'neg_ttl': self.options['neg_ttl'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_soa(
                view_zones=self.view_zones,
                soa_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class SrvResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'priority', 'weight', 'port', 'target'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'priority': self.options['priority'],
            'weight': self.options['weight'],
            'port': self.options['port'],
            'target': self.options['target'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_srv(
                view_zones=self.view_zones,
                srv_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


class TxtResourceRecord(ResourceRecord):
    REQUIRED_PARAMS = [
        'domain_name', 'text'
    ]

    def create_record(self):
        records = [[{
            'domain_name': self.options['domain_name'],
            'text': self.options['text'],
            'ttl': self.ttl
        }]]

        try:
            self.client.Management.ResourceRecord.add_txt(
                view_zones=self.view_zones,
                txt_records=records
            )
        except Exception as e:
            raise ResourceRecordException(str(e))


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        type=dict(default=None, required=True, choices=RECORDS),
        ttl=dict(default=60),
        view=dict(default='external'),
        zone=dict(required=True),
        options=dict(required=True, type='dict')
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    try:
        obj = BigIpApiFactory.factory(module)
        result = obj.flush()

        module.exit_json(**result)
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host")
    except bigsuds.ServerError as e:
        if 'folder not found' in str(e):
            module.fail_json(msg="Partition not found")
        else:
            pass

    state = module.params["state"]

    try:
        record = get_resource_record(module)

        if state == "present":
            record.create_record()
            changed = True
        elif state == "absent":
            record.delete_record()
    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
