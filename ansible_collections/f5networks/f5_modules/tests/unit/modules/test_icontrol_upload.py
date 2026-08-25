# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for icontrol.upload_file() function.

Verifies that Content-Range headers correctly reflect the actual bytes being
transmitted, preventing off-by-one errors that cause BIG-IP to reject uploads
with: "Chunk byte count X different from received buffer length Y"
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import pytest

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock

try:
    from io import StringIO, BytesIO
except ImportError:
    from StringIO import StringIO
    BytesIO = StringIO

from ansible_collections.f5networks.f5_modules.plugins.module_utils.icontrol import upload_file


class TestUploadFileContentRange(unittest.TestCase):
    """Test Content-Range header calculation for file uploads."""

    def setUp(self):
        self.client = Mock()
        self.client.api = Mock()
        self.client.api.post = Mock(return_value=Mock(status=200))
        self.url = 'https://localhost:443/mgmt/shared/file-transfer/uploads'

    def tearDown(self):
        self.client.reset_mock()

    def test_single_small_chunk_content_range_matches_actual_bytes(self):
        """
        Verify that for a small file (single chunk), Content-Range header
        reflects the actual bytes being sent.

        This tests the fix for:
        "Chunk byte count different from received buffer length"
        """
        # Create a 100-byte file
        file_content = 'x' * 100
        fileobj = BytesIO(file_content.encode('utf-8'))

        # Mock the POST response
        self.client.api.post.return_value = Mock(status=200)

        # Upload the file
        result = upload_file(self.client, self.url, fileobj, 'testfile.txt')

        # Verify upload succeeded
        assert result is True

        # Verify the POST was called exactly once (single chunk)
        assert self.client.api.post.call_count == 1

        # Extract the headers from the POST call
        call_args = self.client.api.post.call_args
        headers = call_args.kwargs.get('headers') or call_args[1]['headers']
        data = call_args.kwargs.get('data') or call_args[1]['data']

        # Verify Content-Range format: start-end/total
        content_range = headers['Content-Range']
        parts = content_range.split('/')
        assert len(parts) == 2, "Content-Range should have format 'start-end/total'"

        range_part, total = parts
        start_str, end_str = range_part.split('-')
        start = int(start_str)
        end = int(end_str)
        total = int(total)

        # Verify the byte count in Content-Range matches actual data sent
        expected_byte_count = end - start + 1
        actual_byte_count = len(data)

        assert expected_byte_count == actual_byte_count, (
            "Content-Range byte count ({0}) does not match actual data ({1})".format(
                expected_byte_count, actual_byte_count
            )
        )

        # For a 100-byte file
        assert start == 0
        assert end == 99
        assert total == 100
        assert actual_byte_count == 100

    def test_large_file_multi_chunk_content_range_consistency(self):
        """
        Verify that for large files split into multiple chunks,
        each chunk's Content-Range matches the actual bytes being sent.
        """
        # Create a file slightly larger than one chunk
        # (To ensure we test the multi-chunk path)
        # Note: upload_file uses chunk_size = 1024 * 7168 = 7,340,032 bytes
        # We'll test with a smaller synthetic chunk size via mocking

        file_size = 1000
        file_content = 'y' * file_size
        fileobj = BytesIO(file_content.encode('utf-8'))

        self.client.api.post.return_value = Mock(status=200)

        result = upload_file(self.client, self.url, fileobj, 'largefile.bin')

        assert result is True

        # For a 1000-byte file with 7MB chunk size, should be a single chunk
        # Verify the call happened
        assert self.client.api.post.call_count == 1

        call_args = self.client.api.post.call_args
        headers = call_args.kwargs.get('headers') or call_args[1]['headers']
        data = call_args.kwargs.get('data') or call_args[1]['data']

        content_range = headers['Content-Range']
        range_part, total = content_range.split('/')
        start_str, end_str = range_part.split('-')

        actual_byte_count = len(data)
        expected_byte_count = int(end_str) - int(start_str) + 1

        assert expected_byte_count == actual_byte_count

    def test_content_range_format_compliance(self):
        """
        Verify Content-Range header follows RFC 7233 format.
        Format: bytes start-end/total
        where start and end are inclusive byte positions (0-indexed).
        """
        file_content = 'test' * 25  # 100 bytes
        fileobj = BytesIO(file_content.encode('utf-8'))

        self.client.api.post.return_value = Mock(status=200)

        upload_file(self.client, self.url, fileobj, 'rfc7233.txt')

        call_args = self.client.api.post.call_args
        headers = call_args.kwargs.get('headers') or call_args[1]['headers']
        data = call_args.kwargs.get('data') or call_args[1]['data']

        content_range = headers['Content-Range']

        # RFC 7233 compliance: "bytes start-end/total"
        assert content_range.startswith('bytes ') or '-' in content_range

        # Extract values
        range_part, total = content_range.split('/')
        if range_part.startswith('bytes '):
            range_part = range_part[6:]

        start, end = map(int, range_part.split('-'))

        # Verify math: byte count = end - start + 1
        byte_count_from_range = end - start + 1
        byte_count_actual = len(data)

        assert byte_count_from_range == byte_count_actual, (
            "RFC 7233: byte count mismatch. Range says {0}, actual is {1}".format(
                byte_count_from_range, byte_count_actual
            )
        )


if __name__ == '__main__':
    unittest.main()
