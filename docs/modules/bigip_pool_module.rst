.. _bigip_pool:


bigip_pool - Manages F5 BIG-IP LTM pools
++++++++++++++++++++++++++++++++++++++++



.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP LTM pools via iControl REST API.


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
                <tr><td>description<br/><div style="font-size: small;"> (added in 2.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies descriptive text that identifies the pool.</div>        </td></tr>
                <tr><td>lb_method<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>dynamic-ratio-member</li><li>dynamic-ratio-node</li><li>fastest-app-response</li><li>fastest-node</li><li>least-connections-member</li><li>least-connections-node</li><li>least-sessions</li><li>observed-member</li><li>observed-node</li><li>predictive-member</li><li>predictive-node</li><li>ratio-least-connections-member</li><li>ratio-least-connections-node</li><li>ratio-member</li><li>ratio-node</li><li>ratio-session</li><li>round-robin</li><li>weighted-least-connections-member</li><li>weighted-least-connections-nod</li></ul></td>
        <td><div>Load balancing method. When creating a new pool, if this value is not specified, the default of <code>round-robin</code> will be used.</div>        </td></tr>
                <tr><td>metadata<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Arbitrary key/value pairs that you can attach to a pool. This is useful in situations where you might want to annotate a pool to me managed by Ansible.</div><div>Key names will be stored as strings; this includes names that are numbers.</div><div>Values for all of the keys will be stored as strings; this includes values that are numbers.</div><div>Data will be persisted, not ephemeral.</div>        </td></tr>
                <tr><td>monitor_type<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>and_list</li><li>m_of_n</li><li>single</li></ul></td>
        <td><div>Monitor rule type when <code>monitors</code> is specified.</div><div>When creating a new pool, if this value is not specified, the default of &#x27;and_list&#x27; will be used.</div><div>When <code>single</code> ensures that all specified monitors are checked, but additionally includes checks to make sure you only specified a single monitor.</div><div>When <code>and_list</code> ensures that <b>all</b> monitors are checked.</div><div>When <code>m_of_n</code> ensures that <code>quorum</code> of <code>monitors</code> are checked. <code>m_of_n</code> <b>requires</b> that a <code>quorum</code> of 1 or greater be set either in the playbook, or already existing on the device.</div><div>Both <code>single</code> and <code>and_list</code> are functionally identical since BIG-IP considers all monitors as &quot;a list&quot;.</div>        </td></tr>
                <tr><td>monitors<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Monitor template name list. If the partition is not provided as part of the monitor name, then the <code>partition</code> option will be used instead.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Pool name</div></br>
    <div style="font-size: small;">aliases: pool<div>        </td></tr>
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
                <tr><td>quorum<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Monitor quorum value when <code>monitor_type</code> is <code>m_of_n</code>.</div><div>Quorum must be a value of 1 or greater when <code>monitor_type</code> is <code>m_of_n</code>.</div>        </td></tr>
                <tr><td>reselect_tries<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the number of times the system tries to contact a pool member after a passive failure.</div>        </td></tr>
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
                <tr><td>service_down_action<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>none</li><li>reset</li><li>drop</li><li>reselect</li></ul></td>
        <td><div>Sets the action to take when node goes down in pool.</div>        </td></tr>
                <tr><td>slow_ramp_time<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the ramp-up time (in seconds) to gradually ramp up the load on newly added or freshly detected up pool members.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>present</li></ul></td>
        <td><div>When <code>present</code>, guarantees that the pool exists with the provided attributes.</div><div>When <code>absent</code>, removes the pool from the system.</div>        </td></tr>
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

    
    - name: Create pool
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
        partition: Common
        lb_method: least-connection-member
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
        <td> monitors </td>
        <td> Monitors set on the pool. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/http', '/Common/gateway_icmp'] </td>
    </tr>
            <tr>
        <td> lb_method </td>
        <td> The LB method set for the pool. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> round-robin </td>
    </tr>
            <tr>
        <td> description </td>
        <td> Description set on the pool. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> Pool of web servers </td>
    </tr>
            <tr>
        <td> slow_ramp_time </td>
        <td> The new value that is set for the slow ramp-up time. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 500 </td>
    </tr>
            <tr>
        <td> service_down_action </td>
        <td> Service down action that is set on the pool. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> reset </td>
    </tr>
            <tr>
        <td> reselect_tries </td>
        <td> The new value that is set for the number of tries to contact member. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 10 </td>
    </tr>
            <tr>
        <td> quorum </td>
        <td> The quorum that was set on the pool. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2 </td>
    </tr>
            <tr>
        <td> monitor_type </td>
        <td> The contact that was set on the datacenter. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> admin@root.local </td>
    </tr>
            <tr>
        <td> metadata </td>
        <td> The new value of the pool. </td>
        <td align=center> changed </td>
        <td align=center> dict </td>
        <td align=center> {'key2': 'bar', 'key1': 'foo'} </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires BIG-IP software version >= 12.
    - To add members do a pool, use the ``bigip_pool_member`` module. Previously, the ``bigip_pool`` module allowed the management of users, but this has been removed in version 2.5 of Ansible.
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