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
module: bigiq_license_pool_member
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
  - https://localhost:10443/mgmt/shared/iapp/global-installed-packages/
requirements:
  - f5-sdk
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()


