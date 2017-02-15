.. _bigip_virtual_server:


bigip_virtual_server - Manage LTM virtual servers on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.1


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage LTM virtual servers on a BIG-IP


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
    <td>all_profiles<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>List of all Profiles (HTTP, ClientSSL, ServerSSL, etc) that must be used by the virtual server</div></td></tr>
            <tr>
    <td>all_rules<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>List of rules to be applied in priority order</div></td></tr>
            <tr>
    <td>default_persistence_profile<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Default Profile which manages the session persistence</div></td></tr>
            <tr>
    <td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Virtual server description</div></td></tr>
            <tr>
    <td>destination<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Destination IP of the virtual server (only host is currently supported). Required when state=present and vs does not exist.</div></br>
        <div style="font-size: small;">aliases: address, ip<div></td></tr>
            <tr>
    <td>enabled_vlans<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>List of vlans to be enabled. When a VLAN named <code>ALL</code> is used, all VLANs will be allowed.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Virtual server name</div></br>
        <div style="font-size: small;">aliases: vs<div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>pool<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Default pool for the virtual server</div></td></tr>
            <tr>
    <td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Port of the virtual server. Required when <code>state</code> is <code>present</code> and virtual server does not exist.</div></td></tr>
            <tr>
    <td>route_advertisement_state<br/><div style="font-size: small;"> (added in 2.3)</div></td>
    <td>no</td>
    <td>disabled</td>
        <td><ul></ul></td>
        <td><div>Enable route advertisement for destination</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The BIG-IP host.</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>The BIG-IP server port.</div></td></tr>
            <tr>
    <td>snat<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>None</li><li>Automap</li><li>Name of a SNAT pool (eg "/Common/snat_pool_name") to enable SNAT with the specific pool</li></ul></td>
        <td><div>Source network address policy</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>The virtual server state. If <code>absent</code>, delete the virtual server if it exists. <code>present</code> creates the virtual server and enable it. If <code>enabled</code>, enable the virtual server if it exists. If <code>disabled</code>, create the virtual server if needed, and set state to <code>disabled</code>.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Add virtual server
      bigip_virtual_server:
          server: lb.mydomain.net
          user: admin
          password: secret
          state: present
          partition: MyPartition
          name: myvirtualserver
          destination: "{{ ansible_default_ipv4['address'] }}"
          port: 443
          pool: "{{ mypool }}"
          snat: Automap
          description: Test Virtual Server
          all_profiles:
              - http
              - clientssl
          enabled_vlans:
              - /Common/vlan2
      delegate_to: localhost
    
    - name: Modify Port of the Virtual Server
      bigip_virtual_server:
          server: lb.mydomain.net
          user: admin
          password: secret
          state: present
          partition: MyPartition
          name: myvirtualserver
          port: 8080
      delegate_to: localhost
    
    - name: Delete virtual server
      bigip_virtual_server:
          server: lb.mydomain.net
          user: admin
          password: secret
          state: absent
          partition: MyPartition
          name: myvirtualserver
      delegate_to: localhost

Return Values
-------------

Common return values are documented here :doc:`common_return_values`, the following are the fields unique to this module:

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
        <td> deleted </td>
        <td> Name of a virtual server that was deleted </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> my-virtual-server </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires BIG-IP software version >= 11
.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

