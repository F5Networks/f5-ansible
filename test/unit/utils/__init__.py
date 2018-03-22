# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import re
import sys
import imp
import importlib
from collections import OrderedDict
from importlib import SourceFileLoader

LIBRARY_MAP = OrderedDict({
    'ansible.modules.network.f5': 'library.modules',
    'ansible.modules.network': 'library.modules',
    'ansible.modules': 'library.modules',
    'ansible.module_utils.network': 'library.module_utils.network'
})


class AnsibleImporter(object):
    def __init__(self, prefix):
        print("Creating AnsibleImportFinder for {0}".format(prefix))
        self.prefix = prefix

    def find_module(self, fullname, path=None):
        print('NoisyMetaImportFinder looking for "%s" with path "%s"' % (fullname, path))
        name_parts = fullname.split('.')
        if name_parts and name_parts[0] == self.prefix:
            print(' ... found prefix, returning loader')
            return NoisyMetaImportLoader(path)
        else:
            print(' ... not the right prefix, cannot load')
        return None


class NoisyMetaImportLoader(object):
    def __init__(self, path_entry):
        self.path_entry = path_entry
        return

    def load_module(self, fullname):
        print('loading %s' % fullname)
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            mod = sys.modules.setdefault(fullname, importlib.import_module(fullname))

        print(mod)
        return

        package = '.'.join(fullname.split('.')[:-1])
        code = self.get_code(fullname)

        # Set a few properties required by PEP 302
        mod.__file__ = fullname
        mod.__name__ = fullname
        mod.__loader__ = self

        ispkg = self.is_package(package)
        if ispkg:
            mod.__path__ = ['path-entry-goes-here']
            mod.__package__ = fullname
        else:
            mod.__package__ = package

        exec(code, mod.__dict__)
        return mod

    def is_package(self, package):
        if package == 'ansible.modules.network.f5':
            return True
        elif package == 'units.modules':
            return True
        return False

    def get_code(self, fullname):
        pattern = re.compile('|'.join(LIBRARY_MAP.keys()))
        result = pattern.sub(lambda x: LIBRARY_MAP[x.group()], fullname)

        print(result)
        ok = imp.find_module(result)
        print(sys.path, ok)
        file = '/here/' + result.replace('.', '/') + '.py'
        print(file)
        fh = open(file)
        return fh.read()


#sys.meta_path.append(AnsibleImporter('ansible'))
