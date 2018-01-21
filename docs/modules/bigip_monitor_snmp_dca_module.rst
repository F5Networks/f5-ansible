.. _bigip_monitor_snmp_dca:


bigip_monitor_snmp_dca - Manages BIG-IP SNMP data collecting agent (DCA) monitors
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* The BIG-IP has an SNMP data collecting agent (DCA) that can query remote SNMP agents of various types, including the UC Davis agent (UCD) and the Windows 2000 Server agent (WIN2000).


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
                <tr><td>agent_type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>UCD</li><li>WIN2000</li><li>GENERIC</li></ul></td>
        <td><div>Specifies the SNMP agent running on the monitored server. When creating a new monitor, the default is <code>UCD</code> (UC-Davis).</div>        </td></tr>
                <tr><td>community<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the community name that the system must use to authenticate with the host server through SNMP. When creating a new monitor, the default value is <code>public</code>. Note that this value is case sensitive.</div>        </td></tr>
                <tr><td>cpu_coefficient<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the coefficient that the system uses to calculate the weight of the CPU threshold in the dynamic ratio load balancing algorithm. When creating a new monitor, the default is <code>1.5</code>.</div>        </td></tr>
                <tr><td>cpu_threshold<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the maximum acceptable CPU usage on the target server. When creating a new monitor, the default is <code>80</code> percent.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies descriptive text that identifies the monitor.</div>        </td></tr>
                <tr><td>disk_coefficient<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the coefficient that the system uses to calculate the weight of the disk threshold in the dynamic ratio load balancing algorithm. When creating a new monitor, the default is <code>2.0</code>.</div>        </td></tr>
                <tr><td>disk_threshold<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the maximum acceptable disk usage on the target server. When creating a new monitor, the default is <code>90</code> percent.</div>        </td></tr>
                <tr><td>interval<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource is down or the status of the resource is unknown. When creating a new monitor, the default is <code>10</code>.</div>        </td></tr>
                <tr><td>memory_coefficient<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the coefficient that the system uses to calculate the weight of the memory threshold in the dynamic ratio load balancing algorithm. When creating a new monitor, the default is <code>1.0</code>.</div>        </td></tr>
                <tr><td>memory_threshold<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the maximum acceptable memory usage on the target server. When creating a new monitor, the default is <code>70</code> percent.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Monitor name.</div>        </td></tr>
                <tr><td>parent<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>/Common/snmp_dca</td>
        <td></td>
        <td><div>The parent template of this monitor template. Once this value has been set, it cannot be changed. By default, this value is the <code>snmp_dca</code> parent on the <code>Common</code> partition.</div>        </td></tr>
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
                <tr><td>state<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>present</code>, ensures that the monitor exists.</div><div>When <code>absent</code>, ensures the monitor is removed.</div>        </td></tr>
                <tr><td>time_until_up<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the number of seconds to wait after a resource first responds correctly to the monitor before setting the resource to &#x27;up&#x27;. During the interval, all responses from the resource must be correct. When the interval expires, the resource is marked &#x27;up&#x27;. A value of 0, means that the resource is marked up immediately upon receipt of the first correct response. When creating a new monitor, the default is <code>0</code>.</div>        </td></tr>
                <tr><td>timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the number of seconds the target has in which to respond to the monitor request. When creating a new monitor, the default is <code>30</code> seconds. If the target responds within the set time period, it is considered &#x27;up&#x27;. If the target does not respond within the set time period, it is considered &#x27;down&#x27;. When this value is set to 0 (zero), the system uses the interval from the parent monitor. Note that <code>timeout</code> and <code>time_until_up</code> combine to control when a resource is set to up.</div>        </td></tr>
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
                <tr><td>version<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>v1</li><li>v2c</li></ul></td>
        <td><div>Specifies the version of SNMP that the host server uses. When creating a new monitor, the default is <code>v1</code>. When <code>v1</code>, specifies that the host server uses SNMP version 1. When <code>v2c</code>, specifies that the host server uses SNMP version 2c.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create SNMP DCS monitor
      bigip_monitor_snmp_dca:
        state: present
        server: lb.mydomain.com
        user: admin
        password: secret
        name: my_monitor
      delegate_to: localhost

    - name: Remove TCP Echo Monitor
      bigip_monitor_snmp_dca:
        state: absent
        server: lb.mydomain.com
        user: admin
        password: secret
        name: my_monitor
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
        <td> timeout </td>
        <td> The new timeout in which the remote system must respond to the monitor. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 10 </td>
    </tr>
            <tr>
        <td> disk_threshold </td>
        <td> The new disk threshold. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 34 </td>
    </tr>
            <tr>
        <td> parent </td>
        <td> New parent template of the monitor. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> snmp_dca </td>
    </tr>
            <tr>
        <td> cpu_coefficient </td>
        <td> The new CPU coefficient. </td>
        <td align=center> changed </td>
        <td align=center> float </td>
        <td align=center> 2.4 </td>
    </tr>
            <tr>
        <td> interval </td>
        <td> The new interval in which to run the monitor check. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2 </td>
    </tr>
            <tr>
        <td> memory_threshold </td>
        <td> The new memory threshold. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 50 </td>
    </tr>
            <tr>
        <td> community </td>
        <td> The new community for the monitor. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> foobar </td>
    </tr>
            <tr>
        <td> disk_coefficient </td>
        <td> The new disk coefficient. </td>
        <td align=center> changed </td>
        <td align=center> float </td>
        <td align=center> 10.2 </td>
    </tr>
            <tr>
        <td> time_until_up </td>
        <td> The new time in which to mark a system as up after first successful response. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2 </td>
    </tr>
            <tr>
        <td> agent_type </td>
        <td> The new agent type to be used by the monitor. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> UCD </td>
    </tr>
            <tr>
        <td> memory_coefficient </td>
        <td> The new memory coefficient. </td>
        <td align=center> changed </td>
        <td align=center> float </td>
        <td align=center> 6.4 </td>
    </tr>
            <tr>
        <td> version </td>
        <td> The new new SNMP version to be used by the monitor. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> v2c </td>
    </tr>
            <tr>
        <td> cpu_threshold </td>
        <td> The new CPU threshold. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 85 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires BIG-IP software version >= 12
    - This module does not support the ``variables`` option because this option is broken in the REST API and does not function correctly in ``tmsh``; for example you cannot remove user-defined params. Therefore, there is no way to automatically configure it.
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