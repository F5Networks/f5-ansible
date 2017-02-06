#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016 F5 Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: bigip_command
short_description: Run arbitrary command on F5 devices
description:
  - Sends an arbitrary command to an BIG-IP node and returns the results
    read from the device. This module includes an argument that will cause
    the module to wait for a specific condition before returning or timing
    out if the condition is not met.
version_added: "2.4"
options:
  commands:
    description:
      - The commands to send to the remote BIG-IP device over the
        configured provider. The resulting output from the command
        is returned. If the I(wait_for) argument is provided, the
        module is not returned until the condition is satisfied or
        the number of retires as expired.
      - The I(commands) argument also accepts an alternative form
        that allows for complex values that specify the command
        to run and the output format to return. This can be done
        on a command by command basis. The complex argument supports
        the keywords C(command) and C(output) where C(command) is the
        command to run and C(output) is 'text' or 'oneline'.
    required: true
  wait_for:
    description:
      - Specifies what to evaluate from the output of the command
        and what conditionals to apply.  This argument will cause
        the task to wait for a particular conditional to be true
        before moving forward.   If the conditional is not true
        by the configured retries, the task fails.  See examples.
    required: false
    default: null
    aliases: ['waitfor']
    version_added: "2.2"
  match:
    description:
      - The I(match) argument is used in conjunction with the
        I(wait_for) argument to specify the match policy.  Valid
        values are C(all) or C(any).  If the value is set to C(all)
        then all conditionals in the I(wait_for) must be satisfied.  If
        the value is set to C(any) then only one of the values must be
        satisfied.
    required: false
    default: all
    version_added: "2.2"
  retries:
    description:
      - Specifies the number of retries a command should by tried
        before it is considered failed.  The command is run on the
        target device every retry and evaluated against the I(wait_for)
        conditionals.
    required: false
    default: 10
  interval:
    description:
      - Configures the interval in seconds to wait between retries
        of the command.  If the command does not pass the specified
        conditional, the interval indicates how to long to wait before
        trying the command again.
    required: false
    default: 1
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
# Note: examples below use the following provider dict to handle
#       transport and authentication to the node.
vars:
  cli:
    host: "{{ inventory_hostname }}"
    username: admin
    password: admin
    transport: cli

- name: run show version on remote devices
  bigip_command:
    commands: show sys version
    provider: "{{ cli }}"

- name: run show version and check to see if output contains BIG-IP
  bigip_command:
    commands: show sys version
    wait_for: result[0] contains BIG-IP
    provider: "{{ cli }}"

- name: run multiple commands on remote nodes
   bigip_command:
    commands:
      - show sys version
      - list ltm virtual
    provider: "{{ cli }}"

- name: run multiple commands and evaluate the output
  bigip_command:
    commands:
      - show sys version
      - list ltm virtual
    wait_for:
      - result[0] contains BIG-IP
      - result[1] contains my-vs
    provider: "{{ cli }}"

- name: tmsh prefixes will automatically be handled
  bigip_command:
    commands:
      - show sys version
      - tmsh list ltm virtual
    provider: "{{ cli }}"
'''

RETURN = '''
stdout:
    description: The set of responses from the commands
    returned: always
    type: list
    sample: ['...', '...']

stdout_lines:
    description: The value of stdout split into a list
    returned: always
    type: list
    sample: [['...', '...'], ['...'], ['...']]

failed_conditions:
    description: The list of conditionals that have failed
    returned: failed
    type: list
    sample: ['...', '...']
