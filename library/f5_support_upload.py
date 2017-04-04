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
module: bigip_partition
short_description: Manage BIG-IP partitions
description:
  - Manage BIG-IP partitions
version_added: "2.3"
options:
  description:
    description:
      - The description to attach to the Partition
    required: False
    default: None
  route_domain:
    description:
      - The default Route Domain to assign to the Partition. If no route domain
        is specified, then the default route domain for the system (typically
        zero) will be used only when creating a new partition. C(route_domain)
        and C(route_domain_id) are mutually exclusive.
    required: False
    default: None
notes:
  - Requires the bigsuds Python package on the host if using the iControl
    interface. This is as easy as pip install bigsuds
requirements:
  - bigsuds
  - requests
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

