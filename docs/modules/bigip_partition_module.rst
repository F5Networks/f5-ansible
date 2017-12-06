.. _bigip_partition:


bigip_partition - Manage BIG-IP partitions
++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage BIG-IP partitions.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.2.3


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
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The description to attach to the Partition.</div>        </td></tr>
                <tr><td>route_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The default Route Domain to assign to the Partition. If no route domain is specified, then the default route domain for the system (typically zero) will be used only when creating a new partition.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the partition should exist or not.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create partition "foo" using the default route domain
      bigip_partition:
        name: foo
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Create partition "bar" using a custom route domain
      bigip_partition:
        name: bar
        route_domain: 3
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Change route domain of partition "foo"
      bigip_partition:
        name: foo
        route_domain: 8
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Set a description for partition "foo"
      bigip_partition:
        name: foo
        description: Tenant CompanyA
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Delete the "foo" partition
      bigip_partition:
        name: foo
        password: secret
        server: lb.mydomain.com
        user: admin
        state: absent
      delegate_to: localhost


Return Values
-------------

Common return values are :doc:`documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`, the following are the fields unique to this module:

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
        <td> route_domain </td>
        <td> Name of the route domain associated with the partition. </td>
        <td align=center> changed and success </td>
        <td align=center> int </td>
        <td align=center> 0 </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The description of the partition. </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> Example partition </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires BIG-IP software version >= 12
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.