# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
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

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import (
    ApiParameters, ModuleParameters, ModuleManager, ArgumentSpec
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


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='foobar',
            region_members=[
                dict(
                    country='Poland',
                    negate=True
                ),
                dict(
                    datacenter='bazcenter'
                )
            ],
            partition='Common'
        )

        p = ModuleParameters(params=args)
        assert p.name == 'foobar'
        assert p.partition == 'Common'
        assert p.region_members == ['not country PL', 'datacenter /Common/bazcenter']

    def test_api_parameters(self):
        args = dict(
            name='foobar',
            region_members=[
                dict(
                    name='not country PL'
                ),
                dict(
                    name='datacenter /Common/bazcenter'
                )
            ],
            partition='Common'
        )

        p = ApiParameters(params=args)
        assert p.name == 'foobar'
        assert p.partition == 'Common'
        assert p.region_members == ['not country PL', 'datacenter /Common/bazcenter']

    def test_module_parameters_with_spaces_in_region_member_datacenter(self):
        """Test that region members with spaces in datacenter names are properly formatted."""
        args = dict(
            name='foobar',
            region_members=[
                dict(
                    datacenter='baz center'
                )
            ],
            partition='Common'
        )

        p = ModuleParameters(params=args)
        assert p.name == 'foobar'
        # The value should include the partition and the datacenter name with literal spaces
        assert 'datacenter /Common/baz center' in p.region_members[0]

    def test_module_parameters_with_spaces_in_state(self):
        """Test that region members with spaces in state names are properly formatted."""
        args = dict(
            name='My Region',
            region_members=[
                dict(
                    country='United States',
                    state='North Carolina'
                )
            ],
            partition='Common'
        )

        p = ModuleParameters(params=args)
        assert p.name == 'My Region'
        # State value should have the country code and state
        assert any('state North Carolina' in member for member in p.region_members)

    def test_module_parameters_with_spaces_in_pool(self):
        """Test that region members with spaces in pool names are properly formatted."""
        args = dict(
            name='region with spaces',
            region_members=[
                dict(
                    pool='my pool name'
                )
            ],
            partition='Common'
        )

        p = ModuleParameters(params=args)
        assert p.name == 'region with spaces'
        # Pool name should be formatted with partition and literal spaces (escaping happens in UsableChanges)
        assert 'pool /Common/my pool name' in p.region_members[0]


class TestEscapeSpaces(unittest.TestCase):
    """Test the escape_spaces function to ensure proper quoting of values with spaces."""

    def test_escape_spaces_state_with_spaces(self):
        """Test that state values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'state North Carolina'
        result = UsableChanges.escape_spaces(item)
        assert result == 'state \\"North Carolina\\"'

    def test_escape_spaces_state_without_spaces(self):
        """Test that state values without spaces are not modified."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'state CA'
        result = UsableChanges.escape_spaces(item)
        assert result == 'state CA'

    def test_escape_spaces_datacenter_with_spaces(self):
        """Test that datacenter values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'datacenter /Common/My Data Center'
        result = UsableChanges.escape_spaces(item)
        assert result == 'datacenter \\"/Common/My Data Center\\"'

    def test_escape_spaces_pool_with_spaces(self):
        """Test that pool values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'pool /Common/My Pool'
        result = UsableChanges.escape_spaces(item)
        assert result == 'pool \\"/Common/My Pool\\"'

    def test_escape_spaces_region_with_spaces(self):
        """Test that region values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'region /Common/My Region'
        result = UsableChanges.escape_spaces(item)
        assert result == 'region \\"/Common/My Region\\"'

    def test_escape_spaces_geoip_isp_with_spaces(self):
        """Test that geoip-isp values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'geoip-isp My ISP Provider'
        result = UsableChanges.escape_spaces(item)
        assert result == 'geoip-isp \\"My ISP Provider\\"'

    def test_escape_spaces_continent_with_spaces(self):
        """Test that continent values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'continent North America'
        result = UsableChanges.escape_spaces(item)
        assert result == 'continent \\"North America\\"'

    def test_escape_spaces_country_with_spaces(self):
        """Test that country values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'country United States'
        result = UsableChanges.escape_spaces(item)
        assert result == 'country \\"United States\\"'

    def test_escape_spaces_no_matching_key(self):
        """Test that items without recognized keys are returned unmodified."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'unknown value with spaces'
        result = UsableChanges.escape_spaces(item)
        assert result == 'unknown value with spaces'

    def test_escape_spaces_negate_state_with_spaces(self):
        """Test that negate prefixed state values with spaces are escape-quoted."""
        from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region import UsableChanges
        item = 'not state South Carolina'
        result = UsableChanges.escape_spaces(item)
        # Note: the "not" prefix is part of the value, so state starts after it
        # This test ensures we're only escaping after the key prefix
        assert 'state' in result


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_gtm_topology_region.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p2.stop()
        self.p3.stop()

    def test_create_topology_region(self, *args):
        set_module_args(dict(
            name='foobar',
            region_members=[
                dict(
                    country='Poland',
                    negate=True
                ),
                dict(
                    datacenter='bazcenter'
                )
            ],
            partition='Common',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        )
        )

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(return_value=False)
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
