#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import glob
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
    c.run("pytest -s {0}/test/".format(BASE_DIR))


@task
def style(c):
    """Doc style testing on modules."""
    c.run("pycodestyle {0}".format(BASE_DIR))


def copy_ignores(c, collection_dir):
    ignores_dir = '{0}/tests/sanity'.format(collection_dir)
    if not os.path.exists(ignores_dir):
        c.run('mkdir -p {0}'.format(ignores_dir))
    if len(list(glob.glob('{0}/*.txt'.format(ignores_dir)))) == 0:
        c.run('cp {0}/devtools/sanity/* {1}'.format(BASE_DIR, ignores_dir))
        print('Ignore files copied.')


@task(name='ansible-sanity')
def ansible_sanity(c, collection='f5_modules', python_version='3.7', requirements=False):
    """ This test is only used during CI/CD."""
    collection_dir = '{0}/local/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    root_dir = '{0}/local/ansible_collections'.format(BASE_DIR)
    workaround_dir = '{0}/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    copy_ignores(c, collection_dir)
    if not os.path.exists(workaround_dir):
        with c.cd(BASE_DIR):
            # As a workaround to the issue ansible-tests has when ansible_collection is nested inside local/ directory,
            # we need to move the directory out
            c.run('mv {0} .'.format(root_dir))
    with c.cd(workaround_dir):
        if requirements:
            execute = 'ansible-test sanity plugins/ --requirements --python {0}'.format(python_version)
        else:
            execute = 'ansible-test sanity plugins/ --python {0}'.format(python_version)
        result = c.run(execute, warn=True)
        if result.failed:
            sys.exit(1)
        c.run('rm -rf {0}/tests/output'.format(workaround_dir))
