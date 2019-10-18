#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
import os
import glob

from .lib.common import BASE_DIR

from invoke import task


HELP1 = dict(
    collection="The collection name to which the plugins are upstreamed, default: 'f5_modules'."
)


def upstream_plugin(c, plugin, collection='f5_modules'):
    plugin_dir = '{0}/library/plugins/{1}/'.format(BASE_DIR, plugin)
    target_dir = '{0}/local/ansible_collections/f5networks/{1}/plugins/{2}/'.format(BASE_DIR, collection, plugin)
    if not os.path.exists(plugin_dir):
        print("No plugin type {0} directory found ...skipping.".format(plugin))
        return
    if len(list(glob.glob('{0}/*.py'.format(target_dir)))) == 0:
        print("No plugin type {0} files found ...skipping.".format(plugin))
        return
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    cmd = [
        'cp', '{0}/*.py'.format(plugin_dir),
        target_dir
    ]
    c.run(' '.join(cmd))
    print("Copy of {0} type plugins complete!".format(plugin))


@task(optional=['collection'], help=HELP1)
def upstream(c, collection='f5_modules'):
    """Copy all plugins, to the local/ansible_collections/f5networks/collection_name directory.
    """
    root_dest = '{0}/local/ansible_collections/'.format(BASE_DIR)
    coll_dest = '{0}/local/ansible_collections/f5networks/{1}/'.format(BASE_DIR, collection)
    if not os.path.exists(root_dest) or not os.path.exists(coll_dest):
        print("The specified upstream directory and/or collection directory does not exist.")
        sys.exit(1)

    upstream_plugin(c, 'action')
    upstream_plugin(c, 'connection')
    upstream_plugin(c, 'filter')
    upstream_plugin(c, 'httpapi')
    upstream_plugin(c, 'lookup')
    upstream_plugin(c, 'terminal')
    print("Plugins copy complete.")
