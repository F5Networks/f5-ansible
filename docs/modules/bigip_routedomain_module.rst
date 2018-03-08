.. _bigip_routedomain:


bigip_routedomain - Manage route domains on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage route domains on a BIG-IP.


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
                <tr><td>bwc_policy<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The bandwidth controller for the route domain.</div>        </td></tr>
                <tr><td>connection_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The maximum number of concurrent connections allowed for the route domain. Setting this to <code>0</code> turns off connection limits.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies descriptive text that identifies the route domain.</div>        </td></tr>
                <tr><td>flow_eviction_policy<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The eviction policy to use with this route domain. Apply an eviction policy to provide customized responses to flow overflows and slow flows on the route domain.</div>        </td></tr>
                <tr><td>id<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The unique identifying integer representing the route domain.</div><div>This field is required when creating a new route domain.</div><div>In version 2.5, this value is no longer used to reference a route domain when making modifications to it (for instance during update and delete operations). Instead, the <code>name</code> parameter is used. In version 2.6, the <code>name</code> value will become a required parameter.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The name of the route domain.</div><div>When creating a new route domain, if this value is not specified, then the value of <code>id</code> will be used for it.</div>        </td></tr>
                <tr><td>parent<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the route domain the system searches when it cannot find a route in the configured domain.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Partition to create the route domain on. Partitions cannot be updated once they are created.</div>        </td></tr>
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
                <tr><td>routing_protocol<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>BFD</li><li>BGP</li><li>IS-IS</li><li>OSPFv2</li><li>OSPFv3</li><li>PIM</li><li>RIP</li><li>RIPng</li></ul></td>
        <td><div>Dynamic routing protocols for the system to use in the route domain.</div>        </td></tr>
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
                <tr><td>service_policy<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Service policy to associate with the route domain.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the route domain should exist or not.</div>        </td></tr>
                <tr><td>strict<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system enforces cross-routing restrictions or not.</div>        </td></tr>
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
                <tr><td>vlans<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>VLANs for the system to use in the route domain</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a route domain
      bigip_routedomain:
        name: foo
        id: 1234
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Set VLANs on the route domain
      bigip_routedomain:
        name: bar
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
        vlans:
          - net1
          - foo
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
        <td> flow_eviction_policy </td>
        <td> The new eviction policy to use with this route domain </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/default-eviction-policy </td>
    </tr>
            <tr>
        <td> service_policy </td>
        <td> The new service policy to use with this route domain </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common-my-service-policy </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The description of the route domain </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> route domain foo </td>
    </tr>
            <tr>
        <td> parent </td>
        <td> The new parent route domain </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 0 </td>
    </tr>
            <tr>
        <td> connection_limit </td>
        <td> The new connection limit for the route domain </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 100 </td>
    </tr>
            <tr>
        <td> strict </td>
        <td> The new strict isolation setting </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> routing_protocol </td>
        <td> List of routing protocols applied to the route domain </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['bfd', 'bgp'] </td>
    </tr>
            <tr>
        <td> bwc_policy </td>
        <td> The new bandwidth controller </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/foo </td>
    </tr>
            <tr>
        <td> vlans </td>
        <td> List of new VLANs the route domain is applied to </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/http-tunnel', '/Common/socks-tunnel'] </td>
    </tr>
            <tr>
        <td> id </td>
        <td> The ID of the route domain that was changed </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2 </td>
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