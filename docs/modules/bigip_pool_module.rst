.. _bigip_pool:


bigip_pool - Manages F5 BIG-IP LTM pools
++++++++++++++++++++++++++++++++++++++++



.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP LTM pools via iControl SOAP API


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds


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
        <td><div>Pool member IP</div></br>
    <div style="font-size: small;">aliases: address<div>        </td></tr>
                <tr><td>lb_method<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td>round_robin</td>
        <td><ul><li>round_robin</li><li>ratio_member</li><li>least_connection_member</li><li>observed_member</li><li>predictive_member</li><li>ratio_node_address</li><li>least_connection_node_address</li><li>fastest_node_address</li><li>observed_node_address</li><li>predictive_node_address</li><li>dynamic_ratio</li><li>fastest_app_response</li><li>least_sessions</li><li>dynamic_ratio_member</li><li>l3_addr</li><li>weighted_least_connection_member</li><li>weighted_least_connection_node_address</li><li>ratio_session</li><li>ratio_least_connection_member</li><li>ratio_least_connection_node_address</li></ul></td>
        <td><div>Load balancing method</div>        </td></tr>
                <tr><td>monitor_type<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>and_list</li><li>m_of_n</li></ul></td>
        <td><div>Monitor rule type when monitors &gt; 1</div>        </td></tr>
                <tr><td>monitors<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Monitor template name list. Always use the full path to the monitor.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Pool name</div></br>
    <div style="font-size: small;">aliases: pool<div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Partition of pool/pool member</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member port</div>        </td></tr>
                <tr><td>quorum<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Monitor quorum value when monitor_type is m_of_n</div>        </td></tr>
                <tr><td>reselect_tries<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the number of times the system tries to contact a pool member after a passive failure</div>        </td></tr>
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
        <td><div>Sets the action to take when node goes down in pool</div>        </td></tr>
                <tr><td>slow_ramp_time<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the ramp-up time (in seconds) to gradually ramp up the load on newly added or freshly detected up pool members</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Pool/pool member state</div>        </td></tr>
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
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          name: "my-pool"
          partition: "Common"
          lb_method: "least_connection_member"
          slow_ramp_time: 120
      delegate_to: localhost
    
    - name: Modify load balancer method
      bigip_pool:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          name: "my-pool"
          partition: "Common"
          lb_method: "round_robin"
    
    - name: Add pool member
      bigip_pool:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          name: "my-pool"
          partition: "Common"
          host: "{{ ansible_default_ipv4["address"] }}"
          port: 80
    
    - name: Remove pool member from pool
      bigip_pool:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "absent"
          name: "my-pool"
          partition: "Common"
          host: "{{ ansible_default_ipv4["address"] }}"
          port: 80
    
    - name: Delete pool
      bigip_pool:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "absent"
          name: "my-pool"
          partition: "Common"


Notes
-----

.. note::
    - Requires BIG-IP software version >= 11
    - F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
    - Best run as a local_action in your playbook



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.