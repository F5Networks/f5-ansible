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


class ModuleDocFragment(object):
    # Standard F5 documentation fragment
    DOCUMENTATION = '''
options:
  password:
    description:
      - The password for the user account used to connect to the BIG-IP.
      - You may omit this option by setting the environment variable C(F5_PASSWORD).
    required: true
    aliases: ['pass', 'pwd']
  server:
    description:
      - The BIG-IP host.
      - You may omit this option by setting the environment variable C(F5_SERVER).
    required: true
  server_port:
    description:
      - The BIG-IP server port.
      - You may omit this option by setting the environment variable C(F5_SERVER_PORT).
    default: 443
    version_added: 2.2
  user:
    description:
      - The username to connect to the BIG-IP with. This user must have
        administrative privileges on the device.
      - You may omit this option by setting the environment variable C(F5_USER).
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates are not validated. Use this only
        on personally controlled sites using self-signed certificates.
      - You may omit this option by setting the environment variable
        C(F5_VALIDATE_CERTS).
    default: yes
    type: bool
    version_added: 2.0
  provider:
    description:
      - A dict object containing connection details.
    default: null
    version_added: 2.5
    suboptions:
      password:
        description:
          - The password for the user account used to connect to the BIG-IP.
          - You may omit this option by setting the environment variable C(F5_PASSWORD).
        required: true
        aliases: ['pass', 'pwd']
      server:
        description:
          - The BIG-IP host.
          - You may omit this option by setting the environment variable C(F5_SERVER).
        required: true
      server_port:
        description:
          - The BIG-IP server port.
          - You may omit this option by setting the environment variable C(F5_SERVER_PORT).
        default: 443
      user:
        description:
          - The username to connect to the BIG-IP with. This user must have
            administrative privileges on the device.
          - You may omit this option by setting the environment variable C(F5_USER).
        required: true
      validate_certs:
        description:
          - If C(no), SSL certificates are not validated. Use this only
            on personally controlled sites using self-signed certificates.
          - You may omit this option by setting the environment variable C(F5_VALIDATE_CERTS).
        default: yes
        type: bool
      timeout:
        description:
          - Specifies the timeout in seconds for communicating with the network device
            for either connecting or sending commands.  If the timeout is
            exceeded before the operation is completed, the module will error.
        default: 10
      ssh_keyfile:
        description:
          - Specifies the SSH keyfile to use to authenticate the connection to
            the remote device.  This argument is only used for I(cli) transports.
          - You may omit this option by setting the environment variable C(ANSIBLE_NET_SSH_KEYFILE).
      transport:
        description:
          - Configures the transport connection to use when connecting to the
            remote device.
        choices:
          - rest
          - cli
        default: rest
notes:
  - For more information on using Ansible to manage F5 Networks devices see U(https://www.ansible.com/integrations/networks/f5).
  - Requires BIG-IP software version >= 12.
  - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP
    specific configuration persists to disk, be sure to include at least one task that uses the
    M(bigip_config) module to save the running configuration. Refer to the module's documentation for
    the correct usage of the module to save your running configuration.
'''
