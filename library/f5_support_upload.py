#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: f5_support_upload
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

EXAMPLES = r'''
- name: Create a ...
  {{ module }}:
    name: foo
    password: secret
    server: lb.mydomain.com
    state: present
    user: admin
  delegate_to: localhost
'''

RETURN = r'''
param1:
  description: The new param1 value of the resource.
  returned: changed
  type: bool
  sample: true
param2:
  description: The new param2 value of the resource.
  returned: changed
  type: string
  sample: Foo is bar
'''
