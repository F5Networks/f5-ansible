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
import subprocess
import sys
import os
import shutil
import re


UPSTREAM_FIXTURE_FILE = '{0}/test/units/modules/network/f5/fixtures/{1}'
UPSTREAM_UNIT_TEST = '{0}/test/units/modules/network/f5/test_{1}.py'
UPSTREAM_INTEGRATION_TEST = '{0}/test/integration/targets/{1}'
UPSTREAM_MODULE = '{0}/lib/ansible/modules/network/f5/{1}.py'
DOWNSTREAM_FIXTURE_FILE = '{0}/test/unit/{1}/fixtures/{2}'
DOWNSTREAM_UNIT_TEST = '{0}/test/unit/{1}/test_{2}.py'
DOWNSTREAM_INTEGRATION_TEST = '{0}/test/integration/targets/{2}'
DOWNSTREAM_MODULE = '{0}/library/{1}.py'


def root_dir():
    result = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    return result


def exit_fail(message):
    print(message)
    sys.exit(1)


def exit_success(message):
    print(message)
    sys.exit(0)


def module_name(module):
    filename, extension = os.path.splitext(module)
    return filename


def product(module):
    if module.startswith('bigip_'):
        return 'bigip'
    elif module.startswith('bigiq_'):
        return 'bigiq'


def module_file_present(module):
    module_dir = '{0}/library/{1}.py'.format(
        root_dir(), module
    )
    if os.path.exists(module_dir):
        return True
    return False


def module_file_absent(module):
    result = module_file_present(module)
    return not result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--upstream-dir',
        action='store',
        default='local/ansible'
    )
    parser.add_argument(
        'module',
        action='store',
    )
    result = parser.parse_args()
    return result


def get_fixtures(module):
    result = []
    pattern1 = r"load_fixture\(\'(?P<fixture>[^']+)"
    pattern2 = r"fixtures\/(?P<fixture>[^']+)"
    p = product(module)
    p1 = subprocess.Popen(
        ['egrep', '(load_fixture|fixtures)', 'test/unit/{0}/test_{1}.py'.format(p, module)],
        stdout=subprocess.PIPE
    )
    p2 = subprocess.Popen(
        ['egrep', '-v', '(def load_fixture|fixture_path)'],
        stdin=p1.stdout, stdout=subprocess.PIPE
    )
    p1.stdout.close()
    stdout, stderr = p2.communicate()
    stdout = str(stdout).split("\n")
    stdout = [x.strip() for x in stdout if x]

    for x in stdout:
        matches = re.search(pattern1, x)
        if matches:
            result.append(matches.group('fixture'))
            continue
        matches = re.search(pattern2, x)
        if matches:
            result.append(matches.group('fixture'))
            continue
    return result


def copy_module(module, upstream_dir):
    upstream = os.path.realpath(upstream_dir)
    r = root_dir()
    dest = UPSTREAM_MODULE.format(upstream, module)
    src = DOWNSTREAM_MODULE.format(r, module)
    shutil.copy(src, dest)


def copy_unit_tests(module, upstream_dir):
    upstream = os.path.realpath(upstream_dir)
    r = root_dir()
    p = product(module)
    dest = UPSTREAM_UNIT_TEST.format(upstream, module)
    src = DOWNSTREAM_UNIT_TEST.format(r, p, module)
    shutil.copy(src, dest)


def copy_unit_test_fixtures(module, upstream_dir):
    fixtures = get_fixtures(module)
    upstream = os.path.realpath(upstream_dir)
    r = root_dir()
    p = product(module)
    for fixture in fixtures:
        dest = UPSTREAM_FIXTURE_FILE.format(upstream, fixture)
        src = DOWNSTREAM_FIXTURE_FILE.format(r, p, fixture)
        shutil.copy(src, dest)


def main():
    args = parse_args()
    module = module_name(args.module)

    root_dest = '{0}/local/ansible/'.format(root_dir())
    if not os.path.exists(root_dest):
        exit_fail("The specified upstream directory does not exist")

    try:
        copy_module(module, args.upstream_dir)
        copy_unit_tests(module, args.upstream_dir)
        copy_unit_test_fixtures(module, args.upstream_dir)
        print("Copy complete")
    except Exception as ex:
        exit_fail(str(ex))


if __name__ == '__main__':
    main()
