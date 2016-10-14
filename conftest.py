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

BIGIP_USER = "admin"
BIGIP_PASSWORD = "secret"
BIGIP_SERVER = "localhost"
BIGIP_PORT = 443
BIGIP_VALIDATE_CERTS = "no"

@pytest.fixture(scope="module")
def module_args_checkmode():
    return dict(
        supports_check_mode=True,
        user=BIGIP_USER,
        password=BIGIP_PASSWORD,
        server=BIGIP_SERVER,
        server_port=BIGIP_PORT,
        validate_certs=BIGIP_VALIDATE_CERTS
    )

@pytest.fixture(scope="module")
def module_args_no_checkmode():
    return dict(
        supports_check_mode=False,
        user=BIGIP_USER,
        password=BIGIP_PASSWORD,
        server=BIGIP_SERVER,
        server_port=BIGIP_PORT,
        validate_certs=BIGIP_VALIDATE_CERTS
    )