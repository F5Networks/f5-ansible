.. _bigip_ucs_fetch:


bigip_ucs_fetch - Fetches a UCS file from remote nodes
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* This module is used for fetching UCS files from remote machines and storing them locally in a file tree, organized by hostname. Note that this module is written to transfer UCS files that might not be present, so a missing remote UCS won't be an error unless fail_on_missing is set to 'yes'.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                <tr><td>backup<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Create a backup file including the timestamp information so you can get the original file back if you somehow clobbered it incorrectly.</div>        </td></tr>
                <tr><td>create_on_missing<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Creates the UCS based on the value of <code>src</code> if the file does not already exist on the remote system.</div>        </td></tr>
                <tr><td>dest<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>A directory to save the UCS file into.</div>        </td></tr>
                <tr><td>encryption_password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Password to use to encrypt the UCS file if desired</div>        </td></tr>
                <tr><td>fail_on_missing<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Make the module fail if the UCS file on the remote system is missing.</div>        </td></tr>
                <tr><td>force<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, the file will only be transferred if the destination does not exist.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td rowspan="2">provider<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>A dict object containing connection details.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object provider</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>True</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>transport<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td>cli</td>
                <td><ul><li>rest</li><li>cli</li></ul></td>
                <td><div>Configures the transport connection to use when connecting to the remote device.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>src<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The name of the UCS file to create on the remote server for downloading</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Download a new UCS
      bigip_ucs_fetch:
        server: lb.mydomain.com
        user: admin
        password: secret
        src: cs_backup.ucs
        dest: /tmp/cs_backup.ucs
      delegate_to: localhost


Return Values
-------------

Common return values are `documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>

        <tr>
        <td> src </td>
        <td> ['Name of the UCS file on the remote BIG-IP to download. If not specified, then this will be a randomly generated filename'] </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> cs_backup.ucs </td>
    </tr>
            <tr>
        <td> backup_file </td>
        <td> Name of backup file created </td>
        <td align=center> changed and if backup=yes </td>
        <td align=center> string </td>
        <td align=center> /path/to/file.txt.2015-02-12@22:09~ </td>
    </tr>
            <tr>
        <td> uid </td>
        <td> Owner id of the UCS file, after execution </td>
        <td align=center> success </td>
        <td align=center> int </td>
        <td align=center> 100 </td>
    </tr>
            <tr>
        <td> dest </td>
        <td> Location on the ansible host that the UCS was saved to </td>
        <td align=center> success </td>
        <td align=center> string </td>
        <td align=center> /path/to/file.txt </td>
    </tr>
            <tr>
        <td> checksum </td>
        <td> The SHA1 checksum of the downloaded file </td>
        <td align=center> success or changed </td>
        <td align=center> string </td>
        <td align=center> 7b46bbe4f8ebfee64761b5313855618f64c64109 </td>
    </tr>
            <tr>
        <td> md5sum </td>
        <td> The MD5 checksum of the downloaded file </td>
        <td align=center> changed or success </td>
        <td align=center> string </td>
        <td align=center> 96cacab4c259c4598727d7cf2ceb3b45 </td>
    </tr>
            <tr>
        <td> gid </td>
        <td> Group id of the UCS file, after execution </td>
        <td align=center> success </td>
        <td align=center> int </td>
        <td align=center> 100 </td>
    </tr>
            <tr>
        <td> mode </td>
        <td> Permissions of the target UCS, after execution </td>
        <td align=center> success </td>
        <td align=center> string </td>
        <td align=center> 420 </td>
    </tr>
            <tr>
        <td> owner </td>
        <td> Owner of the UCS file, after execution </td>
        <td align=center> success </td>
        <td align=center> string </td>
        <td align=center> httpd </td>
    </tr>
            <tr>
        <td> group </td>
        <td> Group of the UCS file, after execution </td>
        <td align=center> success </td>
        <td align=center> string </td>
        <td align=center> httpd </td>
    </tr>
            <tr>
        <td> size </td>
        <td> Size of the target UCS, after execution </td>
        <td align=center> success </td>
        <td align=center> int </td>
        <td align=center> 1220 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - BIG-IP provides no way to get a checksum of the UCS files on the system via any interface except, perhaps, logging in directly to the box (which would not support appliance mode). Therefore, the best this module can do is check for the existence of the file on disk; no check-summing.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.