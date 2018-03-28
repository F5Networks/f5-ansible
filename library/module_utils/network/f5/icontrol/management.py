# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from library.module_utils.network.f5.icontrol.models import Request
from library.module_utils.network.f5.icontrol.models import Response


class Management(object):

    def get(self, url, **kwargs):
        """Sends a HTTP GET command to an F5 REST Server.

        Use this method to send a GET command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
            \*\*kwargs (dict): Dictionary containing other information that may need to be
                sent to the request. Typically this contains extra headers, or headers that the
                caller wants to override, such as the Content-Type.
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        if self.debug:
            self._debug_output.append(debug_prepared_request(url, 'GET', headers))
        try:
            response = open_url(
                url, method='GET', headers=headers, validate_certs=self._validate_certs
            )
            result = Response(response=response)
            return result
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise F5ModuleError("Exception at line {0}, of file {1}, with error '{2}'".format(exc_tb.tb_lineno, fname, str(ex)))

    def patch(self, url, data=None, json=None, **kwargs):
        """Sends a HTTP PATCH command to an F5 REST Server.

        Use this method to send a PATCH command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
            data (bytes): An object specifying additional data to send to the server,
                or ``None`` if no such data is needed. Currently HTTP requests are the
                only ones that use data. The supported object types include bytes,
                file-like objects, and iterables.
                See https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
            \*\*kwargs (dict): Dictionary containing other information that may need to be
                sent to the request. Typically this contains extra headers, or headers that the
                caller wants to override, such as the Content-Type.
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        if self.debug:
            self._debug_output.append(debug_prepared_request(url, 'PATCH', headers, data))
        try:
            response = open_url(
                url, method='PATCH', data=data, headers=headers,
                validate_certs=self._validate_certs
            )
            return Response(response=response)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise F5ModuleError("Exception at line {0}, of file {1}, with error '{2}'".format(exc_tb.tb_lineno, fname, str(ex)))

    def post(self, url, data=None, json=None, **kwargs):
        """Sends a HTTP POST command to an F5 REST Server.

        Use this method to send a POST command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
            data (bytes): An object specifying additional data to send to the server,
                or ``None`` if no such data is needed. Currently HTTP requests are the
                only ones that use data. The supported object types include bytes,
                file-like objects, and iterables.
                See https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
            \*\*kwargs (dict): Dictionary containing other information that may need to be
                sent to the request. Typically this contains extra headers, or headers that the
                caller wants to override, such as the Content-Type.
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        if self.debug:
            self._debug_output.append(debug_prepared_request(url, 'POST', headers, data))
        try:
            response = open_url(
                url, method='POST', data=data, headers=headers,
                validate_certs=self._validate_certs
            )
            return Response(response=response)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise F5ModuleError("Exception at line {0}, of file {1}, with error '{2}'".format(exc_tb.tb_lineno, fname, str(ex)))

    def put(self, url, data=None, json=None, **kwargs):
        """Sends a HTTP PUT command to an F5 REST Server.

        Use this method to send a PUT command to an F5 product.

        Args:
            url (string): Path of URL on the server to call.
            data (bytes): An object specifying additional data to send to the server,
                or ``None`` if no such data is needed. Currently HTTP requests are the
                only ones that use data. The supported object types include bytes,
                file-like objects, and iterables.
                See https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
            \*\*kwargs (dict): Dictionary containing other information that may need to be
                sent to the request. Typically this contains extra headers, or headers that the
                caller wants to override, such as the Content-Type.
        """
        headers = self.get_headers(**kwargs)
        url = self.get_full_url(url)
        if self.debug:
            self._debug_output.append(debug_prepared_request(url, 'PUT', headers, data))
        try:
            response = open_url(
                url, method='PUT', data=data, headers=headers,
                validate_certs=self._validate_certs
            )
            return Response(response=response)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise F5ModuleError("Exception at line {0}, of file {1}, with error '{2}'".format(exc_tb.tb_lineno, fname, str(ex)))

    def request(self):
