:source: bigip_apm_network_access.py

:orphan:

.. _bigip_apm_network_access_module:


bigip_apm_network_access - Manage APM Network Access resource
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.9

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage APM Network Access resource.




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
                    <b>allow_local_dns</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables local access to DNS servers configured on client prior to establishing network access connection.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>allow_local_subnet</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables local subnet access and local access to any host or subnet in routes specified in the client routing table.</div>
                                                    <div>When <code>yes</code> the system does not support integrated IP filtering.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>User created network access description.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dns_address_space</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a list of domain names describing the target LAN DNS addresses.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dtls</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>yes</code> the network access connection uses Datagram Transport Level Security instead of TCP, to provide better throughput for high demand applications like VoIP or streaming video.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dtls_port</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the port number that the network access resource uses for secure UDP traffic with DTLS.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>excluded_dns_addresses</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the DNS address spaces for which traffic is not forced through the tunnel.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>excluded_ipv4_adresses</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies IPV4 address spaces for which traffic is not forced through the tunnel.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>subnet</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The address of subnet in CIDR format, e.g. <code>192.168.1.0/24</code></div>
                                                    <div>Host addresses can be specified without the CIDR mask notation.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>excluded_ipv6_adresses</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies IPV6 address spaces for which traffic is not forced through the tunnel.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>subnet</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The address of subnet in CIDR format, e.g. <code>2001:db8:abcd:8000::/52</code></div>
                                                    <div>Host addresses can be specified without the CIDR mask notation.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>ip_version</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>ipv4</li>
                                                                                                                                                                                                <li>ipv4-ipv6</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Supported IP version on the network access resource.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ipv4_addresses_space</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a list of IPv4 hosts or networks describing the target LAN.</div>
                                                    <div>This option is mandatory when creating a new resource and <code>split_tunnel</code> is set to <code>yes</code>.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>subnet</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The address of subnet in CIDR format, e.g. <code>192.168.1.0/24</code></div>
                                                    <div>Host addresses can be specified without the CIDR mask notation.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>ipv4_lease_pool</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies IPV4 lease pool resource to use with network access.</div>
                                                    <div>Referencing lease pool can be done in the full path format for example, <code>/Common/pool_name</code>.</div>
                                                    <div>When lease pool is referenced in full path format, the <code>partition</code> parameter is ignored.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ipv6_address_space</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a list of IPv6 hosts or networks describing the target LAN.</div>
                                                    <div>This option is mandatory when creating a new resource and <code>split_tunnel</code> is set to <code>yes</code>.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>subnet</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The address of subnet in CIDR format, e.g. <code>2001:db8:abcd:8000::/52</code></div>
                                                    <div>Host addresses can be specified without the CIDR mask notation.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>ipv6_lease_pool</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies IPV6 lease pool resource to use with network access.</div>
                                                    <div>Referencing lease pool can be done in the full path format for example, <code>/Common/pool_name</code>.</div>
                                                    <div>When lease pool is referenced in full path format, the <code>partition</code> parameter is ignored.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the APM network access to manage/create.</div>
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
                                                                <td colspan="2">
                    <b>snat_pool</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of a SNAT pool used for implementing selective and intelligent SNATs.</div>
                                                    <div>When <code>none</code> the system uses no SNAT pool for this network resource.</div>
                                                    <div>When <code>automap</code> the system uses all of the self IP addresses as the translation addresses for the pool.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>split_tunnel</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies that only the traffic targeted to a specified address space is sent over the network access tunnel.</div>
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
                                                                        <div>When <code>state</code> is <code>present</code>, ensures that the ACL exists.</div>
                                                    <div>When <code>state</code> is <code>absent</code>, ensures that the ACL is removed.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Create a split tunnel IPV4 Network Access
      bigip_apm_network_access:
        name: foobar
        ip_version: ipv4
        split_tunnel: yes
        snat_pool: "none"
        ipv4_lease_pool: leasefoo
        ipv4_address_space:
          - subnet: 10.10.1.1
          - subnet: 10.10.2.0/24
        excluded_ipv4_adresses:
          - subnet: 192.168.1.0/24
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Modify a split tunnel IPV4 Network Access
      bigip_apm_network_access:
        name: foobar
        snat_pool: /Common/poolsnat
        ipv4_address_space:
          - subnet: 172.16.23.0/24
        excluded_ipv4_adresses:
          - subnet: 10.10.2.0/24
        allow_local_subnet: yes
        allow_local_dns: yes
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Remove Network Access
      bigip_apm_network_access:
        name: foobar
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
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="2">
                    <b>allow_local_dns</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables local access to DNS servers configured on client.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>allow_local_subnet</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables local subnet access.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new description of Network Access.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">My Access</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>dns_address_space</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies a list of domain names describing the target LAN DNS addresses.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;internal.net&#x27;, &#x27;*.engnet.org&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>dtls</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables use of DTLS by network access.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>dtls_port</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies the port number that the network access resource uses for DTLS.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">4433</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>excluded_dns_addresses</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies the DNS address spaces for which traffic is not forced through the tunnel.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;foobar.com&#x27;, &#x27;bazbar.org&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>excluded_ipv4_adresses</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies IPV4 address spaces for which traffic is not forced through the tunnel.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>subnet</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The host or network address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">192.168.10.1</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>excluded_ipv6_adresses</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies IPV6 address spaces for which traffic is not forced through the tunnel.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>subnet</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The host or network address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2001:DB8:ABCD:0012::0</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>ip_version</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Supported IP version on the network access resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">ipv4-ipv6</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ipv4_addresses_space</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies a list of IPv4 hosts or networks describing the target LAN.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>subnet</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The host or network address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">192.168.10.1</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>ipv4_lease_pool</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies IPV4 lease pool resource to use with network access.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/leasepoolv4</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ipv6_address_space</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies a list of IPv6 hosts or networks describing the target LAN.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>subnet</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The host or network address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2001:DB8:ABCD:0012::0</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>ipv6_lease_pool</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies IPV6 lease pool resource to use with network access.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/leasepoolv6</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>snat_pool</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of a SNAT pool used by network access resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/my-pool</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>split_tunnel</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables split tunnel on network access resource.</div>
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

