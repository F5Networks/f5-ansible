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

from .lib.upstream import module_name
from .lib.upstream import get_fixtures

from .lib.stubber import HAS_JINJA
from .lib.stubber import stub_roles_dirs
from .lib.stubber import stub_roles_yaml_files
from .lib.stubber import stub_playbook_file
from .lib.stubber import stub_library_file
from .lib.stubber import stub_module_documentation
from .lib.stubber import stub_unit_test_file

from .lib.stubber import unstub_roles_dirs
from .lib.stubber import unstub_playbook_file
from .lib.stubber import unstub_library_file
from .lib.stubber import unstub_module_documentation
from .lib.stubber import unstub_unit_test_file

from invoke import task


@task
def stub(c, module=None):
    """Create module stubs

    This command can be used to create the stub files necessary to start
    work on a new module.
    """
    if not HAS_JINJA:
        click.echo("The jinja library is required", err=True)
        sys.exit(1)
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    stub_roles_dirs(module)
    stub_roles_yaml_files(module)
    stub_playbook_file(module)
    stub_library_file(module, extension)
    stub_module_documentation(module)
    stub_unit_test_file(module, extension)


@task
def unstub(c, module=None):
    """Remove module stubs

    This command can be used to remove the stub files created by the stub process.
    """
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    unstub_roles_dirs(module)
    unstub_playbook_file(module)
    unstub_library_file(module, extension)
    unstub_module_documentation(module)
    unstub_unit_test_file(module, extension)


@task
def upstream(c, module):
    module = module_name(module)
    root_dest = '{0}/local/ansible/'.format(BASE_DIR)
    if not os.path.exists(root_dest):
        print("The specified upstream directory does not exist")
        sys.exit(1)

    # Handle deprecated modules
    if module.startswith('_'):
        module = module[1:]

    # - upstream unit test file
    cmd = [
        'cp', '{0}/test/unit/test_{1}.py'.format(BASE_DIR, module),
        '{0}/local/ansible/test/units/modules/network/f5/test_{1}.py'.format(BASE_DIR, module)
    ]
    c.run(' '.join(cmd))

    # - upstream unit test fixtures
    fixtures = get_fixtures(c, module)
    for fixture in fixtures:
        cmd = [
            'cp', '{0}/test/unit/fixtures/{1}'.format(BASE_DIR, fixture),
            '{0}/local/ansible/test/units/modules/network/f5/fixtures/{1}'.format(BASE_DIR, fixture)
        ]
        c.run(' '.join(cmd))

    # - upstream module file
    cmd = [
        'cp', '{0}/library/modules/{1}.py'.format(BASE_DIR, module),
        '{0}/local/ansible/lib/ansible/modules/network/f5/{1}.py'.format(BASE_DIR, module)
    ]
    c.run(' '.join(cmd))

    print("Copy complete")
