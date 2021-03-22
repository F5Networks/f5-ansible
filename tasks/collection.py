#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 F5 Networks Inc.
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

BUILD_DIR = '{0}/builds'.format(BASE_DIR)

HELP = dict(
    filename="Name of the tarball file to be published found in builds directory.",
    api_key="The api key from Ansible Galaxy to be used to upload",
    ah="Indicates if we are publishing AH."
)


def update_galaxy_file(version, collection):
    # updates galaxy.yml file for collection update
    galaxy_file = '{0}/ansible_collections/f5networks/{1}/galaxy.yml'.format(BASE_DIR, collection)

    template = JINJA_ENV.get_template('collection_galaxy_{0}.yml'.format(collection))
    content = template.render(version=version, collection=collection)

    fh = open(galaxy_file, 'w')
    fh.write(content)
    fh.close()


def validate_version(version):
    try:
        semver.parse_version_info(version)
    except ValueError as ex:
        print(str(ex))
        sys.exit(1)


@task(name='change-version', optional=['collection'], help=dict(
    version="What version of collection to set in the galaxy.yml file, the version must follow in SemVer format.",
    collection="The collection name for which the galaxy.yml file to be changed, DEFAULT: 'f5_modules'.",
))
def change_galaxy_version(c, version, collection='f5_modules'):
    """Changes version of the collection in galaxy.yml file."""
    validate_version(version)
    update_galaxy_file(version, collection)
    print("File galaxy.yml updated.")


@task(optional=['collection'], help=dict(
    version="Version of the collection to build, the version must follow in SemVer format.",
    collection="The collection name to which the modules are upstreamed, DEFAULT: 'f5_modules'.",
    update="Allows updating galaxy file when requested."
))
def build(c, version, collection='f5_modules', update=False):
    """Creates collection builds in the ansible_collections/_build directory."""
    validate_version(version)
    if update:
        update_galaxy_file(version, collection)
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
    coll_dest = '{0}/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    cmd = 'ansible-galaxy collection build {0} -f --output-path {1}'.format(coll_dest, BUILD_DIR)
    c.run(cmd)


@task(optional=['ah'], help=HELP)
def publish(c, filename, api_key, ah=None):
    """Publish collection on Galaxy."""
    file = '{0}/{1}'.format(BUILD_DIR, os.path.basename(filename))
    if not os.path.exists(file):
        print("Requested file {0} not found.".format(file))
        sys.exit(1)
    if ah:
        cmd = 'ansible-galaxy collection publish {0} --api-key={1} -s https://cloud.redhat.com/ansible/automation-hub'.format(file, api_key)
    else:
        cmd = 'ansible-galaxy collection publish {0} --api-key={1}'.format(file, api_key)

    c.run(cmd)


@task(help=dict(
    version="What version of collection to set in the galaxy.yml file, the version must follow in SemVer format."
))
def changelog(c, version):
    """Build changelog and update galaxy.yml file version number."""
    collection = '{0}/ansible_collections/f5networks/f5_modules'.format(BASE_DIR)
    validate_version(version)
    with c.cd(collection):
        print('Linting changelog fragments.')
        cmd = "antsibull-changelog lint -v"
        result = c.run(cmd, warn=True)
        if result.failed:
            sys.exit(1)
        print('Generating changelog.')
        cmd = 'antsibull-changelog release'
        result = c.run(cmd, warn=True)
        if result.failed:
            sys.exit(1)
    print('Updating galaxy.yaml file.')
    update_galaxy_file(version, 'f5_modules')
    print('Changelog release complete.')
