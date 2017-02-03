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

from tests.tools import *

def required_present_params():
    return dict(
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
        destination='10.10.10.10',
        name='test-route',
        netmask='255.255.255.0',
        password='admin',
        resource='reject',
        server='localhost',
        server_port='443',
        user='admin'
    )


def missing_required_present_param_resource():
    return dict(
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
        destination='10.10.10.10',
        name='test-route',
        netmask='255.255.255.0',
        password='admin',
        server='localhost',
        server_port='443',
        user='admin'
    )

def missing_required_present_param_destination():
    return dict(
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
        name='test-route',
        netmask='255.255.255.0',
        resource='reject',
        password='admin',
        server='localhost',
        server_port='443',
        user='admin'
    )

def missing_required_present_param_netmask():
    return dict(
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
        destination='10.10.10.10',
        name='test-route',
        resource='reject',
        password='admin',
        server='localhost',
        server_port='443',
        user='admin'
    )