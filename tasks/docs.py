#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import os

from invoke import task

from .lib.common import BASE_DIR


@task(name='module')
def module_(c):
    excludes = ['__init__.py']
    files = os.listdir('{0}/library/modules'.format(BASE_DIR))
    files = [os.path.splitext(x)[0] for x in files if x not in excludes]
    limit_to = ','.join(files)

    c.run('rm {0}/docs/modules/* || true'.format(BASE_DIR))

    cmd = [
        'python', '{0}/tasks/bin/plugin_formatter.py'.format(BASE_DIR),
        '--module-dir', '{0}/library/modules/'.format(BASE_DIR),
        '--template-dir', '{0}/devtools/templates/'.format(BASE_DIR),
        '--output-dir', '{0}/docs/modules/'.format(BASE_DIR),
        '-vvvv',
        '--limit-to', limit_to
    ]
    c.run(' '.join(cmd))


@task
def build(c):
    with c.cd("{0}/docs".format(BASE_DIR)):
        c.run("rm -rf _build")
        c.run("make html")


@task(module_, build)
def make(c):
    print("done")
