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
from .lib.common import copy_ignores
from .lib.common import cmp_dir

from .lib.upstream import module_name
from .lib.upstream import get_fixtures
from .lib.upstream import get_all_module_names
from .lib.upstream import should_upstream_module

from .lib.stubber import HAS_JINJA
from .lib.stubber import stub_roles_dirs
from .lib.stubber import stub_roles_yaml_files
from .lib.stubber import stub_playbook_file
from .lib.stubber import stub_library_file
from .lib.stubber import stub_unit_test_file

from .lib.stubber import unstub_roles_dirs
from .lib.stubber import unstub_roles_yaml_files
from .lib.stubber import unstub_playbook_file
from .lib.stubber import unstub_library_file
from .lib.stubber import unstub_unit_test_file

from invoke import task
from invoke.exceptions import Exit


@task
def stub(c, module=None):
    """Create module stubs.

    This command can be used to create the stub files necessary to start
    work on a new module.
    """
    if not HAS_JINJA:
        print("The jinja library is required")
        sys.exit(1)
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    stub_roles_dirs(module)
    stub_roles_yaml_files(module)
    stub_playbook_file(module)
    stub_library_file(module, extension)
    stub_unit_test_file(module, extension)


@task
def unstub(c, module=None):
    """Remove module stubs.

    This command can be used to remove the stub files created by the stub process.
    """
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    unstub_roles_yaml_files(module)
    unstub_roles_dirs(module)
    unstub_playbook_file(module)
    unstub_library_file(module, extension)
    unstub_unit_test_file(module, extension)


HELP1 = dict(
    module="A module name or list of module names separated by commas to be upstreamed. "
           "If all modules are required specify 'all' instead of a module name.",
    collection="The collection name to which the modules are upstreamed, default: 'f5_modules'.",
    verbose="Enables verbose message output."
)


def purge_upstreamed_module_files(c, collection, modules, test, verbose):
    if not os.path.exists(collection):
        return
    if os.path.exists(test) and len(os.listdir(test)) > 0:
        if verbose:
            print("Purging contents from {0}.".format(test))
        with c.cd(test):
            c.run('rm -rf *')
    if os.path.exists(modules) and len(os.listdir(modules)) > 0:
        if verbose:
            print("Purging contents from {0}.".format(modules))
        with c.cd(modules):
            c.run('rm -f *')


def copy_ignore_files(c, collection='f5_modules'):
    """Copy new version of ignore files."""
    coll_dest = '{0}/local/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    copy_ignores(c, coll_dest)


def create_directories(c, coll_dest, modules_dir, test_dir, fixtures_dir, verbose):
    if not os.path.exists(coll_dest):
        if verbose:
            print("The required collection directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(coll_dest))
        if verbose:
            print("Collection directory created.")

    if not os.path.exists(modules_dir):
        if verbose:
            print("The required module directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(modules_dir))
        if verbose:
            print("Module directory created.")

    if not os.path.exists(fixtures_dir):
        if verbose:
            print("The required test fixtures directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(fixtures_dir))
        if verbose:
            print("Test fixtures directory created.")

    if not os.path.exists(test_dir):
        if verbose:
            print("The required test directory does not exist, creating...")
        c.run('mkdir -p {0}'.format(test_dir))
        if verbose:
            print("Test directory created.")


def files_upstream(c, module, modules_dir, test_dir, fixtures_dir, verbose):
    if len(module) == 1 and module[0] == 'all':
        modules = get_all_module_names()
    else:
        modules = [module_name(m) for m in module]

    for module in modules:
        deprecated = True if module.startswith('_') else False

        if not deprecated and not should_upstream_module(module):
            continue

        if deprecated and verbose:
            print("Warning: Upstreaming deprecated module: {0}".format(module))
        if verbose:
            print("Upstreaming {0}".format(module))

        if os.path.exists('{0}/library/modules/{1}.py'.format(BASE_DIR, module)):
            # - upstream module file
            cmd = [
                'cp', '{0}/library/modules/{1}.py'.format(BASE_DIR, module),
                '{0}/{1}.py'.format(modules_dir, module)
            ]
            c.run(' '.join(cmd))

        if os.path.exists('{0}/test/unit/modules/network/f5/test_{1}.py'.format(
                BASE_DIR, module.lstrip('_'))) and not deprecated:
            # - upstream unit test file for non deprecated modules
            cmd = [
                'cp', '{0}/test/unit/modules/network/f5/test_{1}.py'.format(BASE_DIR, module.lstrip('_')),
                '{0}/test_{1}.py'.format(test_dir, module.lstrip('_'))
            ]
            c.run(' '.join(cmd))

        # - upstream unit test fixtures
        if not deprecated:
            fixtures = get_fixtures(c, module)
            for fixture in fixtures:
                cmd = [
                    'cp', '{0}/test/unit/modules/network/f5/fixtures/{1}'.format(BASE_DIR, fixture),
                    '{0}/{1}'.format(fixtures_dir, fixture)
                ]
                c.run(' '.join(cmd))

        if not should_upstream_module(module) and verbose:
            print("This module {0} is not marked for upstreaming in the YAML playbook metadata.".format(module))
        if verbose:
            print("Copy of {0} complete.".format(module))


@task(iterable=['module'], optional=['collection', 'verbose'], help=HELP1)
def upstream(c, module, collection='f5_modules', verbose=False):
    """Copy specified module and its dependencies to the local/ansible_collections/f5networks/collection_name directory.
    """
    coll_dest = '{0}/local/ansible_collections/f5networks/{1}'.format(BASE_DIR, collection)
    dst_test = '{0}/local/ansible_collections/f5networks/{1}/tests/unit/modules/network/f5/'.format(BASE_DIR, collection)
    dst_fixture = '{0}/local/ansible_collections/f5networks/{1}/tests/unit/modules/network/f5/fixtures/'.format(BASE_DIR, collection)
    dst_module = '{0}/local/ansible_collections/f5networks/{1}/plugins/modules/'.format(BASE_DIR, collection)

    src_module = '{0}/library/modules/'.format(BASE_DIR)

    purge_upstreamed_module_files(c, coll_dest, dst_module, dst_test, verbose)
    create_directories(c, coll_dest, dst_module, dst_test, dst_fixture, verbose)
    files_upstream(c, module, dst_module, dst_test, dst_fixture, verbose)

    retries = 1
    while not cmp_dir(src_module, dst_module):
        print("Retry file upstreaming, attempt {0} of 3".format(retries))
        purge_upstreamed_module_files(c, coll_dest, dst_module, dst_test, verbose)
        create_directories(c, coll_dest, dst_module, dst_test, dst_fixture, verbose)
        files_upstream(c, module, dst_module, dst_test, dst_fixture, verbose)

        retries = retries + 1

        if retries > 3:
            raise Exit('Failed to upstream modules, exiting.')

    copy_ignore_files(c)
    print("Module files upstreamed successfully.")
