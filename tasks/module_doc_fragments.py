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


@task
def upstream(c):
    """Upstream module_doc_fragments to Ansible core

    Module doc fragments are documentation blobs that apply to **all** F5
    Ansible modules. They are typically used to document parameters that
    are available to all modules (such as connection params).

    Args:
        c:

    Returns:

    """
    root_dest = '{0}/local/ansible/'.format(BASE_DIR)
    if not os.path.exists(root_dest):
        print("The specified upstream directory does not exist")
        sys.exit(1)

    # - upstream module utils files
    cmd = [
        'cp', '{0}/library/utils/module_docs_fragments/*'.format(BASE_DIR),
        '{0}/local/ansible/lib/ansible/utils/module_docs_fragments/'.format(BASE_DIR)
    ]
    c.run(' '.join(cmd))
    print("Copy complete")
