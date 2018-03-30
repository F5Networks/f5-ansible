.. _bigip_gtm_monitor_firepass:


bigip_gtm_monitor_firepass - Manages F5 BIG-IP GTM FirePass monitors
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.6


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP GTM FirePass monitors.


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
                <tr><td>cipher_list<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the list of ciphers for this monitor.</div><div>The items in the cipher list are separated with the colon <code>:</code> symbol.</div><div>When creating a new monitor, if this parameter is not specified, the default list is <code>HIGH:!ADH</code>.</div>        </td></tr>
                <tr><td>concurrency_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the maximum percentage of licensed connections currently in use under which the monitor marks the Secure Access Manager system up.</div><div>As an example, a setting of 95 percent means that the monitor marks the Secure Access Manager system up until 95 percent of licensed connections are in use.</div><div>When the number of in-use licensed connections exceeds 95 percent, the monitor marks the Secure Access Manager system down.</div><div>When creating a new monitor, if this parameter is not specified, the default is <code>95</code>.</div>        </td></tr>
                <tr><td>ignore_down_response<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Specifies that the monitor allows more than one probe attempt per interval.</div><div>When <code>yes</code>, specifies that the monitor ignores down responses for the duration of the monitor timeout. Once the monitor timeout is reached without the system receiving an up response, the system marks the object down.</div><div>When <code>no</code>, specifies that the monitor immediately marks an object down when it receives a down response.</div><div>When creating a new monitor, if this parameter is not provided, then the default value will be <code>no</code>.</div>        </td></tr>
                <tr><td>interval<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The interval specifying how frequently the monitor instance of this template will run.</div><div>If this parameter is not provided when creating a new monitor, then the default value will be 30.</div><div>This value <b>must</b> be less than the <code>timeout</code> value.</div>        </td></tr>
                <tr><td>ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>IP address part of the IP/port definition. If this parameter is not provided when creating a new monitor, then the default value will be &#x27;*&#x27;.</div><div>If this value is an IP address, then a <code>port</code> number must be specified.</div>        </td></tr>
                <tr><td>max_load_average<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the number that the monitor uses to mark the Secure Access Manager system up or down.</div><div>The system compares the Max Load Average setting against a one-minute average of the Secure Access Manager system load.</div><div>When the Secure Access Manager system-load average falls within the specified Max Load Average, the monitor marks the Secure Access Manager system up.</div><div>When the average exceeds the setting, the monitor marks the system down.</div><div>When creating a new monitor, if this parameter is not specified, the default is <code>12</code>.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Monitor name.</div>        </td></tr>
                <tr><td>parent<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>/Common/firepass_gtm</td>
        <td></td>
        <td><div>The parent template of this monitor template. Once this value has been set, it cannot be changed. By default, this value is the <code>tcp</code> parent on the <code>Common</code> partition.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
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
        <td><div>Port address part of the IP/port definition. If this parameter is not provided when creating a new monitor, then the default value will be &#x27;*&#x27;. Note that if specifying an IP address, a value between 1 and 65535 must be specified.</div>        </td></tr>
                <tr><td>probe_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the number of seconds after which the system times out the probe request to the system.</div><div>When creating a new monitor, if this parameter is not provided, then the default value will be <code>5</code>.</div>        </td></tr>
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
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>yes</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>present</code>, ensures that the monitor exists.</div><div>When <code>absent</code>, ensures the monitor is removed.</div>        </td></tr>
                <tr><td>target_password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the password, if the monitored target requires authentication.</div>        </td></tr>
                <tr><td>target_username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the user name, if the monitored target requires authentication.</div>        </td></tr>
                <tr><td>timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The number of seconds in which the node or service must respond to the monitor request. If the target responds within the set time period, it is considered up. If the target does not respond within the set time period, it is considered down. You can change this number to any number you want, however, it should be 3 times the interval number of seconds plus 1 second.</div><div>If this parameter is not provided when creating a new monitor, then the default value will be 90.</div>        </td></tr>
                <tr><td>update_password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>always</td>
        <td><ul><li>always</li><li>on_create</li></ul></td>
        <td><div><code>always</code> will update passwords if the <code>target_password</code> is specified.</div><div><code>on_create</code> will only set the password for newly created monitors.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>yes</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a GTM FirePass monitor
      bigip_gtm_monitor_firepass:
        name: my_monitor
        ip: 1.1.1.1
        port: 80
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Remove FirePass Monitor
      bigip_gtm_monitor_firepass:
        name: my_monitor
        state: absent
        server: lb.mydomain.com
        user: admin
        password: secret
      delegate_to: localhost

    - name: Add FirePass monitor for all addresses, port 514
      bigip_gtm_monitor_firepass:
        name: my_monitor
        server: lb.mydomain.com
        user: admin
        port: 514
        password: secret
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
        <td> parent </td>
        <td> New parent template of the monitor. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> firepass_gtm </td>
    </tr>
            <tr>
        <td> ip </td>
        <td> The new IP of IP/port definition. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 10.12.13.14 </td>
    </tr>
            <tr>
        <td> port </td>
        <td> The new port the monitor checks the resource on. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 8080 </td>
    </tr>
            <tr>
        <td> interval </td>
        <td> The new interval in which to run the monitor check. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2 </td>
    </tr>
            <tr>
        <td> timeout </td>
        <td> The new timeout in which the remote system must respond to the monitor. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 10 </td>
    </tr>
            <tr>
        <td> ignore_down_response </td>
        <td> Whether to ignore the down response or not. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> probe_timeout </td>
        <td> The new timeout in which the system will timeout the monitor probe. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 10 </td>
    </tr>
            <tr>
        <td> cipher_list </td>
        <td> The new value for the cipher list. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> +3DES:+kEDH </td>
    </tr>
            <tr>
        <td> max_load_average </td>
        <td> The new value for the max load average. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 12 </td>
    </tr>
            <tr>
        <td> concurrency_limit </td>
        <td> The new value for the concurrency limit. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 95 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
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