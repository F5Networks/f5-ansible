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

  * f5-sdk
  * Python >= 2.7


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
                <tr><td>host<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member IP.</div><div>Deprecated in 2.4. Use the <code>bigip_pool_member</code> module instead.</div></br>
    <div style="font-size: small;">aliases: address<div>        </td></tr>
                <tr><td>lb_method<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>dynamic-ratio-member</li><li>dynamic-ratio-node</li><li>fastest-app-response</li><li>fastest-node</li><li>least-connections-member</li><li>least-connections-node</li><li>least-sessions</li><li>observed-member</li><li>observed-node</li><li>predictive-member</li><li>predictive-node</li><li>ratio-least-connections-member</li><li>ratio-least-connections-node</li><li>ratio-member</li><li>ratio-node</li><li>ratio-session</li><li>round-robin</li><li>weighted-least-connections-member</li><li>weighted-least-connections-nod</li></ul></td>
        <td><div>Load balancing method. When creating a new pool, if this value is not specified, the default of <code>round-robin</code> will be used.</div>        </td></tr>
                <tr><td>monitor_type<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>and_list</li><li>m_of_n</li><li>single</li></ul></td>
        <td><div>Monitor rule type when <code>monitors</code> is specified. When creating a new pool, if this value is not specified, the default of 'and_list' will be used.</div><div>Both <code>single</code> and <code>and_list</code> are functionally identical since BIG-IP considers all monitors as "a list". BIG=IP either has a list of many, or it has a list of one. Where they differ is in the extra guards that <code>single</code> provides; namely that it only allows a single monitor.</div>        </td></tr>
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
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member port.</div><div>Deprecated in 2.4. Use the <code>bigip_pool_member</code> module instead.</div>        </td></tr>
                <tr><td>quorum<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Monitor quorum value when <code>monitor_type</code> is <code>m_of_n</code>.</div>        </td></tr>
                <tr><td>reselect_tries<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the number of times the system tries to contact a pool member after a passive failure.</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
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
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
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
        lb_method: least_connection_member
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
        lb_method: round_robin
      delegate_to: localhost
    
    - name: Add pool member
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        name: my-pool
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
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
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

Return Values
-------------

Common return values are :doc:`documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`, the following are the fields unique to this module:

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
        <td> port </td>
        <td> Port of pool member included in pool. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 80 </td>
    </tr>
            <tr>
        <td> host </td>
        <td> IP of pool member included in pool. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 10.10.10.10 </td>
    </tr>
            <tr>
        <td> reselect_tries </td>
        <td> The new value that is set for the number of tries to contact member. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 10 </td>
    </tr>
            <tr>
        <td> monitor_type </td>
        <td> The contact that was set on the datacenter. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> admin@root.local </td>
    </tr>
            <tr>
        <td> quorum </td>
        <td> The quorum that was set on the pool. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires BIG-IP software version >= 12.
    - F5 developed module 'F5-SDK' required (https://github.com/F5Networks/f5-common-python).
    - Best run as a local_action in your playbook.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.