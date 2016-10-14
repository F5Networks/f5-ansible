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

import pytest
import requests_mock

from library.bigip_user import BigIpUserManager

@pytest.fixture
def defaults():
    return dict(
        username_credential="johnd",
        password_credential="password",
        partition_access1=[
            "all:admin",
            "Common:guest",
            "Common:operator"
        ],
        partition_access2=[
            "all:admin",
            "Common:operator"
        ],
        partition_access3=[
            "foo:operator"
        ],
        partition="foo",
        full_name="John Doe"
    )

@requests_mock.Mocker(kw='mock')
class MockManagementRoot:
    def __init__(self, *args, **kwargs):
        pass

class MockBigIpUserManager(BigIpUserManager):
    def connect_to_bigip(self, **kwargs):
        return MockManagementRoot(kwargs['server'],
                              kwargs['user'],
                              kwargs['password'],
                              port=kwargs['server_port'])

pytest.mark.usefixtures('module_args_checkmode', 'defaults')
class TestBigIpUserCheckMode(object):
    def test_Create_user(self, module_args_checkmode, defaults):
        test_args = dict(
            username_credential=defaults['username_credential'],
            password_credential=defaults['password_credential'],
            update_password="on_create",
            state='present'
        )
        module_args_checkmode.update(test_args)
        obj = MockBigIpUserManager(**module_args_checkmode)
        obj.apply_changes()