#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import sys
from invoke import task

AVAILABLE_PYTHON=['2.7', '3.5', '3.6', '3.7']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONFIG_DIR = os.path.expanduser('~/.f5ansible')


def init(c):
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    if not os.path.exists(CONFIG_DIR + '/docker-compose.site.yaml'):
        print("No docker-compose.site.yaml found in ~/.f5ansible directory.")
        sys.exit(1)


@task
def container_update(c):
    init(c)
    cmd = [
        'docker-compose', '-f', '{0}/devtools/docker-compose.yaml'.format(BASE_DIR),
        '-f {0}/docker-compose.site.yaml'.format(CONFIG_DIR),
        'pull'
    ]
    c.run(' '.join(cmd), hide='err')


@task
def module_docs(c):
    init(c)
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


@task(help={'python': "Python version to use in container."})
def run(c, python='3.6'):
    if str(python) not in AVAILABLE_PYTHON:
        print("The specified --python value is not in the allowed list")
        print("Allowed values are {0}".format(', '.join(AVAILABLE_PYTHON)))
        sys.exit(1)

    try:
        container_update(c)
    except:
        pass

    cmd = [
        'docker-compose', '-f', '{0}/devtools/docker-compose.yaml'.format(BASE_DIR),
        '-f {0}/docker-compose.site.yaml'.format(CONFIG_DIR),
        'run', 'py{0}'.format(python)
    ]
    c.run(' '.join(cmd), pty=True)


@task
def ip_add(c):
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
def ip_delete(c):
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


@task
def docs_build(c):
    with c.cd("docs"):
        c.run("rm -rf _build")
        c.run("make html")


@task(module_docs, docs_build)
def docs(c):
    print("done")


@task
def style(c):
    c.run("pycodestyle .")


@task
def unit(c):
    c.run("pytest -s test/")


@task
def docker_prune(c):
    print("Reclaiming container space")
    c.run("docker container prune -f")
    print("\n")

    print("Reclaiming image space")
    c.run("docker image prune -f")
    print("\n")

    print("Reclaiming volume space")
    c.run("docker volume prune -f")
    print("\n")


@task
def docker_df(c):
    c.run("docker system df")


@task
def sanity_run(c):
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
