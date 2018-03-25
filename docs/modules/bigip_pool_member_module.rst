.. _bigip_pool_member:


bigip_pool_member - Manages F5 BIG-IP LTM pool members
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP LTM pool members via iControl SOAP API.


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
                <tr><td>address<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>IP address of the pool member. This can be either IPv4 or IPv6. When creating a new pool member, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div></br>
    <div style="font-size: small;">aliases: ip, host<div>        </td></tr>
                <tr><td>connection_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member connection limit. Setting this to 0 disables the limit.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member description.</div>        </td></tr>
                <tr><td>fqdn<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>FQDN name of the pool member. This can be any name that is a valid RFC 1123 DNS name. Therefore, the only characters that can be used are &quot;A&quot; to &quot;Z&quot;, &quot;a&quot; to &quot;z&quot;, &quot;0&quot; to &quot;9&quot;, the hyphen (&quot;-&quot;) and the period (&quot;.&quot;).</div><div>FQDN names must include at lease one period; delineating the host from the domain. ex. <code>host.domain</code>.</div><div>FQDN names must end with a letter or a number.</div><div>When creating a new pool member, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div></br>
    <div style="font-size: small;">aliases: hostname<div>        </td></tr>
                <tr><td>fqdn_auto_populate<br/><div style="font-size: small;"> (added in 2.6)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies whether the system automatically creates ephemeral nodes using the IP addresses returned by the resolution of a DNS query for a node defined by an FQDN.</div><div>When <code>enabled</code>, the system generates an ephemeral node for each IP address returned in response to a DNS query for the FQDN of the node. Additionally, when a DNS response indicates the IP address of an ephemeral node no longer exists, the system deletes the ephemeral node.</div><div>When <code>disabled</code>, the system resolves a DNS query for the FQDN of the node with the single IP address associated with the FQDN.</div><div>When creating a new pool member, the default for this parameter is <code>yes</code>.</div><div>This parameter is ignored when <code>reuse_nodes</code> is <code>yes</code>.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Name of the node to create, or re-use, when creating a new pool member.</div><div>This parameter is optional and, if not specified, a node name will be created automatically from either the specified <code>address</code> or <code>fqdn</code>.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Partition</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td>pool<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Pool name. This pool must exist.</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Pool member port.</div><div>This value cannot be changed after it has been set.</div>        </td></tr>
                <tr><td>preserve_node<br/><div style="font-size: small;"> (added in 2.1)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>When state is <code>absent</code> attempts to remove the node that the pool member references.</div><div>The node will not be removed if it is still referenced by other pool members. If this happens, the module will not raise an error.</div><div>Setting this to <code>yes</code> disables this behavior.</div>        </td></tr>
                <tr><td>priority_group<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies a number representing the priority group for the pool member.</div><div>When adding a new member, the default is 0, meaning that the member has no priority.</div><div>To specify a priority, you must activate priority group usage when you create a new pool or when adding or removing pool members. When activated, the system load balances traffic according to the priority group number assigned to the pool member.</div><div>The higher the number, the higher the priority, so a member with a priority of 3 has higher priority than a member with a priority of 1.</div>        </td></tr>
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
                <tr><td>rate_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member rate limit (connections-per-second). Setting this to 0 disables the limit.</div>        </td></tr>
                <tr><td>ratio<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member ratio weight. Valid values range from 1 through 100. New pool members -- unless overridden with this value -- default to 1.</div>        </td></tr>
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
    <td>yes</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li><li>forced_offline</li></ul></td>
        <td><div>Pool member state.</div>        </td></tr>
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

    
    - name: Add pool member
      bigip_pool_member:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
        description: web server
        connection_limit: 100
        rate_limit: 50
        ratio: 2
      delegate_to: localhost

    - name: Modify pool member ratio and description
      bigip_pool_member:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
        ratio: 1
        description: nginx server
      delegate_to: localhost

    - name: Remove pool member from pool
      bigip_pool_member:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
      delegate_to: localhost

    - name: Force pool member offline
      bigip_pool_member:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: forced_offline
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
      delegate_to: localhost

    - name: Create members with priority groups
      bigip_pool_member:
        server: lb.mydomain.com
        user: admin
        password: secret
        pool: my-pool
        partition: Common
        host: "{{ item.address }}"
        name: "{{ item.name }}"
        priority_group: "{{ item.priority_group }}"
        port: 80
      delegate_to: localhost
      loop:
        - host: 1.1.1.1
          name: web1
          priority_group: 4
        - host: 2.2.2.2
          name: web2
          priority_group: 3
        - host: 3.3.3.3
          name: web3
          priority_group: 2
        - host: 4.4.4.4
          name: web4
          priority_group: 1      


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
        <td> rate_limit </td>
        <td> The new rate limit, in connections per second, of the pool member. </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 100 </td>
    </tr>
            <tr>
        <td> connection_limit </td>
        <td> The new connection limit of the pool member </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 1000 </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The new description of pool member. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> My pool member </td>
    </tr>
            <tr>
        <td> ratio </td>
        <td> The new pool member ratio weight. </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 50 </td>
    </tr>
            <tr>
        <td> priority_group </td>
        <td> The new priority group. </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 3 </td>
    </tr>
            <tr>
        <td> fqdn_auto_populate </td>
        <td> Whether FQDN auto population was set on the member or not. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> fqdn </td>
        <td> The FQDN of the pool member. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> foo.bar.com </td>
    </tr>
            <tr>
        <td> address </td>
        <td> The address of the pool member. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 1.2.3.4 </td>
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