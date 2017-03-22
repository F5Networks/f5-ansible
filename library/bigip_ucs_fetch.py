#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016 F5 Networks Inc.
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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.0'
}

DOCUMENTATION = '''
---
module: bigip_ucs_fetch
short_description: Fetches a UCS file from remote nodes
description:
   - This module is used for fetching UCS files from remote machines and
     storing them locally in a file tree, organized by hostname. Note that
     this module is written to transfer UCS files that might not be present,
     so a missing remote UCS won't be an error unless fail_on_missing is
     set to 'yes'.
version_added: "2.2"
options:
  backup:
    description:
      - Create a backup file including the timestamp information so you can
        get the original file back if you somehow clobbered it incorrectly.
    default: no
    required: False
    choices:
      - yes
      - no
  create_on_missing:
    description:
      - Creates the UCS based on the value of C(src) if the file does not already
        exist on the remote system.
    default: True
    required: False
  dest:
    description:
      - A directory to save the UCS file into.
    required: yes
  encryption_password:
    description:
      - Password to use to encrypt the UCS file if desired
    required: False
  fail_on_missing:
    description:
      - Make the module fail if the UCS file on the remote system is missing.
    default: False
    required: False
  force:
    description:
      - If C(no), the file will only be transferred if the destination does not
        exist.
    default: yes
    required: False
  password:
    description:
      - BIG-IP password
    required: true
  src:
    description:
      - The name of the UCS file to create on the remote server for downloading
    required: false
    default: temporary file name
  server:
    description:
      - BIG-IP host
    required: true
  user:
    description:
      - BIG-IP username
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be
        used on personally controlled sites using self-signed certificates.
    required: false
    default: true
notes:
  - Requires the bigsuds Python package on the host if using the iControl
    interface. This is as easy as pip install bigsuds
  - BIG-IP provides no way to get a checksum of the UCS files on the system
    via any interface except, perhaps, logging in directly to the box (which
    would not support appliance mode). Therefore, the best this module can
    do is check for the existence of the file on disk; no checksumming.
requirements:
  - bigsuds
  - requests
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = '''
- name: Download a new UCS
  bigip_ucs_fetch:
      server: "bigip.localhost.localdomain"
      user: "admin"
      password: "admin"
      src: "cs_backup.ucs"
      dest: "/tmp/cs_backup.ucs"
  delegate_to: localhost
'''

RETURN = '''
checksum:
  description: The SHA1 checksum of the downloaded file
  returned: success or changed
  type: string
  sample: 7b46bbe4f8ebfee64761b5313855618f64c64109
dest:
  description: Location on the ansible host that the UCS was saved to
  returned: success
  type: string
  sample: "/path/to/file.txt"
src:
  description:
    - Name of the UCS file on the remote BIG-IP to download. If not
      specified, then this will be a randomly generated filename
  returned: changed
  type: string
  sample: "cs_backup.ucs"
backup_file:
  description: Name of backup file created
  returned: changed and if backup=yes
  type: string
  sample: "/path/to/file.txt.2015-02-12@22:09~"
gid:
  description: Group id of the UCS file, after execution
  returned: success
  type: int
  sample: 100
group:
  description: Group of the UCS file, after execution
  returned: success
  type: string
  sample: "httpd"
owner:
  description: Owner of the UCS file, after execution
  returned: success
  type: string
  sample: "httpd"
uid:
  description: Owner id of the UCS file, after execution
  returned: success
  type: int
  sample: 100
md5sum:
  description: The MD5 checksum of the downloaded file
  returned: changed or success
  type: string
  sample: 96cacab4c259c4598727d7cf2ceb3b45
mode:
  description: Permissions of the target UCS, after execution
  returned: success
  type: string
  sample: "0644"
size:
  description: Size of the target UCS, after execution
  returned: success
  type: int
  sample: 1220
