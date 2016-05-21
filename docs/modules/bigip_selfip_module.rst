.. _bigip_selfip:


bigip_selfip - Manage Self-IPs on a BIG-IP system
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Self-IPs on a BIG-IP system


Requirements (on host that executes module)
-------------------------------------------

  * netaddr
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
            <tr>
    <td>address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The IP addresses for the new self IP</div></td></tr>
            <tr>
    <td>floating_state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>disabled</td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>The floating attributes of the self IPs.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Value of C(address)</td>
        <td><ul></ul></td>
        <td><div>The self IP to create</div></td></tr>
            <tr>
    <td>netmask<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The netmasks for the self IP</div></td></tr>
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
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>present</li></ul></td>
        <td><div>The state of the variable on the system. When <code>present</code>, guarantees that the Self-IP exists with the provided attributes. When <code>absent</code>, removes the floating IP from the system.</div></td></tr>
            <tr>
    <td>traffic_group<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The traffic group for the self IP addresses in an active-active, redundant load balancer configuration</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
            <tr>
    <td>vlan<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The VLAN that the new self IPs will be on</div></td></tr>
        </table>
    </br>






Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk
.. note:: Requires the netaddr Python package on the host


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

