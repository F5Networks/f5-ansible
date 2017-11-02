#!/usr/bin/env python

def stub(module):
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    stub_roles_dirs(module)
    stub_roles_yaml_files(module)
    stub_playbook_file(module)
    stub_library_file(module, extension)
    stub_module_documentation(module)
    stub_unit_test_file(module, extension)


def unstub(module):
    module, extension = os.path.splitext(module)
    extension = extension + '.py' if extension == '' else extension
    unstub_roles_dirs(module)
    unstub_playbook_file(module)
    unstub_library_file(module, extension)
    unstub_module_documentation(module)
    unstub_unit_test_file(module, extension)


def rename(from_module, to_module):
    from_module, from_extension = os.path.splitext(from_module)
    from_extension = from_extension + '.py' if from_extension == '' else from_extension
    to_module, to_extension = os.path.splitext(to_module)
    to_extension = to_extension + '.py' if to_extension == '' else to_extension

    rename_roles_dir(from_module, to_module)
    rename_playbook_file(from_module, to_module)

    unstub_roles_dirs(from_module)
    unstub_playbook_file(from_module)
    unstub_library_file(from_module, from_extension)
    unstub_module_documentation(from_module)
    unstub_unit_test_file(from_module, from_extension)


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Manages module related stubs')
    parser.add_argument('action', choices=('stub', 'unstub', 'rename'),
                        default='stub',
                        help='How to manage stubbed files for a module (default: stub)')
    parser.add_argument('--module',
                        action='store',
                        help='Module to use for stubbing',
                        required=True)
    parser.add_argument('--to-module',
                        action='store',
                        help='When renaming, rename to this module',
                        required=False)
    return parser.parse_args()


def main():
    args = parse_args()

    if args.action == 'stub':
        stub(args.module)
    else:
        unstub(args.module)


if __name__ == '__main__':
    import argparse
    import os
    import sys

    if __package__ is None:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from lib.stubber import stub_roles_dirs
        from lib.stubber import stub_roles_yaml_files
        from lib.stubber import stub_playbook_file
        from lib.stubber import stub_library_file
        from lib.stubber import stub_module_documentation
        from lib.stubber import stub_unit_test_file
        from lib.stubber import unstub_roles_dirs
        from lib.stubber import unstub_playbook_file
        from lib.stubber import unstub_library_file
        from lib.stubber import unstub_module_documentation
        from lib.stubber import unstub_unit_test_file
    else:
        from ..lib.stubber import stub_roles_dirs
        from ..lib.stubber import stub_roles_yaml_files
        from ..lib.stubber import stub_playbook_file
        from ..lib.stubber import stub_library_file
        from ..lib.stubber import stub_module_documentation
        from ..lib.stubber import stub_unit_test_file
        from ..lib.stubber import unstub_roles_dirs
        from ..lib.stubber import unstub_playbook_file
        from ..lib.stubber import unstub_library_file
        from ..lib.stubber import unstub_module_documentation
        from ..lib.stubber import unstub_unit_test_file
    main()
