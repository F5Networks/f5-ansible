#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import re

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
    stdout = c.run(' ' .join(cmd), hide='out')
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
