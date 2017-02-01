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
    from unittest.mock import Mock, patch, MagicMock, call
except ImportError:
    from mock import Mock, patch, MagicMock, call


import os
from library.bigip_static_route import BigIpStaticRouteModule


class TestBigIpStaticRouteModule(object):
    @patch('os.remove', return_value="asd")
    def test_params1(self, *args):
        ok = os.remove('/tmp/foo')
        print ok

