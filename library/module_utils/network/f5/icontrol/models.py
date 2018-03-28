# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class Request(object):
    """
            req = Request(url=url, data=data, json=json, **kwargs)
        req.prepare_authentication_headers()

    """
    def __init__(self, method=None, url=None, headers=None, data=None,
                 params=None, auth=None, cookies=None, json=None):
        pass

    def json(self):
        if not data and json is not None:
            content_type = 'application/json'
            body = json.dumps(json)
            if not isinstance(body, bytes):
                body = body.encode('utf-8')
        if content_type and ('Content-Type' not in headers):
            headers['Content-Type'] = content_type
