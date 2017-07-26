.. __bigip_pool_member:


_bigip_pool_member - Manages F5 BIG-IP LTM pool members
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4


.. contents::
   :local:
   :depth: 2

DEPRECATED
----------

Deprecated in 2.5. Use the bigip_pool_member module instead.

Synopsis
--------

* Manages F5 BIG-IP LTM pool members via iControl SOAP API


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
                <tr><td>connection_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member connection limit. Setting this to 0 disables the limit.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member description</div>        </td></tr>
                <tr><td>host<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Pool member IP</div></br>
    <div style="font-size: small;">aliases: address, name<div>        </td></tr>
                <tr><td>monitor_state<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set monitor availability status for pool member</div>        </td></tr>
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
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Pool name. This pool must exist.</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Pool member port</div>        </td></tr>
                <tr><td>preserve_node<br/><div style="font-size: small;"> (added in 2.1)</div></td>
    <td>no</td>
    <td>no</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>When state is absent and the pool member is no longer referenced in other pools, the default behavior removes the unused node o bject. Setting this to 'yes' disables this behavior.</div>        </td></tr>
                <tr><td>rate_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member rate limit (connections-per-second). Setting this to 0 disables the limit.</div>        </td></tr>
                <tr><td>ratio<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Pool member ratio weight. Valid values range from 1 through 100. New pool members -- unless overridden with this value -- default to 1.</div>        </td></tr>
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
                <tr><td>session_state<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Set new session availability status for pool member</div>        </td></tr>
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

    
    - name: Add pool member
      bigip_pool_member:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          pool: "my-pool"
          partition: "Common"
          host: "{{ ansible_default_ipv4["address"] }}"
          port: 80
          description: "web server"
          connection_limit: 100
          rate_limit: 50
          ratio: 2
      delegate_to: localhost
    
    - name: Modify pool member ratio and description
      bigip_pool_member:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          pool: "my-pool"
          partition: "Common"
          host: "{{ ansible_default_ipv4["address"] }}"
          port: 80
          ratio: 1
          description: "nginx server"
      delegate_to: localhost
    
    - name: Remove pool member from pool
      bigip_pool_member:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "absent"
          pool: "my-pool"
          partition: "Common"
          host: "{{ ansible_default_ipv4["address"] }}"
          port: 80
      delegate_to: localhost
    
    
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
      bigip_pool_member:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          session_state: "disabled"
          monitor_state: "disabled"
          pool: "my-pool"
          partition: "Common"
          host: "{{ ansible_default_ipv4["address"] }}"
          port: 80
      delegate_to: localhost


Notes
-----

.. note::
    - Requires BIG-IP software version >= 11
    - F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
    - Best run as a local_action in your playbook
    - Supersedes bigip_pool for managing pool members


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.