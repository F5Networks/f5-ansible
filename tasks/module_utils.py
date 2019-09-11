#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import sys

from .lib.common import BASE_DIR

from invoke import task


HELP1 = dict(
    collection="The collection name to which the modules are upstreamed, default: 'f5_modules'."
)


@task(optional=['collection'], help=HELP1)
def upstream(c, collection='f5_modules'):
    """Copy all module utils, to the local/ansible_collections/F5Networks/collection_name directory.
    """
    root_dest = '{0}/local/ansible_collections/'.format(BASE_DIR)
    coll_dest = '{0}/local/ansible_collections/F5Networks/{1}'.format(BASE_DIR, collection)
    if not os.path.exists(root_dest) or os.path.exists(coll_dest):
        print("The specified upstream directory and/or collection directory does not exist.")
        sys.exit(1)

    # - upstream module utils files
    cmd = [
        'cp', '{0}/library/module_utils/network/f5/*'.format(BASE_DIR),
        '{0}/local/ansible_collections/F5Networks/{1}/plugins/module_utils/'.format(BASE_DIR, collection)
    ]
    c.run(' '.join(cmd))
    print("Copy complete")
