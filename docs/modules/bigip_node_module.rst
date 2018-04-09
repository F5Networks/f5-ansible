:source: modules/bigip_node.py

.. _bigip_node:


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
- netaddr


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                <tr>
            <th class="head"><div class="cell-border">Parameter</div></th>
            <th class="head"><div class="cell-border">Choices/<font color="blue">Defaults</font></div></th>
                        <th class="head" width="100%"><div class="cell-border">Comments</div></th>
        </tr>
                    <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>address</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>IP address of the node. This can be either IPv4 or IPv6. When creating a new node, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div>
                                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: ip, host</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>description</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies descriptive text that identifies the node.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>fqdn</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>FQDN name of the node. This can be any name that is a valid RFC 1123 DNS name. Therefore, the only characters that can be used are &quot;A&quot; to &quot;Z&quot;, &quot;a&quot; to &quot;z&quot;, &quot;0&quot; to &quot;9&quot;, the hyphen (&quot;-&quot;) and the period (&quot;.&quot;).</div>
                                                            <div>FQDN names must include at lease one period; delineating the host from the domain. ex. <code>host.domain</code>.</div>
                                                            <div>FQDN names must end with a letter or a number.</div>
                                                            <div>When creating a new node, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div>
                                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: hostname</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>monitor_type</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 1.3)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                                    <li>and_list</li>
                                                                                                                                                                                                                        <li>m_of_n</li>
                                                                                                                                                                                                                        <li>single</li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Monitor rule type when <code>monitors</code> is specified. When creating a new pool, if this value is not specified, the default of &#x27;and_list&#x27; will be used.</div>
                                                            <div>Both <code>single</code> and <code>and_list</code> are functionally identical since BIG-IP considers all monitors as &quot;a list&quot;. BIG=IP either has a list of many, or it has a list of one. Where they differ is in the extra guards that <code>single</code> provides; namely that it only allows a single monitor.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>monitors</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the health monitors that the system currently uses to monitor this node.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>name</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the name of the node.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>partition</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">Common</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Device partition to manage resources on.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>password</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>provider</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>A dict object containing connection details.</div>
                                                                                                </div>
                </td>
            </tr>
                                                            <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>ssh_keyfile</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>timeout</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">10</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>server</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>user</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>server_port</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">443</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>password</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>validate_certs</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                                    <li>no</li>
                                                                                                                                                                                                                        <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>transport</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                                    <li>rest</li>
                                                                                                                                                                                                                        <li><div style="color: blue"><b>cli</b>&nbsp;&larr;</div></li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                                </div>
                </td>
            </tr>
                    
                                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>quorum</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Monitor quorum value when <code>monitor_type</code> is <code>m_of_n</code>.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>server</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>server_port</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">443</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>state</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                                        <li>absent</li>
                                                                                                                                                                                                                        <li>enabled</li>
                                                                                                                                                                                                                        <li>disabled</li>
                                                                                                                                                                                                                        <li>offline</li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the current state of the node. <code>enabled</code> (All traffic allowed), specifies that system sends traffic to this node regardless of the node&#x27;s state. <code>disabled</code> (Only persistent or active connections allowed), Specifies that the node can handle only persistent or active connections. <code>offline</code> (Only active connections allowed), Specifies that the node can handle only active connections. In all cases except <code>absent</code>, the node will be created if it does not yet exist.</div>
                                                            <div>Be particularly careful about changing the status of a node whose FQDN cannot be resolved. These situations disable your ability to change their <code>state</code> to <code>disabled</code> or <code>offline</code>. They will remain in an *Unavailable - Enabled* state.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>user</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>validate_certs</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.0)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                                    <li>no</li>
                                                                                                                                                                                                                        <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the netaddr Python package on the host. This is as easy as `pip install netaddr`.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as `pip install f5-sdk`.


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
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th class="head"><div class="cell-border">Key</div></th>
            <th class="head"><div class="cell-border">Returned</div></th>
            <th class="head" width="100%"><div class="cell-border">Description</div></th>
        </tr>
                    <tr class="return-value-column">
                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>description</b>
                            <br/><div style="font-size: small; color: red">string</div>
                        </div>
                    </div>
                </td>
                <td><div class="cell-border">changed and success</div></td>
                <td>
                    <div class="cell-border">
                                                                                    <div>Changed value for the description of the node.</div>
                                                                            <br/>
                                                    <div style="font-size: smaller"><b>Sample:</b></div>
                                                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">E-Commerce webserver in ORD</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>monitor_type</b>
                            <br/><div style="font-size: small; color: red">string</div>
                        </div>
                    </div>
                </td>
                <td><div class="cell-border">changed and success</div></td>
                <td>
                    <div class="cell-border">
                                                                                    <div>Changed value for the monitor_type of the node.</div>
                                                                            <br/>
                                                    <div style="font-size: smaller"><b>Sample:</b></div>
                                                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">m_of_n</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>monitors</b>
                            <br/><div style="font-size: small; color: red">list</div>
                        </div>
                    </div>
                </td>
                <td><div class="cell-border">changed and success</div></td>
                <td>
                    <div class="cell-border">
                                                                                    <div>Changed list of monitors for the node.</div>
                                                                            <br/>
                                                    <div style="font-size: smaller"><b>Sample:</b></div>
                                                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;icmp&#x27;, &#x27;tcp_echo&#x27;]</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>quorum</b>
                            <br/><div style="font-size: small; color: red">int</div>
                        </div>
                    </div>
                </td>
                <td><div class="cell-border">changed and success</div></td>
                <td>
                    <div class="cell-border">
                                                                                    <div>Changed value for the quorum of the node.</div>
                                                                            <br/>
                                                    <div style="font-size: smaller"><b>Sample:</b></div>
                                                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>session</b>
                            <br/><div style="font-size: small; color: red">string</div>
                        </div>
                    </div>
                </td>
                <td><div class="cell-border">changed and success</div></td>
                <td>
                    <div class="cell-border">
                                                                                    <div>Changed value for the internal session of the node.</div>
                                                                            <br/>
                                                    <div style="font-size: smaller"><b>Sample:</b></div>
                                                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">user-disabled</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>state</b>
                            <br/><div style="font-size: small; color: red">string</div>
                        </div>
                    </div>
                </td>
                <td><div class="cell-border">changed and success</div></td>
                <td>
                    <div class="cell-border">
                                                                                    <div>Changed value for the internal state of the node.</div>
                                                                            <br/>
                                                    <div style="font-size: smaller"><b>Sample:</b></div>
                                                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">m_of_n</div>
                                            </div>
                </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

