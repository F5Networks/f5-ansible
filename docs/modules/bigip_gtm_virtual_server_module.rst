.. _bigip_gtm_virtual_server:


bigip_gtm_virtual_server - Manages F5 BIG-IP GTM virtual servers
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.6


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP GTM virtual servers. A GTM server can have many virtual servers associated with it. They are arranged in much the same way that pool members are to pools.


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
                <tr><td>address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the IP Address of the virtual server.</div><div>When creating a new GTM virtual server, this parameter is required.</div>        </td></tr>
                <tr><td rowspan="2">availability_requirements<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>Specifies, if you activate more than one health monitor, the number of health monitors that must receive successful responses in order for the link to be considered available.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object availability_requirements</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>type<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td><ul><li>all</li><li>at_least</li><li>require</li></ul></td>
                <td><div>Monitor rule type when <code>monitors</code> is specified.</div><div>When creating a new pool, if this value is not specified, the default of &#x27;all&#x27; will be used.</div>        </td></tr>
                    <tr><td>at_least<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the minimum number of active health monitors that must be successful before the link is considered up.</div><div>This parameter is only relevant when a <code>type</code> of <code>at_least</code> is used.</div><div>This parameter will be ignored if a type of either <code>all</code> or <code>require</code> is used.</div>        </td></tr>
                    <tr><td>number_of_probes<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the minimum number of probes that must succeed for this server to be declared up.</div><div>When creating a new virtual server, if this parameter is specified, then the <code>number_of_probers</code> parameter must also be specified.</div><div>The value of this parameter should always be <b>lower</b> than, or <b>equal to</b>, the value of <code>number_of_probers</code>.</div><div>This parameter is only relevant when a <code>type</code> of <code>require</code> is used.</div><div>This parameter will be ignored if a type of either <code>all</code> or <code>at_least</code> is used.</div>        </td></tr>
                    <tr><td>number_of_probers<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the number of probers that should be used when running probes.</div><div>When creating a new virtual server, if this parameter is specified, then the <code>number_of_probes</code> parameter must also be specified.</div><div>The value of this parameter should always be <b>higher</b> than, or <b>equal to</b>, the value of <code>number_of_probers</code>.</div><div>This parameter is only relevant when a <code>type</code> of <code>require</code> is used.</div><div>This parameter will be ignored if a type of either <code>all</code> or <code>at_least</code> is used.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td rowspan="2">limits<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>Specifies resource thresholds or limit requirements at the server level.</div><div>When you enable one or more limit settings, the system then uses that data to take servers in and out of service.</div><div>You can define limits for any or all of the limit settings. However, when a server does not meet the resource threshold limit requirement, the system marks the entire server as unavailable and directs load-balancing traffic to another resource.</div><div>The limit settings available depend on the type of server.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object limits</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>bits_enabled<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>Whether the bits limit it enabled or not.</div><div>This parameter allows you to switch on or off the effect of the limit.</div>        </td></tr>
                    <tr><td>packets_enabled<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>Whether the packets limit it enabled or not.</div><div>This parameter allows you to switch on or off the effect of the limit.</div>        </td></tr>
                    <tr><td>connections_enabled<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>Whether the current connections limit it enabled or not.</div><div>This parameter allows you to switch on or off the effect of the limit.</div>        </td></tr>
                    <tr><td>bits_limit<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the maximum allowable data throughput rate, in bits per second, for the virtual servers on the server.</div><div>If the network traffic volume exceeds this limit, the system marks the server as unavailable.</div>        </td></tr>
                    <tr><td>packets_limit<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the maximum allowable data transfer rate, in packets per second, for the virtual servers on the server.</div><div>If the network traffic volume exceeds this limit, the system marks the server as unavailable.</div>        </td></tr>
                    <tr><td>connections_limit<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the maximum number of concurrent connections, combined, for all of the virtual servers on the server.</div><div>If the connections exceed this limit, the system marks the server as unavailable.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>link<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies a link to assign to the server or virtual server.</div>        </td></tr>
                <tr><td>monitors<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the health monitors that the system currently uses to monitor this resource.</div><div>When <code>availability_requirements.type</code> is <code>require</code>, you may only have a single monitor in the <code>monitors</code> list.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the name of the virtual server.</div>        </td></tr>
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
        <td><div>Specifies the service port number for the virtual server or pool member. For example, the HTTP service is typically port 80.</div><div>To specify all ports, use an <code>*</code>.</div><div>When creating a new GTM virtual server, if this parameter is not specified, a default of <code>*</code> will be used.</div>        </td></tr>
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
        <td>True</td>
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
                <tr><td>server_name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the name of the server that the virtual server is associated with.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>When <code>present</code>, ensures that the resource exists.</div><div>When <code>absent</code>, ensures the resource is removed.</div>        </td></tr>
                <tr><td>translation_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the translation IP address for the virtual server.</div><div>To unset this parameter, provide an empty string (<code>&quot;&quot;</code>) as a value.</div><div>When creating a new GTM virtual server, if this parameter is not specified, a default of <code>::</code> will be used.</div>        </td></tr>
                <tr><td>translation_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the translation port number or service name for the virtual server.</div><div>To specify all ports, use an <code>*</code>.</div><div>When creating a new GTM virtual server, if this parameter is not specified, a default of <code>*</code> will be used.</div>        </td></tr>
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
                <tr><td rowspan="2">virtual_server_dependencies<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>Specifies the virtual servers on which the current virtual server depends.</div><div>If any of the specified servers are unavailable, the current virtual server is also listed as unavailable.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object virtual_server_dependencies</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>Server which the dependant virtual server is part of.</div>        </td></tr>
                    <tr><td>virtual_server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>Virtual server to depend on.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Enable virtual server
      bigip_gtm_virtual_server:
        server: lb.mydomain.com
        user: admin
        password: secret
        server_name: server1
        name: my-virtual-server
        state: enabled
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
        <td> server_name </td>
        <td> The server name associated with the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/my-gtm-server </td>
    </tr>
            <tr>
        <td> address </td>
        <td> The new address of the resource. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 1.2.3.4 </td>
    </tr>
            <tr>
        <td> port </td>
        <td> The new port of the resource. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 500 </td>
    </tr>
            <tr>
        <td> translation_address </td>
        <td> The new translation address of the resource. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 500 </td>
    </tr>
            <tr>
        <td> translation_port </td>
        <td> The new translation port of the resource. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 500 </td>
    </tr>
            <tr>
        <td> availability_requirements </td>
        <td> The new availability requirement configurations for the resource. </td>
        <td align=center> changed </td>
        <td align=center> dict </td>
        <td align=center> {'type': 'all'} </td>
    </tr>
            <tr>
        <td> monitors </td>
        <td> The new list of monitors for the resource. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/monitor1', '/Common/monitor2'] </td>
    </tr>
            <tr>
        <td> virtual_server_dependencies </td>
        <td> The new list of virtual server dependencies for the resource </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/vs1', '/Common/vs2'] </td>
    </tr>
            <tr>
        <td> link </td>
        <td> The new link value for the resource. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/my-link </td>
    </tr>
            <tr>
        <td> limits </td>
        <td> The new limit configurations for the resource. </td>
        <td align=center> changed </td>
        <td align=center> dict </td>
        <td align=center> {'bits_enabled': True, 'bits_limit': 100} </td>
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