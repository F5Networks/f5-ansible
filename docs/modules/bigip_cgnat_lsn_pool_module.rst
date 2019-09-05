:source: bigip_cgnat_lsn_pool.py

:orphan:

.. _bigip_cgnat_lsn_pool_module:


bigip_cgnat_lsn_pool - Manage CGNAT LSN Pools
+++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.1

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage CGNAT LSN Pools.




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
                    <b>backup_members</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies translation IP addresses available for backup members, which is used by Deterministic translation mode if <code>deterministic</code> mode translation fails and falls back to <code>napt</code> mode.</div>
                                                    <div>This is a collection of IP prefixes with their prefix lengths.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>client_conn_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the maximum number of simultaneous translated connections a client or subscriber is allowed to have.</div>
                                                    <div>Valid range of values is between <code>0</code> and <code>4294967295</code> inclusive.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>User created lsn pool description.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>egress_interfaces</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the set of interfaces on which the source address translation is allowed or disallowed, as determined by the <code>egress_intf_enabled</code> setting.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>egress_intf_enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies how the system handles address translation on the interfaces specified in <code>egress_interfaces</code>.</div>
                                                    <div>When set to <code>yes</code> the source address translation is allowed only on the specified <code>egress_interfaces</code>.</div>
                                                    <div>When set to <code>no</code> source address translation is disabled on specified <code>egress_interfaces</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>harpin_mode</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables or disables hairpinning for incoming connections to active translation end-points.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>icmp_echo</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables or disables ICMP echo on translated addresses.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>inbound_connections</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>explicit</li>
                                                                                                                                                                                                <li>automatic</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Controls whether or not the BIG-IP system supports inbound connections for each outbound mapping.</div>
                                                    <div>When <code>disabled</code> system does not support inbound connections for outbound mappings, which prevents Port Control Protocol <code>pcp</code> from functioning.</div>
                                                    <div>When <code>explicit</code> system supports inbound connections for explicit outbound mappings.</div>
                                                    <div>When <code>automatic</code> system supports inbound connections for every outbound mapping as it gets used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>log_profile</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the logging profile the pool uses.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>log_publisher</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the log publisher that logs translation events.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>members</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the set of translation IP addresses available in the pool. This is a collection of IP prefixes with their prefix lengths.</div>
                                                    <div>All public-side addresses come from the addresses in this group of subnets. Members of two or more deterministic LSN pools must not overlap. Every external address used for deterministic mapping must occur only in one LSN pool.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>mode</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>napt</li>
                                                                                                                                                                                                <li>deterministic</li>
                                                                                                                                                                                                <li>pba</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the translation address mapping mode.</div>
                                                    <div>The <code>napt</code> mode provides standard address and port translation allowing multiple clients in a private network to access remote networks using the single IP address assigned to their router.</div>
                                                    <div>The <code>deterministic</code> address translation mode provides address translation that eliminates logging of every address mapping, while still allowing internal client address tracking using only an external address and port, and a destination address and port.</div>
                                                    <div>The <code>pba</code>mode logs the allocation and release of port blocks for subscriber translation requests, instead of separately logging each translation request.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the lsn pool to manage.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>partition</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">Common</div>
                                    </td>
                                                                <td>
                                                                        <div>Device partition to manage resources on.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pba_block_idle_timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the timeout duration subsequent to the point when the port block becomes idle.</div>
                                                    <div>Valid range of values is between <code>0</code> and <code>4294967295</code> inclusive.&quot;</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pba_block_lifetime</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the timeout for the port block, after which the block is not used for new port allocations.</div>
                                                    <div>Valid range of values is between <code>0</code> and <code>4294967295</code> inclusive.</div>
                                                    <div>The value of <code>0</code> corresponds to an infinite timeout.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pba_block_size</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the number of ports in a block.</div>
                                                    <div>Valid range of values is between <code>0</code> and <code>65535</code> inclusive.</div>
                                                    <div>The <code>pba_block_size</code> value be less than or equal to the LSN pool range i.e range of ports defined by <code>port_range_low</code> and <code>port_range_high</code> values.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pba_client_block_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the number of blocks that can be assigned to a single subscriber IP address.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pba_zombie_timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the timeout duration for a zombie port block, which is a timed out port block with one or more active connections. When the timeout duration expires, connections using the zombie block are killed and the zombie port block becomes an available port block.</div>
                                                    <div>The value of <code>0</code> corresponds to an infinite timeout.</div>
                                                    <div>System ignores this parameter value if <code>pba_block_lifetime</code> is <code>0</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>persistence_mode</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>address</li>
                                                                                                                                                                                                <li>address-port</li>
                                                                                                                                                                                                <li>none</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the persistence settings for LSN translation entries.</div>
                                                    <div>When <code>address</code> the translation attempts to reuse the address mapping, but not the port mapping.</div>
                                                    <div>When <code>address-port</code> the translation attempts to reuse both the address and port mapping  for subsequent packets sent from the same internal IP address and port.</div>
                                                    <div>When <code>none</code> the peristence is disabled.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>persistence_timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the persistence timeout value for LSN translation entries.</div>
                                                    <div>If a particular mapping is unused for this length of time, the mapping expires and the public-side address/port pair is free for use in other mappings.</div>
                                                    <div>Valid range of values is between <code>0</code> and <code>31536000</code> inclusive.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>port_range_high</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the high end of the range of port numbers available for use with translation IP addresses.</div>
                                                    <div>The <code>port_range_high</code> must always be higher or equal to <code>port_range_high</code> value.</div>
                                                    <div>Valid range of values is between <code>0</code> and <code>65535</code> inclusive.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>port_range_low</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the low end of the range of port numbers available for use with translation IP addresses.</div>
                                                    <div>The <code>port_range_low</code> must always be lower or equal to <code>port_range_high</code> value.</div>
                                                    <div>Valid range of values is between <code>0</code> and <code>65535</code> inclusive.</div>
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
                                                                        <div>The password for the user account used to connect to the BIG-IP.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_PASSWORD</code>.</div>
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
                                                                        <div>The BIG-IP host.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER</code>.</div>
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
                                                                        <div>The BIG-IP server port.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER_PORT</code>.</div>
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
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_USER</code>.</div>
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
                                                                        <div>If <code>no</code>, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_VALIDATE_CERTS</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>timeout</b>
                                                        </td>
                                <td>
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
                                                                        <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports.</div>
                                                    <div>You may omit this option by setting the environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>transport</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>cli</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>rest</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>auth_provider</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Configures the auth provider for to obtain authentication tokens from the remote device.</div>
                                                    <div>This option is really used when working with BIG-IQ devices.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>route_advertisement</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the translation addresses are passed to the Advanced Routing Module for advertisement through dynamic routing protocols.</div>
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
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>state</code> is <code>present</code>, ensures that the LSN pool exists.</div>
                                                    <div>When <code>state</code> is <code>absent</code>, ensures that the LSN pool is removed.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires CGNAT licensed and enabled on BIG-IP.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Create an lsn pool
      bigip_cgnat_lsn_pool:
        name: foo
        mode: napt
        client_conn_limit: 100
        log_profile: foo_profile
        log_publisher: foo_publisher
        members:
          - 10.1.1.0/24
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Update lsn pool
      bigip_cgnat_lsn_pool:
        name: foo
        mode: pba
        pba_block_size: 128
        pba_block_lifetime: 7200
        pba_block_idle_timeout: 1800
        pba_zombie_timeout: 900
        log_profile: foo_profile
        log_publisher: foo_publisher
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Remove lsn pool
      bigip_cgnat_lsn_pool:
        name: foo
        state: absent
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
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
                    <b>backup_members</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The translation IP addresses available for backup members.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/10.10.10.0/24&#x27;, &#x27;/Common/11.11.11.0/25&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>client_conn_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The maximum number of simultaneous translated connections a client or subscriber is allowed to have.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">50</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>User created LSN pool description.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">some description</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>egress_interfaces</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The set of interfaces on which the source address translation is allowed or disallowed.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/tunnel1&#x27;, &#x27;/Common/tunnel2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>egress_intf_enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies how the system handles address translation on the egress interfaces.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>harpin_mode</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables or disables hairpinning for incoming connections to active translation end-points.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>icmp_echo</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables or disables ICMP echo on translated addresses.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>inbound_connections</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Controls BIG-IP system support of inbound connections for each outbound mapping.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">explicit</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>log_profile</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of the logging profile the pool uses.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/foo_log_profile</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>log_publisher</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of the log publisher that logs translation events.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/publisher_1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>members</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The et of translation IP addresses available in the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/10.10.10.0/24&#x27;, &#x27;/Common/11.11.11.0/25&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>mode</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies the translation address mapping mode.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">napt</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>pba_block_idle_timeout</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The timeout duration subsequent to the point when the port block becomes idle.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">3600</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>pba_block_lifetime</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The timeout for the port block.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">7200</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>pba_block_size</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The number of ports in a block.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">128</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>pba_client_block_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The number of blocks that can be assigned to a single subscriber IP address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">3</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>pba_zombie_timeout</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The timeout duration for a zombie port block.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">180</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>persistence_mode</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies the persistence settings for LSN translation entries.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">address</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>persistence_timeout</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies the persistence timeout value for LSN translation entries.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">500</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>port_range_high</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The high end of the range of port numbers available for use with translation IP addresses.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">65535</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>port_range_low</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The low end of the range of port numbers available for use with translation IP addresses.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1025</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>route_advertisement</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies whether the translation addresses are advertised through dynamic routing protocols.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Wojciech Wypior (@wojtek0806)

