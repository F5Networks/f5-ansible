# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

import pytest

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import MagicMock

from ansible_collections.f5networks.f5_modules.plugins.terminal.bigip import TerminalModule


def _make_terminal(prompt):
    """Builds a TerminalModule instance with _get_prompt/_exec_cli_command mocked out."""
    terminal = TerminalModule(connection=MagicMock())
    terminal._get_prompt = MagicMock(return_value=prompt)
    terminal._exec_cli_command = MagicMock()
    return terminal


class TestOnOpenShell:
    """
    Regression tests for on_open_shell() prompt detection and command
    dispatch.

    These cover the bug where a long device prompt could be wrapped by
    the terminal before its width was increased via 'stty cols', which
    injected a stray carriage return/line feed into the middle of the
    word 'tmos' (e.g. splitting it into b'tmo\r\ns'). This broke the
    substring check used to detect tmos shells, causing the wrong branch
    to run and a malformed 'stty' command to be sent to the device.
    """

    def test_tmos_prompt_detected_normally(self):
        prompt = b'svc_user@(bigip1)(cfg-sync In Sync)(Active)(/Common)(tmos)#'
        terminal = _make_terminal(prompt)

        terminal.on_open_shell()

        calls = [c.args[0] for c in terminal._exec_cli_command.call_args_list]
        assert calls == [
            b'modify cli preference display-threshold 0 pager disabled',
            b'run /util bash -c "stty cols 1000000" 2> /dev/null',
        ]

    def test_tmos_prompt_wrapped_with_embedded_crlf(self):
        # Simulates a long prompt getting wrapped by the terminal, which
        # splits the literal string 'tmos' into 'tmo\r\ns'.
        prompt = (
            b'svc_mrchntsc_ntwkaut@(ukdc2b-n-ext-slb01)(cfg-sync In Sync)'
            b'(Active)(/Common)(tmo\r\ns)#'
        )
        terminal = _make_terminal(prompt)

        terminal.on_open_shell()

        calls = [c.args[0] for c in terminal._exec_cli_command.call_args_list]
        assert calls == [
            b'modify cli preference display-threshold 0 pager disabled',
            b'run /util bash -c "stty cols 1000000" 2> /dev/null',
        ]

    def test_tmos_prompt_wrapped_with_embedded_cr_only(self):
        # Some terminals only inject a bare \r without \n.
        prompt = b'user@(bigip1)(Active)(/Common)(tm\ros)#'
        terminal = _make_terminal(prompt)

        terminal.on_open_shell()

        calls = [c.args[0] for c in terminal._exec_cli_command.call_args_list]
        assert calls == [
            b'modify cli preference display-threshold 0 pager disabled',
            b'run /util bash -c "stty cols 1000000" 2> /dev/null',
        ]

    def test_non_tmos_shell_prompt(self):
        prompt = b'[root@bigip1:Active:In Sync] ~ #'
        terminal = _make_terminal(prompt)

        terminal.on_open_shell()

        calls = [c.args[0] for c in terminal._exec_cli_command.call_args_list]
        # Regression check for the stray/unbalanced quote bug: the stty
        # command must not contain a bare double-quote character.
        assert calls == [
            b'stty cols 1000000 2> /dev/null',
            b'tmsh modify cli preference display-threshold 0 pager disabled',
        ]
        assert b'"' not in calls[0]

    def test_empty_prompt_does_not_raise(self):
        terminal = _make_terminal(b'')

        terminal.on_open_shell()

        calls = [c.args[0] for c in terminal._exec_cli_command.call_args_list]
        assert calls == [
            b'stty cols 1000000 2> /dev/null',
            b'tmsh modify cli preference display-threshold 0 pager disabled',
        ]

    def test_none_prompt_does_not_raise(self):
        terminal = _make_terminal(None)

        terminal.on_open_shell()

        calls = [c.args[0] for c in terminal._exec_cli_command.call_args_list]
        assert calls == [
            b'stty cols 1000000 2> /dev/null',
            b'tmsh modify cli preference display-threshold 0 pager disabled',
        ]

    def test_tmos_prompt_many_parentheses_and_newline_hash(self):
        prompt = (
            b'svc_mrchntsc_ntwkaut(admin)@(ukdc2b.n.ext.slb01)(avc 0)(mcp )'
            b'(cfg-load )(cfg-sync Standalone)(Active)(/Common)(tmos)\r\n# '
        )
        terminal = _make_terminal(prompt)

        terminal.on_open_shell()

        calls = [c.args[0] for c in terminal._exec_cli_command.call_args_list]
        assert calls == [
            b'modify cli preference display-threshold 0 pager disabled',
            b'run /util bash -c "stty cols 1000000" 2> /dev/null',
        ]


class TestTerminalStdoutRegex:
    def test_multi_parentheses_wrapped_prompt_matches_tmos_pattern(self):
        prompt = (
            b'svc_mrchntsc_ntwkaut(admin)@(ukdc2b.n.ext.slb01)(avc 0)(mcp )'
            b'(cfg-load )(cfg-sync Standalone)(Active)(/Common)(tmos)\r\n# '
        )
        pattern = TerminalModule.terminal_stdout_re[0]
        match = pattern.search(prompt)
        assert match is not None
        assert b'tmos' in match.group(0)

    def test_bare_newline_hash_does_not_match_first_pattern(self):
        pattern = TerminalModule.terminal_stdout_re[0]
        assert pattern.search(b'\r\n# ') is None
        assert pattern.search(b'\n# ') is None

    def test_standard_tmos_prompt_matches_first_pattern(self):
        prompt = b'admin@(bigip1)(Active)(/Common)(tmos)#'
        pattern = TerminalModule.terminal_stdout_re[0]
        match = pattern.search(prompt)
        assert match is not None
        assert b'tmos' in match.group(0)
