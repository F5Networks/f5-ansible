#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import sys

TASKS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, TASKS_DIR)


from tasks.lib.plugin_formatter import main as _main


def main():
    _main()


if __name__ == '__main__':
    main()
