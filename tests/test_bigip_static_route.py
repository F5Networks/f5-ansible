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


try:
    from unittest.mock import Mock, patch, MagicMock, mock_open
except ImportError:
    from mock import Mock, patch, MagicMock, mock_open

import ansible.module_utils.basic

from library.bigip_static_route import BigIpStaticRouteModule
from tests.data.fixtures.bigip_static_route import (
    all_params
)


class TestBigIpStaticRouteModule(object):
    def test_params1(self, all_params):
        ansible.module_utils.basic._ANSIBLE_ARGS = all_params
        module = BigIpStaticRouteModule()

        assert 'name' in module.params
        assert 'description' in module.params
        assert 'destination' in module.params
        assert 'netmask' in module.params
        assert 'resource' in module.params
        assert 'gateway_address' in module.params
        assert 'state' in module.params
