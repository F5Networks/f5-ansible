:source: bigip_vlan.py

:orphan:

.. _bigip_vlan_module:


bigip_vlan - Manage VLANs on a BIG-IP system
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage VLANs on a BIG-IP system




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
                    <b>cmp_hash</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>default</li>
                                                                                                                                                                                                <li>destination-address</li>
                                                                                                                                                                                                <li>source-address</li>
                                                                                                                                                                                                <li>dst-ip</li>
                                                                                                                                                                                                <li>src-ip</li>
                                                                                                                                                                                                <li>dest</li>
                                                                                                                                                                                                <li>destination</li>
                                                                                                                                                                                                <li>source</li>
                                                                                                                                                                                                <li>dst</li>
                                                                                                                                                                                                <li>src</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies how the traffic on the VLAN will be disaggregated. The value selected determines the traffic disaggregation method. You can choose to disaggregate traffic based on <code>source-address</code> (the source IP address), <code>destination-address</code> (destination IP address), or <code>default</code>, which specifies that the default CMP hash uses L4 ports.</div>
                                                    <div>When creating a new VLAN, if this parameter is not specified, the default of <code>default</code> is used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dag_round_robin</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether some of the stateless traffic on the VLAN should be disaggregated in a round-robin order instead of using a static hash. The stateless traffic includes non-IP L2 traffic, ICMP, some UDP protocols, and so on.</div>
                                                    <div>When creating a new VLAN, if this parameter is not specified, the default of (no) is used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dag_tunnel</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>inner</li>
                                                                                                                                                                                                <li>outer</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies how the disaggregator (DAG) distributes received tunnel-encapsulated packets to TMM instances. Select <code>inner</code> to distribute packets based on information in inner headers. Select <code>outer</code> to distribute packets based on information in outer headers without inspecting inner headers.</div>
                                                    <div>When creating a new VLAN, if this parameter is not specified, the default of <code>outer</code> is used.</div>
                                                    <div>This parameter is not supported on Virtual Editions of BIG-IP.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The description to give to the VLAN.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fail_safe</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>yes</code>, specifies that the VLAN takes the specified <code>fail_safe_action</code> if the system detects a loss of traffic on this VLAN&#x27;s interfaces.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fail_safe_action</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>reboot</li>
                                                                                                                                                                                                <li>restart-all</li>
                                                                                                                                                                                                <li>failover</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the action that the system takes when it does not detect any traffic on this VLAN, and the <code>fail_safe_timeout</code> has expired.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fail_safe_timeout</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the number of seconds that a system can run without detecting network traffic on this VLAN before it takes the <code>fail_safe_action</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>interfaces</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Interfaces that you want added to the VLAN. This can include both tagged and untagged interfaces as the <code>tagging</code> parameter specifies.</div>
                                                    <div>This parameter is mutually exclusive with the <code>untagged_interfaces</code> and <code>tagged_interfaces</code> parameters.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>interface</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The name of the interface</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>tagging</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>tagged</li>
                                                                                                                                                                                                <li>untagged</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Whether the interface is <code>tagged</code> or <code>untagged</code>.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>mtu</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the maximum transmission unit (MTU) for traffic on this VLAN. When creating a new VLAN, if this parameter is not specified, the default value used will be <code>1500</code>.</div>
                                                    <div>This number must be between 576 to 9198.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The VLAN to manage. If the special VLAN <code>ALL</code> is specified with the <code>state</code> value of <code>absent</code> then all VLANs will be removed.</div>
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
                    <b>sflow_poll_interval</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the maximum interval in seconds between two pollings.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>sflow_sampling_rate</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the ratio of packets observed to the samples generated.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>source_check</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>yes</code>, specifies that the system verifies that the return route to an initial packet is the same VLAN from which the packet originated.</div>
                                                    <div>The system performs this verification only if the <code>auto_last_hop</code> option is <code>no</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The state of the VLAN on the system. When <code>present</code>, guarantees that the VLAN exists with the provided attributes. When <code>absent</code>, removes the VLAN from the system.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>tag</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Tag number for the VLAN. The tag number can be any integer between 1 and 4094. The system automatically assigns a tag number if you do not specify a value.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>tagged_interfaces</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a list of tagged interfaces and trunks that you want to configure for the VLAN. Use tagged interfaces or trunks when you want to assign a single interface or trunk to multiple VLANs.</div>
                                                    <div>This parameter is mutually exclusive with the <code>untagged_interfaces</code> and <code>interfaces</code> parameters.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: tagged_interface</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>untagged_interfaces</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a list of untagged interfaces and trunks that you want to configure for the VLAN.</div>
                                                    <div>This parameter is mutually exclusive with the <code>tagged_interfaces</code> and <code>interfaces</code> parameters.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: untagged_interface</div>
                                    </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires BIG-IP versions >= 12.0.0
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Create VLAN
      bigip_vlan:
        name: net1
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Set VLAN tag
      bigip_vlan:
        name: net1
        tag: 2345
        provider:
          user: admin
          password: secret
          server: lb.mydomain.com
      delegate_to: localhost

    - name: Add VLAN 2345 as tagged to interface 1.1
      bigip_vlan:
        tagged_interface: 1.1
        name: net1
        tag: 2345
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Add VLAN 1234 as tagged to interfaces 1.1 and 1.2
      bigip_vlan:
        tagged_interfaces:
          - 1.1
          - 1.2
        name: net1
        tag: 1234
        provider:
          user: admin
          password: secret
          server: lb.mydomain.com
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
                    <b>cmp_hash</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New traffic disaggregation method.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">source-address</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>dag_tunnel</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new DAG tunnel setting.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">outer</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The description set on the VLAN.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">foo VLAN</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>fail_safe</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Fail Safe setting.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>fail_safe_action</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Fail Safe Action setting.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">reboot</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>fail_safe_timeout</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Fail Safe Timeout setting.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">90</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>interfaces</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Interfaces that the VLAN is assigned to.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;1.1&#x27;, &#x27;1.2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>partition</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The partition that the VLAN was created on.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Common</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>sflow_poll_interval</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new sFlow Polling Interval setting.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>sflow_sampling_rate</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new sFlow Sampling Rate setting.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">20</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>source_check</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Source Check setting.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>tag</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The ID of the VLAN.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2345</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **stableinterface** which means that the maintainers for this module guarantee that no backward incompatible interface changes will be made.




Author
~~~~~~

- Tim Rupp (@caphrim007)
- Wojciech Wypior (@wojtek0806)

