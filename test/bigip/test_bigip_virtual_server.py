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
import yaml

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    AnsibleF5Client
)
from library.bigip_virtual_server2 import (
    Parameters,
    ModuleManager,
    ArgumentSpec
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


class TestParameters(unittest.TestCase):

    def test_module_no_partition_prefix_parameters(self):
        args = dict(
            server='localhost',
            user='admin',
            password='secret',
            state='present',
            partition='Common',
            name='my-virtual-server',
            destination='10.10.10.10',
            port=443,
            pool='my-pool',
            snat='Automap',
            description='Test Virtual Server',
            profiles_both=['fix'],
            profiles_server_side=['clientssl'],
            profiles_client_side=['ilx'],
            enabled_vlans=['vlan2']
        )
        p = Parameters(args)
        assert p.name == 'my-virtual-server'
        assert p.partition == 'Common'
        assert p.port == 443
        assert p.server == 'localhost'
        assert p.user == 'admin'
        assert p.password == 'secret'
        assert p.destination == '/Common/10.10.10.10:443'
        assert p.pool == '/Common/my-pool'
        assert p.snat == {'type': 'automap'}
        assert p.description == 'Test Virtual Server'
        assert {'context': 'all', 'name': 'fix'} in p.profiles_both
        assert {'context': 'serverside', 'name': 'clientssl'} in \
               p.profiles_server_side
        assert {'context': 'clientside', 'name': 'ilx'} in \
               p.profiles_client_side
        assert '/Common/vlan2' in p.enabled_vlans

    def test_module_partition_prefix_parameters(self):
        args = dict(
            server='localhost',
            user='admin',
            password='secret',
            state='present',
            partition='Common',
            name='my-virtual-server',
            destination='10.10.10.10',
            port=443,
            pool='/Common/my-pool',
            snat='Automap',
            description='Test Virtual Server',
            profiles_both=['fix'],
            profiles_server_side=['serverssl'],
            profiles_client_side=['ilx'],
            enabled_vlans=['/Common/vlan2']
        )
        p = Parameters(args)
        assert p.name == 'my-virtual-server'
        assert p.partition == 'Common'
        assert p.port == 443
        assert p.server == 'localhost'
        assert p.user == 'admin'
        assert p.password == 'secret'
        assert p.destination == '/Common/10.10.10.10:443'
        assert p.pool == '/Common/my-pool'
        assert p.snat == {'type': 'automap'}
        assert p.description == 'Test Virtual Server'
        assert {'context': 'all', 'name': 'fix'} in p.profiles_both
        assert {'context': 'serverside', 'name': 'serverssl'} in \
               p.profiles_server_side
        assert {'context': 'clientside', 'name': 'ilx'} in \
               p.profiles_client_side
        assert '/Common/vlan2' in p.enabled_vlans

    def test_api_parameters_variables(self):
        args = {
            "kind": "tm:ltm:virtual:virtualstate",
            "name": "my-virtual-server",
            "partition": "Common",
            "fullPath": "/Common/my-virtual-server",
            "generation": 54,
            "selfLink": "https://localhost/mgmt/tm/ltm/virtual/~Common~my-virtual-server?expandSubcollections=true&ver=12.1.2",
            "addressStatus": "yes",
            "autoLasthop": "default",
            "cmpEnabled": "yes",
            "connectionLimit": 0,
            "description": "Test Virtual Server",
            "destination": "/Common/10.10.10.10:443",
            "enabled": True,
            "gtmScore": 0,
            "ipProtocol": "tcp",
            "mask": "255.255.255.255",
            "mirror": "disabled",
            "mobileAppTunnel": "disabled",
            "nat64": "disabled",
            "rateLimit": "disabled",
            "rateLimitDstMask": 0,
            "rateLimitMode": "object",
            "rateLimitSrcMask": 0,
            "serviceDownImmediateAction": "none",
            "source": "0.0.0.0/0",
            "sourceAddressTranslation": {
                "type": "automap"
            },
            "sourcePort": "preserve",
            "synCookieStatus": "not-activated",
            "translateAddress": "enabled",
            "translatePort": "enabled",
            "vlansEnabled": True,
            "vsIndex": 3,
            "vlans": [
                "/Common/net1"
            ],
            "vlansReference": [
                {
                    "link": "https://localhost/mgmt/tm/net/vlan/~Common~net1?ver=12.1.2"
                }
            ],
            "policiesReference": {
                "link": "https://localhost/mgmt/tm/ltm/virtual/~Common~my-virtual-server/policies?ver=12.1.2",
                "isSubcollection": True
            },
            "profilesReference": {
                "link": "https://localhost/mgmt/tm/ltm/virtual/~Common~my-virtual-server/profiles?ver=12.1.2",
                "isSubcollection": True,
                "items": [
                    {
                        "kind": "tm:ltm:virtual:profiles:profilesstate",
                        "name": "http",
                        "partition": "Common",
                        "fullPath": "/Common/http",
                        "generation": 54,
                        "selfLink": "https://localhost/mgmt/tm/ltm/virtual/~Common~my-virtual-server/profiles/~Common~http?ver=12.1.2",
                        "context": "all",
                        "nameReference": {
                            "link": "https://localhost/mgmt/tm/ltm/profile/http/~Common~http?ver=12.1.2"
                        }
                    },
                    {
                        "kind": "tm:ltm:virtual:profiles:profilesstate",
                        "name": "serverssl",
                        "partition": "Common",
                        "fullPath": "/Common/serverssl",
                        "generation": 54,
                        "selfLink": "https://localhost/mgmt/tm/ltm/virtual/~Common~my-virtual-server/profiles/~Common~serverssl?ver=12.1.2",
                        "context": "serverside",
                        "nameReference": {
                            "link": "https://localhost/mgmt/tm/ltm/profile/server-ssl/~Common~serverssl?ver=12.1.2"
                        }
                    },
                    {
                        "kind": "tm:ltm:virtual:profiles:profilesstate",
                        "name": "tcp",
                        "partition": "Common",
                        "fullPath": "/Common/tcp",
                        "generation": 54,
                        "selfLink": "https://localhost/mgmt/tm/ltm/virtual/~Common~my-virtual-server/profiles/~Common~tcp?ver=12.1.2",
                        "context": "all",
                        "nameReference": {
                            "link": "https://localhost/mgmt/tm/ltm/profile/tcp/~Common~tcp?ver=12.1.2"
                        }
                    }
                ]
            }
        }
        p = Parameters(args)
        assert p.name == 'my-virtual-server'
        assert p.partition == 'Common'
        assert p.port == 443
        assert p.destination == '/Common/10.10.10.10:443'
        assert p.snat == {'type': 'automap'}
        assert p.description == 'Test Virtual Server'
        assert {'context': 'all', 'name': 'http'} in p.profiles_both
        assert {'context': 'serverside', 'name': 'serverssl'} in \
               p.profiles_server_side
        assert '/Common/net1' in p.enabled_vlans

class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
           return_value=True)
    def test_create_service(self, *args):
        set_module_args(dict(
            all_profiles=[
                'http', 'clientssl'
            ],
            description="Test Virtual Server",
            destination="10.10.10.10",
            name="my-snat-pool",
            partition="Common",
            password="secret",
            port="443",
            server="localhost",
            snat="Automap",
            state="present",
            user="admin",
            validate_certs="no"
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )
        mm = ModuleManager(client)

        # Override methods to force specific logic in the module to happen
        mm.exit_json = lambda x: True
        mm.exists = lambda: False
        mm.create_on_device = lambda: True

        results = mm.exec_module()
        assert results['changed'] is True
#
#
#    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
#           return_value=True)
#    def test_update_agent_status_traps(self, *args):
#        parameters = load_fixture('update_iapp_service_parameters_f5_http.json')
#        set_module_args(dict(
#            name='foo',
#            template='f5.http',
#            parameters=parameters,
#            state='present',
#            password='passsword',
#            server='localhost',
#            user='admin'
#        ))
#
#        # Configure the parameters that would be returned by querying the
#        # remote device
#        parameters = load_fixture('create_iapp_service_parameters_f5_http.json')
#        current = Parameters(parameters)
#
#        client = AnsibleF5Client(
#            argument_spec=self.spec.argument_spec,
#            supports_check_mode=self.spec.supports_check_mode,
#            f5_product_name=self.spec.f5_product_name
#        )
#        mm = ModuleManager(client)
#
#        # Override methods to force specific logic in the module to happen
#        mm.exit_json = lambda x: False
#        mm.exists = lambda: True
#        mm.update_on_device = lambda: True
#        mm.read_current_from_device = lambda: current
#
#        results = mm.exec_module()
#        assert results['changed'] is True
#
