#!/usr/bin/python

import q
import os


def q_debug(value):
    q.q(value)


class FilterModule(object):
    def filters(self):
        return {
            'q': d_debug
        }
