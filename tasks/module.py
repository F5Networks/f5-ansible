#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

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
