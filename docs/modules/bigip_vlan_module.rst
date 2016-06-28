.. _bigip_vlan:


bigip_vlan - Manage VLANs on a BIG-IP system
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage VLANs on a BIG-IP system


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
            <tr>
    <td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The description to give to the VLAN</div></td></tr>
            <tr>
    <td>interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Specifies a list of tagged or untagged interfaces and trunks that you want to configure for the VLAN. Use tagged interfaces or trunks when you want to assign a single interface or trunk to multiple VLANs.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The VLAN to manage. If the special VLAN <code>ALL</code> is specified with the <code>state</code> value of <code>absent</code> then all VLANs will be removed.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>route_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The route domain that the VLAN is associated with if something other than Common</div></td></tr>
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
        <td><div>The state of the VLAN on the system. When <code>present</code>, guarantees that the VLAN exists with the provided attributes. When <code>absent</code>, removes the VLAN from the system.</div></td></tr>
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
    <td>vlan_id<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The ID (tag) of the VLAN</div></br>
        <div style="font-size: small;">aliases: tag<div></td></tr>
        </table>
    </br>






Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk
.. note:: Requires BIG-IP versions >= 12.0.0


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

