#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
    callback: f5_save_config
    callback_type: aggregate
    requirements:
      - whitelist in configuration
    short_description: Saves a running F5 configuration, at play end, if any of the tasks changed config.
    version_added: 2.6
    description:
        - This is an Ansible callback plugin that will commit the running configuration to
          the saved sys configuration at the end of a playbook.
        - The callback will not save the running configuration if no changes have been reported.
    options:
      server:
        required: True
        description: The BIG-IP to connect to.
        env:
          - name: F5_SERVER
        ini:
          - section: callback_f5_save_config
            key: server
      user:
        required: True
        description: The username to connect to the BIG-IP with.
        env:
          - name: F5_USER
        ini:
          - section: callback_f5_save_config
            key: user
      password:
        required: True
        description: The password for the user account used to connect to the BIG-IP.
        env:
          - name: F5_PASSWORD
        ini:
          - section: callback_f5_save_config
            key: password
      server_port:
        required: True
        description: The port to connect to the BIG-IP on.
        env:
          - name: F5_SERVER_PORT
        ini:
          - section: callback_f5_save_config
            key: server_port
      validate_certs:
        required: False
        default: yes
        description: Used to validate SSL certificates offered by the BIG-IP.
        env:
          - name: F5_VALIDATE_CERTS
        ini:
          - section: callback_f5_save_config
            key: validate_certs
'''

import json
import os

try:
    from __main__ import cli
except ImportError:
    cli = None

from ansible.module_utils.urls import open_url
from ansible.plugins.callback import CallbackBase
from ansible.template import Templar
from ansible.plugins.strategy import SharedPluginLoaderObj

try:
    # Sideband repository used for dev
    from library.module_utils.network.f5.bigip import HAS_F5SDK
    from library.module_utils.network.f5.bigip import F5Client
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import cleanup_tokens
    try:
        from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False
    HAS_DEVEL_IMPORTS = True
except ImportError:
    # Upstream Ansible
    from ansible.module_utils.network.f5.bigip import HAS_F5SDK
    from ansible.module_utils.network.f5.bigip import F5Client
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import cleanup_tokens
    try:
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False


class CallbackModule(CallbackBase):
    """Callback plugin which commits BIG-IP config on change
    """
    CALLBACK_VERSION = 1.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'f5_save_config'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self, display=None):

        super(CallbackModule, self).__init__(display=display)

        if not HAS_F5SDK:
            self.disabled = True
            self._display.warning(
                'The `f5-sdk` python module is not installed. Disabling the F5 Save Config callback plugin.')

        self.playbook_name = None

    def send_msg(self, attachments):
        payload = {
            'channel': self.channel,
            'username': self.username,
            'attachments': attachments,
            'parse': 'none',
            'icon_url': ('http://cdn2.hubspot.net/hub/330046/'
                         'file-449187601-png/ansible_badge.png'),
        }

        data = json.dumps(payload)
        self._display.debug(data)
        self._display.debug(self.webhook_url)
        try:
            response = open_url(self.webhook_url, data=data)
            return response.read()
        except Exception as e:
            self._display.warning('Could not submit message to Slack: %s' %
                                  str(e))

    def v2_playbook_on_start(self, playbook):
        self.playbook = playbook

    def v2_playbook_on_play_start(self, play):
        self.play = play

    def _all_vars(self, host=None, task=None):
        # host and task need to be specified in case 'magic variables' (host vars, group vars, etc) need to be loaded as well
        return self.play.get_variable_manager().get_vars(
            play=self.play,
            host=host,
            task=task
        )

    def v2_runner_on_ok(self, result):
        templar = Templar(
            loader=self.playbook.get_loader(),
            shared_loader_obj=SharedPluginLoaderObj(),
            variables=self._all_vars(host=result._host, task=result._task)
        )

        result._task.squash()
        foo = templar.template(result._task._attributes['environment'])
        q.q(foo)
