:source: bigip_node.py

:orphan:

.. _bigip_node_module:


bigip_node - Manages F5 BIG-IP LTM nodes
++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages F5 BIG-IP LTM nodes.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- f5-sdk >= 3.0.9


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                    <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="2">
                    <b>address</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>IP address of the node. This can be either IPv4 or IPv6. When creating a new node, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: ip, host</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>connection_limit</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Node connection limit. Setting this to 0 disables the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies descriptive text that identifies the node.</div>
                                                    <div>You can remove a description by either specifying an empty string, or by specifying the special value <code>none</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dynamic_ratio</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The dynamic ratio number for the node. Used for dynamic ratio load balancing.</div>
                                                    <div>When creating a new node, if this parameter is not specified, the default of <code>1</code> will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fqdn</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>FQDN name of the node. This can be any name that is a valid RFC 1123 DNS name. Therefore, the only characters that can be used are &quot;A&quot; to &quot;Z&quot;, &quot;a&quot; to &quot;z&quot;, &quot;0&quot; to &quot;9&quot;, the hyphen (&quot;-&quot;) and the period (&quot;.&quot;).</div>
                                                    <div>FQDN names must include at lease one period; delineating the host from the domain. ex. <code>host.domain</code>.</div>
                                                    <div>FQDN names must end with a letter or a number.</div>
                                                    <div>When creating a new node, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: hostname</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fqdn_address_type</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>ipv4</li>
                                                                                                                                                                                                <li>ipv6</li>
                                                                                                                                                                                                <li>all</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the FQDN of the node resolves to an IPv4 or IPv6 address.</div>
                                                    <div>When creating a new node, if this parameter is not specified and <code>fqdn</code> is specified, this parameter will default to <code>ipv4</code>.</div>
                                                    <div>This parameter cannot be changed after it has been set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fqdn_auto_populate</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system automatically creates ephemeral nodes using the IP addresses returned by the resolution of a DNS query for a node defined by an FQDN.</div>
                                                    <div>When <code>yes</code>, the system generates an ephemeral node for each IP address returned in response to a DNS query for the FQDN of the node. Additionally, when a DNS response indicates the IP address of an ephemeral node no longer exists, the system deletes the ephemeral node.</div>
                                                    <div>When <code>no</code>, the system resolves a DNS query for the FQDN of the node with the single IP address associated with the FQDN.</div>
                                                    <div>When creating a new node, if this parameter is not specified and <code>fqdn</code> is specified, this parameter will default to <code>yes</code>.</div>
                                                    <div>This parameter cannot be changed after it has been set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fqdn_down_interval</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the interval in which a query occurs, when the DNS server is down. The associated monitor continues polling as long as the DNS server is down.</div>
                                                    <div>When creating a new node, if this parameter is not specified and <code>fqdn</code> is specified, this parameter will default to <code>5</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fqdn_up_interval</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the interval in which a query occurs, when the DNS server is up. The associated monitor attempts to probe three times, and marks the server down if it there is no response within the span of three times the interval value, in seconds.</div>
                                                    <div>This parameter accepts a value of <code>ttl</code> to query based off of the TTL of the FQDN. The default TTL interval is akin to specifying <code>3600</code>.</div>
                                                    <div>When creating a new node, if this parameter is not specified and <code>fqdn</code> is specified, this parameter will default to <code>3600</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>monitor_type</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 1.3)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>and_list</li>
                                                                                                                                                                                                <li>m_of_n</li>
                                                                                                                                                                                                <li>single</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Monitor rule type when <code>monitors</code> is specified. When creating a new pool, if this value is not specified, the default of &#x27;and_list&#x27; will be used.</div>
                                                    <div>Both <code>single</code> and <code>and_list</code> are functionally identical since BIG-IP considers all monitors as &quot;a list&quot;. BIG=IP either has a list of many, or it has a list of one. Where they differ is in the extra guards that <code>single</code> provides; namely that it only allows a single monitor.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>monitors</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the health monitors that the system currently uses to monitor this node.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the node.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>partition</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">Common</div>
                                    </td>
                                                                <td>
                                                                        <div>Device partition to manage resources on.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>provider</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>A dict object containing connection details.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>server_port</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>validate_certs</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">10</div>
                                    </td>
                                                                <td>
                                                                        <div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>ssh_keyfile</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>transport</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>rest</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>cli</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>quorum</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Monitor quorum value when <code>monitor_type</code> is <code>m_of_n</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>rate_limit</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Node rate limit (connections-per-second). Setting this to 0 disables the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ratio</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Node ratio weight. Valid values range from 1 through 100.</div>
                                                    <div>When creating a new node, if this parameter is not specified, the default of <code>1</code> will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>server_port</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>offline</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the current state of the node. <code>enabled</code> (All traffic allowed), specifies that system sends traffic to this node regardless of the node&#x27;s state. <code>disabled</code> (Only persistent or active connections allowed), Specifies that the node can handle only persistent or active connections. <code>offline</code> (Only active connections allowed), Specifies that the node can handle only active connections. In all cases except <code>absent</code>, the node will be created if it does not yet exist.</div>
                                                    <div>Be particularly careful about changing the status of a node whose FQDN cannot be resolved. These situations disable your ability to change their <code>state</code> to <code>disabled</code> or <code>offline</code>. They will remain in an *Unavailable - Enabled* state.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>validate_certs</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.0)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.


Examples
--------

.. code-block:: yaml

    
    - name: Add node
      bigip_node:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        partition: Common
        host: 10.20.30.40
        name: 10.20.30.40
      delegate_to: localhost

    - name: Add node with a single 'ping' monitor
      bigip_node:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        partition: Common
        host: 10.20.30.40
        name: mytestserver
        monitors:
          - /Common/icmp
      delegate_to: localhost

    - name: Modify node description
      bigip_node:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        partition: Common
        name: 10.20.30.40
        description: Our best server yet
      delegate_to: localhost

    - name: Delete node
      bigip_node:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        partition: Common
        name: 10.20.30.40
      delegate_to: localhost

    - name: Force node offline
      bigip_node:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: disabled
        partition: Common
        name: 10.20.30.40
      delegate_to: localhost

    - name: Add node by their FQDN
      bigip_node:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        partition: Common
        fqdn: foo.bar.com
        name: 10.20.30.40
      delegate_to: localhost




Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                                                                        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed and success</td>
                <td>
                                                                        <div>Changed value for the description of the node.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">E-Commerce webserver in ORD</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>monitor_type</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed and success</td>
                <td>
                                                                        <div>Changed value for the monitor_type of the node.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">m_of_n</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>monitors</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed and success</td>
                <td>
                                                                        <div>Changed list of monitors for the node.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;icmp&#x27;, &#x27;tcp_echo&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>quorum</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed and success</td>
                <td>
                                                                        <div>Changed value for the quorum of the node.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>session</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed and success</td>
                <td>
                                                                        <div>Changed value for the internal session of the node.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">user-disabled</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>state</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed and success</td>
                <td>
                                                                        <div>Changed value for the internal state of the node.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">m_of_n</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

