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
import json

@pytest.fixture(scope='module')
def all_params():
    return json.dumps(dict(
        ANSIBLE_MODULE_ARGS=dict(
            _ansible_check_mode=False,
            _ansible_debug=False,
            _ansible_diff=False,
            _ansible_module_name="bigip_static_route",
            _ansible_no_log=False,
            _ansible_selinux_special_fs=[
                "fuse", "nfs", "vboxsf", "ramfs"
            ],
            _ansible_syslog_facility="LOG_USER",
            _ansible_verbosity=4,
            _ansible_version="2.2.0",
            name="test-route",
            password="admin",
            server="localhost",
            server_port="10443",
            user="admin"
        )
    ))