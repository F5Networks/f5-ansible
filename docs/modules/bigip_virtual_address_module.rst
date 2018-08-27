:source: bigip_virtual_address.py

:orphan:

.. _bigip_virtual_address_module:


bigip_virtual_address - Manage LTM virtual addresses on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage LTM virtual addresses on a BIG-IP.



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
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Virtual address. This value cannot be modified after it is set.</div>
                                                    <div>If you never created a virtual address, but did create virtual servers, then a virtual address for each virtual server was created automatically. The name of this virtual address is its IP address value.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>arp</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system accepts ARP requests.</div>
                                                    <div>When <code>no</code>, specifies that the system does not accept ARP requests.</div>
                                                    <div>When <code>yes</code>, then the packets are dropped.</div>
                                                    <div>Note that both ARP and ICMP Echo must be disabled in order for forwarding virtual servers using that virtual address to forward ICMP packets.</div>
                                                    <div>When creating a new virtual address, if this parameter is not specified, the default value is <code>yes</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>arp_state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system accepts ARP requests. When (disabled), specifies that the system does not accept ARP requests. Note that both ARP and ICMP Echo must be disabled in order for forwarding virtual servers using that virtual address to forward ICMP packets. If (enabled), then the packets are dropped.</div>
                                                    <div>Deprecated. Use the <code>arp</code> parameter instead.</div>
                                                    <div>When creating a new virtual address, if this parameter is not specified, the default value is <code>enabled</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>auto_delete</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system automatically deletes the virtual address with the deletion of the last associated virtual server. When <code>disabled</code>, specifies that the system leaves the virtual address even when all associated virtual servers have been deleted. When creating the virtual address, the default value is <code>enabled</code>.</div>
                                                    <div><code>enabled</code> and <code>disabled</code> are deprecated and will be removed in Ansible 2.11. Instead, use known Ansible booleans such as <code>yes</code> and <code>no</code></div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>availability_calculation</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>always</li>
                                                                                                                                                                                                <li>when_all_available</li>
                                                                                                                                                                                                <li>when_any_available</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies what routes of the virtual address the system advertises. When <code>when_any_available</code>, advertises the route when any virtual server is available. When <code>when_all_available</code>, advertises the route when all virtual servers are available. When (always), always advertises the route regardless of the virtual servers available.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: advertise_route</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>connection_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the number of concurrent connections that the system allows on this virtual address.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>icmp_echo</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>selective</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies how the systems sends responses to (ICMP) echo requests on a per-virtual address basis for enabling route advertisement. When <code>enabled</code>, the BIG-IP system intercepts ICMP echo request packets and responds to them directly. When <code>disabled</code>, the BIG-IP system passes ICMP echo requests through to the backend servers. When (selective), causes the BIG-IP system to internally enable or disable responses based on virtual server state; <code>when_any_available</code>, <code>when_all_available, or C(always</code>, regardless of the state of any virtual servers.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the virtual address.</div>
                                                    <div>If this parameter is not provided, then the value of <code>address</code> will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>netmask</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">255.255.255.255</div>
                                    </td>
                                                                <td>
                                                                        <div>Netmask of the provided virtual address. This value cannot be modified after it is set.</div>
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
                    <b>route_advertisement</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>always</li>
                                                                                                                                                                                                <li>selective</li>
                                                                                                                                                                                                <li>any</li>
                                                                                                                                                                                                <li>all</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system uses route advertisement for this virtual address.</div>
                                                    <div>When disabled, the system does not advertise routes for this virtual address.</div>
                                                    <div>The majority of these options are only supported on versions 13.0.0-HF1 or higher. On versions less than this, all choices expect <code>disabled</code> will translate to <code>enabled</code>.</div>
                                                    <div>When <code>always</code>, the BIG-IP system will always advertise the route for the virtual address, regardless of availability status. This requires an <code>enabled</code> virtual address.</div>
                                                    <div>When <code>enabled</code>, the BIG-IP system will advertise the route for the available virtual address, based on the calculation method in the availability calculation.</div>
                                                    <div>When <code>disabled</code>, the BIG-IP system will not advertise the route for the virtual address, regardless of the availability status.</div>
                                                    <div>When <code>selective</code>, you can also selectively enable ICMP echo responses, which causes the BIG-IP system to internally enable or disable responses based on virtual server state. Either <code>any</code> virtual server, <code>all</code> virtual servers, or <code>always</code>, regardless of the state of any virtual server.</div>
                                                    <div>When <code>any</code>, the BIG-IP system will advertise the route for the virtual address when any virtual server is available.</div>
                                                    <div>When <code>all</code>, the BIG-IP system will advertise the route for the virtual address when all virtual servers are available.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>route_domain</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The route domain of the <code>address</code> that you want to use.</div>
                                                    <div>This value cannot be modified after it is set.</div>
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
                    <b>spanning</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables all BIG-IP systems in a device group to listen for and process traffic on the same virtual address.</div>
                                                    <div>Spanning for a virtual address occurs when you enable the <code>spanning</code> option on a device and then sync the virtual address to the other members of the device group.</div>
                                                    <div>Spanning also relies on the upstream router to distribute application flows to the BIG-IP systems using ECMP routes. ECMP defines a route to the virtual address using distinct Floating self-IP addresses configured on each BIG-IP system.</div>
                                                    <div>You must also configure MAC masquerade addresses and disable <code>arp</code> on the virtual address when Spanning is enabled.</div>
                                                    <div>When creating a new virtual address, if this parameter is not specified, the default valus is <code>no</code>.</div>
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
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The virtual address state. If <code>absent</code>, an attempt to delete the virtual address will be made. This will only succeed if this virtual address is not in use by a virtual server. <code>present</code> creates the virtual address and enables it. If <code>enabled</code>, enable the virtual address if it exists. If <code>disabled</code>, create the virtual address if needed, and set state to <code>disabled</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>traffic_group</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The traffic group for the virtual address. When creating a new address, if this value is not specified, the default of <code>/Common/traffic-group-1</code> will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>use_route_advertisement</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system uses route advertisement for this virtual address.</div>
                                                    <div>When disabled, the system does not advertise routes for this virtual address.</div>
                                                    <div>Deprecated. Use the <code>route_advertisement</code> parameter instead.</div>
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
                    <b>address</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>created</td>
                <td>
                                            <div>The address of the virtual address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2345</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>arp</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new way the virtual address handles ARP requests.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>auto_delete</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New setting for auto deleting virtual address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">enabled</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>connection_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new connection limit of the virtual address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1000</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>icmp_echo</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New ICMP echo setting applied to virtual address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">disabled</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>netmask</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>created</td>
                <td>
                                            <div>The netmask of the virtual address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2345</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>spanning</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether spanning is enabled or not</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">disabled</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>state</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new state of the virtual address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">disabled</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>use_route_advertisement</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new setting for whether to use route advertising or not.</div>
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

- Tim Rupp (@caphrim007)

