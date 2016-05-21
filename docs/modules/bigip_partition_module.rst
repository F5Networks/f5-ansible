.. _bigip_partition:


bigip_partition - Manage BIG-IP partitions
++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage BIG-IP partitions


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds
  * requests


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
        <td><div>The description to attach to the Partition</div></td></tr>
            <tr>
    <td>route_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The default Route Domain to assign to the Partition. If no route domain is specified, then the default route domain for the system (typically zero) will be used only when creating a new partition. <code>route_domain</code> and <code>route_domain_id</code> are mutually exclusive.</div></td></tr>
            <tr>
    <td>route_domain_id<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The default Route Domain ID to assign to the Partition. If you track the route domains by their numeric identifier, then this argument can be used to supply that ID. <code>route_domain</code> and <code>route_domain_id</code> are mutually exclusive.</div></td></tr>
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
        <td><div>Whether the partition should exist or not</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></td></tr>
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

    - name: Create partition "foo" using the default route domain
      bigip_partition:
          name: "foo"
          password: "secret"
          server: "lb.mydomain.com"
          user: "admin"
    
    - name: Delete the foo partition
      bigip_partition:
          name: "foo"
          password: "secret"
          server: "lb.mydomain.com"
          user: "admin"
          state: "absent"

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
        <td> route_domain_id </td>
        <td> ID of the route domain associated with the partition </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> 0 </td>
    </tr>
            <tr>
        <td> route_domain </td>
        <td> Name of the route domain associated with the partition </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> /Common/asdf </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The description of the partition </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> Example partition </td>
    </tr>
            <tr>
        <td> name </td>
        <td> The name of the partition </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> /foo </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the bigsuds Python package on the host if using the iControl interface. This is as easy as pip install bigsuds


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

