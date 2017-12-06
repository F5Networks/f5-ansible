#!/usr/bin/python

import os


def abspath(file):
    return os.path.abspath(file)


class FilterModule(object):
    def filters(self):
        return {
            'abspath': abspath
        }
