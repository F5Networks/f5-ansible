#!/usr/bin/env python
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import sys
import yaml
import importlib

from os.path import dirname

found = []
no_docs = []
tld = dirname(dirname(dirname(dirname(os.path.realpath(__file__)))))
sys.path.append(tld)

for file in os.listdir(tld + '/library'):
    if file in ['__init__.py']:
        continue
    elif not file.endswith('.py'):
        continue
    importable = 'library.{0}'.format(os.path.splitext(file)[0])

    # Syntax errors can occur here, but I let them bubble up and stop the script
    # because their error messages provide sufficient information to debug the problem
    # and fix it.
    module = importlib.import_module(importable)

    try:
        documentation = yaml.load(module.DOCUMENTATION)
    except AttributeError:
        no_docs.append(file)
        continue

    if documentation['short_description'].endswith('.'):
        found.append(file)

if no_docs:
    for f in no_docs:
        print("No DOCUMENTATION variable was found in {0}".format(f))
if found:
    for f in found:
        print(
            "Trailing period found in short_description of DOCUMENTATION variable in {0}".format(f)
        )
    sys.exit(1)
