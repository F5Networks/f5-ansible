# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import sys

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch, Mock, DEFAULT
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import AnsibleF5Client

try:
    from library.bigip_virtual_server import VirtualAddressParameters
    from library.bigip_virtual_server import VirtualServerParameters
    from library.bigip_virtual_server import ModuleManager
    from library.bigip_virtual_server import VirtualServerManager
    from library.bigip_virtual_server import VirtualAddressManager
    from library.bigip_virtual_server import ArgumentSpec
    from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_virtual_server import VirtualAddressParameters
        from ansible.modules.network.f5.bigip_virtual_server import VirtualServerParameters
        from ansible.modules.network.f5.bigip_virtual_server import ModuleManager
        from ansible.modules.network.f5.bigip_virtual_server import VirtualServerManager
        from ansible.modules.network.f5.bigip_virtual_server import VirtualAddressManager
        from ansible.modules.network.f5.bigip_virtual_server import ArgumentSpec
        from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

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
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_destination_mutex_1(self):
        args = dict(
            destination='1.1.1.1'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'

    def test_destination_mutex_2(self):
        args = dict(
            destination='1.1.1.1%2'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'
        assert p.destination_tuple.route_domain == 2

    def test_destination_mutex_3(self):
        args = dict(
            destination='1.1.1.1:80'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'
        assert p.destination_tuple.port == 80

    def test_destination_mutex_4(self):
        args = dict(
            destination='1.1.1.1%2:80'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'
        assert p.destination_tuple.port == 80
        assert p.destination_tuple.route_domain == 2

    def test_destination_mutex_5(self):
        args = dict(
            destination='/Common/1.1.1.1'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'

    def test_destination_mutex_6(self):
        args = dict(
            destination='/Common/1.1.1.1%2'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'
        assert p.destination_tuple.route_domain == 2

    def test_destination_mutex_7(self):
        args = dict(
            destination='/Common/1.1.1.1:80'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'
        assert p.destination_tuple.port == 80

    def test_destination_mutex_8(self):
        args = dict(
            destination='/Common/1.1.1.1%2:80'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '1.1.1.1'
        assert p.destination_tuple.port == 80
        assert p.destination_tuple.route_domain == 2

    def test_destination_mutex_9(self):
        args = dict(
            destination='2700:bc00:1f10:101::6'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '2700:bc00:1f10:101::6'

    def test_destination_mutex_10(self):
        args = dict(
            destination='2700:bc00:1f10:101::6%2'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '2700:bc00:1f10:101::6'
        assert p.destination_tuple.route_domain == 2

    def test_destination_mutex_11(self):
        args = dict(
            destination='2700:bc00:1f10:101::6.80'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '2700:bc00:1f10:101::6'
        assert p.destination_tuple.port == 80

    def test_destination_mutex_12(self):
        args = dict(
            destination='2700:bc00:1f10:101::6%2.80'
        )
        p = VirtualServerParameters(args)
        assert p.destination_tuple.ip == '2700:bc00:1f10:101::6'
        assert p.destination_tuple.port == 80
        assert p.destination_tuple.route_domain == 2

#
#    def test_destination_mutex_6(self):
#        args = dict(
#            destination='/Common/2700:bc00:1f10:101::6'
#        )
#        p = VirtualServerParameters(args)
#        assert p.destination_tuple.ip == '2700:bc00:1f10:101::6'
#
#    def test_destination_mutex_5(self):
#        args = dict(
#            destination='/Common/2700:bc00:1f10:101::6'
#        )
#        p = VirtualServerParameters(args)
#        assert p.destination_tuple.ip == '2700:bc00:1f10:101::6'

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
            profiles=[
                dict(
                    name='fix',
                    context='all'
                )
            ],
            enabled_vlans=['vlan2']
        )
        p = VirtualServerParameters(args)
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
        assert len(p.profiles) == 1
        assert 'context' in p.profiles[0]
        assert 'name' in p.profiles[0]
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
            profiles=[
                dict(
                    name='fix',
                    context='all'
                )
            ],
            enabled_vlans=['/Common/vlan2']
        )
        p = VirtualServerParameters(args)
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
        assert len(p.profiles) == 1
        assert 'context' in p.profiles[0]
        assert 'name' in p.profiles[0]
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
        p = VirtualServerParameters(args)
        assert p.name == 'my-virtual-server'
        assert p.partition == 'Common'
        assert p.port == 443
        assert p.destination == '/Common/10.10.10.10:443'
        assert p.snat == {'type': 'automap'}
        assert p.description == 'Test Virtual Server'
        assert {'context': 'all', 'name': 'http'} in p.profiles
        assert '/Common/net1' in p.enabled_vlans


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create_virtual_server(self, *args):
        set_module_args(dict(
            all_profiles=[
                dict(
                    name='http'
                ),
                dict(
                    name='clientssl'
                )
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

        # Override methods to force specific logic in the module to happen
        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=False)
        vsm.create_on_device = Mock(return_value=True)

        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=vsm)
        results = mm.exec_module()

        assert results['changed'] is True

    def test_delete_virtual_server(self, *args):
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
            state="absent",
            user="admin",
            validate_certs="no"
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=False)

        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=vsm)

        results = mm.exec_module()

        assert results['changed'] is False

    def test_enable_vs_that_is_already_enabled(self, *args):
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
            state="absent",
            user="admin",
            validate_certs="no"
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = VirtualServerParameters(
            dict(
                agent_status_traps='disabled'
            )
        )

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=False)
        vsm.update_on_device = Mock(return_value=True)
        vsm.read_current_from_device = Mock(return_value=current)

        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=vsm)
        results = mm.exec_module()

        assert results['changed'] is False

    def test_modify_port(self, *args):
        set_module_args(dict(
            name="my-virtual-server",
            partition="Common",
            password="secret",
            port="10443",
            server="localhost",
            state="present",
            user="admin",
            validate_certs="no"
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = VirtualServerParameters(load_fixture('load_ltm_virtual_1.json'))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=True)
        vsm.read_current_from_device = Mock(return_value=current)
        vsm.update_on_device = Mock(return_value=True)

        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=vsm)
        results = mm.exec_module()

        assert results['changed'] is True

    def test_modify_port_idempotent(self, *args):
        set_module_args(dict(
            name="my-virtual-server",
            partition="Common",
            password="secret",
            port="443",
            server="localhost",
            state="present",
            user="admin",
            validate_certs="no"
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = VirtualServerParameters(load_fixture('load_ltm_virtual_1.json'))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=True)
        vsm.read_current_from_device = Mock(return_value=current)

        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=vsm)
        results = mm.exec_module()

        assert results['changed'] is False

    def test_modify_vlans_idempotent(self, *args):
        set_module_args(dict(
            name="my-virtual-server",
            partition="Common",
            password="secret",
            enabled_vlans=[
                "net1"
            ],
            server="localhost",
            state="present",
            user="admin",
            validate_certs="no"
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = VirtualServerParameters(load_fixture('load_ltm_virtual_2.json'))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=True)
        vsm.read_current_from_device=Mock(return_value=current)

        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=vsm)

        results = mm.exec_module()

        assert results['changed'] is False

    def test_modify_profiles(self, *args):
        set_module_args(dict(
            name="my-virtual-server",
            partition="Common",
            password="secret",
            profiles=[
                'http', 'clientssl'
            ],
            server="localhost",
            state="present",
            user="admin",
            validate_certs="no"
        ))

        # Configure the parameters that would be returned by querying the
        # remote device
        current = VirtualServerParameters(load_fixture('load_ltm_virtual_2.json'))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        # Override methods to force specific logic in the module to happen
        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=True)
        vsm.read_current_from_device=Mock(return_value=current)
        vsm.update_on_device = Mock(return_value=True)

        mm = ModuleManager(client)
        mm.get_manager = Mock(return_value=vsm)

        results = mm.exec_module()

        assert results['changed'] is True
        assert len(results['profiles']) == 2
        assert 'name' in results['profiles'][0]
        assert 'context' in results['profiles'][0]
        assert results['profiles'][0]['name'] == 'http'
        assert results['profiles'][0]['context'] == 'all'
        assert 'name' in results['profiles'][1]
        assert 'context' in results['profiles'][1]
        assert results['profiles'][1]['name'] == 'clientssl'
        assert results['profiles'][1]['context'] == 'clientside'


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestDeprecatedAnsible24Manager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()

    def test_modify_port_idempotent(self, *args):
        set_module_args(dict(
            destination="10.10.10.10",
            name="my-virtual-server",
            route_advertisement_state="enabled",
            partition="Common",
            password="secret",
            port="443",
            server="localhost",
            state="present",
            user="admin",
            validate_certs="no"
        ))

        client = AnsibleF5Client(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            f5_product_name=self.spec.f5_product_name
        )

        vsm_current = VirtualServerParameters(load_fixture('load_ltm_virtual_1.json'))
        vam_current = VirtualAddressParameters(load_fixture('load_ltm_virtual_1_address.json'))

        vsm = VirtualServerManager(client)
        vsm.exists = Mock(return_value=True)
        vsm.read_current_from_device = Mock(return_value=vsm_current)
        vam = VirtualAddressManager(client)
        vam.exists = Mock(return_value=True)
        vam.read_current_from_device = Mock(return_value=vam_current)

        mm = ModuleManager(client)
        mm.get_manager = Mock(side_effect=[vsm, vam])

        results = mm.exec_module()

        assert results['changed'] is False
