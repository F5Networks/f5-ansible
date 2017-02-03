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
from library.bigip_static_route import BigIpStaticRouteModule
from tests.data.fixtures.bigip_static_route import (
    required_present_params,
    missing_required_present_param_resource,
    missing_required_present_param_destination,
    missing_required_present_param_netmask
)

@patch('library.bigip_static_route.BigIpStaticRouteModule.fail_json',
       return_value=None)
class TestValidParams(object):

    @patch('library.bigip_static_route.BigIpStaticRouteModule._load_params',
           return_value=None)
    @patch('library.bigip_static_route.BigIpStaticRouteModule.params',
           new_callable=PropertyMock,
           return_value=required_present_params(),
           create=True)
    def test_required_present_params(self, *args):
        """Provide required parameters and ensure no exception

        The parameters provided to the module should match the constraints
        that the module implements. This test ensures that a valid set
        of credentials will raise no exception.

        The `_load_params` method is patched to avoid the AnsibleModule base
        class attempting to load the parameters from where Ansible normally
        expects them

        The `params` attribute is patched to provide to the module a set of
        parameters to try to instantiate itself with

        Arguments:
            *args: The patches applied in the function decorators

        Returns:
            void
        """
        BigIpStaticRouteModule()


@patch('library.bigip_static_route.BigIpStaticRouteModule._load_params',
       return_value=None)
@patch('library.bigip_static_route.BigIpStaticRouteModule.fail_json',
       return_value=None)
class TestMissingRequiredParams(object):

    @patch('library.bigip_static_route.BigIpStaticRouteModule.params',
           new_callable=PropertyMock,
           return_value=missing_required_present_param_resource(),
           create=True)
    def test_missing_required_present_param_resource(self, *args):
        """Provide required parameters, missing the `resource` parameter

        The resource parameter is required if the state is present. Therefore,
        test to ensure that the appropriate failure in Ansible has occurred.

        :param args:
        :return:
        """
        BigIpStaticRouteModule()

    @patch('library.bigip_static_route.BigIpStaticRouteModule.params',
           new_callable=PropertyMock,
           return_value=missing_required_present_param_destination(),
           create=True)
    def test_missing_required_present_param_destination(self, *args):
        """Provide required parameters, missing the `destination` parameter

        The `destination` parameter is required if the state is present.
        Therefore, test to ensure that the appropriate failure in Ansible
        has occurred.

        :param args:
        :return:
        """
        BigIpStaticRouteModule()

    @patch('library.bigip_static_route.BigIpStaticRouteModule.params',
           new_callable=PropertyMock,
           return_value=missing_required_present_param_netmask(),
           create=True)
    def test_missing_required_present_param_netmask(self, *args):
        """Provide required parameters, missing the `netmask` parameter

        The `netmask` parameter is required if the state is present.
        Therefore, test to ensure that the appropriate failure in Ansible
        has occurred.

        :param args:
        :return:
        """
        BigIpStaticRouteModule()


