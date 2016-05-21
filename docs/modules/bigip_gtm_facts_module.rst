.. _bigip_gtm_facts:


bigip_gtm_facts - Collect facts from F5 BIG-IP GTM devices
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Collect facts from F5 BIG-IP GTM devices


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds
  * re


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
    <td>fact_filter<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Perform regex filter of response</div></td></tr>
            <tr>
    <td>include<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul><li>pool</li><li>wide_ip</li><li>virtual_server</li></ul></td>
        <td><div>Fact category to collect</div></td></tr>
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
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

      - name: Get pool facts
        local_action: >
          bigip_gtm_facts
          server=192.168.0.1
          user=admin
          password=mysecret
          include=pool
          fact_filter=my_pool

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
        <td> bigip_gtm_facts </td>
        <td> Details about GTM wide ip, pool, virtual servers </td>
        <td align=center> success </td>
        <td align=center> dictionary </td>
        <td align=center>  </td>
    </tr>
        <tr><td>contains: </td>
    <td colspan=4>
        <table border=1 cellpadding=2>
        <tr>
        <th class="head">name</th>
        <th class="head">description</th>
        <th class="head">returned</th>
        <th class="head">type</th>
        <th class="head">sample</th>
        </tr>

                <tr>
        <td> virtual_server </td>
        <td> Contains the virtual server enabled and availability status, and address </td>
        <td align=center> when include contains virtual_server </td>
        <td align=center> dictionary </td>
        <td align=center> {"virtual_server": {"/Common/MN-LTM": {"mn-test_example_com": {"address": {"address": "192.168.1.1", "port": 80}, "enabled_state": "STATE_ENABLED", "object_status": {"availability_status": "AVAILABILITY_STATUS_GREEN", "enabled_status": "ENABLED_STATUS_ENABLED", "status_description": " Monitor /Common/bigip from 192.168.0.1 : UP"}}, "va-test_example_com": {"address": {"address": "192.168.1.2", "port": 80}, "enabled_state": "STATE_ENABLED", "object_status": {"availability_status": "AVAILABILITY_STATUS_GREEN", "enabled_status": "ENABLED_STATUS_ENABLED", "status_description": " Monitor /Common/bigip from 192.168.0.1 : UP"}}}}} </td>
        </tr>
                <tr>
        <td> wide_ip </td>
        <td> Contains the lb method for the wide ip and the pools that are within the wide ip </td>
        <td align=center> when include contains wide_ip </td>
        <td align=center> dictionary </td>
        <td align=center> {"wide_ip": {"/Common/test.example.com": {"lb_method": "LB_METHOD_ROUND_ROBIN", "pool": [{"order": 0, "pool_name": "/Common/MN-test.example.com", "ratio": 1}, {"order": 1, "pool_name": "/Common/VA-test.example.com", "ratio": 1}]}}} </td>
        </tr>
                <tr>
        <td> pool </td>
        <td> Contains the pool object status and enabled status </td>
        <td align=center> when include contains pool </td>
        <td align=center> dictionary </td>
        <td align=center> {"pool": {"/Common/VA-test.example.com": {"member": [{"name": "VA-test_example_com", "server": "/Common/VA-Server"}], "object_status": {"availability_status": "AVAILABILITY_STATUS_RED", "enabled_status": "ENABLED_STATUS_DISABLED", "status_description": "No enabled pool members available: disabled directly"}}}} </td>
        </tr>
        
        </table>
    </td></tr>

        
    </table>
    </br></br>

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

