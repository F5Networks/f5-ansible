#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: bigip_license
short_description: Manage license installation and activation on BIG-IP devices
description:
  - Manage license installation and activation on BIG-IP devices. This module
    provides two different ways to license a device. Either via a activation key
    (which requires a connection back to the f5.com licensing server from the Ansible control machine) or, with the content of a license
    and dossier that you have acquired manually.
version_added: "2.5"
options:
  dossier_content:
    description:
      - Path to file containing kernel dossier for your system.
  key:
    description:
      - The registration key to use to license the BIG-IP. This is required
        if the C(state) is equal to C(present) or C(latest).
  license_content:
    description:
      - Path to file containing the license to use. In most cases you will want
        to use a C(lookup) for this.
  state:
    description:
      - The state of the license on the system. When C(present), only guarantees
        that a license is there. When C(latest) ensures that the license is always
        valid. When C(absent) removes the license on the system. C(latest) is
        most useful internally. When using C(absent), the account accessing the
        device must be configured to use the advanced shell instead of Appliance
        Mode.
    default: present
    choices:
      - absent
      - latest
      - present
  accept_eula:
    description:
      - Declares whether you accept the BIG-IP EULA or not. By default, this
        value is C(no). You must specifically declare that you have viewed and
        accepted the license. This module will not present you with that EULA
        though, so it is incumbent on you to re
notes:
  - Requires BIG-IP software version >= 12
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: License BIG-IP using a key
  bigip_license:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
  delegate_to: localhost

- name: License BIG-IP using a development key
  bigip_license:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
      license_server: "xxx.f5net.com"
  delegate_to: localhost

- name: License BIG-IP using a pre-acquired license
  bigip_license:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      license_content: "{{ lookup('file', 'license.lic') }}"
      dossier_content: "{{ lookup('file', 'dossier.txt') }}"
  delegate_to: localhost

- name: Remove the license from the system
  bigip_license:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      state: "absent"
  delegate_to: localhost

- name: Update the current license of the BIG-IP
  bigip_license:
      server: "lb.mydomain.com"
      user: "admin"
      password: "secret"
      key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
      state: "latest"
  delegate_to: localhost
