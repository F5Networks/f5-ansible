#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import glob
import os
import re
import yaml

from . common import BASE_DIR


def module_name(module):
    filename, extension = os.path.splitext(module)
    return filename


def get_fixtures(c, module):
    result = []

    pattern1 = r"load_fixture\(\'(?P<fixture>[^']+)"
    pattern2 = r"fixtures\/(?P<fixture>[^']+)"
    pattern3 = r"fixture_path\,\s+\'(?P<fixture>[^']+)"

    cmd = [
        'egrep', '"(load_fixture|fixtures|fixture_path)" {0}/test/unit/test_{1}.py'.format(BASE_DIR, module),
        '|', 'egrep -v "(def load_fixture|fixture_path\,\s+name)"'
    ]
    stdout = c.run(' ' .join(cmd), hide='out', warn=True)
    stdout = [x.strip() for x in stdout.stdout.split("\n") if x]

    for x in stdout:
        matches = re.search(pattern1, x)
        if matches:
            result.append(matches.group('fixture'))
            continue
        matches = re.search(pattern2, x)
        if matches:
            result.append(matches.group('fixture'))
            continue
        matches = re.search(pattern3, x)
        if matches:
            result.append(matches.group('fixture'))
            continue
    return result


def get_all_module_names():
    files = get_all_module_files()
    result = [os.path.splitext(x)[0] for x in files]
    return result


def get_all_module_files():
    result = []
    for filename in glob.glob('{0}/library/modules/*.py'.format(BASE_DIR)):
        f = os.path.basename(filename)
        if f == '__init__.py':
            continue
        if 'iworkflow' in f:
            continue
        if os.path.islink(filename):
            continue
        result.append(f)
    return result


def should_upstream_module(module):
    # - read in the yaml playbook for the module
    yfile = '{0}/test/integration/{1}.yaml'.format(BASE_DIR, module)
    with open(yfile, 'r') as fh:
        pb = yaml.load(fh)
        try:
            if 'Metadata of' in pb[0]['name']:
                result = pb[0]['vars']['__metadata__']['upstream']
                return result
        except KeyError:
            raise Exception(
                "Could not file the appropriate 'upstream' key in the "
                "module's integration test playbook."
            )
