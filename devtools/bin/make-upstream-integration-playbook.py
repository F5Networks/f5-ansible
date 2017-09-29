#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
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

import argparse
import glob
import sys
import os


UPSTREAM_PLAYBOOK = '{0}/test/integration/bigip.yaml'


def root_dir():
    result = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    return result


def exit_fail(message):
    print(message)
    sys.exit(1)


def exit_success(message):
    print(message)
    sys.exit(0)


def get_upstream_roles(upstream_dir):
    targets = '{0}/test/integration/targets/bigip*'.format(upstream_dir)
    return glob.iglob(targets)


def write_playbook_to_disk(targets, upstream_dir):
    upstream = os.path.realpath(upstream_dir)
    dest = UPSTREAM_PLAYBOOK.format(upstream)
    PREAMBLE = """---

- hosts: f5
  gather_facts: no
  connection: local

  vars:
    limit_to: "*"
    debug: false

  roles:
"""

    with open(dest, 'w') as fh:
        fh.write(PREAMBLE)
        for target in targets:
            line = '      - { role: %s, when: "limit_to in [\'*\', \'%s\']" }' % (target, target)
            fh.write(line)
        fh.write("\n")


def create_integration_playbook(upstream_dir):
    targets = get_upstream_roles(upstream_dir)
    targets = [os.path.basename(t) for t in targets]
    write_playbook_to_disk(targets, upstream_dir)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--upstream-dir',
        action='store',
        default='local/ansible'
    )
    result = parser.parse_args()
    return result


def main():
    args = parse_args()

    root_dest = '{0}/local/ansible/'.format(root_dir())
    if not os.path.exists(root_dest):
        exit_fail("The specified upstream directory does not exist")

    create_integration_playbook(args.upstream_dir)


if __name__ == '__main__':
    main()
