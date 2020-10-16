# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import sys
import uuid
import re

from time import time
from datetime import datetime

from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError

from .constants import (
    TEEM_ENDPOINT, TEEM_KEY, TEEM_TIMEOUT, TEEM_VERIFY,
    CURRENT_COLL_VERSION, BASE_HEADERS, PLATFORM
)


class TeemClient(object):
    def __init__(self, start_time, module, version):
        self.module_name = module._name
        self.ansible_version = module.ansible_version
        self.version = version
        self.start_time = start_time

    def prepare_request(self):
        asset_id = str(uuid.uuid4())
        user_agent = 'F5_MODULES{0}'.format(CURRENT_COLL_VERSION)
        telemetry = self.build_telemetry()
        url = 'https://%s/ee/v1/telemetry' % TEEM_ENDPOINT
        headers = {
            'F5-ApiKey': TEEM_KEY,
            'F5-DigitalAssetId': asset_id,
            'F5-TraceId': str(uuid.uuid4()),
            'User-Agent': user_agent
        }
        headers.update(BASE_HEADERS)
        data = {
            'digitalAssetName': 'F5_MODULES',
            'digitalAssetVersion': CURRENT_COLL_VERSION,
            'digitalAssetId': asset_id,
            'documentType': 'F5_MODULES Ansible Collection',
            'documentVersion': '1',
            'observationStartTime': self.start_time,
            'observationEndTime': datetime.now().isoformat(),
            'epochTime': time(),
            'telemetryId': str(uuid.uuid4()),
            'telemetryRecords': telemetry
        }

        return url, headers, data

    def send(self):
        url, headers, data = self.prepare_request()
        payload = json.dumps(data)
        try:
            response = open_url(
                url=url,
                method='POST',
                headers=headers,
                timeout=TEEM_TIMEOUT,
                validate_certs=TEEM_VERIFY,
                data=payload
            )
        except HTTPError:
            return False
        ok = re.search(r'20[01-4]', str(response.code))
        if ok:
            return True
        return False

    def build_telemetry(self):
        platform = PLATFORM.get(self.module_name.split('_')[0], '')
        python_version = sys.version.split(' ')[0]

        return [{
            'CollectionName': 'F5_MODULES',
            'CollectionVersion': CURRENT_COLL_VERSION,
            'CollectionModuleName': self.module_name,
            'f5Platform': platform,
            'f5SoftwareVersion': self.version,
            'ControllerAnsibleVersion': self.ansible_version,
            'ControllerPythonVersion': python_version
        }]


def send_teem(start_time, module, version=None):
    """ Sends Teem Data if allowed."""
    if module.params['provider']['no_f5_teem'] is True:
        return False
    teem = TeemClient(start_time, module, version)
    teem.send()
