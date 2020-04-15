#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

from .lib.common import BASE_DIR
from .lib.common import cmp_dir

from invoke import task
from invoke.exceptions import Exit


HELP1 = dict(
    collection="The collection name to which the modules are upstreamed, default: 'f5_modules'.",
    verbose="Enables verbose message output."
)


def purge_upstreamed_files(c, module_utils, collection, verbose):
    if not os.path.exists(collection):
        return
    if not os.path.exists(module_utils):
        return
    if len(os.listdir(module_utils)) > 0:
        if verbose:
            print("Purging contents from {0}.".format(module_utils))
        with c.cd(module_utils):
            c.run('rm -rf *')


def files_upstream(c, module_utils_src, module_utils_dst):
    cmd = [
        'cp', '{0}/*.py'.format(module_utils_src),
        '{0}'.format(module_utils_dst)
    ]
    c.run(' '.join(cmd))


def create_directories(c, coll_dest, module_utils_dst, verbose):
    if not os.path.exists(coll_dest):
        if verbose:
            print("The required collection directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(coll_dest))
        if verbose:
            print("Collection directory created.")

    if not os.path.exists(module_utils_dst):
        if verbose:
            print("The required module_utils directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(module_utils_dst))
        if verbose:
            print("Module utils directory created.")


@task(optional=['collection', 'verbose'], help=HELP1)
def upstream(c, collection='f5_modules', verbose=False):
    """Copy all module utils, to the local/ansible_collections/f5networks/collection_name directory.
    """
    coll_dest = '{0}/local/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    module_utils_dst = '{0}/local/ansible_collections/f5networks/{1}/plugins/module_utils/'.format(BASE_DIR, collection)
    module_utils_src = '{0}/library/module_utils/network/f5/'.format(BASE_DIR)

    purge_upstreamed_files(c, module_utils_dst, coll_dest, verbose)
    create_directories(c, coll_dest, module_utils_dst, verbose)
    files_upstream(c, module_utils_src, module_utils_dst)

    retries = 0
    while not cmp_dir(module_utils_src, module_utils_dst):
        purge_upstreamed_files(c, module_utils_dst, coll_dest, verbose)
        create_directories(c, coll_dest, module_utils_dst, verbose)
        files_upstream(c, module_utils_src, module_utils_dst)
        retries = retries + 1

    if retries > 2:
        raise Exit('Failed to upstream module utils, exiting.')

    print("Module utils files upstreamed successfully.")
