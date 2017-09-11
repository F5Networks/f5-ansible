#!/usr/bin/env python
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

import argparse
import os
from tabulate import tabulate

table = [["spam",42],["eggs",451],["bacon",0]]
headers = ["item", "qty"]
print tabulate(table, headers, tablefmt="psql")

def main():
    common = argparse.ArgumentParser(add_help=False)

    common.add_argument('--readthedocs',
                        action='store_true',
                        help='Create visual represation for ReadTheDocs')

    common.add_argument('-v', '--verbose',
                        dest='verbosity',
                        action='count',
                        default=0,
                        help='display more output')

    common.add_argument('--color',
                        metavar='COLOR',
                        nargs='?',
                        help='generate color output: %(choices)s',
                        choices=('yes', 'no', 'auto'),
                        const='yes',
                        default='auto')

if __name__ == '__main__':
    main()
