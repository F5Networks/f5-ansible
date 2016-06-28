.. _bigip_pool:


bigip_pool - Manages F5 BIG-IP LTM pools
++++++++++++++++++++++++++++++++++++++++



.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages F5 BIG-IP LTM pools via iControl SOAP API


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
            <tr>
    <td>host<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member IP</div></br>
        <div style="font-size: small;">aliases: address<div></td></tr>
            <tr>
    <td>lb_method<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td>round_robin</td>
        <td><ul><li>round_robin</li><li>ratio_member</li><li>least_connection_member</li><li>observed_member</li><li>predictive_member</li><li>ratio_node_address</li><li>least_connection_node_address</li><li>fastest_node_address</li><li>observed_node_address</li><li>predictive_node_address</li><li>dynamic_ratio</li><li>fastest_app_response</li><li>least_sessions</li><li>dynamic_ratio_member</li><li>l3_addr</li><li>weighted_least_connection_member</li><li>weighted_least_connection_node_address</li><li>ratio_session</li><li>ratio_least_connection_member</li><li>ratio_least_connection_node_address</li></ul></td>
        <td><div>Load balancing method</div></td></tr>
            <tr>
    <td>monitor_type<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>and_list</li><li>m_of_n</li></ul></td>
        <td><div>Monitor rule type when monitors &gt; 1</div></td></tr>
            <tr>
    <td>monitors<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Monitor template name list. Always use the full path to the monitor.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool name</div></br>
        <div style="font-size: small;">aliases: pool<div></td></tr>
            <tr>
    <td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td><ul></ul></td>
        <td><div>Partition of pool/pool member</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member port</div></td></tr>
            <tr>
    <td>quorum<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Monitor quorum value when monitor_type is m_of_n</div></td></tr>
            <tr>
    <td>reselect_tries<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Sets the number of times the system tries to contact a pool member after a passive failure</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>BIG-IP server port</div></td></tr>
            <tr>
    <td>service_down_action<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>none</li><li>reset</li><li>drop</li><li>reselect</li></ul></td>
        <td><div>Sets the action to take when node goes down in pool</div></td></tr>
            <tr>
    <td>slow_ramp_time<br/><div style="font-size: small;"> (added in 1.3)</div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Sets the ramp-up time (in seconds) to gradually ramp up the load on newly added or freshly detected up pool members</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Pool/pool member state</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>yes</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites.  Prior to 2.0, this module would always validate on python &gt;= 2.7.9 and never validate on python &lt;= 2.7.8</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    ## playbook task examples:
    
    ---
    # file bigip-test.yml
    # ...
    - hosts: localhost
      tasks:
      - name: Create pool
        local_action: >
          bigip_pool
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          name=matthite-pool
          partition=matthite
          lb_method=least_connection_member
          slow_ramp_time=120
    
      - name: Modify load balancer method
        local_action: >
          bigip_pool
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          name=matthite-pool
          partition=matthite
          lb_method=round_robin
    
    - hosts: bigip-test
      tasks:
      - name: Add pool member
        local_action: >
          bigip_pool
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          name=matthite-pool
          partition=matthite
          host="{{ ansible_default_ipv4["address"] }}"
          port=80
    
      - name: Remove pool member from pool
        local_action: >
          bigip_pool
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=absent
          name=matthite-pool
          partition=matthite
          host="{{ ansible_default_ipv4["address"] }}"
          port=80
    
    - hosts: localhost
      tasks:
      - name: Delete pool
        local_action: >
          bigip_pool
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=absent
          name=matthite-pool
          partition=matthite
    


Notes
-----

.. note:: Requires BIG-IP software version >= 11
.. note:: F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
.. note:: Best run as a local_action in your playbook


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

