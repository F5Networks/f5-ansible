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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: bigip_iapp_service
short_description: Manages TCL iApp services on a BIG-IP
description:
  - Manages TCL iApp services on a BIG-IP
version_added: "2.3"
options:
  name:
    description:
      - The name of the iApp template that you want to delete. This option
        is only available when specifying a C(state) of C(absent) and is
        provided as a way to delete templates that you may no longer have
        the source of.
    required: False
  template:
    description:
      - The iApp template from which to instantiate a new service.
    required: true
  tables:
    description:
      - Dictionary of tables and values to supply to the iApp service
    required: False
    default: None
  variables:
    description:
      - Dictionary of variables names and their values to supply to the iApp
        service
    required: False
    default: None
  state:
    description:
      - Whether the iRule should exist or not.
    required: false
    default: present
    choices:
      - present
      - absent
notes:
  - Requires the f5-sdk Python package on the host. This is as easy as pip
    install f5-sdk.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
