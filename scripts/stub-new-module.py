#!/usr/bin/env python

import fire
import os
import shutil
from jinja2 import Environment, FileSystemLoader


class ModuleStubber(object):
    def __init__(self):
        self._file_path = os.path.realpath(__file__)
        self._top_level = os.path.dirname(os.path.dirname(self._file_path))
        self._module = None
        self.env = Environment(
            loader=FileSystemLoader([
                os.path.join(os.path.dirname(__file__),'stubs')
            ])
        )

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
        for file in ['setup.yaml', 'teardown.yaml']:
            defaults_file = '{0}/test/integration/targets/{1}/tasks/{2}'.format(
                self._top_level, self._module, file
            )
            self.__touch(defaults_file)
        main_tests = '{0}/test/integration/targets/{1}/tasks/main.yaml'.format(
            self._top_level, self._module
        )
        with open(main_tests, 'w') as fh:
            fh.write("---\n\n")
            fh.write("- include: setup.yaml\n\n")
            fh.write("# tests go here\n\n")
            fh.write("- include: teardown.yaml")

    def __stub_playbook_file(self):
        # Stub out the test playbook
        playbook_file = '{0}/test/integration/{1}.yaml'.format(
            self._top_level, self._module
        )

        template = self.env.get_template('playbooks_module.yaml')
        content = template.render(module=self._module)

        fh = open(playbook_file, 'w')
        fh.write(content)
        fh.close()

    def __stub_library_file(self):
        # Create your new module python file
        library_file = '{0}/library/{1}{2}'.format(
            self._top_level, self._module, self._extension
        )

        template = self.env.get_template('library_module.py')
        content = template.render(module=self._module)

        fh = open(library_file, 'w')
        fh.write(content)
        fh.close()

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

        template = self.env.get_template('tests_unit_module.py')
        content = template.render(module=self._module)

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
        else:
            test_dir = 'misc'
        return test_dir


def main():
    fire.Fire(ModuleStubber)

if __name__ == '__main__':
    main()
