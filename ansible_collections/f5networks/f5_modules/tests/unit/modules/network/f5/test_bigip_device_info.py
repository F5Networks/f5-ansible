# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_info import (
    Parameters, VirtualAddressesFactManager, LtmPoolsFactManager,
    GtmServersFactManager, VirtualServersFactManager, ArgumentSpec, ModuleManager,
    GtmServersParameters, F5ModuleError
)
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock, patch
from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


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


class FakeVirtualAddress:
    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop('params', {})
        for key, value in iteritems(attrs):
            setattr(self, key, value)


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            gather_subset=['virtual-servers'],
        )
        p = Parameters(params=args)
        assert p.gather_subset == ['virtual-servers']


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

        self.p1 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_info.modules_provisioned')
        self.m1 = self.p1.start()
        self.m1.return_value = ['ltm', 'gtm', 'asm']
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_info.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_info.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True
        self.p4 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_info.packages_installed')
        self.m4 = self.p4.start()
        self.m4.return_value = []

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()

    def test_get_trunk_facts(self, *args):
        set_module_args(dict(
            gather_subset=['virtual-addresses'],
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        fixture1 = load_fixture('load_ltm_virtual_address_collection_1.json')
        collection = fixture1['items']

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        tm = VirtualAddressesFactManager(module=module)
        tm.read_collection_from_device = Mock(side_effect=[collection, []])

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['queried'] is True
        assert 'virtual_addresses' in results
        assert len(results['virtual_addresses']) > 0

    def test_expand_subcollections_default_true(self, *args):
        set_module_args(dict(
            gather_subset=['ltm-pools'],
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        tm = LtmPoolsFactManager(module=module)
        tm.read_collection_from_device = Mock(side_effect=[[], []])

        mm = ModuleManager(module=module)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['queried'] is True
        # Verify the default value is True
        assert module.params['expand_subcollections'] is True

    def test_expand_subcollections_set_false(self, *args):
        set_module_args(dict(
            gather_subset=['gtm-servers'],
            expand_subcollections=False,
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        tm = GtmServersFactManager(module=module)
        tm.read_collection_from_device = Mock(side_effect=[[], []])

        mm = ModuleManager(module=module)
        mm.get_manager = Mock(return_value=tm)

        results = mm.exec_module()

        assert results['queried'] is True
        assert module.params['expand_subcollections'] is False

    def test_expand_subcollections_true_includes_query_param(self, *args):
        set_module_args(dict(
            gather_subset=['gtm-servers'],
            expand_subcollections=True,
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 200
        fake_response.json.return_value = {'items': []}
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        tm = GtmServersFactManager(module=module, client=fake_client)
        result = tm.read_collection_from_device(skip=0)

        call_url = fake_client.api.get.call_args[0][0]
        assert 'expandSubcollections=true' in call_url
        assert result == []

    def test_expand_subcollections_false_excludes_query_param(self, *args):
        set_module_args(dict(
            gather_subset=['gtm-servers'],
            expand_subcollections=False,
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 200
        fake_response.json.return_value = {'items': []}
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        tm = GtmServersFactManager(module=module, client=fake_client)
        result = tm.read_collection_from_device(skip=0)

        call_url = fake_client.api.get.call_args[0][0]
        assert 'expandSubcollections' not in call_url
        assert '$top=' in call_url
        assert '$skip=' in call_url
        assert result == []

    def test_expand_subcollections_false_with_partition_all(self, *args):
        set_module_args(dict(
            gather_subset=['virtual-servers'],
            expand_subcollections=False,
            partition='all',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 200
        fake_response.json.return_value = {'items': []}
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        tm = VirtualServersFactManager(module=module, client=fake_client)
        result = tm.read_collection_from_device(skip=0)

        call_url = fake_client.api.get.call_args[0][0]
        assert 'expandSubcollections' not in call_url
        assert '$filter' not in call_url
        assert '$top=' in call_url
        assert '$skip=' in call_url
        assert result == []

    def test_expand_subcollections_true_with_partition_all(self, *args):
        set_module_args(dict(
            gather_subset=['virtual-servers'],
            expand_subcollections=True,
            partition='all',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 200
        fake_response.json.return_value = {'items': []}
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        tm = VirtualServersFactManager(module=module, client=fake_client)
        result = tm.read_collection_from_device(skip=0)

        call_url = fake_client.api.get.call_args[0][0]
        assert 'expandSubcollections=true' in call_url
        assert '$filter' not in call_url
        assert result == []

    def test_gtm_server_vs_stats_404_with_single_space_in_name(self, *args):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 404
        fake_response.json.return_value = {
            'code': 404,
            'message': 'Object not found - host_domain_com - vs 1',
            'errorStack': [],
            'apiError': 1
        }
        fake_response.content = json.dumps(fake_response.json.return_value).encode('utf-8')
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        fake_module = Mock()
        params = GtmServersParameters(client=fake_client, params={}, module=fake_module)
        url_with_single_space = '/mgmt/tm/gtm/server/~Common~host_domain_com/virtual-servers/vs 1'
        result = params._read_virtual_stats_from_device(url_with_single_space)
        assert result == {}
        assert fake_module.warn.called

    def test_gtm_server_vs_stats_404_with_multiple_spaces_in_name(self, *args):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 404
        fake_response.json.return_value = {
            'code': 404,
            'message': 'Object not found - host_domain_com - vs with multiple spaces',
            'errorStack': [],
            'apiError': 1
        }
        fake_response.content = json.dumps(fake_response.json.return_value).encode('utf-8')
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        fake_module = Mock()
        params = GtmServersParameters(client=fake_client, params={}, module=fake_module)
        url_with_multiple_spaces = '/mgmt/tm/gtm/server/~Common~host_domain_com/virtual-servers/vs with multiple spaces'
        result = params._read_virtual_stats_from_device(url_with_multiple_spaces)
        assert result == {}
        assert fake_module.warn.called

    def test_gtm_server_vs_stats_404_with_encoded_space_in_name(self, *args):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 404
        fake_response.json.return_value = {
            'code': 404,
            'message': 'Object not found - host_domain_com - CA_HTTPS',
            'errorStack': [],
            'apiError': 1
        }
        fake_response.content = json.dumps(fake_response.json.return_value).encode('utf-8')
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        fake_module = Mock()
        params = GtmServersParameters(client=fake_client, params={}, module=fake_module)
        url_with_encoded_space = '/mgmt/tm/gtm/server/~Common~host_domain_com/virtual-servers/host_domain_com%20-%20CA_HTTPS'
        result = params._read_virtual_stats_from_device(url_with_encoded_space)
        assert result == {}
        assert fake_module.warn.called

    def test_gtm_server_vs_stats_404_without_space_in_vs_name_raises(self, *args):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 404
        fake_response.json.return_value = {
            'code': 404,
            'message': 'Object not found - vs1',
            'errorStack': [],
            'apiError': 1
        }
        fake_response.content = json.dumps(fake_response.json.return_value).encode('utf-8')
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        fake_module = Mock()
        params = GtmServersParameters(client=fake_client, params={}, module=fake_module)
        url_without_space = '/mgmt/tm/gtm/server/~Common~server1/virtual-servers/vs1/stats'
        with pytest.raises(F5ModuleError) as exc_info:
            params._read_virtual_stats_from_device(url_without_space)
        assert 'Object not found - vs1' in str(exc_info.value)
        assert not fake_module.warn.called

    def test_gtm_server_vs_stats_404_space_in_server_name_only_does_not_match(self, *args):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 404
        fake_response.json.return_value = {
            'code': 404,
            'message': 'Object not found - vs1',
            'errorStack': [],
            'apiError': 1
        }
        fake_response.content = json.dumps(fake_response.json.return_value).encode('utf-8')
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        fake_module = Mock()
        params = GtmServersParameters(client=fake_client, params={}, module=fake_module)
        url_space_in_server_only = '/mgmt/tm/gtm/server/~Common~server space/virtual-servers/vs1/stats'
        with pytest.raises(F5ModuleError) as exc_info:
            params._read_virtual_stats_from_device(url_space_in_server_only)
        assert 'Object not found - vs1' in str(exc_info.value)
        assert not fake_module.warn.called

    def test_gtm_server_vs_stats_500_error_raises(self, *args):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 500
        fake_response.json.return_value = {
            'code': 500,
            'message': 'Internal Server Error'
        }
        fake_response.content = json.dumps(fake_response.json.return_value).encode('utf-8')
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        params = GtmServersParameters(client=fake_client, params={})
        url_with_space = '/mgmt/tm/gtm/server/~Common~host_domain_com/virtual-servers/host_domain_com - CA_HTTPS'
        with pytest.raises(F5ModuleError) as exc_info:
            params._read_virtual_stats_from_device(url_with_space)
        assert 'Internal Server Error' in str(exc_info.value)

    def test_gtm_server_vs_stats_200_success(self, *args):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.status = 200
        fake_response.json.return_value = {
            'entries': {
                'https://localhost/mgmt/tm/gtm/server/~Common~server1/virtual-servers/vs1/stats': {
                    'nestedStats': {
                        'entries': {
                            'status.availabilityState': {'description': 'available'},
                            'status.statusReason': {'description': 'Virtual server is available'},
                            'status.enabledState': {'description': 'enabled'},
                            'bitsPerSecIn': {'value': 100},
                            'bitsPerSecOut': {'value': 200},
                            'pktsPerSecIn': {'value': 10},
                            'pktsPerSecOut': {'value': 20},
                            'connections': {'value': 5},
                            'picks': {'value': 1},
                            'vsScore': {'value': 10},
                            'uptime': {'value': 1000}
                        }
                    }
                }
            }
        }
        fake_client.api.get.return_value = fake_response
        fake_client.provider = {'server': 'localhost', 'server_port': 443}

        params = GtmServersParameters(client=fake_client, params={})
        url = '/mgmt/tm/gtm/server/~Common~server1/virtual-servers/vs1'
        result = params._read_virtual_stats_from_device(url)
        assert result['status']['availabilityState'] == 'available'
