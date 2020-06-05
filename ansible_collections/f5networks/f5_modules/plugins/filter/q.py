
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import q
import os


def q_debug(value):
    q.q(value)


class FilterModule(object):
    def filters(self):
        return {
            'q': q_debug
        }
