# (c) 2013, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: Select a random license key from a file and remove it from future lookups
    author: Tim Rupp <caphrim007@gmail.com>
    version_added: "2.5"
    short_description: Return random license from list
    description:
      - Select a random license key from a file and remove it from future lookups
      - Can optionally remove the key if C(remove=True) is specified
"""

EXAMPLES = """
- name: Get a regkey license from a stash
  bigiq_regkey_license:
    key: "{{ lookup('license_hopper', 'filename=/path/to/licenses.txt') }}"
    state: present
    pool: regkey1 
"""

RETURN = """
  _raw:
    description:
      - random item
"""

import random

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.plugins.lookup import LookupBase
from ansible.parsing.splitter import parse_kv


class LookupModule(LookupBase):
    def __init__(self, loader=None, templar=None, **kwargs):

        super(LookupModule, self).__init__(loader, templar, **kwargs)

        self.filename = None
        self.remove = False

    def parse_kv_args(self, args):
        """
        parse key-value style arguments
        """

        for arg in ["filename"]:
            arg_raw = args.pop(arg, None)
            try:
                if arg_raw is None:
                    continue
                parsed = str(arg_raw)
                setattr(self, arg, parsed)
            except ValueError:
                raise AnsibleError(
                    "can't parse arg {}={} as string".format(arg, arg_raw)
                )
        if args:
            raise AnsibleError(
                "unrecognized arguments to with_sequence: %r" % args.keys()
            )

    def run(self, terms, variables=None, **kwargs):
        ret = []

        for term in terms:
            self.parse_kv_args(parse_kv(term))

            lookupfile = self.find_file_in_search_path(variables, 'files', self.filename)
            fh = open(lookupfile, 'r')
            lines = fh.readlines()
            fh.close()
            print("ASASD")
            try:
                ret = [random.choice(lines)]
            except Exception as e:
                raise AnsibleError("Unable to choose random license: %s" % to_native(e))

            if self.remove:
                to_write = [x for x in lines if x != ret[0]]
                fh = open(lookupfile, 'w')
                fh.writelines(to_write)
        return ret
