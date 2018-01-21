.. _bigip_ucs:


bigip_ucs - Manage upload, installation and removal of UCS files
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage upload, installation and removal of UCS files.


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
                <tr><td>force<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>yes</code> will upload the file every time and replace the file on the device. If <code>no</code>, the file will only be uploaded if it does not already exist. Generally should be <code>yes</code> only in cases where you have reason to believe that the image was corrupted during upload.</div>        </td></tr>
                <tr><td>include_chassis_level_config<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>During restore of the UCS file, include chassis level configuration that is shared among boot volume sets. For example, cluster default configuration.</div>        </td></tr>
                <tr><td>no_license<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Performs a full restore of the UCS file and all the files it contains, with the exception of the license file. The option must be used to restore a UCS on RMA devices (Returned Materials Authorization).</div>        </td></tr>
                <tr><td>no_platform_check<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Bypasses the platform check and allows a UCS that was created using a different platform to be installed. By default (without this option), a UCS created from a different platform is not allowed to be installed.</div>        </td></tr>
                <tr><td>passphrase<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Specifies the passphrase that is necessary to load the specified UCS file.</div>        </td></tr>
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
                <tr><td>reset_trust<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>When specified, the device and trust domain certs and keys are not loaded from the UCS. Instead, a new set is regenerated.</div>        </td></tr>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>installed</li><li>present</li></ul></td>
        <td><div>When <code>installed</code>, ensures that the UCS is uploaded and installed, on the system. When <code>present</code>, ensures that the UCS is uploaded. When <code>absent</code>, the UCS will be removed from the system. When <code>installed</code>, the uploading of the UCS is idempotent, however the installation of that configuration is not idempotent.</div>        </td></tr>
                <tr><td>ucs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The path to the UCS file to install. The parameter must be provided if the <code>state</code> is either <code>installed</code> or <code>activated</code>. When <code>state</code> is <code>absent</code>, the full path for this parameter will be ignored and only the filename will be used to select a UCS for removal. Therefore you could specify <code>/mickey/mouse/test.ucs</code> and this module would only look for <code>test.ucs</code>.</div>        </td></tr>
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

    
    - name: Upload UCS
      bigip_ucs:
        server: lb.mydomain.com
        user: admin
        password: secret
        ucs: /root/bigip.localhost.localdomain.ucs
        state: present
      delegate_to: localhost

    - name: Install (upload, install) UCS.
      bigip_ucs:
        server: lb.mydomain.com
        user: admin
        password: secret
        ucs: /root/bigip.localhost.localdomain.ucs
        state: installed
      delegate_to: localhost

    - name: Install (upload, install) UCS without installing the license portion
      bigip_ucs:
        server: lb.mydomain.com
        user: admin
        password: secret
        ucs: /root/bigip.localhost.localdomain.ucs
        state: installed
        no_license: yes
      delegate_to: localhost

    - name: Install (upload, install) UCS except the license, and bypassing the platform check
      bigip_ucs:
        server: lb.mydomain.com
        user: admin
        password: secret
        ucs: /root/bigip.localhost.localdomain.ucs
        state: installed
        no_license: yes
        no_platform_check: yes
      delegate_to: localhost

    - name: Install (upload, install) UCS using a passphrase necessary to load the UCS
      bigip_ucs:
        server: lb.mydomain.com
        user: admin
        password: secret
        ucs: /root/bigip.localhost.localdomain.ucs
        state: installed
        passphrase: MyPassphrase1234
      delegate_to: localhost

    - name: Remove uploaded UCS file
      bigip_ucs:
        server: lb.mydomain.com
        user: admin
        password: secret
        ucs: bigip.localhost.localdomain.ucs
        state: absent
      delegate_to: localhost



Notes
-----

.. note::
    - Only the most basic checks are performed by this module. Other checks and considerations need to be taken into account. See the following URL. https://support.f5.com/kb/en-us/solutions/public/11000/300/sol11318.html
    - This module does not handle devices with the FIPS 140 HSM
    - This module does not handle BIG-IPs systems on the 6400, 6800, 8400, or 8800 hardware platform.
    - This module does not verify that the new or replaced SSH keys from the UCS file are synchronized between the BIG-IP system and the SCCP
    - This module does not support the 'rma' option
    - This module does not support restoring a UCS archive on a BIG-IP 1500, 3400, 4100, 6400, 6800, or 8400 hardware platform other than the system from which the backup was created
    - The UCS restore operation restores the full configuration only if the hostname of the target system matches the hostname on which the UCS archive was created. If the hostname does not match, only the shared configuration is restored. You can ensure hostnames match by using the ``bigip_hostname`` Ansible module in a task before using this module.
    - This module does not support re-licensing a BIG-IP restored from a UCS
    - This module does not support restoring encrypted archives on replacement RMA units.
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