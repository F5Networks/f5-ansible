# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

import pytest

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible_collections.f5networks.f5_modules.plugins.module_utils.common import is_valid_fqdn


class TestIsValidFqdn:
    """Tests for is_valid_fqdn covering normal, underscore, wildcard, and invalid inputs."""

    def test_standard_fqdn(self):
        assert is_valid_fqdn("www.example.com") is True

    def test_subdomain_fqdn(self):
        assert is_valid_fqdn("host.sub.example.com") is True

    def test_trailing_dot(self):
        assert is_valid_fqdn("www.example.com.") is True

    def test_underscore_srv_record(self):
        assert is_valid_fqdn("_sip._tcp.example.com") is True

    def test_underscore_in_label(self):
        assert is_valid_fqdn("my_host.example.com") is True

    def test_wildcard_fqdn(self):
        assert is_valid_fqdn("*.example.com") is True

    def test_single_label_not_fqdn(self):
        assert is_valid_fqdn("localhost") is False

    def test_empty_string(self):
        assert is_valid_fqdn("") is False

    def test_too_long(self):
        # 256 characters exceeds the 255 max
        long_host = "a" * 63 + "." + "b" * 63 + "." + "c" * 63 + "." + "d" * 63 + ".e"
        assert is_valid_fqdn(long_host) is False

    def test_label_too_long(self):
        # A single label exceeding 63 characters
        assert is_valid_fqdn("a" * 64 + ".example.com") is False

    def test_hyphen_at_start_of_label(self):
        assert is_valid_fqdn("-host.example.com") is False

    def test_hyphen_at_end_of_label(self):
        assert is_valid_fqdn("host-.example.com") is False

    def test_hyphen_in_middle(self):
        assert is_valid_fqdn("my-host.example.com") is True

    def test_numeric_labels(self):
        assert is_valid_fqdn("123.456.789.com") is True

    def test_invalid_characters(self):
        assert is_valid_fqdn("host!name.example.com") is False
