.. _bigip_device_sshd:


bigip_device_sshd - Manage the SSHD settings of a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage the SSHD settings of a BIG-IP.


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
                <tr><td>allow<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>all</li><li>IP address, such as 172.27.1.10</li><li>IP range, such as 172.27.*.* or 172.27.0.0/255.255.0.0</li></ul></td>
        <td><div>Specifies, if you have enabled SSH access, the IP address or address range for other systems that can use SSH to communicate with this system.</div>        </td></tr>
                <tr><td>banner<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Whether to enable the banner or not.</div>        </td></tr>
                <tr><td>banner_text<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the text to include on the pre-login banner that displays when a user attempts to login to the system using SSH.</div>        </td></tr>
                <tr><td>inactivity_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the number of seconds before inactivity causes an SSH session to log out.</div>        </td></tr>
                <tr><td>log_level<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>debug</li><li>debug1</li><li>debug2</li><li>debug3</li><li>error</li><li>fatal</li><li>info</li><li>quiet</li><li>verbose</li></ul></td>
        <td><div>Specifies the minimum SSHD message level to include in the system log.</div>        </td></tr>
                <tr><td>login<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies, when checked <code>enabled</code>, that the system accepts SSH communications.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Port that you want the SSH daemon to run on.</div>        </td></tr>
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

    
    - name: Set the banner for the SSHD service from a string
      bigip_device_sshd:
        banner: enabled
        banner_text: banner text goes here
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Set the banner for the SSHD service from a file
      bigip_device_sshd:
        banner: enabled
        banner_text: "{{ lookup('file', '/path/to/file') }}"
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Set the SSHD service to run on port 2222
      bigip_device_sshd:
        password: secret
        port: 2222
        server: lb.mydomain.com
        user: admin
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
        <td> log_level </td>
        <td> The minimum SSHD message level to include in the system log. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> debug </td>
    </tr>
            <tr>
        <td> allow </td>
        <td> Specifies, if you have enabled SSH access, the IP address or address range for other systems that can use SSH to communicate with this system.
 </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 192.0.2.* </td>
    </tr>
            <tr>
        <td> banner_text </td>
        <td> Specifies the text included on the pre-login banner that displays when a user attempts to login to the system using SSH.
 </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> This is a corporate device. Connecting to it without... </td>
    </tr>
            <tr>
        <td> inactivity_timeout </td>
        <td> The number of seconds before inactivity causes an SSH session to log out.
 </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 10 </td>
    </tr>
            <tr>
        <td> login </td>
        <td> Specifies that the system accepts SSH communications or not. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> banner </td>
        <td> Whether the banner is enabled or not. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> port </td>
        <td> Port that you want the SSH daemon to run on. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 22 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires BIG-IP version 12.0.0 or greater
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