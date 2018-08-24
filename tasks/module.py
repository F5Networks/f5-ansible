#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import hashlib
import os
import sys
import tarfile
import yaml

from .lib.common import BASE_DIR

from .lib.upstream import module_name
from .lib.upstream import get_fixtures
from .lib.upstream import get_all_module_names
from .lib.upstream import should_upstream_module

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
    root_dest = '{0}/local/ansible/'.format(BASE_DIR)
    if not os.path.exists(root_dest):
        print("The specified upstream directory does not exist")
        sys.exit(1)

    if module == 'all':
        modules = get_all_module_names()
    else:
        modules = [module_name(module)]

    for module in modules:
        deprecated = True if module.startswith('_') else False

        # Handle deprecated modules
        if module.startswith('_'):
            module = module[1:]

        if not deprecated and not should_upstream_module(module):
            continue

        print("Upstreaming {0}".format(module))
        if os.path.exists('{0}/test/unit/test_{1}.py'.format(BASE_DIR, module)):
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

        if os.path.exists('{0}/library/modules/{1}.py'.format(BASE_DIR, module)):
            # - upstream module file
            cmd = [
                'cp', '{0}/library/modules/{1}.py'.format(BASE_DIR, module),
                '{0}/local/ansible/lib/ansible/modules/network/f5/{1}.py'.format(BASE_DIR, module)
            ]
            c.run(' '.join(cmd))

    print("Copy complete")


@task
def md5_update(c, branch=None):
    branches = [
        '2.4.0.0',
        '2.4.1.0',
        '2.4.2.0',
        '2.4.3.0',
        '2.4.4.0',
        '2.4.5.0',
        '2.4.6.0',
        '2.5.0',
        '2.5.1',
        '2.5.2',
        '2.5.3',
        '2.5.4',
        '2.5.5',
        '2.5.6',
        '2.5.7',
        '2.5.8',
        '2.6.0',
        '2.6.1',
        '2.6.2',
        '2.6.3',
    ]

    work_dir = '{0}/tmp/ansible-hashes'.format(BASE_DIR)
    c.run('mkdir -p {0}'.format(work_dir))
    results = dict()
    with c.cd(work_dir):
        for branch in branches:
            c.run('pip download --exists-action=i --no-deps --no-binary --progress-bar=off ansible=={0}'.format(branch))
            tar = tarfile.open("{0}/ansible-{1}.tar.gz".format(work_dir, branch), "r:gz")
            results[branch] = []
            for member in tar.getmembers():
                if 'lib/ansible/modules/network/f5/' not in member.name:
                    continue
                if member.name.endswith('__init__.py'):
                    continue
                if 'iworkflow' in member.name:
                    continue

                hash_md5 = hashlib.md5()
                f = tar.extractfile(member)
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                results[branch].append(dict(
                    name=os.path.basename(member.name),
                    hash=hash_md5.hexdigest())
                )
            tar.close()
        with open('{0}/docs/data/hashes.yaml'.format(BASE_DIR), 'w') as outfile:
            yaml.dump(results, outfile, default_flow_style=False)
