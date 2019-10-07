#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from .lib.common import BASE_DIR

from invoke import task


@task(name='sanity-all')
def sanity_all_(c):
    """Runs additional sanity tests on the F5 modules."""
    cmds = [
        'bash {0}/test/ansible/sanity/correct-defaultdict-import.sh'.format(BASE_DIR),
        'bash {0}/test/ansible/sanity/correct-iteritems-import.sh'.format(BASE_DIR),
        'bash {0}/test/ansible/sanity/incorrect-comparisons.sh'.format(BASE_DIR),
        'bash {0}/test/ansible/sanity/integration-test-idempotent-names.sh'.format(BASE_DIR),
        'bash {0}/test/ansible/sanity/q-debugging-exists.sh'.format(BASE_DIR),
        'bash {0}/test/ansible/sanity/unnecessary-quotes-around-common.sh'.format(BASE_DIR),
        'bash {0}/test/ansible/sanity/unnecessary-default-none.sh'.format(BASE_DIR),
        'bash {0}/test/ansible/sanity/unnecessary-required-false.sh'.format(BASE_DIR),
        'python {0}/test/ansible/sanity/short-description-ends-with-period.py'.format(BASE_DIR),
    ]

    for cmd in cmds:
        c.run(cmd, pty=True)


@task
def unit(c):
    """Unit tests on F5 Ansible modules."""
    c.run("pytest -s {0}/test/".format(BASE_DIR))


@task
def style(c):
    """Doc style testing on modules."""
    c.run("pycodestyle {0}".format(BASE_DIR))
