#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

from invoke import task


@task
def create(c):
    result = c.run('uname -s', hide='out')
    if result.failed:
        print(result.stderr)
        sys.exit(1)
    if result.stdout.startswith('Linux'):
        c.run('sudo ip addr add 1.2.3.4/8 dev lo label lo', pty=True)
    elif result.stdout.startswith('Darwin'):
        c.run("sudo ifconfig lo0 alias 1.2.3.4", pty=True)
    else:
        print('Platform not currently supported to create lo alias')
        sys.exit(1)


@task
def delete(c):
    result = c.run('uname -s')
    if result.failed:
        print(result.stderr)
        sys.exit(1)
    if result.stdout.startswith('Linux'):
        c.run('sudo ip addr del 1.2.3.4/8 dev lo label lo', pty=True)
    elif result.stdout.startswith('Darwin'):
        c.run("sudo ifconfig lo0 -alias 1.2.3.4", pty=True)
    else:
        print('Platform not currently supported to create lo alias')
        sys.exit(1)
