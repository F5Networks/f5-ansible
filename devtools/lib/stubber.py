#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public Liccense for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
from jinja2 import Environment, FileSystemLoader
from os.path import isfile, join

FILE_PATH = os.path.realpath(__file__)
TOP_LEVEL = os.path.dirname(os.path.dirname(os.path.dirname(FILE_PATH)))
JINJA_ENV = Environment(
    loader=FileSystemLoader([
        os.path.join(os.path.dirname(os.path.dirname(__file__)),'stubs')
    ])
)


def stub_roles_dirs(module):
    # Create role containing all of your future functional tests
    for dir in ['defaults', 'tasks']:
        directory = '{0}/test/integration/targets/{1}/{2}'.format(TOP_LEVEL, module, dir)
        if not os.path.exists(directory):
            os.makedirs(directory)


def stub_roles_yaml_files(module):
    # Create default vars to contain any playbook variables
    for dir in ['defaults', 'tasks']:
        defaults_file = '{0}/test/integration/targets/{1}/{2}/main.yaml'.format(TOP_LEVEL, module, dir)
        touch(defaults_file)
    for file in ['setup.yaml', 'teardown.yaml']:
        defaults_file = '{0}/test/integration/targets/{1}/tasks/{2}'.format(TOP_LEVEL, module, file)
        touch(defaults_file)
    main_tests = '{0}/test/integration/targets/{1}/tasks/main.yaml'.format(TOP_LEVEL, module)

    template = JINJA_ENV.get_template('test_integration_targets_main.yaml')
    content = template.render()

    with open(main_tests, 'w') as fh:
        fh.write(content)


def stub_playbook_file(module):
    # Stub out the test playbook
    playbook_file = '{0}/test/integration/{1}.yaml'.format(TOP_LEVEL, module)

    template = JINJA_ENV.get_template('playbooks_module.yaml')
    content = template.render(module=module)

    fh = open(playbook_file, 'w')
    fh.write(content)
    fh.close()


def stub_library_file(module, extension):
    # Create your new module python file
    library_file = '{0}/library/{1}{2}'.format(TOP_LEVEL, module, extension)

    template = JINJA_ENV.get_template('library_module.py')
    content = template.render(module=module)

    fh = open(library_file, 'w')
    fh.write(content)
    fh.close()


def stub_module_documentation(module):
    # Create the documentation link for your module
    documentation_file = '{0}/docs/modules/{1}.rst'.format(TOP_LEVEL, module)
    touch(documentation_file)


#def restub_test_automation():
#    dest = "{0}/test/runner/jenkins-jobs/ci.f5.f5-ansible-run-one.groovy".format(TOP_LEVEL)
#    library = "{0}/library".format(TOP_LEVEL)
#    with open(dest, "r") as fh:
#        content = fh.readlines()
#    start = content.index("modules = [\n") + 1
#    end = content.index("]\n", start)
#    content[start:end] = []
#    files = [f for f in os.listdir(library) if isfile(join(library, f))]
#    files = [f for f in files if not f.startswith('_')]
#    for l in reversed(files):
#        content.insert(start, "    '{0}',\n".format(l))
#    with open(dest, "w") as fh:
#        to_write = "".join(content)
#        fh.write(to_write)


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def stub_unit_test_file(module, extension):
    test_dir = get_test_dir(module)

    test_dir_path = '{0}/test/unit/{1}'.format(TOP_LEVEL, test_dir)
    if not os.path.exists(test_dir_path):
        os.makedirs(test_dir_path)
    test_file = '{0}/test/unit/{1}/test_{2}{3}'.format(
        TOP_LEVEL, test_dir, module, extension
    )

    template = JINJA_ENV.get_template('tests_unit_module.py')
    content = template.render(module=module)

    fh = open(test_file, 'w')
    fh.write(content)
    fh.close()


def get_test_dir(module):
    if module.startswith('bigip'):
        test_dir = 'bigip'
    elif module.startswith('iworkflow'):
        test_dir = 'iworkflow'
    elif module.startswith('bigiq'):
        test_dir = 'bigiq'
    elif module.startswith('wait'):
        test_dir = 'bigip'
    elif module.startswith('f5'):
        test_dir = 'f5'
    else:
        test_dir = 'misc'
    return test_dir


def unstub_roles_dirs(module):
    for dir in ['defaults', 'tasks']:
        directory = '{0}/test/integration/targets/{1}/{2}'.format(TOP_LEVEL, module, dir)
        if os.path.exists(directory):
            shutil.rmtree(directory)


def unstub_playbook_file(module):
    playbook_file = '{0}/test/integration/{1}.yaml'.format(TOP_LEVEL, module)
    if os.path.exists(playbook_file):
        os.remove(playbook_file)


def unstub_library_file(module, extension):
    library_file = '{0}/library/{1}{2}'.format(TOP_LEVEL, module, extension)
    if os.path.exists(library_file):
        os.remove(library_file)


def unstub_module_documentation(module):
    documentation_file = '{0}/docs/modules/{1}.rst'.format(TOP_LEVEL, module)
    if os.path.exists(documentation_file):
        os.remove(documentation_file)


def unstub_unit_test_file(module, extension):
    test_dir = get_test_dir(module)

    test_dir_path = '{0}/test/unit/{1}'.format(TOP_LEVEL, test_dir)
    if not os.path.exists(test_dir_path):
        os.makedirs(test_dir_path)
    test_file = '{0}/test/unit/{1}/test_{2}{3}'.format(
        TOP_LEVEL, test_dir, module, extension
    )
    if os.path.exists(test_file):
        os.remove(test_file)
