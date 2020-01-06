#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

from .lib.common import BASE_DIR

from invoke import task


HELP1 = dict(
    collection="The collection name to which the modules are upstreamed, default: 'f5_modules'."
)


def purge_upstreamed_files(c, module_utils, collection):
    if not os.path.exists(collection):
        return
    if not os.path.exists(module_utils):
        return
    if len(os.listdir(module_utils)) > 0:
        print("Purging contents from {0}.".format(module_utils))
        with c.cd(module_utils):
            c.run('rm -rf *')


@task(optional=['collection'], help=HELP1)
def upstream(c, collection='f5_modules'):
    """Copy all module utils, to the local/ansible_collections/f5networks/collection_name directory.
    """
    coll_dest = '{0}/local/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    module_utils = '{0}/local/ansible_collections/f5networks/{1}/plugins/module_utils/'.format(BASE_DIR, collection)

    purge_upstreamed_files(c, module_utils, coll_dest)

    if not os.path.exists(coll_dest):
        print("The required collection directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(coll_dest))
        print("Collection directory created.")

    if not os.path.exists(module_utils):
        print("The required module_utils directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(module_utils))
        print("Module utils directory created.")

    # - upstream module utils files
    cmd = [
        'cp', '{0}/library/module_utils/network/f5/*.py'.format(BASE_DIR),
        '{0}'.format(module_utils)
    ]
    c.run(' '.join(cmd))
    print("Copy complete")
