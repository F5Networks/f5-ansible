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
notes:
  - Requires the f5-sdk Python package on the remote host. This is as easy as
    pip install f5-sdk
requirements:
  - f5-sdk
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''

'''

RETURN = r'''

'''

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
