#!/usr/bin/env python

import argparse
import os


from lib.stubber import stub_roles_dirs
from lib.stubber import stub_roles_yaml_files
from lib.stubber import stub_playbook_file
from lib.stubber import stub_library_file
from lib.stubber import stub_module_documentation
from lib.stubber import stub_unit_test_file
#from lib.stubber import restub_test_automation

from lib.stubber import unstub_roles_dirs
from lib.stubber import unstub_playbook_file
from lib.stubber import unstub_library_file
from lib.stubber import unstub_module_documentation
from lib.stubber import unstub_unit_test_file


def stub(module):
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    stub_roles_dirs(module)
    stub_roles_yaml_files(module)
    stub_playbook_file(module)
    stub_library_file(module, extension)
    stub_module_documentation(module)
    stub_unit_test_file(module, extension)
    #restub_test_automation()


def unstub(module):
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    unstub_roles_dirs(module)
    unstub_playbook_file(module)
    unstub_library_file(module, extension)
    unstub_module_documentation(module)
    unstub_unit_test_file(module, extension)
    #restub_test_automation()


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Manages module related stubs')
    parser.add_argument('action', choices=('stub', 'unstub'),
                        default='stub',
                        help='How to manage stubbed files for a module (default: stub)')
    parser.add_argument('--module',
                        action='store',
                        help='Module to use for stubbing',
                        required=True)
    return parser.parse_args()


def main():
    args = parse_args()

    if args.action == 'stub':
        stub(args.module)
    else:
        unstub(args.module)


if __name__ == '__main__':
    main()
