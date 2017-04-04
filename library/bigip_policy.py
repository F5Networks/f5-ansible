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
module: bigip_policy
short_description: Manage general policy configuration on a BIG-IP.
description:
  - Manages general policy configuration on a BIG-IP. This module is best
    used in conjunction with the C(bigip_policy_rule) module. This module
    can handle general configuration like setting the draft state of the policy,
    the description, and things unrelated to the policy rules themselves.
    It is also the first module that should be used when creating rules as
    the C(bigip_policy_rule) module requires a policy parameter.
version_added: "2.4"
options:
  description:
    description:
      - The description to attach to the Partition.
    required: False
    default: None
  name:
    description:
      - The name of the policy to create.
    required: True
  state:
    description:
      - Whether the partition should exist or not.
    required: false
    default: present
    choices:
      - present
      - absent
      - draft
  strategy:
    description:
      - Specifies the method to determine which actions get executed in the
        case where there are multiple rules that match. When creating new
        policies, the default is C(first).
    default: None
    required: False
    choices:
      - first
      - all
      - best
notes:
   - Requires the f5-sdk Python package on the host. This is as easy as
     pip install f5-sdk
requirements:
  - f5-sdk
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
vars:
    policy_rules:
        - name: rule1
          actions:
              - forward: "yes"
                select: "yes"
                pool: "pool-svrs"
          conditions:
              - http_uri: "yes"
                path: "yes"
                starts-with:
                    - /euro
          ordinal: 8
        - name: HomePage
          actions:
              - forward: yes
                select: yes
                pool: "pool-svrs"
          conditions:
              - http-uri: yes
                path: yes
                starts-with:
                    - /HomePage/
          ordinal: 4

- name: Create policies
  bigip_policy:
      name: "Policy-Foo"
      state: present
  delegate_to: localhost

- name: Add a rule to the new policy
  bigip_policy_rule:
      policy: "Policy-Foo"
      name: "ABC"
      ordinal: 11
      conditions:
          - http_uri: "yes"
            path: "yes"
            starts_with:
                - "/ABC"
      actions:
          - forward: "yes"
            select: "yes"
            pool: "pool-svrs"

- name: Add multiple rules to the new policy
  bigip_policy_rule:
      policy: "Policy-Foo"
      name: "{{ item.name }}"
      ordinal: "{{ item.ordinal }}"
      conditions: "{{ item.conditions }}"
      actions: "{{ item.actions }}"
  with_items:
      - policy_rules
'''

