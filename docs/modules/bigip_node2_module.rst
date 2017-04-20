.. _bigip_node:


bigip_node - Manages F5 BIG-IP LTM nodes
++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP LTM nodes via iControl SOAP API.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk


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
                <tr><td>availability_requirement<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>C(and_list)</td>
        <td><ul><li>all</li><li>at_least</li></ul></td>
        <td><div>Specifies, if you activate more than one health monitor, the number of health monitors that must receive successful responses in order for the node to be considered available. The default is <code>all</code>.</div></br>
    <div style="font-size: small;">aliases: monitor_type<div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies descriptive text that identifies the node.</div>        </td></tr>
                <tr><td>host<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>None</td>
        <td></td>
        <td><div>Node IP. Required when <code>state</code> is present and node does not exist. Error when <code>state</code> is equal to <code>absent</code>.</div></br>
    <div style="font-size: small;">aliases: address, ip<div>        </td></tr>
                <tr><td>monitors<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies the health monitors that the system currently uses to monitor this node.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies the name of the node.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>quorum<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Monitor quorum value when <code>monitor_type</code> is <code>at_least</code>.</div>        </td></tr>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li><li>offline</li></ul></td>
        <td><div>Specifies the current state of the node. <code>enabled</code> (All traffic allowed), specifies that system sends traffic to this node regardless of the node's state. <code>disabled</code> (Only persistent or active connections allowed), Specifies that the node can handle only persistent or active connections. <code>offline</code> (Only active connections allowed), Specifies that the node can handle only active connections. In all cases except <code>absent</code>, the node will be created if it does not yet exist.</div>        </td></tr>
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

    
    - name: Add node
      bigip_node:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          partition: "Common"
          host: "10.20.30.40"
          name: "10.20.30.40"
      delegate_to: localhost
    
    - name: Add node with a single 'ping' monitor
      bigip_node:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          partition: "Common"
          host: "10.20.30.40"
          name: "mytestserver"
          monitors:
              - /Common/icmp
      delegate_to: localhost
    
    - name: Modify node description
      bigip_node:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          partition: "Common"
          name: "10.20.30.40"
          description: "Our best server yet"
      delegate_to: localhost
    
    - name: Delete node
      bigip_node:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "absent"
          partition: "Common"
          name: "10.20.30.40"
      delegate_to: localhost
    
    - name: Force node offline
      bigip_node:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "disabled"
          partition: "Common"
          name: "10.20.30.40"
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
        <td> members </td>
        <td> ['List of members that are part of the SNAT pool.'] </td>
        <td align=center> changed and success </td>
        <td align=center> list </td>
        <td align=center> ['10.10.10.10'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires BIG-IP software version >= 11
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.