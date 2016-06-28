.. _bigip_gtm_virtual_server:


bigip_gtm_virtual_server - Manages F5 BIG-IP GTM virtual servers
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages F5 BIG-IP GTM virtual servers


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
    <td>host<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Virtual server host</div></br>
        <div style="font-size: small;">aliases: address<div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Virtual server port</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>BIG-IP server port</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Virtual server state</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></td></tr>
            <tr>
    <td>virtual_server_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Virtual server name</div></td></tr>
            <tr>
    <td>virtual_server_server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Virtual server server</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

      - name: Enable virtual server
        local_action: >
          bigip_gtm_virtual_server
          server=192.168.0.1
          user=admin
          password=mysecret
          virtual_server_name=myname
          virtual_server_server=myserver
          state=enabled


Notes
-----

.. note:: Requires BIG-IP software version >= 11.4
.. note:: F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
.. note:: Best run as a local_action in your playbook
.. note:: Tested with manager and above account privilege level


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

