#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from invoke import task


@task(name='sanity-all')
def sanity_all_(c):
    cmds = [
        'bash test/ansible/sanity/correct-defaultdict-import.sh',
        'bash test/ansible/sanity/correct-iteritems-import.sh',
        'bash test/ansible/sanity/incorrect-comparisons.sh',
        'bash test/ansible/sanity/integration-test-idempotent-names.sh',
        'bash test/ansible/sanity/q-debugging-exists.sh',
        'python test/ansible/sanity/f5-sdk-install-missing-code-highlighting.py',
        'python test/ansible/sanity/short-description-ends-with-period.py'
    ]

    for cmd in cmds:
        c.run(cmd, pty=True)


@task
def unit(c):
    c.run("pytest -s test/")


@task
def style(c):
    c.run("pycodestyle .")
