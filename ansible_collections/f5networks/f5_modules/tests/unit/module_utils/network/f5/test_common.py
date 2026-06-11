from __future__ import absolute_import, division, print_function

import sys
from unittest.mock import MagicMock

import pytest

# Mock heavy dependencies so we can import common.py without ansible/netcommon installed
for mod_name in [
    'ansible', 'ansible.module_utils', 'ansible.module_utils._text',
    'ansible.module_utils.connection', 'ansible.module_utils.basic',
    'ansible.module_utils.six', 'ansible.module_utils.parsing',
    'ansible.module_utils.parsing.convert_bool',
    'ansible_collections.ansible',
    'ansible_collections.ansible.netcommon',
    'ansible_collections.ansible.netcommon.plugins',
    'ansible_collections.ansible.netcommon.plugins.module_utils',
    'ansible_collections.ansible.netcommon.plugins.module_utils.network',
    'ansible_collections.ansible.netcommon.plugins.module_utils.network.common',
    'ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config',
    'ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils',
    'ansible_collections.f5networks.f5_modules.plugins.module_utils.constants',
]:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MagicMock()

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
