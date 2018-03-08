.. _bigip_virtual_address:


bigip_virtual_address - Manage LTM virtual addresses on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage LTM virtual addresses on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9
  * netaddr


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
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Virtual address. This value cannot be modified after it is set.</div></br>
    <div style="font-size: small;">aliases: name<div>        </td></tr>
                <tr><td>advertise_route<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>always</li><li>when_all_available</li><li>when_any_available</li></ul></td>
        <td><div>Specifies what routes of the virtual address the system advertises. When <code>when_any_available</code>, advertises the route when any virtual server is available. When <code>when_all_available</code>, advertises the route when all virtual servers are available. When (always), always advertises the route regardless of the virtual servers available.</div>        </td></tr>
                <tr><td>arp_state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system accepts ARP requests. When (disabled), specifies that the system does not accept ARP requests. Note that both ARP and ICMP Echo must be disabled in order for forwarding virtual servers using that virtual address to forward ICMP packets. If (enabled), then the packets are dropped.</div>        </td></tr>
                <tr><td>auto_delete<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system automatically deletes the virtual address with the deletion of the last associated virtual server. When <code>disabled</code>, specifies that the system leaves the virtual address even when all associated virtual servers have been deleted. When creating the virtual address, the default value is <code>enabled</code>.</div>        </td></tr>
                <tr><td>connection_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the number of concurrent connections that the system allows on this virtual address.</div>        </td></tr>
                <tr><td>icmp_echo<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li><li>selective</li></ul></td>
        <td><div>Specifies how the systems sends responses to (ICMP) echo requests on a per-virtual address basis for enabling route advertisement. When <code>enabled</code>, the BIG-IP system intercepts ICMP echo request packets and responds to them directly. When <code>disabled</code>, the BIG-IP system passes ICMP echo requests through to the backend servers. When (selective), causes the BIG-IP system to internally enable or disable responses based on virtual server state; <code>when_any_available</code>, <code>when_all_available, or C(always</code>, regardless of the state of any virtual servers.</div>        </td></tr>
                <tr><td>netmask<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>255.255.255.255</td>
        <td></td>
        <td><div>Netmask of the provided virtual address. This value cannot be modified after it is set.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>The virtual address state. If <code>absent</code>, an attempt to delete the virtual address will be made. This will only succeed if this virtual address is not in use by a virtual server. <code>present</code> creates the virtual address and enables it. If <code>enabled</code>, enable the virtual address if it exists. If <code>disabled</code>, create the virtual address if needed, and set state to <code>disabled</code>.</div>        </td></tr>
                <tr><td>traffic_group<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The traffic group for the virtual address. When creating a new address, if this value is not specified, the default of <code>/Common/traffic-group-1</code> will be used.</div>        </td></tr>
                <tr><td>use_route_advertisement<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Specifies whether the system uses route advertisement for this virtual address. When disabled, the system does not advertise routes for this virtual address.</div>        </td></tr>
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

    
    - name: Add virtual address
      bigip_virtual_address:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: present
        partition: Common
        address: 10.10.10.10
      delegate_to: localhost

    - name: Enable route advertisement on the virtual address
      bigip_virtual_address:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: present
        address: 10.10.10.10
        use_route_advertisement: yes
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
        <td> icmp_echo </td>
        <td> New ICMP echo setting applied to virtual address. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> disabled </td>
    </tr>
            <tr>
        <td> use_route_advertisement </td>
        <td> The new setting for whether to use route advertising or not. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> connection_limit </td>
        <td> The new connection limit of the virtual address. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 1000 </td>
    </tr>
            <tr>
        <td> netmask </td>
        <td> The netmask of the virtual address. </td>
        <td align=center> created </td>
        <td align=center> int </td>
        <td align=center> 2345 </td>
    </tr>
            <tr>
        <td> state </td>
        <td> The new state of the virtual address. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> disabled </td>
    </tr>
            <tr>
        <td> arp_state </td>
        <td> The new way the virtual address handles ARP requests. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> disabled </td>
    </tr>
            <tr>
        <td> address </td>
        <td> The address of the virtual address. </td>
        <td align=center> created </td>
        <td align=center> int </td>
        <td align=center> 2345 </td>
    </tr>
            <tr>
        <td> auto_delete </td>
        <td> New setting for auto deleting virtual address. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr.
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