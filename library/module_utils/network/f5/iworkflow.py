# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.network.f5.common import F5BaseClient


class F5Client(F5BaseClient):
    @property
    def mgmt(self):
        return iWorkflowMgmt(
            self.params['server'],
            self.params['user'],
            self.params['password'],
            port=self.params['server_port'],
            token='local'
        )
