#!/usr/bin/env python

import fire
import os
import shutil


class ModuleStubber(object):
    def __init__(self):
        self._file_path = os.path.realpath(__file__)
        self._top_level = os.path.dirname(os.path.dirname(self._file_path))
        self._module = None

    def stub(self, module):
        self._module, self._extension = os.path.splitext(module)
        if self._extension == '':
            self._extension = '.py'
        self.__stub_roles_dirs()
        self.__stub_roles_yaml_files()
        self.__stub_playbook_file()
        self.__stub_library_file()
        self.__stub_module_documentation()
        self.__stub_unit_test_file()

    def unstub(self, module):
        self._module, self._extension = os.path.splitext(module)
        if self._extension == '':
            self._extension = '.py'
        try:
            for dir in ['defaults', 'tasks']:
                directory = '{0}/test/integration/targets/{1}/{2}'.format(
                    self._top_level, self._module, dir
                )
                shutil.rmtree(directory)
        except Exception:
            pass

        try:
            playbook_file = '{0}/test/integration/{1}.yaml'.format(
                self._top_level, self._module
            )
            os.remove(playbook_file)
        except Exception:
            pass

        try:
            library_file = '{0}/library/{1}{2}'.format(
                self._top_level, self._module, self._extension
            )
            os.remove(library_file)
        except Exception:
            pass

        try:
            documentation_file = '{0}/docs/modules/{1}.rst'.format(
                self._top_level, self._module
            )
            os.remove(documentation_file)
        except Exception:
            pass

        try:
            test_dir = self.__get_test_dir()
            test_file = '{0}/test/unit/{1}/test_{2}{3}'.format(
                self._top_level, test_dir, self._module, self._extension
            )
            os.remove(test_file)
        except Exception:
            pass

    def __stub_roles_dirs(self):
        # Create role containing all of your future functional tests
        for dir in ['defaults', 'tasks']:
            directory = '{0}/test/integration/targets/{1}/{2}'.format(
                self._top_level, self._module, dir
            )
            if not os.path.exists(directory):
                os.makedirs(directory)

    def __stub_roles_yaml_files(self):
        # Create default vars to contain any playbook variables
        for dir in ['defaults', 'tasks']:
            defaults_file = '{0}/test/integration/targets/{1}/{2}/main.yaml'.format(
                self._top_level, self._module, dir
            )
            self.__touch(defaults_file)

    def __stub_playbook_file(self):
        # Stub out the test playbook
        playbook_file = '{0}/test/integration/{1}.yaml'.format(
            self._top_level, self._module
        )

        playbook_content = """---

# Test the {module} module
#
# Running this playbook assumes that you have a BIG-IP installation at the
# ready to receive the commands issued in this Playbook.
#
# This module will run tests against a BIG-IP host to verify that the
# {module} module behaves as expected.
#
# Usage:
#
#    ansible-playbook -i notahost, test/integration/{module}.yaml
#
# Examples:
#
#    Run all tests on the {module} module
#
#    ansible-playbook -i notahost, test/integration/{module}.yaml
#
# Tested platforms:
#
#    - NA
#

- name: Test the {module} module
  hosts: "f5-test[0]"
  connection: local

  environment:
      F5_SERVER: "{{{{ inventory_hostname }}}}"
      F5_USER: "{{{{ bigip_username }}}}"
      F5_PASSWORD: "{{{{ bigip_password }}}}"
      F5_SERVER_PORT: "{{{{ bigip_port }}}}"
      F5_VALIDATE_CERTS: "{{{{ validate_certs }}}}"

  roles:
      - {module}
""".format(module=self._module)

        fh = open(playbook_file, 'w')
        fh.write(playbook_content)
        fh.close()

    def __stub_library_file(self):
        # Create your new module python file
        library_file = '{0}/library/{1}{2}'.format(
            self._top_level, self._module, self._extension
        )
        self.__touch(library_file)

    def __stub_module_documentation(self):
        # Create the documentation link for your module
        documentation_file = '{0}/docs/modules/{1}.rst'.format(
            self._top_level, self._module
        )
        self.__touch(documentation_file)

    def __touch(self, fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    def __stub_unit_test_file(self):
        test_dir = self.__get_test_dir()

        test_dir_path = '{0}/test/unit/{1}'.format(
            self._top_level, test_dir
        )
        if not os.path.exists(test_dir_path):
            os.makedirs(test_dir_path)
        test_file = '{0}/test/unit/{1}/test_{2}{3}'.format(
            self._top_level, test_dir, self._module, self._extension
        )

        content = """---

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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client
from ansible.module_utils.f5_utils import F5ModuleError

try:
    raise Exception('You must write your own local includes. See examples, then remove this exception')
    # from library.bigip_pool import Parameters
    # from library.bigip_pool import ModuleManager
    # from library.bigip_pool import ArgumentSpec
except ImportError:
    try:
        raise Exception('You must write your own upstream includes. See examples, then remove this exception')
        # from ansible.modules.network.f5.bigip_pool import Parameters
        # from ansible.modules.network.f5.bigip_pool import ModuleManager
        # from ansible.modules.network.f5.bigip_pool import ArgumentSpec
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        raise Exception('You must write your own module param test. See examples, then remove this exception')
        # args = dict(
        #     monitor_type='m_of_n',
        #     host='192.168.1.1',
        #     port=8080
        # )
        # 
        # p = Parameters(args)
        # assert p.monitor == 'min 1 of'
        # assert p.host == '192.168.1.1'
        # assert p.port == 8080

    def test_api_parameters(self):
        raise Exception('You must write your own API param test. See examples, then remove this exception')
        # args = dict(
        #     monitor_type='and_list',
        #     slowRampTime=200,
        #     reselectTries=5,
        #     serviceDownAction='drop'
        # )
        # 
        # p = Parameters(args)
        # assert p.slow_ramp_time == 200
        # assert p.reselect_tries == 5
        # assert p.service_down_action == 'drop'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def test_create(self, *args):
        raise Exception('Must write a creation test')

""".format(module=self._module)

        fh = open(test_file, 'w')
        fh.write(content)
        fh.close()

    def __get_test_dir(self):
        if self._module.startswith('bigip'):
            test_dir = 'bigip'
        elif self._module.startswith('iworkflow'):
            test_dir = 'iworkflow'
        elif self._module.startswith('bigiq'):
            test_dir = 'bigiq'
        elif self._module.startswith('wait'):
            test_dir = 'bigip'
        elif self._module.startswith('f5'):
            test_dir = 'f5'
        return test_dir


def main():
    fire.Fire(ModuleStubber)

if __name__ == '__main__':
    main()
