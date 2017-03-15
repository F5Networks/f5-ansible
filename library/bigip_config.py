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
module: bigip_config
short_description: Manage BIG-IP configuration sections
description:
  - Cisco NXOS configurations use a simple block indent file syntax
    for segmenting configuration into sections. This module provides
    an implementation for working with NXOS configuration sections in
    a deterministic way. This module works with either CLI or NXAPI
    transports.
version_added: "2.3"
options:
  save:
    description:
      - The C(save) argument instructs the module to save the
        running-config to startup-config. This operation is performed
        after any changes are made to the current running config. If
        no changes are made, the configuration is still saved to the
        startup config. This option will always cause the module to
        return changed.
    choices:
      - yes
      - no
    required: false
    default: false
  load_sys_default:
    description:
      - Loads the default configuration on the device
notes:
  - Requires the f5-sdk Python package on the remote host. This is as easy as
    pip install f5-sdk
extends_documentation_fragment: f5
requirements:
  - f5-sdk
author:
    - Tim Rupp (@caphrim007)
'''

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
