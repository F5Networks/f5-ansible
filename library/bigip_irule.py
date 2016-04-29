#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: bigip_irule
short_description: Manage iRules across different modules on a BIG-IP
description:
  - Manage iRules across different modules on a BIG-IP
version_added: "2.2"
options:
  content:
    description:
      - When used instead of 'src', sets the contents of an iRule directly to
        the specified value. This is for simple values, but can be used with
        lookup plugins for anything complex or with formatting. Either one
        of C(src) or C(content) must be provided.
  connection:
    description:
      - The connection used to interface with the BIG-IP
    required: false
    default: smart
    choices:
      - rest
      - soap
  server:
    description:
      - BIG-IP host
    required: true
  password:
    description:
      - BIG-IP password
    required: true
  module:
    description:
      - The BIG-IP module to add the iRule to
    required: true
    choices:
      - ltm
      - gtm
      - pem
  partition:
    description:
      - The partition to create the iRule on
    required: false
    default: Common
  name:
    description:
      - The name of the iRule
    required: true
  user:
    description:
      - BIG-IP username
    required: true
  src:
    description:
      - The iRule file to interpret and upload to the BIG-IP. Either one
        of C(src) or C(content) must be provided.
    required: true
  state:
    description:
      - Whether the iRule should exist or not
    required: false
    default: present
    choices:
      - present
      - absent
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
  - Requires the bigsuds Python package on the host if using the iControl
    interface. This is as easy as pip install bigsuds
  - Requires the requests Python package on the host. This is as easy as
    pip install requests
requirements:
    - bigsuds
    - requests
author:
    - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Add the iRule contained in templated irule.tcl to the LTM module
  bigip_irule:
      content: "{{ lookup('template', 'irule-template.tcl') }}"
      module: "ltm"
      name: "MyiRule"
      password: "secret"
      server: "lb.mydomain.com"
      state: "present"
      user: "admin"
  delegate_to: localhost

- name: Add the iRule contained in static file irule.tcl to the LTM module
  bigip_irule:
      module: "ltm"
      name: "MyiRule"
      password: "secret"
      server: "lb.mydomain.com"
      src: "irule-static.tcl"
      state: "present"
      user: "admin"
  delegate_to: localhost
'''

RETURN = '''
full_name:
    description: Full name of the user
    returned: changed and success
    type: string
    sample: "John Doe"
