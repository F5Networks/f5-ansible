:source: bigip_pool_member.py

:orphan:

.. _bigip_pool_member_module:


bigip_pool_member - Manages F5 BIG-IP LTM pool members
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages F5 BIG-IP LTM pool members via iControl SOAP API.




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
                                                                        <div>IP address of the pool member. This can be either IPv4 or IPv6. When creating a new pool member, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: ip, host</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>aggregate</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>List of pool member definitions to be created, modified or removed.</div>
                                                    <div>When using <code>aggregates</code> the if one of the aggregate definitions is invalid, the aggregate run will fail, indicating the error it last encountered.</div>
                                                    <div>The module will <code>NOT</code> rollback any changes it has made prior to encountering the error.</div>
                                                    <div>The module also will not indicate what changes were made prior to failure, therefore it is strongly advised to run the module in check mode to make basic validation, prior to module execution.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: members</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>availability_requirements</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies, if you activate more than one health monitor, the number of health monitors that must receive successful responses in order for the link to be considered available.</div>
                                                    <div>Specifying an empty string will remove the monitors and revert to inheriting from pool (default).</div>
                                                    <div>Specifying <code>none</code> value will remove any health monitoring from the member completely.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>all</li>
                                                                                                                                                                                                <li>at_least</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Monitor rule type when <code>monitors</code> is specified.</div>
                                                    <div>When creating a new pool, if this value is not specified, the default of &#x27;all&#x27; will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>at_least</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the minimum number of active health monitors that must be successful before the link is considered up.</div>
                                                    <div>This parameter is only relevant when a <code>type</code> of <code>at_least</code> is used.</div>
                                                    <div>This parameter will be ignored if a type of <code>all</code> is used.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>connection_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Pool member connection limit. Setting this to 0 disables the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Pool member description.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fqdn</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>FQDN name of the pool member. This can be any name that is a valid RFC 1123 DNS name. Therefore, the only characters that can be used are &quot;A&quot; to &quot;Z&quot;, &quot;a&quot; to &quot;z&quot;, &quot;0&quot; to &quot;9&quot;, the hyphen (&quot;-&quot;) and the period (&quot;.&quot;).</div>
                                                    <div>FQDN names must include at lease one period; delineating the host from the domain. ex. <code>host.domain</code>.</div>
                                                    <div>FQDN names must end with a letter or a number.</div>
                                                    <div>When creating a new pool member, one of either <code>address</code> or <code>fqdn</code> must be provided. This parameter cannot be updated after it is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: hostname</div>
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
                                                    <div>When creating a new pool member, the default for this parameter is <code>yes</code>.</div>
                                                    <div>Once set this parameter cannot be changed afterwards.</div>
                                                    <div>This parameter is ignored when <code>reuse_nodes</code> is <code>yes</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ip_encapsulation</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the IP encapsulation using either IPIP (IP encapsulation within IP, RFC 2003) or GRE (Generic Router Encapsulation, RFC 2784) on outbound packets (from BIG-IP system to server-pool member).</div>
                                                    <div>When <code>none</code>, disables IP encapsulation.</div>
                                                    <div>When <code>inherit</code>, inherits IP encapsulation setting from the member&#x27;s pool.</div>
                                                    <div>When any other value, Options are None, Inherit from Pool, and Member Specific.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>monitors</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the health monitors that the system currently uses to monitor this resource.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the node to create, or re-use, when creating a new pool member.</div>
                                                    <div>This parameter is optional and, if not specified, a node name will be created automatically from either the specified <code>address</code> or <code>fqdn</code>.</div>
                                                    <div>The <code>enabled</code> state is an alias of <code>present</code>.</div>
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
                                                                        <div>Partition to manage resources on.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pool</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Pool name. This pool must exist.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>port</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Pool member port.</div>
                                                    <div>This value cannot be changed after it has been set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>preserve_node</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.1)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When state is <code>absent</code> attempts to remove the node that the pool member references.</div>
                                                    <div>The node will not be removed if it is still referenced by other pool members. If this happens, the module will not raise an error.</div>
                                                    <div>Setting this to <code>yes</code> disables this behavior.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>priority_group</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a number representing the priority group for the pool member.</div>
                                                    <div>When adding a new member, the default is 0, meaning that the member has no priority.</div>
                                                    <div>To specify a priority, you must activate priority group usage when you create a new pool or when adding or removing pool members. When activated, the system load balances traffic according to the priority group number assigned to the pool member.</div>
                                                    <div>The higher the number, the higher the priority, so a member with a priority of 3 has higher priority than a member with a priority of 1.</div>
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
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Pool member rate limit (connections-per-second). Setting this to 0 disables the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ratio</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Pool member ratio weight. Valid values range from 1 through 100. New pool members -- unless overridden with this value -- default to 1.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>replace_all_with</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Remove members not defined in the <code>aggregate</code> parameter.</div>
                                                    <div>This operation is all or none, meaning that it will stop if there are some pool members that cannot be removed.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: purge</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>reuse_nodes</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Reuses node definitions if requested.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>forced_offline</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Pool member state.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - In previous versions of this module, which used the SDK, the ``name`` parameter would act as ``fqdn`` if ``address`` or ``fqdn`` were not provided.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Add pool member
      bigip_pool_member:
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
        description: web server
        connection_limit: 100
        rate_limit: 50
        ratio: 2
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Modify pool member ratio and description
      bigip_pool_member:
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
        ratio: 1
        description: nginx server
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Remove pool member from pool
      bigip_pool_member:
        state: absent
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Force pool member offline
      bigip_pool_member:
        state: forced_offline
        pool: my-pool
        partition: Common
        host: "{{ ansible_default_ipv4['address'] }}"
        port: 80
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Create members with priority groups
      bigip_pool_member:
        pool: my-pool
        partition: Common
        host: "{{ item.address }}"
        name: "{{ item.name }}"
        priority_group: "{{ item.priority_group }}"
        port: 80
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost
      loop:
        - address: 1.1.1.1
          name: web1
          priority_group: 4
        - address: 2.2.2.2
          name: web2
          priority_group: 3
        - address: 3.3.3.3
          name: web3
          priority_group: 2
        - address: 4.4.4.4
          name: web4
          priority_group: 1

    - name: Add pool members aggregate
      bigip_pool_member:
        pool: my-pool
        aggregate:
          - host: 192.168.1.1
            partition: Common
            port: 80
            description: web server
            connection_limit: 100
            rate_limit: 50
            ratio: 2
          - host: 192.168.1.2
            partition: Common
            port: 80
            description: web server
            connection_limit: 100
            rate_limit: 50
            ratio: 2
          - host: 192.168.1.3
            partition: Common
            port: 80
            description: web server
            connection_limit: 100
            rate_limit: 50
            ratio: 2
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Add pool members aggregate, remove non aggregates
      bigip_pool_member:
        pool: my-pool
        aggregate:
          - host: 192.168.1.1
            partition: Common
            port: 80
            description: web server
            connection_limit: 100
            rate_limit: 50
            ratio: 2
          - host: 192.168.1.2
            partition: Common
            port: 80
            description: web server
            connection_limit: 100
            rate_limit: 50
            ratio: 2
          - host: 192.168.1.3
            partition: Common
            port: 80
            description: web server
            connection_limit: 100
            rate_limit: 50
            ratio: 2
        replace_all_with: yes
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
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
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The address of the pool member.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1.2.3.4</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>connection_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new connection limit of the pool member</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1000</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new description of pool member.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">My pool member</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>fqdn</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The FQDN of the pool member.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">foo.bar.com</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>fqdn_auto_populate</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether FQDN auto population was set on the member or not.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>monitors</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new list of monitors for the resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/monitor1&#x27;, &#x27;/Common/monitor2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>priority_group</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new priority group.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">3</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new rate limit, in connections per second, of the pool member.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">100</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>ratio</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new pool member ratio weight.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">50</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>replace_all_with</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Purges all non-aggregate pool members from device</div>
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
- Wojciech Wypior (@wojtek0806)

