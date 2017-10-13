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
import pytest
import json

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    F5ModuleError
)
from library.iworkflow_local_connector_node import (
    Parameters,
    Connector,
    Device
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

        self.loaded_connectors = []
        devices_json = load_fixture('load_connectors.json')
        for item in devices_json:
            self.loaded_connectors.append(Namespace(**item))

    @patch.object(Device, '_get_device_collection')
    @patch.object(Connector, '_get_connector_collection')
    def test_module_parameters_general(self, *args):
        args[0].return_value = self.loaded_connectors
        args[1].return_value = self.loaded_devices
        args = dict(
            device="10.2.2.3",
            password_credential="admin",
            username_credential="root",
            state="present",
            connector="foo",
            hostname="foo.example.com",
            interfaces=[
                dict(
                    local_address="10.0.1.4",
                    subnet_address="10.0.1.0/24"
                ),
                dict(
                    local_address="10.2.2.3",
                    subnet_address="10.2.2.0/24",
                    name="external"
                )
            ]
        )

        p = Parameters(args)
        assert p.device.address == '10.2.2.3'
        assert p.hostname == 'foo.example.com'
        assert len(p.interfaces) == 2
        assert p.interfaces[0]['localAddress'] == '10.0.1.4'
        assert p.interfaces[0]['subnetAddress'] == '10.0.1.0/24'
        assert p.interfaces[1]['localAddress'] == '10.2.2.3'
        assert p.interfaces[1]['subnetAddress'] == '10.2.2.0/24'
        assert p.interfaces[1]['name'] == 'external'

    def test_module_parameters_missing_subnet_address(self, *args):
        args = dict(
            interfaces=[
                dict(
                    local_address="10.0.1.4"
                )
            ]
        )

        p = Parameters(args)
        with pytest.raises(F5ModuleError):
            assert len(p.interfaces) == 1

    def test_module_parameters_missing_local_address(self, *args):
        args = dict(
            interfaces=[
                dict(
                    subnet_address="10.0.1.4"
                )
            ]
        )

        p = Parameters(args)
        with pytest.raises(F5ModuleError):
            assert len(p.interfaces) == 1

    def test_module_parameters_subnet_not_ipaddress(self, *args):
        args = dict(
            interfaces=[
                dict(
                    subnet_address="foo"
                )
            ]
        )

        p = Parameters(args)
        with pytest.raises(F5ModuleError):
            assert len(p.interfaces) == 1

    def test_module_parameters_local_not_ipaddress(self, *args):
        args = dict(
            interfaces=[
                dict(
                    local_address="foo"
                )
            ]
        )

        p = Parameters(args)
        with pytest.raises(F5ModuleError):
            assert len(p.interfaces) == 1

    def test_module_parameters_virtual_not_ipaddress(self, *args):
        args = dict(
            interfaces=[
                dict(
                    virtual_address="foo"
                )
            ]
        )

        p = Parameters(args)
        with pytest.raises(F5ModuleError):
            assert len(p.interfaces) == 1

    def test_module_parameters_gateway_not_ipaddress(self, *args):
        args = dict(
            interfaces=[
                dict(
                    gateway_address="foo"
                )
            ]
        )

        p = Parameters(args)
        with pytest.raises(F5ModuleError):
            assert len(p.interfaces) == 1
