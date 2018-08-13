#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import shutil

from .common import BASE_DIR

try:
    from jinja2 import Environment
    from jinja2 import FileSystemLoader
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False

if HAS_JINJA:
    JINJA_ENV = Environment(
        loader=FileSystemLoader(BASE_DIR + '/devtools/stubs')
    )


def module_file_present(module):
    module_file = '{0}/library/modules/{1}.py'.format(BASE_DIR, module)
    if os.path.exists(module_file):
        print('Module file "{0}" exists'.format(module_file))
        return True
    return False


def module_file_absent(module):
    result = module_file_present(module)
    return not result


def stub_roles_dirs(module):
    # Create role containing all of your future functional tests
    for d in ['defaults', 'tasks']:
        directory = '{0}/test/integration/targets/{1}/{2}'.format(BASE_DIR, module, d)
        if not os.path.exists(directory):
            os.makedirs(directory)


def stub_roles_yaml_files(module):
    # Create default vars to contain any playbook variables
    for dir in ['defaults', 'tasks']:
        defaults_file = '{0}/test/integration/targets/{1}/{2}/main.yaml'.format(
            BASE_DIR, module, dir
        )
        touch(defaults_file)
    for f in ['setup.yaml', 'teardown.yaml']:
        defaults_file = '{0}/test/integration/targets/{1}/tasks/{2}'.format(BASE_DIR, module, f)
        touch(defaults_file)
    main_tests = '{0}/test/integration/targets/{1}/tasks/main.yaml'.format(BASE_DIR, module)

    template = JINJA_ENV.get_template('test_integration_targets_main.yaml')
    content = template.render()

    with open(main_tests, 'w') as fh:
        fh.write(content)


def stub_playbook_file(module):
    # Stub out the test playbook
    playbook_file = '{0}/test/integration/{1}.yaml'.format(BASE_DIR, module)

    template = JINJA_ENV.get_template('playbooks_module.yaml')
    content = template.render(module=module)

    fh = open(playbook_file, 'w')
    fh.write(content)
    fh.close()


def stub_library_file(module, extension):
    # Create your new module python file
    library_file = '{0}/library/modules/{1}{2}'.format(BASE_DIR, module, extension)

    template = JINJA_ENV.get_template('library_module.py')
    content = template.render(module=module)

    fh = open(library_file, 'w')
    fh.write(content)
    fh.close()


def stub_module_documentation(module):
    # Create the documentation link for your module
    documentation_file = '{0}/docs/modules/{1}.rst'.format(BASE_DIR, module)
    touch(documentation_file)


def touch(name, times=None):
    with open(name, 'a'):
        os.utime(name, times)


def stub_unit_test_file(module, extension):
    test_dir_path = '{0}/test/unit/'.format(BASE_DIR)
    if not os.path.exists(test_dir_path):
        os.makedirs(test_dir_path)
    test_file = '{0}/test/unit/test_{1}{2}'.format(
        BASE_DIR, module, extension
    )

    template = JINJA_ENV.get_template('tests_unit_module.py')
    content = template.render(module=module)

    fh = open(test_file, 'w')
    fh.write(content)
    fh.close()


def unstub_roles_dirs(module):
    for dir in ['defaults', 'tasks']:
        directory = '{0}/test/integration/targets/{1}/{2}'.format(BASE_DIR, module, dir)
        if os.path.exists(directory):
            shutil.rmtree(directory)


def unstub_playbook_file(module):
    playbook_file = '{0}/test/integration/{1}.yaml'.format(BASE_DIR, module)
    if os.path.exists(playbook_file):
        os.remove(playbook_file)


def unstub_library_file(module, extension):
    library_file = '{0}/library/modules/{1}{2}'.format(BASE_DIR, module, extension)
    if os.path.exists(library_file):
        os.remove(library_file)


def unstub_module_documentation(module):
    documentation_file = '{0}/docs/modules/{1}.rst'.format(BASE_DIR, module)
    if os.path.exists(documentation_file):
        os.remove(documentation_file)


def unstub_unit_test_file(module, extension):
    test_dir_path = '{0}/test/unit/'.format(BASE_DIR)
    if not os.path.exists(test_dir_path):
        os.makedirs(test_dir_path)
    test_file = '{0}/test/unit/test_{1}{2}'.format(
        BASE_DIR, module, extension
    )
    if os.path.exists(test_file):
        os.remove(test_file)
