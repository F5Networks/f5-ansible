.. _bigip_virtual_server:


bigip_virtual_server - Manages F5 BIG-IP LTM virtual servers
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.1


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP LTM virtual servers via iControl SOAP API


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
                <tr><td>all_policies<br/><div style="font-size: small;"> (added in 2.3)</div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>List of all policies enabled for the virtual server.</div>        </td></tr>
                <tr><td>all_profiles<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>List of all Profiles (HTTP,ClientSSL,ServerSSL,etc) that must be used by the virtual server</div>        </td></tr>
                <tr><td>all_rules<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>List of rules to be applied in priority order</div>        </td></tr>
                <tr><td>default_persistence_profile<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Default Profile which manages the session persistence</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Virtual server description</div>        </td></tr>
                <tr><td>destination<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Destination IP of the virtual server (only host is currently supported). Required when state=present and vs does not exist.</div></br>
    <div style="font-size: small;">aliases: address, ip<div>        </td></tr>
                <tr><td>enabled_vlans<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>List of vlans to be enabled. When a VLAN named <code>ALL</code> is used, all VLANs will be allowed.</div>        </td></tr>
                <tr><td>fallback_persistence_profile<br/><div style="font-size: small;"> (added in 2.3)</div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies the persistence profile you want the system to use if it cannot use the specified default persistence profile.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Virtual server name</div></br>
    <div style="font-size: small;">aliases: vs<div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Partition</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>pool<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Default pool for the virtual server</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Port of the virtual server. Required when state=present and vs does not exist. If you specify a value for this field, it must be a number between 0 and 65535.</div>        </td></tr>
                <tr><td>route_advertisement_state<br/><div style="font-size: small;"> (added in 2.3)</div></td>
    <td>no</td>
    <td>disabled</td>
        <td></td>
        <td><div>Enable route advertisement for destination</div>        </td></tr>
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
                <tr><td>snat<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>None</li><li>Automap</li><li>Name of a SNAT pool (eg "/Common/snat_pool_name") to enable SNAT with the specific pool</li></ul></td>
        <td><div>Source network address policy</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Virtual Server state</div><div>Absent, delete the VS if present</div><div><code>present</code> (and its synonym enabled), create if needed the VS and set state to enabled</div><div><code>disabled</code>, create if needed the VS and set state to disabled</div>        </td></tr>
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