'''

import base64
import os
import socket
import tempfile

# Size of chunks of data to read and send via the iControl API
CHUNK_SIZE = 512 * 1024
SAVE_FULL = "SAVE_FULL"


def bigip_version():
    """Check the BIG-IP version

    Different versions of BIG-IP support different arguments to the load
    command. This method will return the version of the system for
    comparison.
    """
    version = self.api.System.SystemInfo.get_version()
    return version


class BigIpCommon(object):
    def __init__(self, username, password, hostname, validate_certs=True,
                 check_mode=False):

        self._username = username
        self._password = password
        self._hostname = hostname
        self._validate_certs = validate_certs


class BigIpIControl(BigIpCommon):
    def __init__(self, username, password, hostname,
                 validate_certs=True, check_mode=False):

        super(BigIpIControl, self).__init__(username, password, hostname,
                                            validate_certs, check_mode)

        self.api = bigip_api(hostname, username, password, validate_certs)

    def create(self, filename, encryption_password=None):
        if encryption_password:
            self.api.System.ConfigSync.save_encrypted_configuration(
                filename=filename,
                passphrase=encryption_password
            )
        else:
            self.api.System.ConfigSync.save_configuration(
                filename=filename,
                save_flag=SAVE_FULL
            )

    def read(self):
        result = []

        try:
            resp = self.api.System.ConfigSync.get_configuration_list()
            for ucs in resp:
                result.append(ucs['file_name'])
        except bigsuds.ServerError:
            pass

        return result

    def is_ucs_available(self, ucs):
        if ucs in self.read():
            return True
        else:
            return False

    def download(self, src, dest):
        fileobj = open(dest, 'wb')
        offset = 0
        done = False

        while not done:
            data = self.api.System.ConfigSync.download_configuration(
                config_name=src,
                chunk_size=CHUNK_SIZE,
                file_offset=offset
            )
            fileobj.write(base64.b64decode(data['return']['file_data']))
            offset = data['file_offset']
            if data['return']['chain_type'] in ['FILE_LAST', 'FILE_FIRST_AND_LAST']:
                break
        fileobj.close()


class BigIpRest(BigIpCommon):
    def __init__(self, username, password, hostname,
                 validate_certs=True, check_mode=False):

        super(BigIpRest, self).__init__(username, password, hostname,
                                        validate_certs, check_mode)

    def download(self, filename):
        headers = {
            'Content-Type': 'application/octet-stream'
        }
        filename = os.path.basename(fp)
        uri = 'https://%s/mgmt/cm/autodeploy/software-image-downloads/%s' % (host, filename)
        requests.packages.urllib3.disable_warnings()

        with open(fp, 'wb') as f:
            start = 0
            end = CHUNK_SIZE - 1
            size = 0
            current_bytes = 0

            while True:
                content_range = "%s-%s/%s" % (start, end, size)
                headers['Content-Range'] = content_range

                resp = requests.get(uri,
                                    auth=creds,
                                    headers=headers,
                                    verify=False,
                                    stream=True)

                if resp.status_code == 200:
                    # If the size is zero, then this is the first time through the
                    # loop and we don't want to write data because we haven't yet
                    # figured out the total size of the file.
                    if size > 0:
                        current_bytes += CHUNK_SIZE
                        for chunk in resp.iter_content(CHUNK_SIZE):
                            f.write(chunk)

                    # Once we've downloaded the entire file, we can break out of
                    # the loop
                    if end == size:
                        break

                crange = resp.headers['Content-Range']

                # Determine the total number of bytes to read
                if size == 0:
                    size = int(crange.split('/')[-1]) - 1

                    # If the file is smaller than the chunk size, BIG-IP will
                    # return an HTTP 400. So adjust the CHUNK_SIZE down to the
                    # total file size...
                    if CHUNK_SIZE > size:
                        end = size

                    # ...and pass on the rest of the code
                    continue

                start += CHUNK_SIZE

                if (current_bytes + CHUNK_SIZE) > size:
                    end = size
                else:
                    end = start + CHUNK_SIZE - 1


def main():
    backup_file = None

    argument_spec = f5_argument_spec()

    meta_args = dict(
        backup=dict(required=False, default=False, type='bool', choices=BOOLEANS),
        create_on_missing=dict(required=False, default=True, type='bool', choices=BOOLEANS),
        encryption_password=dict(required=False, default=None),
        dest=dict(required=True),
        force=dict(required=False, default=True, type='bool', choices=BOOLEANS),
        fail_on_missing=dict(required=False, default=False, type='bool', choices=BOOLEANS),
        src=dict(required=False, default=None)
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        add_file_common_args=True,
        supports_check_mode=True
    )

    (server, user, password, state, partition, validate_certs) = f5_parse_arguments(module)

    try:
        backup = module.params['backup']
        connection = module.params['connection']
        create_on_missing = module.params['create_on_missing']
        dest = os.path.expanduser(module.params['dest'])
        encryption_password = module.params.get('encryption_password')
        force = module.params.get('force')
        fail_on_missing = module.params['fail_on_missing']
        src = module.params.get('src')

        # Generates a random filename if no 'src' argument was provided
        #
        # This random name will be supplied in the output of this module as the
        # value of the 'src' field so that you can use it in later modules
        if not src:
            tf = tempfile.NamedTemporaryFile(suffix='.ucs')
            src = os.path.basename(tf.name)
            tf.close()

        if connection == 'soap':
            if not BIGSUDS_AVAILABLE:
                raise Exception("The python bigsuds module is required")

            test_icontrol(user, password, server, validate_certs)
            obj = BigIpIControl(user, password, server, validate_certs)
        elif connection == 'rest':
            module.fail_json(msg='The REST connection is currently not supported')

        if fail_on_missing and not obj.is_ucs_available(src):
            module.exit_json(msg="UCS was not found", src=src, dest=dest, changed=False)

        if not create_on_missing and not obj.is_ucs_available(src):
            module.exit_json(msg="UCS was not found", src=src, dest=dest, changed=False)

        if create_on_missing and not obj.is_ucs_available(src):
            obj.create(src, encryption_password)

        if os.path.exists(dest):
            if not force:
                module.exit_json(msg="File already exists", src=src, dest=dest, changed=False)

        if os.path.isdir(dest):
            dest = os.path.join(dest, src)
        else:
            if not os.path.exists(os.path.dirname(dest)):
                try:
                    # os.path.exists() can return false in some
                    # circumstances where the directory does not have
                    # the execute bit for the current user set, in
                    # which case the stat() call will raise an OSError
                    os.stat(os.path.dirname(dest))
                except OSError as e:
                    if "permission denied" in str(e).lower():
                        module.fail_json(msg="Destination directory %s is not accessible" % (os.path.dirname(dest)))
                module.fail_json(msg="Destination directory %s does not exist" % (os.path.dirname(dest)))

        if not os.access(os.path.dirname(dest), os.W_OK):
            module.fail_json(msg="Destination %s not writable" % (os.path.dirname(dest)))

        try:
            if backup:
                if os.path.exists(dest):
                    backup_file = module.backup_local(dest)
            obj.download(src, dest)
        except IOError:
            module.fail_json(msg="Failed to copy: %s to %s" % (src, dest))

        changed = True
        checksum_dest = module.sha1(dest)
        try:
            md5sum_dest = module.md5(dest)
        except ValueError:
            md5sum_dest = None

        res_args = dict(
            dest=dest,
            src=src,
            changed=changed,
            md5sum=md5sum_dest,
            checksum=checksum_dest
        )
        if backup_file:
            res_args['backup_file'] = backup_file
    except (bigsuds.ConnectionError, bigsuds.ParseError) as e:
        module.fail_json(msg="Could not connect to BIG-IP host %s" % server)
    except socket.timeout as e:
        module.fail_json(msg="Timed out connecting to the BIG-IP")
    except socket.timeout as e:
        module.fail_json(msg=str(e))

    file_args = module.load_file_common_arguments(module.params)
    res_args['changed'] = module.set_fs_attributes_if_different(file_args, res_args['changed'])

    module.exit_json(**res_args)

from ansible.module_utils.basic import *
from ansible.module_utils.f5_utils import *

if __name__ == '__main__':
    main()
