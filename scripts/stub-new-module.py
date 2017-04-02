#!/usr/bin/env python

import fire
import os

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
  hosts: f5-test
  connection: local

  environment:
      F5_SERVER: "{{ inventory_hostname }}"
      F5_USER: "{{ bigip_username }}"
      F5_PASSWORD: "{{ bigip_password }}"
      F5_SERVER_PORT: "{{ bigip_port }}"
      F5_VALIDATE_CERTS: "{{ validate_certs }}"

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
        if self._module.startswith('bigip'):
            test_dir = 'bigip'
        elif self._module.startswith('iworkflow'):
            test_dir = 'iworkflow'
        elif self._module.startswith('bigiq'):
            test_dir = 'bigiq'
        elif self._module.startswith('wait'):
            test_dir = 'bigip'

        test_dir_path = '{0}/test/unit/{1}'.format(
            self._top_level, test_dir
        )
        if not os.path.exists(test_dir_path):
            os.makedirs(test_dir_path)
        test_file = '{0}/test/unit/{1}/test_{2}{3}'.format(
            self._top_level, test_dir, self._module, self._extension
        )
        self.__touch(test_file)


def main():
    fire.Fire(ModuleStubber)

if __name__ == '__main__':
    main()
