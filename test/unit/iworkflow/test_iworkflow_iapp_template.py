#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    AnsibleF5Client
)
from library.iworkflow_iapp_template import (
    ArgumentSpec,
    ModuleManager,
    Parameters
)


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except:
        pass

    fixture_data[path] = data
    return data


class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestParameters(unittest.TestCase):

    def setUp(self):
        self.loaded_devices = []
        devices_json = load_fixture('load_cm_cloud_managed_devices.json')
        for item in devices_json:
            self.loaded_devices.append(Namespace(**item))

    def test_module_parameters(self, *args):
        devices_json = load_fixture('load_cm_cloud_managed_devices.json')
        template_content = load_fixture('f5.microsoft_adfs.v1.0.0.tmpl')
        arguments = dict(
            template_content=template_content,
            device='bigip1'
        )
        with patch.object(Parameters, '_get_device_collection') as mo:
            mo.return_value = self.loaded_devices
            p = Parameters(arguments)

            assert p.name == 'f5.microsoft_adfs.v1.0.0'
            assert p.device == \
                'https://localhost/mgmt/shared/resolver/device-groups/cm-cloud-managed-devices/devices/d13074df-4f0c-4ed3-baf6-0050fe74695f'  # NOQA


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

        self.loaded_devices = []
        devices_json = load_fixture('load_cm_cloud_managed_devices.json')
        for item in devices_json:
            self.loaded_devices.append(Namespace(**item))

    def test_add_device(self, *args):
        template_content = load_fixture('f5.microsoft_adfs.v1.0.0.tmpl')
        set_module_args(dict(
            template_content=template_content,
            device='bigip1',
            server='localhost',
            user='admin',
            password='password'
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        with patch.object(Parameters, '_get_device_collection') as mo:
            mo.return_value = self.loaded_devices

            mm = ModuleManager(client)

            # Override methods to force specific logic in the module to happen
            mm.exit_json = lambda x: True
            mm.read_current_from_device = lambda: current
            mm.exists = lambda: False
            mm.create_on_device = lambda: True

            results = mm.exec_module()

        assert results['changed'] is True
