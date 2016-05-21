.. _bigip_node:


bigip_node - Manages F5 BIG-IP LTM nodes
++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages F5 BIG-IP LTM nodes via iControl SOAP API


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
    <td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Node description.</div></td></tr>
            <tr>
    <td>host<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Node IP. Required when state=present and node does not exist. Error when state=absent.</div></br>
        <div style="font-size: small;">aliases: address, ip<div></td></tr>
            <tr>
    <td>monitor_state<br/><div style="font-size: small;"> (added in 1.9)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set monitor availability status for node</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Node name</div></td></tr>
            <tr>
    <td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td><ul></ul></td>
        <td><div>Partition</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>session_state<br/><div style="font-size: small;"> (added in 1.9)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set new session availability status for node</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Pool member state</div></td></tr>
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
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites. Prior to 2.0, this module would always validate on python &gt;= 2.7.9 and never validate on python &lt;= 2.7.8</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    ---
    - name: Add node
      local_action: >
          bigip_node
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          partition=matthite
          host="{{ ansible_default_ipv4["address"] }}"
          name="{{ ansible_default_ipv4["address"] }}"
    
    # Note that the BIG-IP automatically names the node using the
    # IP address specified in previous play's host parameter.
    # Future plays referencing this node no longer use the host
    # parameter but instead use the name parameter.
    # Alternatively, you could have specified a name with the
    # name parameter when state=present.
    
      - name: Modify node description
        local_action: >
          bigip_node
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          partition=matthite
          name="{{ ansible_default_ipv4["address"] }}"
          description="Our best server yet"
    
      - name: Delete node
        local_action: >
          bigip_node
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=absent
          partition=matthite
          name="{{ ansible_default_ipv4["address"] }}"
    
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
        local_action: >
          bigip_node
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          session_state=disabled
          monitor_state=disabled
          partition=matthite
          name="{{ ansible_default_ipv4["address"] }}"
    


Notes
-----

.. note:: Requires BIG-IP software version >= 11
.. note:: F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
.. note:: Best run as a local_action in your playbook


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

