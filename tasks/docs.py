#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from invoke import task
from .lib.common import init


@task(name='module')
def module_(c):
    init()
    result = c.run('python ./devtools/bin/limit_module_docs.py')
    c.run('rm docs/modules/* || true')

    cmd = [
        'python', 'devtools/bin/plugin_formatter.py',
        '--module-dir', 'library/',
        '--template-dir', 'devtools/templates/',
        '--output-dir', 'docs/modules/',
        '-v',
        '--limit-to', result.stdout
    ]
    c.run(' '.join(cmd))


@task
def build(c):
    with c.cd("docs"):
        c.run("rm -rf _build")
        c.run("make html")


@task(module_, build)
def docs(c):
    print("done")