'''

import json

STATES = ['absent', 'present']
MODULES = ['gtm', 'ltm', 'pem']


class CreateRuleError(Exception):
    pass


class DeleteRuleError(Exception):
    pass


class ContentOrSrcRequiredError(Exception):
    pass


class BigIpApiFactory(object):
    def factory(module):
        type = module.params.get('connection')

        if type == "rest":
            if not requests_found:
                raise Exception("The python requests module is required")
            return BigIpRestApi(check_mode=module.check_mode, **module.params)
        elif type == "soap":
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")
            return BigIpSoapApi(check_mode=module.check_mode, **module.params)

    factory = staticmethod(factory)


class BigIpCommon(object):
    def __init__(self, *args, **kwargs):
        self.result = dict(changed=False, changes=dict())

        self.params = kwargs

        if self.params['state'] != 'absent':
            if not self.params['content'] and not self.params['src']:
                raise ContentOrSrcRequiredError()

        source = self.params['src']
        if source:
            fh = open(source)
            self.params['content'] = fh.read()
            fh.close()

    def flush(self):
        result = dict()
        state = self.params['state']

        if state == "present":
            if self.params['check_mode']:
                current = self.read()

            else:
                changed = self.present()
                current = self.read()
                result.update(current)
        else:
            changed = self.absent()

        result.update(dict(changed=changed))
        return result


class BigIpSoapApi(BigIpCommon):
    """Manipulate user accounts via SOAP
    """

    def __init__(self, *args, **kwargs):
        super(BigIpSoapApi, self).__init__(*args, **kwargs)

        self.api = bigip_api(kwargs['server'],
                             kwargs['user'],
                             kwargs['password'],
                             kwargs['validate_certs'])
        self.irule = "/%s/%s" % (kwargs['partition'], kwargs['name'])

    def exists(self):
        module = self.params['module']
        partition = self.params['partition']

        with bigsuds.Transaction(self.api):
            # need to switch to root, set recursive query state
            current_folder = self.api.System.Session.get_active_folder()
            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder='/' + partition)

            current_query_state = self.api.System.Session.get_recursive_query_state()
            if current_query_state == 'STATE_DISABLED':
                self.api.System.Session.set_recursive_query_state('STATE_ENABLED')

            if module == 'ltm':
                rules = self.api.LocalLB.Rule.get_list()
            elif module == 'gtm':
                rules = self.api.GlobalLB.Rule.get_list()
            else:
                rules = self.api.PEM.Policy.get_list()

            # set everything back
            if current_query_state == 'STATE_DISABLED':
                self.api.System.Session.set_recursive_query_state('STATE_DISABLED')

            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder=current_folder)

        if self.irule in rules:
            return True
        else:
            return False

    def read(self):
        result = {}

        module = self.params['module']

        if module == 'ltm':
            irule = self.api.LocalLB.Rule.query_rule(rule_names=[self.irule])
        elif module == 'gtm':
            irule = self.api.GlobalLB.Rule.query_rule(rule_names=[self.irule])
        else:
            irule = self.api.PEM.Policy.query_rule(rule_names=[self.irule])

        result['name'] = irule[0]['rule_name']

        if 'rule_definition' in irule[0]:
            result['definition'] = irule[0]['rule_definition'].strip()
        else:
            result['definition'] = ''

        return result

    def absent(self):
        module = self.params['module']
        partition = self.params['partition']

        if not self.exists():
            return False

        if self.params['check_mode']:
            return True

        with bigsuds.Transaction(self.api):
            # need to switch to root, set recursive query state
            current_folder = self.api.System.Session.get_active_folder()
            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder='/' + partition)

            current_query_state = self.api.System.Session.get_recursive_query_state()
            if current_query_state == 'STATE_DISABLED':
                self.api.System.Session.set_recursive_query_state('STATE_ENABLED')

            if module == 'ltm':
                self.api.LocalLB.Rule.delete_rule(rule_names=[self.irule])
            elif module == 'gtm':
                self.api.GlobalLB.Rule.delete_rule(rule_names=[self.irule])
            else:
                self.api.PEM.Policy.delete_policy(policies=[self.irule])

            # set everything back
            if current_query_state == 'STATE_DISABLED':
                self.api.System.Session.set_recursive_query_state('STATE_DISABLED')

            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder=current_folder)

        if self.exists():
            raise DeleteRuleError()
        else:
            return True

    def update(self):
        module = self.params['module']
        name = self.params['name']
        content = self.params['content'].strip()
        partition = self.params['partition']

        current = self.read()
        if current['definition'] == content:
            return False

        rules = dict(
            rule_name=name,
            rule_definition=content
        )

        if self.params['check_mode']:
            changed = True
        else:
            with bigsuds.Transaction(self.api):
                # need to switch to root, set recursive query state
                current_folder = self.api.System.Session.get_active_folder()
                if current_folder != '/' + partition:
                    self.api.System.Session.set_active_folder(folder='/' + partition)

                current_query_state = self.api.System.Session.get_recursive_query_state()
                if current_query_state == 'STATE_DISABLED':
                    self.api.System.Session.set_recursive_query_state('STATE_ENABLED')

                if module == 'ltm':
                    self.api.LocalLB.Rule.modify_rule(rules=[rules])
                elif module == 'gtm':
                    self.api.GlobalLB.Rule.modify_rule(rules=[rules])
                else:
                    # The PEM SOAP API provides no way to modify a policy.
                    # So to "modify" it we need to delete it and re-create it.
                    self.api.PEM.Policy.delete_policy(policies=[rules])

                # set everything back
                if current_query_state == 'STATE_DISABLED':
                    self.api.System.Session.set_recursive_query_state('STATE_DISABLED')

                if current_folder != '/' + partition:
                    self.api.System.Session.set_active_folder(folder=current_folder)
            changed = True

        return changed

    def create(self):
        partition = self.params['partition']
        module = self.params['module']
        name = self.params['name']
        content = self.params['content'].strip()

        rules = dict(
            rule_name=name,
            rule_definition=content
        )

        with bigsuds.Transaction(self.api):
            current_folder = self.api.System.Session.get_active_folder()
            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder='/' + partition)

            if module == 'ltm':
                self.api.LocalLB.Rule.create(rules=[rules])
            elif module == 'gtm':
                self.api.GlobalLB.Rule.create(rules=[rules])
            else:
                self.api.PEM.Policy.create(rules=[rules])

            if current_folder != '/' + partition:
                self.api.System.Session.set_active_folder(folder=current_folder)

        if self.exists():
            return True
        else:
            raise CreateRuleError()

    def present(self):
        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True

            return self.create()


class BigIpRestApi(BigIpCommon):
    """Manipulate iRules via REST

    {
      "kind": "tm:ltm:rule:rulestate",
      "name": "foobar",
      "partition": "Common",
      "fullPath": "/Common/foobar",
      "generation": 1,
      "selfLink": "https://localhost/mgmt/tm/ltm/rule/~Common~foobar",
      "apiAnonymous": "nodelete nowrite \nwhen HTTP_REQUEST {\n",
      "apiRawValues": {
        "verificationStatus": "signature-verified"
      }
    }
    """

    def __init__(self, *args, **kwargs):
        super(BigIpRestApi, self).__init__(*args, **kwargs)

        server = self.params['server']
        module = self.params['module']

        # REST endpoints look like this
        #
        #    https://localhost/mgmt/tm/ltm/rule/~Common~irule_name?ver=11.6.0"

        if module == 'ltm':
            self._uri = 'https://%s/mgmt/tm/ltm/rule' % (server)
        elif module == 'gtm':
            self._uri = 'https://%s/mgmt/tm/gtm/rule' % (server)
        else:
            self._uri = 'https://%s/mgmt/tm/pem/rules' % (server)

        self._headers = {
            'Content-Type': 'application/json'
        }

    def read(self):
        result = {}

        user = self.params['user']
        password = self.params['password']
        validate_certs = self.params['validate_certs']
        partition = self.params['partition']
        name = self.params['name']

        url = "%s/~%s~%s" % (self._uri, partition, name)
        resp = requests.get(url,
                            auth=(user, password),
                            verify=validate_certs)

        if resp.status_code == 200:
            res = resp.json()

            result['name'] = res['name']

            if 'apiAnonymous' in res:
                result['definition'] = res['apiAnonymous'].strip()
            else:
                result['definition'] = ''

        return result

    def exists(self):
        user = self.params['user']
        password = self.params['password']
        validate_certs = self.params['validate_certs']
        partition = self.params['partition']
        name = self.params['name']

        url = "%s/~%s~%s" % (self._uri, partition, name)
        resp = requests.get(url,
                            auth=(user, password),
                            verify=validate_certs)

        if resp.status_code != 200:
            return False
        else:
            return True

    def present(self):
        if self.exists():
            return self.update()
        else:
            if self.params['check_mode']:
                return True
            return self.create()

    def update(self):
        user = self.params['user']
        password = self.params['password']
        validate_certs = self.params['validate_certs']
        partition = self.params['partition']
        name = self.params['name']
        content = self.params['content'].strip()

        current = self.read()
        if current['definition'] == content:
            return False
        else:
            payload = dict(
                apiAnonymous=content
            )

        if self.params['check_mode']:
            return True

        url = "%s/~%s~%s" % (self._uri, partition, name)
        resp = requests.patch(url,
                              auth=(user, password),
                              data=json.dumps(payload),
                              verify=validate_certs,
                              headers=self._headers)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def create(self):
        user = self.params['user']
        password = self.params['password']
        validate_certs = self.params['validate_certs']
        partition = self.params['partition']
        name = self.params['name']
        content = self.params['content'].strip()

        payload = dict(
            name=name,
            apiAnonymous=content,
            partition=partition
        )

        resp = requests.post(self._uri,
                             auth=(user, password),
                             data=json.dumps(payload),
                             verify=validate_certs,
                             headers=self._headers)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])

    def absent(self):
        user = self.params['user']
        password = self.params['password']
        validate_certs = self.params['validate_certs']
        partition = self.params['partition']
        name = self.params['name']

        if not self.exists():
            return False

        if self.params['check_mode']:
            return True

        uri = "%s/~%s~%s" % (self._uri, partition, name)
        resp = requests.delete(uri,
                               auth=(user, password),
                               verify=validate_certs)
        if resp.status_code == 200:
            return True
        else:
            res = resp.json()
            raise Exception(res['message'])


def main():
    argument_spec = f5_argument_spec()

    meta_args = dict(
        content=dict(required=False),
        src=dict(required=False),
        name=dict(required=True),
        module=dict(required=True, choices=MODULES),
        state=dict(default='present', choices=STATES),
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ['content', 'src']
        ]
    )

    try:
        obj = BigIpApiFactory.factory(module)
        result = obj.flush()

        module.exit_json(**result)
    except bigsuds.ConnectionError:
        module.fail_json(msg="Could not connect to BIG-IP host")
    except requests.exceptions.SSLError:
        module.fail_json(msg='Certificate verification failed. Consider using validate_certs=no')

from ansible.module_utils.basic import *
from ansible.module_utils.f5 import *

if __name__ == '__main__':
    main()
