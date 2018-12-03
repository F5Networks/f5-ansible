# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")


try:
    from library.module_utils.network.f5.common import transform_name

    # In Ansible 2.8, Ansible changed import paths.
    from test.units.compat import unittest
except ImportError:
    from ansible.module_utils.network.f5.common import transform_name

    # Ansible 2.8 imports
    from units.compat import unittest


class TestModuleUtils(unittest.TestCase):
    def test_transform_name_1(self):
        # A simple partition and a simple name
        #
        # This is the most likely scenario in the module code.
        # The partition has no special characters that need to be
        # replaced and neither does the name
        #
        assert transform_name('Common', 'foo') == '~Common~foo'

    def test_transform_name_2(self):
        # Test partition with leading slash
        #
        # There are cases where people may think that a leading slash
        # is required when specifying the partition. This is not the
        # case, and therefore, we need to make sure it is properly
        # squashed so that calls to specific ``*_on_device`` methods
        # will succeed.
        #
        assert transform_name('/Common', 'foo') == '~Common~foo'

    def test_transform_name_3(self):
        # Test the same partition being specified in the resource name
        #
        # This is a special case which can creep up when users translate
        # (literally) the names of items in a bigip.conf file into an
        # Ansible playbook.
        #
        # When the requested partition is part of the resource name, we
        # erase the partition from the resource name.
        assert transform_name('/Common', '/Common/foo') == '~Common~foo'

    def test_transform_name_4(self):
        # Test a resource name created by an iApp
        #
        # iApps are weird because they introduce a new feature called a
        # sub-path. This sub-path exists **between** the partition and
        # the resource name.
        assert transform_name('Common', 'foo', 'bar.app') == '~Common~bar.app~foo'

    def test_transform_name_5(self):
        # Test resource name that has special characters
        #
        # Because the partition is not in the name, replace the slashes
        # in the name accordingly instead of erasing the partition from
        # the name.
        assert transform_name('/Common', '/foo') == '~Common~~foo'

    def test_transform_name_6(self):
        # Test a resource name created by an iApp, with partition in name
        #
        # iApps are weird because they introduce a new feature called a
        # sub-path. This sub-path exists **between** the partition and
        # the resource name.
        assert transform_name('/Common', '/Common/foo', 'bar.app') == '~Common~bar.app~foo'

    def test_transform_name_7(self):
        # Test the same partition being specified in the resource name,
        # but without leading slash
        #
        assert transform_name('Common', '/Common/foo') == '~Common~foo'

    def test_transform_name_8(self):
        # Test a resource name created by an iApp, with partition in name
        # no leading slash in partition
        #
        # iApps are weird because they introduce a new feature called a
        # sub-path. This sub-path exists **between** the partition and
        # the resource name.
        assert transform_name('Common', '/Common/foo', 'bar.app') == '~Common~bar.app~foo'
