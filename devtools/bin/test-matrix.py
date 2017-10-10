#!/usr/bin/env python
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import os
import sys
import yaml
from os.path import dirname
from tabulate import tabulate
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--include-legacy',
        action='store_true',
        help='Include legacy versions in the list of tested versions.',
        default=False
    )
    parser.add_argument(
        '--list-legacy',
        action='store_true',
        help='List legacy tested versions.',
        default=False
    )
    parser.add_argument(
        '-m', '--module',
        action='store',
        help='List tested versions for the specified module',
        default=False
    )
    result = parser.parse_args()
    return result

tld = dirname(dirname(dirname(os.path.realpath(__file__))))

table = []
headers = ['Module']
versions = sorted([
    '11.5.4-hf1',
    '11.6.0',
    '11.6.1',
    '11.6.1-hf1',
    '12.0.0', '12.1.0', '12.1.1', '12.1.2', '13.0.0',
    '12.1.0-hf1',
    '12.1.0-hf2',
    '12.1.1-hf1',
    '12.1.1-hf2',
    '12.1.2-hf1',
    '13.0.0-hf1',
])
headers += versions

for file in os.listdir(tld + '/test/integration'):
    if not file.endswith('.yaml'):
        continue

    fh = open(tld + '/test/integration/' + file)
    doc = yaml.load(fh)

    row = [os.path.splitext(file)[0]]
    try:
        vars = doc[0]['vars']
        tested = vars['__metadata__']['tested_platforms']
    except KeyError:
        tested = []

    result = map(lambda x: 'X' if x in tested else '', headers[1:])
    row += result
    table.append(row)

result = tabulate(table, headers=headers, tablefmt='grid')
print result

def main():
    pass