'''


import re

from ansible.module_utils.network import add_argument, register_transport, to_list
from ansible.module_utils.shell import CliBase


class Cli(CliBase):

    CLI_PROMPTS_RE = [
        # One of the default prompts on 12.x
        re.compile(r"\[\w+\@[\w\-\.]+"),

        # Found on 11.6.1
        re.compile(r"[\w-]+\@\([\w\-\.]+\)"),
    ]

    CLI_ERRORS_RE = [
        re.compile(r"connection timed out", re.I),
        re.compile(r"syntax error: unexpected argument", re.I)
    ]

    NET_PASSWD_RE = re.compile(r"[\r\n]?password: $", re.I)

    def connect(self, params, **kwargs):
        super(Cli, self).connect(params, kickstart=False, **kwargs)


Cli = register_transport('cli', default=True)(Cli)




from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *
from ansible.module_utils.basic import get_exception
from ansible.module_utils.network import NetworkModule, NetworkError
from ansible.module_utils.netcli import CommandRunner
from ansible.module_utils.netcli import AddCommandError, FailedConditionsError
from ansible.module_utils.netcli import FailedConditionalError, AddConditionError
from ansible.module_utils.six import string_types


VALID_KEYS = ['command', 'output', 'prompt', 'response']
VALID_CONFIG_MODES = ['modify', 'delete', 'add']

def to_lines(stdout):
    for item in stdout:
        if isinstance(item, string_types):
            item = str(item).split('\n')
        yield item


def parse_commands(module):
    for cmd in module.params['commands']:
        cmd = cmd.strip()

        if isinstance(cmd, basestring):
            cmd = dict(command=cmd, output=None)
        elif 'command' not in cmd:
            module.fail_json(msg='command keyword argument is required')
        elif cmd.get('output') not in [None, 'text', 'oneline']:
            module.fail_json(msg='invalid output specified for command')
        elif not set(cmd.keys()).issubset(VALID_KEYS):
            module.fail_json(msg='unknown keyword specified')

        yield cmd


def is_config_mode_command(cmd):
    if all(cmd['command'].startswith(x) for x in VALID_CONFIG_MODES):
        return True
    return False


def strip_tmsh_prefix(cmd):
    if cmd['command'][0:4] == 'tmsh':
        cmd['command'] = cmd['command'][4:].strip()
    return cmd

def main():
    spec = dict(
        # { command: <str>, output: <str>, prompt: <str>, response: <str> }
        commands=dict(type='list', required=True),

        wait_for=dict(type='list', aliases=['waitfor']),
        match=dict(default='all', choices=['any', 'all']),

        retries=dict(default=10, type='int'),
        interval=dict(default=1, type='int')
    )

    module = NetworkModule(argument_spec=spec,
                           supports_check_mode=True)

    commands = list(parse_commands(module))
    conditionals = module.params['wait_for'] or list()

    warnings = list()

    runner = CommandRunner(module)

    try:
        # This tries to detect command mode.
        runner.add_command('tmsh')
        runner.run()
        shell = "bash"
    except NetworkError:
        shell = "tmsh"

    # Resets the runner because raised exceptions do not remove the
    # erroneous commands
    module.disconnect()
    runner.commands = []
    runner.module.cli._commands = []

    if shell == "tmsh":
        disable_pager = dict(
            output=None,
            command='modify cli preference pager disabled'
        )
        runner.add_command(**disable_pager)
    else:
        disable_pager = dict(
            output=None,
            command='tmsh modify cli preference pager disabled'
        )
        runner.add_command(**disable_pager)
     
    for cmd in commands:
        cmd = strip_tmsh_prefix(cmd)

        if module.check_mode and not is_config_mode_command(cmd):
            warnings.append('only show or list commands are supported when '
                            'using check mode, not executing `%s`'
                            % cmd['command'])
        else:
            if is_config_mode_command(cmd):
                module.fail_json(msg='bigip_command does not support running '
                                     'config mode commands. Please use '
                                     'bigip_config instead')
            try:
                if shell == 'bash':
                    cmd['command'] = 'tmsh ' + cmd['command']
                runner.add_command(**cmd)
            except AddCommandError:
                warnings.append('Duplicate command detected: %s' % cmd)

    try:
        for item in conditionals:
            runner.add_conditional(item)
    except AddConditionError:
        exc = get_exception()
        module.fail_json(msg=str(exc), condition=exc.condition)

    runner.retries = module.params['retries']
    runner.interval = module.params['interval']
    runner.match = module.params['match']

    try:
        runner.run()
    except FailedConditionsError:
        exc = get_exception()
        module.fail_json(msg=str(exc), failed_conditions=exc.failed_conditions)
    except FailedConditionalError:
        exc = get_exception()
        module.fail_json(msg=str(exc), failed_conditional=exc.failed_conditional)
    except NetworkError:
        exc = get_exception()
        module.fail_json(msg=str(exc), **exc.kwargs)

    result = dict(changed=False)

    result['stdout'] = list()
    for cmd in commands:
        try:
            output = runner.get_command(cmd['command'], cmd.get('output'))
        except ValueError:
            output = 'command not executed due to check_mode, see warnings'
        result['stdout'].append(output)

    result['warnings'] = warnings
    result['stdout_lines'] = list(to_lines(result['stdout']))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
