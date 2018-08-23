#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from invoke import Collection

from . import container
from . import docs
from . import ip
from . import module
from . import module_utils
from . import test

ns = Collection(
    container,
    docs,
    ip,
    module,
    module_utils,
    test,
)
