#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests import unittest
from library.module_utils.network.f5.common import AnsibleF5Parameters


class TestRegular(unittest.TestCase):
    class Foo(AnsibleF5Parameters):
        @property
        def dns(self):
            return self._values['dns']

        @dns.setter
        def dns(self, value):
            self._values['dns'] = value

        @property
        def lb_method(self):
            return self._values['lb_method']

        @lb_method.setter
        def lb_method(self, value):
            self._values['lb_method'] = value

    def test_run(self):
        args = dict(
            dns='alice',
            lb_method='bob'
        )
        test = TestRegular.Foo(params=args)
        assert test.dns == 'alice'
        assert test.lb_method == 'bob'


class TestKeysWithPunctuation(unittest.TestCase):
    class Foo(AnsibleF5Parameters):
        api_map = {
            'dns.proxy.__iter__': 'bar'
        }

        @property
        def bar(self):
            return self._values['bar']

        @bar.setter
        def bar(self, value):
            self._values['bar'] = value

        @property
        def baz(self):
            return self._values['baz']

        @baz.setter
        def baz(self, value):
            self._values['baz'] = value

    def test_run(self):
        args = {
            'dns.proxy.__iter__': 'alice',
            'baz': 'bob'
        }
        test = TestKeysWithPunctuation.Foo(params=args)
        assert test.bar == 'alice'
        assert test.baz == 'bob'
        assert 'dns.proxy.__iter__' not in test._values


class TestInheritence(unittest.TestCase):
    class Baz(AnsibleF5Parameters):
        @property
        def baz(self):
            return self._values['baz']

        @baz.setter
        def baz(self, value):
            self._values['baz'] = value

    class Bar(Baz):
        @property
        def bar(self):
            return self._values['bar']

        @bar.setter
        def bar(self, value):
            self._values['bar'] = value

    class Foo(Bar):
        @property
        def foo(self):
            return self._values['foo']

        @foo.setter
        def foo(self, value):
            self._values['foo'] = value

    def test_run(self):
        args = {
            'foo': 'alice',
            'bar': 'bob',
            'baz': 'carol',
            'dns.proxy.__iter__': 'dan',
        }
        test = TestInheritence.Foo(params=args)
        assert test.foo == 'alice'
        assert test.bar == 'bob'
        assert test.baz == 'carol'


class TestNoProperties(unittest.TestCase):
    class Foo(AnsibleF5Parameters):
        pass

    def test_run(self):
        args = dict(
            dns='alice',
            lb_method='bob'
        )
        test = TestNoProperties.Foo(params=args)
        assert test.dns == 'alice'
        assert test.lb_method == 'bob'


class TestReferenceAnother(unittest.TestCase):
    class Foo(AnsibleF5Parameters):
        @property
        def poolLbMode(self):
            return self.lb_method

        @poolLbMode.setter
        def poolLbMode(self, value):
            self.lb_method = value

        @property
        def lb_method(self):
            return self._values['lb_method']

        @lb_method.setter
        def lb_method(self, value):
            self._values['lb_method'] = value

    def test_run(self):
        args = dict(
            lb_method='bob'
        )
        test = TestReferenceAnother.Foo(params=args)
        assert test.lb_method == 'bob'
        assert test.poolLbMode == 'bob'


class TestMissingAttrSetter(unittest.TestCase):
    class Foo(AnsibleF5Parameters):
        @property
        def reject(self):
            return self._values['reject']

        @property
        def destination(self):
            return self._values['destination']

    def test_run(self):
        args = dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            destination='10.10.10.10',
            reject='yes'
        )
        test = TestMissingAttrSetter.Foo(params=args)
        assert test.destination == '10.10.10.10'
        assert test.reject == 'yes'


class TestAssureNoInstanceAttributes(unittest.TestCase):
    class Foo(AnsibleF5Parameters):
        @property
        def reject(self):
            return self._values['reject']

    def test_run(self):
        args = dict(
            name='test-route',
            password='admin',
            server='localhost',
            user='admin',
            state='present',
            destination='10.10.10.10',
            reject='yes'
        )
        test = TestAssureNoInstanceAttributes.Foo(params=args)
        assert test.destination == '10.10.10.10'
        assert test.reject == 'yes'
        assert 'destination' not in dir(test)
