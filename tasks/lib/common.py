#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import os
import sys
import glob
from filecmp import dircmp


AVAILABLE_PYTHON = ['2.7', '3.5', '3.6', '3.7']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
CONFIG_DIR = os.path.expanduser('~/.f5ansible')


def init():
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    if not os.path.exists(CONFIG_DIR + '/docker-compose.site.yaml'):
        print("No docker-compose.site.yaml found in ~/.f5ansible directory.")
        sys.exit(1)


def in_container():
    """Check to see if we are running in a container

    Returns:
        bool: True if in a container. False otherwise.
    """
    try:
        with open('/proc/1/cgroup') as fh:
            lines = fh.readlines()
    except IOError:
        return False
    if any('/docker/' in x for x in lines):
        return True
    return False


def cmp_dir(d1, d2):
    cmpdir = dircmp(d1, d2)
    if len(cmpdir.left_list) == len(cmpdir.right_list):
        if len(cmpdir.diff_files) > 0:
            return False
        return True
    return False


def copy_ignores(c, collection_dir):
    ignores_dir = '{0}/tests/sanity'.format(collection_dir)
    if not os.path.exists(ignores_dir):
        c.run('mkdir -p {0}'.format(ignores_dir))
    if len(list(glob.glob('{0}/*.txt'.format(ignores_dir)))) == 0:
        c.run('cp {0}/devtools/sanity/* {1}'.format(BASE_DIR, ignores_dir))
        print('Ignore files copied.')