'''

import base64
import time


class BigIpLicenseCommon(object):
    def get_license_activation_status(self):
        """Returns the license status

        This method will return the license activation status of a BIG-IP. The
        following status may be returned from this method.

            STATE_DISABLED when it is not licensed
            STATE_ENABLED when it is licensed
        """
        return self.client.Management.LicenseAdministration.get_license_activation_status()

    def absent(self):
        self.cli.connect(self.hostname, username=self.username, password=self.password)

        # I am deleting all of the BIG-IP and BIG-IQ licenses so that this
        # module can be used by both devices
        for license in licenses:
            # If the file does not exist, the SOAP client will raise an
            # exception. Handle it and move on
            try:
                self.client.System.ConfigSync.delete_file(license)
            except bigsuds.ServerError:
                pass

        # The reloadlic command is used to refresh the state that is
        # reported by the APIs. If this is not done, then the existing
        # state reported does not changed from STATE_ENABLED
        cmd = "/usr/bin/reloadlic"

        stdin, stdout, stderr = self.cli.exec_command(cmd)
        self.cli.close()

        # reloadlic doesn't actually return anything, and it also doesn't
        # correctly report back its status upon failure (for example by
        # exiting with return codes greater than zero
        #
        # So the only way to really know if the license was succesfully
        # deleted is to recheck the state of the license
        stop_time = time.time() + 60
        while True:
            status = self.get_license_activation_status()
            if status == 'STATE_DISABLED':
                break
            elif time.time() >= stop_time:
                # ensure we do not run forever
                break
            time.sleep(1)

            stop_time = time.time() + 60
            while True:
                self.set_shell(shell)
                time.sleep(5)
                resp = self.client.Management.UserManagement.get_login_shell([self.username])
                if resp[0] == shell:
                    break
                elif time.time() >= stop_time:
                    # ensure we do not run forever
                    break
                time.sleep(5)

        return True


class BigIpLicenseIControl(BigIpLicenseCommon):
    def __init__(self, module):
        super(BigIpLicenseIControl, self).__init__(module)

        self.eula_file = 'LICENSE.F5'
        self.license = None
        self.dossier = None
        self.license_file = module.params.get('license_file')
        self.dossier_file = module.params.get('dossier_file')
        self.regkey = module.params.get('key')
        self.license_server = None

    def get_license(self):
        client = suds.client.Client(url=url, location=url)
        resp = client.service.getLicense(
            self.dossier,
            self.license_options['eula'],
            self.license_options['email'],
            self.license_options['firstname'],
            self.license_options['lastname'],
            self.license_options['company'],
            self.license_options['phone'],
            self.license_options['jobtitle'],
            self.license_options['address'],
            self.license_options['city'],
            self.license_options['state'],
            self.license_options['postalcode'],
            self.license_options['country'],
        )

        return resp

    def get_dossier(self, key):
        response = self.client.Management.LicenseAdministration.get_system_dossier(
            registration_keys=[key]
        )
        self.dossier = response
        return response

    def install_license(self, license):
        license = base64.b64encode(license)
        self.client.Management.LicenseAdministration.install_license(
            license_file_data=license
        )

        status = self.get_license_activation_status()
        if status == 'STATE_ENABLED':
            return True
        else:
            return False

    def upload_eula(self, eula):
        file_name = '/%s' % self.eula_file

        self.client.System.ConfigSync.upload_file(
            file_name=file_name,
            file_context=dict(
                file_data=base64.b64encode(eula),
                chain_type='FILE_FIRST_AND_LAST'
            )
        )

    def present(self):
        if is_production_key(self.regkey):
            license_server = LIC_EXTERNAL
        else:
            license_server = LIC_INTERNAL

        self.license_server = license_server

        if self.license_file:
            fh = open(license_file)
            self.license = fh.read()
            fh.close()

        if self.dossier_file:
            fh = open(dossier_file)
            self.dossier = fh.read()
            fh.close()

        if not self.dossier:
            self.get_dossier(self.regkey)
            if not self.dossier:
                raise F5ModuleError(
                    "Dossier not generated"
                )

        resp = self.get_license()
        if resp.state == "EULA_REQUIRED":
            # Extract the eula offered from first try
            eula_string = resp.eula
            self.license_options['eula'] = eula_string
            resp = self.get_license()

        # Try again, this time with eula populated
        if resp.state == 'LICENSE_RETURNED':
            big_license = resp.license
            if big_license:
                self.upload_eula(resp.eula)
        else:
            raise F5ModuleError(resp.fault.faultText)

        if self.install_license(big_license):
            return True
        else:
            return False


class ModuleManager(object):
    def __init__(self, client):
        self.client = client
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Parameters()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = Parameters(params=changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            else:
                changed[k] = change
        if changed:
            self.changes = Parameters(params=changed)
            return True
        return False

    def _announce_deprecations(self):
        warnings = []
        if self.want:
            warnings += self.want._values.get('__warnings', [])
        if self.have:
            warnings += self.have._values.get('__warnings', [])
        for warning in warnings:
            self.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        """
        common = BigIpLicenseCommon(module)
        lic_status = common.get_license_activation_status()

        if state == "present" and lic_status == 'STATE_ENABLED':
            module.exit_json(changed=False)

        if state == "absent" and lic_status == 'STATE_DISABLED':
            module.exit_json(changed=False)

        if state == "present" or state == "latest":
            if not bigsuds_found:
                raise Exception("The python bigsuds module is required")

            obj = BigIpLicenseIControl(module)

            if obj.present():
                changed = True
            else:
                module.fail_json(msg="License not installed")
        elif state == 'absent':
            if not paramiko_found:
                raise Exception("The python paramiko module is required")

            result = common.absent()
            if result:
                changed = True
            else:
                module.fail_json(msg="License not removed")

        module.exit_json(changed=changed)
        """

        try:
            if state == "present":
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations()
        return result

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def create(self):
        self._set_changed_options()
        if self.want.timeout is None:
            self.want.update({'timeout': 16})
        if self.want.interval is None:
            self.want.update({'interval': 5})
        if self.want.time_until_up is None:
            self.want.update({'time_until_up': 0})
        if self.want.ip is None:
            self.want.update({'ip': '*'})
        if self.module.check_mode:
            return True
        self.create_on_device()
        return True

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.module.check_mode:
            return True
        self.update_on_device()
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the monitor.")
        return True

    def read_current_from_device(self):
        resource = self.client.api.tm.ltm.monitor.tcp_echos.tcp_echo.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result = resource.attrs
        return Parameters(params=result)

    def exists(self):
        result = self.client.api.tm.ltm.monitor.tcp_echos.tcp_echo.exists(
            name=self.want.name,
            partition=self.want.partition
        )
        return result

    def update_on_device(self):
        params = self.want.api_params()
        result = self.client.api.tm.ltm.monitor.tcp_echos.tcp_echo.load(
            name=self.want.name,
            partition=self.want.partition
        )
        result.modify(**params)

    def create_on_device(self):
        params = self.want.api_params()
        self.client.api.tm.ltm.monitor.tcp_echos.tcp_echo.create(
            name=self.want.name,
            partition=self.want.partition,
            **params
        )

    def remove_from_device(self):
        result = self.client.api.tm.ltm.monitor.tcp_echos.tcp_echo.load(
            name=self.want.name,
            partition=self.want.partition
        )
        if result:
            result.delete()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = dict(
            key=dict(),
            dossier_content=dict(),
            license_content=dict(),
            license_server=dict(
                default='activate.f5.com'
            ),
            state=dict(
                choices=['absent', 'present', 'latest'],
                default='present'
            ),
            accept_eula=dict(
                type='bool',
                default='no'
            )
        )
        self.f5_product_name = 'bigip'
        self.required_if = [
            ['state', 'present', ['key', 'accept_eula']],
        ]
        self.required_together = [
            ['key', 'license_server'],
        ]
        self.mutually_exclusive = [
            ['key', 'license_content'],
            ['key', 'dossier_content']
        ]


def main():
    try:
        spec = ArgumentSpec()

        client = AnsibleF5Client(
            argument_spec=spec.argument_spec,
            supports_check_mode=spec.supports_check_mode,
            f5_product_name=spec.f5_product_name,
            required_if=spec.required_if,
            required_together=spec.required_together,
            mutually_exclusive=spec.mutually_exclusive
        )

        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
