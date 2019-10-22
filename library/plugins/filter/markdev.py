#!/usr/bin/python


class FilterModule(object):
    def filters(self):
        return {
            'verchg': self.mark_devel
        }

    def mark_devel(self, var):
        result = var.split('-')[0] + '-devel'
        return result

