# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes

from library.iworkflow_service import (
    Parameters
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
    except Exception:
        pass

    fixture_data[path] = data
    return data


class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
       return_value=True)
class TestParameters(unittest.TestCase):

    def setUp(self):
        self.loaded_connectors = []
        connectors_json = load_fixture('load_connectors.json')
        for item in connectors_json:
            self.loaded_connectors.append(Namespace(**item))

    def test_module_parameters(self, *args):
        arguments = dict(
            service_template="app-svcs-int-v2.0-default",
            connector="foo",
            name="bar",
            parameters=load_fixture('create_iworkflow_service.json'),
            tenant="tenant-foo",
            state="present"
        )
        with patch.object(Parameters, '_get_connector_collection') as mo:
            mo.return_value = self.loaded_connectors
            p = Parameters(arguments)

            assert p.name == 'bar'

            # Check that tenant is correct
            assert 'link' in p.tenantTemplateReference
            assert p.tenantTemplateReference['link'] == \
                'https://localhost/mgmt/cm/cloud/tenant/templates/iapp/app-svcs-int-v2.0-default'

            # Check that cloud connector is correct
            assert len(p.connector) == 1
            assert p.connector[0]['id'] == 'cloudConnectorReference'
            assert p.connector[0]['value'] == \
                'https://localhost/mgmt/cm/cloud/connectors/local/212301e6-6d01-4509-bfe3-8e372e792fb0'

            # Check that vars are correct
            assert len(p.vars) == 3
            assert p.vars[0]['name'] == 'pool__addr'
            assert p.vars[0]['value'] == '172.27.1.10'
            assert p.vars[1]['name'] == 'pool__port'
            assert p.vars[1]['value'] == '900'
            assert p.vars[2]['name'] == 'vs__ProfileClientProtocol'
            assert p.vars[2]['value'] == 'tcp'

            # Check that tables are correct
            assert len(p.tables) == 1
            assert 'name' in p.tables[0]
            assert 'section' in p.tables[0]
            assert 'columnNames' in p.tables[0]
            assert 'rows' in p.tables[0]

            assert p.tables[0]['name'] == 'pool__Members'
            assert p.tables[0]['section'] == 'pool'
            assert p.tables[0]['columnNames'] == ['IPAddress', 'Port']

            assert len(p.tables[0]['rows']) == 2
            assert len(p.tables[0]['rows'][0]) == 2
            assert p.tables[0]['rows'][0] == ['20.0.1.11', '80']
            assert p.tables[0]['rows'][1] == ['20.0.1.12']
            assert p.tables[0]['rows'][0][0] == '20.0.1.11'
            assert p.tables[0]['rows'][0][1] == '80'
            assert p.tables[0]['rows'][1][0] == '20.0.1.12'
