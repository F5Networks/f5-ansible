#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import sys


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
