#!/usr/bin/env python

import json
import os
import os.path
import re
import sys
from collections import defaultdict
from distutils.command.build_scripts import build_scripts as BuildScripts
from distutils.command.sdist import sdist as SDist

try:
    from setuptools import setup, find_packages
    from setuptools.command.build_py import build_py as BuildPy
    from setuptools.command.install_lib import install_lib as InstallLib
    from setuptools.command.install_scripts import install_scripts as InstallScripts
except ImportError:
    print("Ansible now needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

sys.path.insert(0, os.path.abspath('library'))

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
    if not install_requirements:
        print("Unable to read requirements from the requirements.txt file"
              "That indicates this copy of the source code is incomplete.")
        sys.exit(2)

setup(
    name='f5-ansible',
    version='2.6',
    description='F5 Modules for Ansible',
    long_description='F5 Modules for Ansible',
    author='Tim Rupp',
    license='GPLv3',
    author_email='solutionsfeedback@f5.com',
    url='https://github.com/F5Networks/f5-ansible',
    install_requires=install_requirements,
    package_dir={'': 'library'},
    packages=find_packages('library'),

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    data_files=[],
    zip_safe=False
)
