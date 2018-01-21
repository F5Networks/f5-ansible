.. _bigip_device_httpd:


bigip_device_httpd - Manage HTTPD related settings on BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages HTTPD related settings on the BIG-IP. These settings are interesting to change when you want to set GUI timeouts and other TMUI related settings.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9
  * requests


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
        <td><div>Specifies, if you have enabled HTTPD access, the IP address or address range for other systems that can communicate with this system.</div>        </td></tr>
                <tr><td>auth_name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the BIG-IP authentication realm name.</div>        </td></tr>
                <tr><td>auth_pam_dashboard_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Sets whether or not the BIG-IP dashboard will timeout.</div>        </td></tr>
                <tr><td>auth_pam_idle_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the GUI timeout for automatic logout, in seconds.</div>        </td></tr>
                <tr><td>auth_pam_validate_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Sets the authPamValidateIp setting.</div>        </td></tr>
                <tr><td>fast_cgi_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the timeout of FastCGI.</div>        </td></tr>
                <tr><td>hostname_lookup<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Sets whether or not to display the hostname, if possible.</div>        </td></tr>
                <tr><td>log_level<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>alert</li><li>crit</li><li>debug</li><li>emerg</li><li>error</li><li>info</li><li>notice</li><li>warn</li></ul></td>
        <td><div>Sets the minimum httpd log level.</div>        </td></tr>
                <tr><td>max_clients<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the maximum number of clients that can connect to the GUI at once.</div>        </td></tr>
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
                <tr><td>redirect_http_to_https<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Whether or not to redirect http requests to the GUI to https.</div>        </td></tr>
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
                <tr><td>ssl_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The HTTPS port to listen on.</div>        </td></tr>
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

    
    - name: Set the BIG-IP authentication realm name
      bigip_device_httpd:
        auth_name: BIG-IP
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Set the auth pam timeout to 3600 seconds
      bigip_device_httpd:
        auth_pam_idle_timeout: 1200
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Set the validate IP settings
      bigip_device_httpd:
        auth_pam_validate_ip: on
        password: secret
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
        <td> auth_pam_validate_ip </td>
        <td> The new authPamValidateIp setting. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> hostname_lookup </td>
        <td> Whether or not to display the hostname, if possible. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> log_level </td>
        <td> The new minimum httpd log level. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> crit </td>
    </tr>
            <tr>
        <td> auth_name </td>
        <td> The new authentication realm name. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> foo </td>
    </tr>
            <tr>
        <td> auth_pam_dashboard_timeout </td>
        <td> Whether or not the BIG-IP dashboard will timeout. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> False </td>
    </tr>
            <tr>
        <td> redirect_http_to_https </td>
        <td> Whether or not to redirect http requests to the GUI to https. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> fast_cgi_timeout </td>
        <td> The new timeout of FastCGI. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 500 </td>
    </tr>
            <tr>
        <td> ssl_port </td>
        <td> The new HTTPS port to listen on. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 10443 </td>
    </tr>
            <tr>
        <td> auth_pam_idle_timeout </td>
        <td> The new number of seconds for GUI timeout. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 1200 </td>
    </tr>
            <tr>
        <td> max_clients </td>
        <td> The new maximum number of clients that can connect to the GUI at once. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 20 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the requests Python package on the host. This is as easy as ``pip install requests``.
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