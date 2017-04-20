.. _bigip_node:


bigip_node - Manages F5 BIG-IP LTM nodes
++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP LTM nodes via iControl SOAP API


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
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Node description.</div>        </td></tr>
                <tr><td>host<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Node IP. Required when state=present and node does not exist. Error when state=absent.</div></br>
    <div style="font-size: small;">aliases: address, ip<div>        </td></tr>
                <tr><td>monitor_state<br/><div style="font-size: small;"> (added in 1.9)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set monitor availability status for node</div>        </td></tr>
                <tr><td>monitor_type<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>and_list</li><li>m_of_n</li></ul></td>
        <td><div>Monitor rule type when monitors &gt; 1</div>        </td></tr>
                <tr><td>monitors<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Monitor template name list. Always use the full path to the monitor.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Node name</div>        </td></tr>
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
                <tr><td>quorum<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Monitor quorum value when monitor_type is m_of_n</div>        </td></tr>
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
                <tr><td>session_state<br/><div style="font-size: small;"> (added in 1.9)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set new session availability status for node</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Pool member state</div>        </td></tr>
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
    
    # Note that the BIG-IP automatically names the node using the
    # IP address specified in previous play's host parameter.
    # Future plays referencing this node no longer use the host
    # parameter but instead use the name parameter.
    # Alternatively, you could have specified a name with the
    # name parameter when state=present.
    
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
    
    # The BIG-IP GUI doesn't map directly to the API calls for "Node ->
    # General Properties -> State". The following states map to API monitor
    # and session states.
    #
    # Enabled (all traffic allowed):
    # monitor_state=enabled, session_state=enabled
    # Disabled (only persistent or active connections allowed):
    # monitor_state=enabled, session_state=disabled
    # Forced offline (only active connections allowed):
    # monitor_state=disabled, session_state=disabled
    #
    # See https://devcentral.f5.com/questions/icontrol-equivalent-call-for-b-node-down
    
    - name: Force node offline
      bigip_node:
          server: "lb.mydomain.com"
          user: "admin"
          password: "mysecret"
          state: "present"
          session_state: "disabled"
          monitor_state: "disabled"
          partition: "Common"
          name: "10.20.30.40"


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