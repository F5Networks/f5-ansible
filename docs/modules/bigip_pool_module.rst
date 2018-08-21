:source: bigip_pool.py

:orphan:

.. _bigip_pool_module:


bigip_pool - Manages F5 BIG-IP LTM pools
++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages F5 BIG-IP LTM pools via iControl REST API.



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
                    <b>description</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.3)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies descriptive text that identifies the pool.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>lb_method</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 1.3)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>dynamic-ratio-member</li>
                                                                                                                                                                                                <li>dynamic-ratio-node</li>
                                                                                                                                                                                                <li>fastest-app-response</li>
                                                                                                                                                                                                <li>fastest-node</li>
                                                                                                                                                                                                <li>least-connections-member</li>
                                                                                                                                                                                                <li>least-connections-node</li>
                                                                                                                                                                                                <li>least-sessions</li>
                                                                                                                                                                                                <li>observed-member</li>
                                                                                                                                                                                                <li>observed-node</li>
                                                                                                                                                                                                <li>predictive-member</li>
                                                                                                                                                                                                <li>predictive-node</li>
                                                                                                                                                                                                <li>ratio-least-connections-member</li>
                                                                                                                                                                                                <li>ratio-least-connections-node</li>
                                                                                                                                                                                                <li>ratio-member</li>
                                                                                                                                                                                                <li>ratio-node</li>
                                                                                                                                                                                                <li>ratio-session</li>
                                                                                                                                                                                                <li>round-robin</li>
                                                                                                                                                                                                <li>weighted-least-connections-member</li>
                                                                                                                                                                                                <li>weighted-least-connections-node</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Load balancing method. When creating a new pool, if this value is not specified, the default of <code>round-robin</code> will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>metadata</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Arbitrary key/value pairs that you can attach to a pool. This is useful in situations where you might want to annotate a pool to me managed by Ansible.</div>
                                                    <div>Key names will be stored as strings; this includes names that are numbers.</div>
                                                    <div>Values for all of the keys will be stored as strings; this includes values that are numbers.</div>
                                                    <div>Data will be persisted, not ephemeral.</div>
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
                                                                        <div>Monitor rule type when <code>monitors</code> is specified.</div>
                                                    <div>When creating a new pool, if this value is not specified, the default of &#x27;and_list&#x27; will be used.</div>
                                                    <div>When <code>single</code> ensures that all specified monitors are checked, but additionally includes checks to make sure you only specified a single monitor.</div>
                                                    <div>When <code>and_list</code> ensures that <b>all</b> monitors are checked.</div>
                                                    <div>When <code>m_of_n</code> ensures that <code>quorum</code> of <code>monitors</code> are checked. <code>m_of_n</code> <b>requires</b> that a <code>quorum</code> of 1 or greater be set either in the playbook, or already existing on the device.</div>
                                                    <div>Both <code>single</code> and <code>and_list</code> are functionally identical since BIG-IP considers all monitors as &quot;a list&quot;.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>monitors</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 1.3)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Monitor template name list. If the partition is not provided as part of the monitor name, then the <code>partition</code> option will be used instead.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Pool name</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pool</div>
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
                    <b>priority_group_activation</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system load balances traffic according to the priority number assigned to the pool member.</div>
                                                    <div>When creating a new pool, if this parameter is not specified, the default of <code>0</code> will be used.</div>
                                                    <div>To disable this setting, provide the value <code>0</code>.</div>
                                                    <div>Once you enable this setting, you can specify pool member priority when you create a new pool or on a pool member&#x27;s properties screen.</div>
                                                    <div>The system treats same-priority pool members as a group.</div>
                                                    <div>To enable priority group activation, provide a number from <code>0</code> to <code>65535</code> that represents the minimum number of members that must be available in one priority group before the system directs traffic to members in a lower priority group.</div>
                                                    <div>When a sufficient number of members become available in the higher priority group, the system again directs traffic to the higher priority group.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: minimum_active_members</div>
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
                                        <br/><div style="font-size: small; color: darkgreen">(added in 1.3)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Monitor quorum value when <code>monitor_type</code> is <code>m_of_n</code>.</div>
                                                    <div>Quorum must be a value of 1 or greater when <code>monitor_type</code> is <code>m_of_n</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>reselect_tries</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Sets the number of times the system tries to contact a pool member after a passive failure.</div>
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
                    <b>service_down_action</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 1.3)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>none</li>
                                                                                                                                                                                                <li>reset</li>
                                                                                                                                                                                                <li>drop</li>
                                                                                                                                                                                                <li>reselect</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Sets the action to take when node goes down in pool.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>slow_ramp_time</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 1.3)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Sets the ramp-up time (in seconds) to gradually ramp up the load on newly added or freshly detected up pool members.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>present</code>, guarantees that the pool exists with the provided attributes.</div>
                                                    <div>When <code>absent</code>, removes the pool from the system.</div>
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
    - To add members do a pool, use the ``bigip_pool_member`` module. Previously, the ``bigip_pool`` module allowed the management of users, but this has been removed in version 2.5 of Ansible.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.


Examples
--------

.. code-block:: yaml

    
    - name: Create pool
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
        partition: Common
        lb_method: least-connections-member
        slow_ramp_time: 120
      delegate_to: localhost

    - name: Modify load balancer method
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
        partition: Common
        lb_method: round-robin
      delegate_to: localhost

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
      delegate_to: localhost

    - name: Set a single monitor (with enforcement)
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
        partition: Common
        monitor_type: single
        monitors:
          - http
      delegate_to: localhost

    - name: Set a single monitor (without enforcement)
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
        partition: Common
        monitors:
          - http
      delegate_to: localhost

    - name: Set multiple monitors (all must succeed)
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
        partition: Common
        monitor_type: and_list
        monitors:
          - http
          - tcp
      delegate_to: localhost

    - name: Set multiple monitors (at least 1 must succeed)
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
        partition: Common
        monitor_type: m_of_n
        quorum: 1
        monitors:
          - http
          - tcp
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

    - name: Delete pool
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
      delegate_to: localhost

    - name: Add metadata to pool
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        metadata:
          ansible: 2.4
          updated_at: 2017-12-20T17:50:46Z
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
                <td>changed</td>
                <td>
                                            <div>Description set on the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Pool of web servers</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>lb_method</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The LB method set for the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">round-robin</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>metadata</b>
                    <br/><div style="font-size: small; color: red">dict</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new value of the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;key1&#x27;: &#x27;foo&#x27;, &#x27;key2&#x27;: &#x27;bar&#x27;}</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>monitor_type</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The contact that was set on the datacenter.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">admin@root.local</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>monitors</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Monitors set on the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/http&#x27;, &#x27;/Common/gateway_icmp&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>priority_group_activation</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new minimum number of members to activate the priorty group.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>quorum</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The quorum that was set on the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>reselect_tries</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new value that is set for the number of tries to contact member.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>service_down_action</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Service down action that is set on the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">reset</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>slow_ramp_time</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new value that is set for the slow ramp-up time.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">500</div>
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

