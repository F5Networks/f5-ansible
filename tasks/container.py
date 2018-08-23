#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from invoke import task
from .lib.common import init
from .lib.common import BASE_DIR
from .lib.common import CONFIG_DIR
from .lib.common import AVAILABLE_PYTHON


@task
def prune(c):
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
def df(c):
    c.run("docker system df")


@task
def container_update(c):
    """Pull containers from registry and update locally

    This command will pull containers from the remote registry using the docker-compose
    files that exist 1. In this repository and 2. In your home directory (for site specific
    configuration).
    """

    init()
    cmd = [
        'docker-compose', '-f', '{0}/devtools/docker-compose.yaml'.format(BASE_DIR),
        '-f {0}/docker-compose.site.yaml'.format(CONFIG_DIR),
        'pull'
    ]
    c.run(' '.join(cmd), hide='err')


@task(help={'python': "Python version to use in container."})
def run(c, python='3.6'):
    """Start a container running a specific version of Python

    Args:
        c:
        python: The python version that you want to run. This determines
                the container that is used.

    Returns:

    """
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
