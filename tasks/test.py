#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
import os

from .lib.common import BASE_DIR
from invoke import task


@task(name='f5-sanity')
def f5_sanity(c):
    """Runs additional sanity tests on the F5 modules."""
    cmds = [
        'bash {0}/test/sanity/correct-defaultdict-import.sh'.format(BASE_DIR),
        'bash {0}/test/sanity/correct-iteritems-import.sh'.format(BASE_DIR),
        'bash {0}/test/sanity/incorrect-comparisons.sh'.format(BASE_DIR),
        'bash {0}/test/sanity/integration-test-idempotent-names.sh'.format(BASE_DIR),
        'bash {0}/test/sanity/q-debugging-exists.sh'.format(BASE_DIR),
        'bash {0}/test/sanity/unnecessary-quotes-around-common.sh'.format(BASE_DIR),
        'bash {0}/test/sanity/unnecessary-default-none.sh'.format(BASE_DIR),
        'bash {0}/test/sanity/unnecessary-required-false.sh'.format(BASE_DIR),
    ]

    for cmd in cmds:
        c.run(cmd, pty=True)


@task
def unit(c):
    """Unit tests on F5 Ansible modules."""
    c.run("pytest -s {0}/ansible_collections/f5networks/f5_modules/tests/".format(BASE_DIR))


@task
def style(c):
    """Doc style testing on modules."""
    c.run("pycodestyle {0}/ansible_collections/f5networks/f5_modules/plugins/".format(BASE_DIR))


@task(name='install-dep')
def install_dependency(c):
    """Install netcommon collection if missing."""
    c.run("ansible-galaxy collection install ansible.netcommon -p {0}".format(BASE_DIR))


@task(name='ansible-test')
def ansible_test(c, python_version='3.7', requirements=False):
    """Runs ansible-test sanity tests against modules."""
    net_dir = '{0}/ansible_collections/ansible/netcommon/'.format(BASE_DIR)
    collection = '{0}/ansible_collections/f5networks/f5_modules'.format(BASE_DIR)
    if not os.path.exists(net_dir):
        install_dependency(c)
    with c.cd(collection):
        if requirements:
            execute = 'ansible-test sanity --requirements --python {0}'.format(python_version)
        else:
            execute = 'ansible-test sanity --python {0}'.format(python_version)
        result = c.run(execute, warn=True)
        if result.failed:
            sys.exit(1)
        c.run('rm -rf {0}/tests/output'.format(collection))

