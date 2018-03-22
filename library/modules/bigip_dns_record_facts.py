#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_dns_record_facts
short_description: foo
description:
  - foo
version_added: "2.2"
options:
  server:
    description:
      - BIG-IP host
    required: true
  user:
    description:
      - BIG-IP username
    required: true
    aliases:
      - username
  password:
    description:
      - BIG-IP password
    required: true
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Create a ...
  bigip_dns_record_facts:
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

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
