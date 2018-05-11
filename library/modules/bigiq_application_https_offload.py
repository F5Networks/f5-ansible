#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigiq_application_https_offload
short_description: Manages BIG-IQ HTTPS offload applications
description:
  - Manages BIG-IQ applications used for load balancing an HTTPS application on
    port 443 with SSL offloading on BIG-IP.
version_added: 2.6
options:
  name:
    description:
      - Name of the new application.
    required: True
  description:
    description:
      - Description of the application.
  servers:
    description:
      - A list of servers that the application is hosted on.
      - If you are familiar with other BIG-IP setting, you might also refer to this
        list as the list of pool members.
      - When creating a new application, at least one server is required.
    suboptions:
      address:
        description:
          - The IP address of the server.
      port:
        description:
          - The port of the server.
  inbound_virtual:
    description:
      - Settings to configure the virtual which will receive the inbound connection.
      - This virtual will be used to host the HTTPS endpoint of the application.
      - Traffic destined to the C(redirect_virtual) will be offloaded to this
        parameter to ensure that proper redirection from insecure, to secure, occurs.
    suboptions:
      destination:
        description:
          - Specifies destination IP address information to which the virtual server
            sends traffic. 
          - This parameter is required when creating a new application.
      netmask:
        description:
          - Specifies the netmask to associate with the given C(destination).
          - This parameter is required when creating a new application. 
      port:
        description:
          - The port that the virtual listens for connections on.
          - When creating a new application, if this parameter is not specified, the
            default value of C(443) will be used.
  redirect_virtual:
    description:
      - Settings to configure the virtual which will receive the connection to be
        redirected.
      - This virtual will be used to host the HTTP endpoint of the application.
      - Traffic destined to this parameter will be offloaded to the
        C(inbound_virtual) parameter to ensure that proper redirection from insecure,
        to secure, occurs.
    suboptions:
      destination:
        description:
          - Specifies destination IP address information to which the virtual server
            sends traffic. 
          - This parameter is required when creating a new application.
      netmask:
        description:
          - Specifies the netmask to associate with the given C(destination).
          - This parameter is required when creating a new application.
      port:
        description:
          - The port that the virtual listens for connections on.
          - When creating a new application, if this parameter is not specified, the
            default value of C(80) will be used.
  client_ssl_profile:
    description:
      - Specifies the SSL profile for managing client-side SSL traffic.
    suboptions:
      name:
        description:
          - The name of the client SSL profile to created and used.
          - When creating a new application, if this value is not specified, the
            default value of C(clientssl) will be used.
      cert_key_chain:
        description:
          - One or more certificates and keys to associate with the SSL profile.
          - This option is always a list. The keys in the list dictate the details
            of the client/key/chain/passphrase combination.
          - Note that BIG-IPs can only have one of each type of each certificate/key
            type. This means that you can only have one RSA, one DSA, and one ECDSA
            per profile.
          - If you attempt to assign two RSA, DSA, or ECDSA certificate/key combo,
            the device will reject this.
          - This list is a complex list that specifies a number of keys. There are
            several supported keys.
          - When creating a new profile, if this parameter is not specified, the
            default value of C(inherit) will be used.
        suboptions:
          cert:
            description:
              - Specifies a cert name for use.
            required: True
          key:
            description:
              - Specifies a key name.
            required: True
          chain:
            description:
              - Specifies a certificate chain that is relevant to the certificate and
                key mentioned earlier.
              - This key is optional.
          passphrase:
            description:
              - Contains the passphrase of the key file, should it require one.
              - Passphrases are encrypted on the remote BIG-IP device.
  service_environment:
    description:
      - Specifies the name of service environment that the application will be
        deployed to.
      - When creating a new application, this parameter is required.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Load balance an HTTPS application on port 443 with SSL offloading on BIG-IP
  bigiq_application_https_offload:
    name: my-app
    description: Redirect HTTP to HTTPS
    service_environment: my-ssg
    servers:
      - address: 1.2.3.4
        port: 8080
      - address: 5.6.7.8
        port: 8080
    inbound_virtual:
      destination: 2.2.2.2
      netmask: 255.255.255.255
      port: 443
    redirect_virtual:
      destination: 2.2.2.2
      netmask: 255.255.255.255
      port: 80
    provider:
      password: secret
      server: lb.mydomain.com
      user: admin
    state: present
  delegate_to: localhost
'''

RETURN = r'''
param1:
  description: The new param1 value of the resource.
  returned: changed
  type: bool
  sample: true
param2:
  description: The new param2 value of the resource.
  returned: changed
  type: string
  sample: Foo is bar
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback

try:
    from library.module_utils.network.f5.bigip import HAS_F5SDK
    from library.module_utils.network.f5.bigip import F5Client
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import cleanup_tokens
    from library.module_utils.network.f5.common import fq_name
    from library.module_utils.network.f5.common import f5_argument_spec
    try:
        from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False
except ImportError:
    from ansible.module_utils.network.f5.bigip import HAS_F5SDK
    from ansible.module_utils.network.f5.bigip import F5Client
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import AnsibleF5Parameters
    from ansible.module_utils.network.f5.common import cleanup_tokens
    from ansible.module_utils.network.f5.common import fq_name
    from ansible.module_utils.network.f5.common import f5_argument_spec
    try:
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False


class Parameters(AnsibleF5Parameters):
    api_map = {

    }

    api_attributes = [

    ]

    returnables = [

    ]

    updatables = [

    ]


class ApiParameters(Parameters):
    pass


class ModuleParameters(Parameters):
    pass


class Changes(Parameters):
    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
        except Exception:
            pass
        return result


class UsableChanges(Changes):
    pass


class ReportableChanges(Changes):
    pass


class Difference(object):
    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            return self.__default(param)

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = kwargs.get('client', None)
        self.want = ModuleParameters(params=self.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = UsableChanges(params=changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                if isinstance(change, dict):
                    changed.update(change)
                else:
                    changed[k] = change
        if changed:
            self.changes = UsableChanges(params=changed)
            return True
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        reportable = ReportableChanges(params=self.changes.to_return())
        changes = reportable.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations(result)
        return result

    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def exists(self):
        result = self.client.api.__API_ENDPOINT__.exists(
            name=self.want.name,
            partition=self.want.partition
        )
        return result

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the resource.")
        return True

    def create(self):
        self._set_changed_options()
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True

    def create_on_device(self):
        params = self.changes.api_params()
        self.client.api.__API_ENDPOINT__.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def update_on_device(self):
        params = self.changes.api_params()
        resource = self.client.api.__API_ENDPOINT__.load(
            name=self.want.name,
            partition=self.want.partition
        )
        resource.modify(**params)

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove_from_device(self):
        resource = self.client.api.__API_ENDPOINT__.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if resource:
            resource.delete()

    def read_current_from_device(self):
        resource = self.client.api.__API_ENDPOINT__.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result = resource.attrs
        return ApiParameters(params=result)


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            __ARGUMENT_SPEC__="__ARGUMENT_SPEC_VALUE__"
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    if not HAS_F5SDK:
        module.fail_json(msg="The python f5-sdk module is required")

    try:
        client = F5Client(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        module.exit_json(**results)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
