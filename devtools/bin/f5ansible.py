#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import click


class Root(object):
    def __init__(self, debug=False):
        self.debug = debug


@click.group()
@click.option('--debug/--no-debug', default=False,
              envvar='F5ANSIBLE_DEBUG')
@click.pass_context
def cli(ctx, debug):
    ctx.obj = Root(debug)


@cli.command(name='module-upstream')
@click.argument('module', required=True)
@click.option('--upstream-dir',
              default='local/ansible', show_default=True)
def module_upstream(module, upstream_dir):
    pass

@cli.command(name='module-stub')
@click.argument('module', required=True)
def module_stub(module):
    pass

if __name__ == '__main__':
    # module-upstream module-name,
    # module-stub list of module names
    # module-unstub list of module names
    # issue-stub (issue number, module)
    # issue-unstub (issue number, module)
    # container-run (name)
    # container-build (all, specific list)
    # container-fetch
    # test-integration (python ver, bigip ver, list of modules; default all)
    # test-unit --sdk --no-sdk
    cli()
