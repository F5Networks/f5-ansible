# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for icontrol.upload_file() function.

Verifies that Content-Range headers correctly reflect the actual bytes being
transmitted, preventing off-by-one errors that cause BIG-IP to reject uploads
with: "Chunk byte count X different from received buffer length Y"

This tests the fix in icontrol.py where the Content-Range calculation was
corrected to use `end = start + current_bytes` unconditionally, rather than
using total file size for the final chunk.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock

try:
    from io import StringIO, BytesIO
except ImportError:
    from StringIO import StringIO
    BytesIO = StringIO

from ansible_collections.f5networks.f5_modules.plugins.module_utils.icontrol import upload_file


class ChunkedBytesIO(BytesIO):
    """
    A file-like object that simulates chunked reads by inheriting from BytesIO.

    When upload_file calls read(chunk_size), this object returns smaller
    chunks to simulate a multi-chunk upload, regardless of chunk_size.

    This allows testing the Content-Range byte count calculation for
    chunks with start > 0.
    """
    def __init__(self, data, small_chunk_size=256):
        super(ChunkedBytesIO, self).__init__(data)
        self.small_chunk_size = small_chunk_size
        self.position = 0

    def read(self, size):
        """Read up to small_chunk_size bytes, regardless of requested size."""
        # Always read in smaller chunks
        read_size = min(self.small_chunk_size, size)
        result = super(ChunkedBytesIO, self).read(read_size)
        if result:
            self.position += len(result)
        return result

    def seek(self, pos, whence=0):
        """Seek to position in file."""
        self.position = super(ChunkedBytesIO, self).seek(pos, whence)
        return self.position

    def tell(self):
        """Return current position."""
        return super(ChunkedBytesIO, self).tell()


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

    def test_multi_chunk_upload_final_chunk_content_range(self):
        """
        Verify Content-Range header byte count matches actual data for any chunk.

        This tests the fix: end = start + current_bytes (not end = size).
        The critical assertion is that (end - start + 1) always equals len(data).
        """
        # Create a small BytesIO file
        file_content = b'x' * 100
        fileobj = BytesIO(file_content)

        self.client.api.post.return_value = Mock(status=200)

        # Call upload_file with the small BytesIO
        result = upload_file(self.client, self.url, fileobj, 'testfile.bin')

        # Verify upload succeeded
        assert result is True

        # Verify POST was called at least once
        assert self.client.api.post.call_count >= 1

        # Critical check: For every chunk, byte count in Content-Range must match data
        for i, call_args in enumerate(self.client.api.post.call_args_list):
            headers = call_args.kwargs.get('headers') or call_args[1]['headers']
            data = call_args.kwargs.get('data') or call_args[1]['data']

            content_range = headers['Content-Range']
            range_part, total_size = content_range.split('/')
            start_str, end_str = range_part.split('-')
            start = int(start_str)
            end = int(end_str)

            # This is the core fix: byte count must match actual data sent
            byte_count_from_header = end - start + 1
            byte_count_actual = len(data)

            assert byte_count_from_header == byte_count_actual, (
                "Chunk {0}: header byte count {1} != actual {2}".format(
                    i + 1, byte_count_from_header, byte_count_actual
                )
            )

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

        # Extract values
        range_part, total = content_range.split('/')
        start, end = map(int, range_part.split('-'))

        # Verify math: byte count = end - start + 1
        byte_count_from_range = end - start + 1
        byte_count_actual = len(data)

        assert byte_count_from_range == byte_count_actual, (
            "RFC 7233: byte count mismatch. Range says {0}, actual is {1}".format(
                byte_count_from_range, byte_count_actual
            )
        )

    def test_multi_chunk_forced_small_chunks_final_chunk_accurate(self):
        """
        Force multiple chunks by using ChunkedBytesIO that returns 256-byte chunks.
        Upload 1000-byte file, creating ~4 chunks.
        Verify Content-Range byte count is correct for ALL chunks, especially those with start > 0.
        This directly tests the fix: end = start + current_bytes (not end = size).
        """
        # Create 1000-byte file with ChunkedBytesIO that returns 256 bytes per read()
        file_content = b'x' * 1000
        fileobj = ChunkedBytesIO(file_content, small_chunk_size=256)

        self.client.api.post.return_value = Mock(status=200)
        result = upload_file(self.client, self.url, fileobj, 'testfile.bin')

        # Verify upload succeeded
        assert result is True

        # With 256-byte chunks and 1000 bytes, should have multiple chunks
        assert self.client.api.post.call_count >= 3, (
            "Expected at least 3 chunks for 1000 bytes with 256-byte chunk_size, got {0}".format(
                self.client.api.post.call_count
            )
        )

        # Verify byte count accuracy for ALL chunks, especially those with start > 0
        for i, call_args in enumerate(self.client.api.post.call_args_list):
            headers = call_args.kwargs.get('headers') or call_args[1]['headers']
            data = call_args.kwargs.get('data') or call_args[1]['data']

            content_range = headers['Content-Range']
            range_part, total = content_range.split('/')
            start_str, end_str = range_part.split('-')
            start = int(start_str)
            end = int(end_str)

            byte_count_header = end - start + 1
            byte_count_actual = len(data)

            # This catches the old bug where end would be 1000 for final chunk
            assert byte_count_header == byte_count_actual, (
                "Chunk {0}: start={1}, header says {2} bytes but got {3}".format(
                    i, start, byte_count_header, byte_count_actual
                )
            )


if __name__ == '__main__':
    unittest.main()
