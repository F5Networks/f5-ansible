# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

from datetime import datetime

from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import patch, Mock, mock_open
from ansible_collections.f5networks.f5_modules.plugins.module_utils.constants import TEEM_KEY
from ansible_collections.f5networks.f5_modules.plugins.module_utils.teem import (
    TeemClient, determine_environment, generate_asset_id, in_docker, in_cicd
)
from ansible_collections.f5networks.f5_modules.plugins.module_utils.version import CURRENT_COLL_VERSION


class FakeHTTPResponse:
    def __init__(self, value):
        self.value = value

    @property
    def code(self):
        return self.value


class TestTeemClient(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.now().isoformat()
        self.fake_module = Mock()
        self.fake_module.ansible_version = '2.10'
        self.python_version = sys.version.split(' ', maxsplit=1)[0]

    @patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.in_cicd', new_callable=Mock())
    def test_teem_client_build_telemetry_no_docker_no_cicd(self, m):
        m.return_value = (False, None)
        self.fake_module._name = 'bigip_fake'
        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        result = teem.build_telemetry()

        assert result[0]['CollectionName'] == 'F5_MODULES'
        assert result[0]['CollectionVersion'] == CURRENT_COLL_VERSION
        assert result[0]['CollectionModuleName'] == 'bigip_fake'
        assert result[0]['f5Platform'] == 'BIG-IP'
        assert result[0]['f5SoftwareVersion'] == '15.1.1'
        assert result[0]['ControllerAnsibleVersion'] == '2.10'
        assert result[0]['ControllerPythonVersion'] == self.python_version
        assert result[0]['ControllerAsDocker'] is False
        assert result[0]['DockerHostname'] == 'none'
        assert result[0]['RunningInCiEnv'] is False
        assert result[0]['CiEnvName'] == 'none'

    @patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.socket.gethostname', new_callable=Mock())
    @patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.in_cicd', new_callable=Mock())
    def test_teem_client_build_telemetry_with_docker_in_cicd(self, m1, m2):
        m1.return_value = (True, 'FOO-CI/CD')
        m2.return_value = '8fc719d06c9e'
        self.fake_module._name = 'bigip_fake'
        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        with patch.object(teem, 'docker', True):
            result = teem.build_telemetry()

        assert result[0]['CollectionName'] == 'F5_MODULES'
        assert result[0]['CollectionVersion'] == CURRENT_COLL_VERSION
        assert result[0]['CollectionModuleName'] == 'bigip_fake'
        assert result[0]['f5Platform'] == 'BIG-IP'
        assert result[0]['f5SoftwareVersion'] == '15.1.1'
        assert result[0]['ControllerAnsibleVersion'] == '2.10'
        assert result[0]['ControllerPythonVersion'] == self.python_version
        assert result[0]['ControllerAsDocker'] is True
        assert result[0]['DockerHostname'] == '8fc719d06c9e'
        assert result[0]['RunningInCiEnv'] is True
        assert result[0]['CiEnvName'] == 'FOO-CI/CD'

    @patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.in_cicd', new_callable=Mock())
    def test_teem_client_prepare_request(self, m):
        m.return_value = (False, None)
        self.fake_module._name = 'bigip_fake'
        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        url, headers, data = teem.prepare_request()

        assert url == 'https://product.apis.f5.com/ee/v1/telemetry'
        assert len(headers) == 5
        assert headers['User-Agent'] == 'F5_MODULES/{0}'.format(CURRENT_COLL_VERSION)
        assert headers['F5-ApiKey'] == TEEM_KEY
        assert len(data) == 10
        assert data['digitalAssetVersion'] == CURRENT_COLL_VERSION
        assert data['observationStartTime'] == self.start_time

    @patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.in_cicd', new_callable=Mock())
    @patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.open_url')
    def test_teem_client_send(self, patched, m):
        m.return_value = (False, None)
        self.fake_module._name = 'bigip_fake'
        patched.return_value = FakeHTTPResponse(200)

        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        teem.send()

        assert patched.call_args[1]['url'] == 'https://product.apis.f5.com/ee/v1/telemetry'
        assert patched.call_args[1]['headers']['User-Agent'] == 'F5_MODULES/{0}'.format(CURRENT_COLL_VERSION)
        assert patched.call_args[1]['headers']['F5-ApiKey'] == TEEM_KEY
        assert CURRENT_COLL_VERSION in patched.call_args[1]['data']
        assert self.start_time in patched.call_args[1]['data']

    def test_teem_get_platform_fq_name(self):
        self.fake_module._name = 'f5networks.f5_modules.bigip_fake'
        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        result = teem.get_platform()

        assert result == 'BIG-IP'
        assert teem.module_name == 'bigip_fake'

    def test_teem_get_platform_fq_name_platform_not_found(self):
        self.fake_module._name = 'f5networks.f5_modules.foobar_fake'
        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        result = teem.get_platform()

        assert result == 'unknown'
        assert teem.module_name == 'foobar_fake'

    def test_teem_get_platform_short_name(self):
        self.fake_module._name = 'bigiq_fake'
        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        result = teem.get_platform()

        assert result == 'BIG-IQ'
        assert teem.module_name == 'bigiq_fake'

    def test_teem_get_platform_short_name_platform_not_found(self):
        self.fake_module._name = 'foobar_fake'
        teem = TeemClient(self.start_time, self.fake_module, '15.1.1')
        result = teem.get_platform()

        assert result == 'unknown'
        assert teem.module_name == 'foobar_fake'


class TestOtherFunctions(unittest.TestCase):
    def test_determine_environment_drone(self):
        def mock_os_env_return(value):
            if value == 'DRONE':
                return True
            return False

        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.os.getenv') as env:
            env.side_effect = mock_os_env_return
            result = determine_environment()

        assert result == 'Drone CI'

    def test_determine_environment_codeship(self):
        def mock_os_env_return(value):
            if value == 'CI_NAME':
                return 'codeship'
            return False

        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.os.getenv') as env:
            env.side_effect = mock_os_env_return
            result = determine_environment()

        assert result == 'CodeShip CI'

    def test_determine_environment_codeship_invalid_value(self):
        def mock_os_env_return(value):
            if value == 'CI_NAME':
                return 'otherci'
            return False

        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.os.getenv') as env:
            env.side_effect = mock_os_env_return
            result = determine_environment()

        assert result is None

    @patch(
        'builtins.open', mock_open(
            read_data='14:name=systemd:/docker/8fc719d06c9e3\n13:rdma:/\n12:pids:/docker/8fc719d06c9e3\n'
        )
    )
    def test_in_docker_true(self):
        result = in_docker()

        assert result is True

    @patch('builtins.open', mock_open(read_data='14:name=systemd:/8fc719d06c9e3\n13:rdma:/\n'))
    def test_in_docker_false(self):
        result = in_docker()

        assert result is False

    @patch('builtins.open', new_callable=mock_open)
    def test_in_docker_except(self, mo):
        ioerror = mo.return_value
        ioerror.read.side_effect = IOError('[Errno 2] No such file or directory')
        result = in_docker()

        assert result is False

    def test_in_cicd_true(self):
        def mock_os_env_return(value):
            if value == 'TF_BUILD':
                return True
            return False

        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.os.getenv') as env:
            env.side_effect = mock_os_env_return
            ok, env = in_cicd()

        assert ok is True
        assert env == 'Azure Pipelines'

    def test_in_cicd_false(self):
        def mock_os_env_return(value):
            return False

        with patch('ansible_collections.f5networks.f5_modules.plugins.module_utils.teem.os.getenv') as env:
            env.side_effect = mock_os_env_return
            ok, env = in_cicd()

        assert ok is False
        assert env is None

    def test_generate_asset_id(self):
        fake_host = '8fc719d06c9e'
        result1 = generate_asset_id(fake_host)
        result2 = generate_asset_id(fake_host)
        result3 = generate_asset_id(fake_host)

        assert result1 == result2 == result3
