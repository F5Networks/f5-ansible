.. _bigip_pool_member:


bigip_pool_member - Manages F5 BIG-IP LTM pool members
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages F5 BIG-IP LTM pool members via iControl SOAP API


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
    <td>connection_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member connection limit. Setting this to 0 disables the limit.</div></td></tr>
            <tr>
    <td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member description</div></td></tr>
            <tr>
    <td>host<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member IP</div></br>
        <div style="font-size: small;">aliases: address, name<div></td></tr>
            <tr>
    <td>monitor_state<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set monitor availability status for pool member</div></td></tr>
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
    <td>pool<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool name. This pool must exist.</div></td></tr>
            <tr>
    <td>port<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member port</div></td></tr>
            <tr>
    <td>preserve_node<br/><div style="font-size: small;"> (added in 2.1)</div></td>
    <td>no</td>
    <td>no</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>When state is absent and the pool member is no longer referenced in other pools, the default behavior removes the unused node object. Setting this to 'yes' disables this behavior.</div></td></tr>
            <tr>
    <td>rate_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member rate limit (connections-per-second). Setting this to 0 disables the limit.</div></td></tr>
            <tr>
    <td>ratio<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Pool member ratio weight. Valid values range from 1 through 100. New pool members -- unless overriden with this value -- default to 1.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>session_state<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set new session availability status for pool member</div></td></tr>
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
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites.  Prior to 2.0, this module would always validate on python &gt;= 2.7.9 and never validate on python &lt;= 2.7.8</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Add pool member
      local_action: >
          bigip_pool_member
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          pool=matthite-pool
          partition=matthite
          host="{{ ansible_default_ipv4["address"] }}"
          port=80
          description="web server"
          connection_limit=100
          rate_limit=50
          ratio=2
    
    - name: Modify pool member ratio and description
      local_action: >
          bigip_pool_member
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          pool=matthite-pool
          partition=matthite
          host="{{ ansible_default_ipv4["address"] }}"
          port=80
          ratio=1
          description="nginx server"
    
    - name: Remove pool member from pool
      local_action: >
          bigip_pool_member
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=absent
          pool=matthite-pool
          partition=matthite
          host="{{ ansible_default_ipv4["address"] }}"
          port=80
    
    
    # The BIG-IP GUI doesn't map directly to the API calls for "Pool ->
    # Members -> State". The following states map to API monitor
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
    
    - name: Force pool member offline
      local_action: >
          bigip_pool_member
          server=lb.mydomain.com
          user=admin
          password=mysecret
          state=present
          session_state=disabled
          monitor_state=disabled
          pool=matthite-pool
          partition=matthite
          host="{{ ansible_default_ipv4["address"] }}"
          port=80


Notes
-----

.. note:: Requires BIG-IP software version >= 11
.. note:: F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
.. note:: Best run as a local_action in your playbook
.. note:: Supersedes bigip_pool for managing pool members


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

