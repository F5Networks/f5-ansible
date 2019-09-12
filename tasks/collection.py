#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import semver
import sys

from .lib.common import BASE_DIR
from invoke import task

try:
    from jinja2 import Environment
    from jinja2 import FileSystemLoader
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False

if HAS_JINJA:
    JINJA_ENV = Environment(
        loader=FileSystemLoader(BASE_DIR + '/devtools/stubs')
    )

BUILD_DIR = '{0}/local/ansible_collections/_builds'.format(BASE_DIR)

HELP1 = dict(
    version="Version of the collection to build, the version must follow in SemVer format.",
    collection="The collection name to which the modules are upstreamed, DEFAULT: 'f5_modules'.",
    skip_tests="Allows bypassing ansible sanity tests when building collection, DEFAULT: false",
)


def update_galaxy_file(version, collection):
    # updates galaxy.yml file for collection update
    galaxy_file = '{0}/local/ansible_collections/f5networks/{1}/galaxy.yml'.format(BASE_DIR, collection)

    template = JINJA_ENV.get_template('collection_galaxy.yml')
    content = template.render(version=version, collection=collection)

    fh = open(galaxy_file, 'w')
    fh.write(content)
    fh.close()


def ansible_test_collection(c, collection):
    ansible_test = '{0}/local/ansible/bin'.format(BASE_DIR)
    collection_dir = '{0}/local/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    if not os.path.exists(ansible_test):
        print("The ansible directory does not exist - skipping tests.")
        return
    with c.cd(collection_dir):
        execute = '{0}/ansible-test sanity plugins/modules/*.*'.format(ansible_test)
        result = c.run(execute, warn=True)
        if result.failed:
            sys.exit(1)
        c.run('rm -rf {0}/tests/output'.format(collection_dir))


def validate_version(version):
    try:
        semver.parse_version_info(version)
    except ValueError as ex:
        print(str(ex))
        sys.exit(1)


@task(optional=['collection', 'skip_tests'], help=HELP1)
def build(c, version, collection='f5_modules', skip_tests=False):
    """Creates collection builds in the ansible_collections/_build directory."""
    if not skip_tests:
        ansible_test_collection(c, collection)
    validate_version(version)
    update_galaxy_file(version, collection)
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
    coll_dest = '{0}/local/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    cmd = 'ansible-galaxy collection build {0} -f --output-path {1}'.format(coll_dest, BUILD_DIR)
    c.run(cmd)


@task
def test(c, collection):
    ansible_test_collection(c, collection)


@task
def publish(c, filename, api_key):
    """Publish collection on Galaxy."""
    file = '{0}/{1}'.format(BUILD_DIR, filename)
    if not os.path.exists(file):
        sys.exit(1)
    cmd = 'ansible-galaxy collection publish {0} --api-key={1}'.format(file, api_key)
    c.run(cmd)
