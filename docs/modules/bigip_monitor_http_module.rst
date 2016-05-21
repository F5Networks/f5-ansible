.. _bigip_monitor_http:


bigip_monitor_http - Manages F5 BIG-IP LTM http monitors
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.4


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages F5 BIG-IP LTM monitors via iControl SOAP API


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
    <td>interval<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>The interval specifying how frequently the monitor instance of this template will run. By default, this interval is used for up and down states. The default API setting is 5.</div></td></tr>
            <tr>
    <td>ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>IP address part of the ipport definition. The default API setting is "0.0.0.0".</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Monitor name</div></br>
        <div style="font-size: small;">aliases: monitor<div></td></tr>
            <tr>
    <td>parent<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>http</td>
        <td><ul></ul></td>
        <td><div>The parent template of this monitor template</div></td></tr>
            <tr>
    <td>parent_partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td><ul></ul></td>
        <td><div>Partition for the parent monitor</div></td></tr>
            <tr>
    <td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td><ul></ul></td>
        <td><div>Partition for the monitor</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>Port address part op the ipport definition. The default API setting is 0.</div></td></tr>
            <tr>
    <td>receive<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>The receive string for the monitor call</div></td></tr>
            <tr>
    <td>receive_disable<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>The receive disable string for the monitor call</div></td></tr>
            <tr>
    <td>send<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>The send string for the monitor call</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Monitor state</div></td></tr>
            <tr>
    <td>time_until_up<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>Specifies the amount of time in seconds after the first successful response before a node will be marked up. A value of 0 will cause a node to be marked up immediately after a valid response is received from the node. The default API setting is 0.</div></td></tr>
            <tr>
    <td>timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>The number of seconds in which the node or service must respond to the monitor request. If the target responds within the set time period, it is considered up. If the target does not respond within the set time period, it is considered down. You can change this number to any number you want, however, it should be 3 times the interval number of seconds plus 1 second. The default API setting is 16.</div></td></tr>
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
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites. Prior to 2.0, this module would always validate on python &gt;= 2.7.9 and never validate on python &lt;= 2.7.8</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Create HTTP Monitor
      local_action:
          module: bigip_monitor_http
          state: present
          server: "{{ f5server }}"
          user: "{{ f5user }}"
          password: "{{ f5password }}"
          name: "{{ item.monitorname }}"
          send: "{{ item.send }}"
          receive: "{{ item.receive }}"
      with_items: f5monitors
    
    - name: Remove HTTP Monitor
      local_action:
          module: bigip_monitor_http
          state: absent
          server: "{{ f5server }}"
          user: "{{ f5user }}"
          password: "{{ f5password }}"
          name: "{{ monitorname }}"


Notes
-----

.. note:: Requires BIG-IP software version >= 11
.. note:: F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
.. note:: Best run as a local_action in your playbook
.. note:: Monitor API documentation: https://devcentral.f5.com/wiki/iControl.LocalLB__Monitor.ashx


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

