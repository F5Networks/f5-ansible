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
    """Upstream module_doc_fragments to Ansible collection.

    Module doc fragments are documentation blobs that apply to **all** F5
    Ansible modules. They are typically used to document parameters that
    are available to all modules (such as connection params).

    """
    root_dest = '{0}/local/ansible/'.format(BASE_DIR)
    if not os.path.exists(root_dest):
        print("The specified upstream directory does not exist")
        sys.exit(1)

    # - upstream doc fragments
    cmd = [
        'cp', '{0}/library/plugins/doc_fragments/*'.format(BASE_DIR),
        '{0}/local/ansible_collections/f5networks/{1}/plugins/doc_fragments'.format(BASE_DIR, collection)
    ]
    c.run(' '.join(cmd))
    print("Copy complete")
