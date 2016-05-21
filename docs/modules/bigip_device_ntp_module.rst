.. _bigip_device_ntp:


bigip_device_ntp - Manage NTP servers on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.1


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage NTP servers on a BIG-IP


Requirements (on host that executes module)
-------------------------------------------

  * requests
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
    <td>append<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>yes</code>, will only add NTP servers, not set them to just the list in <code>ntp_servers</code> or the value of <code>ntp_server</code>.</div></td></tr>
            <tr>
    <td>ntp_server<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>A single NTP server to set on the device. At least one of <code>ntp_servers</code> or <code>ntp_server</code> are required.</div></td></tr>
            <tr>
    <td>ntp_servers<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>A list of NTP servers to set on the device. At least one of <code>ntp_servers</code> or <code>ntp_server</code> are required.</div></td></tr>
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
        <td><div>The state of the NTP servers on the system. When <code>present</code>, guarantees that the NTP servers are set on the system. When <code>absent</code>, removes the specified NTP servers from the device configuration.</div></td></tr>
            <tr>
    <td>timezone<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>UTC</td>
        <td><ul></ul></td>
        <td><div>The timezone to set for NTP lookups</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></br>
        <div style="font-size: small;">aliases: username<div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Set the boot.quiet DB variable on the BIG-IP
      bigip_sysdb:
          server: "big-ip"
          key: "boot.quiet"
          value: "disable"
      delegate_to: localhost


Notes
-----

.. note:: Requires the requests Python package on the host. This is as easy as pip install requests


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

