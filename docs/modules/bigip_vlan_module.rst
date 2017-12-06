.. _bigip_vlan:


bigip_vlan - Manage VLANs on a BIG-IP system
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage VLANs on a BIG-IP system


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
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The description to give to the VLAN.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The VLAN to manage. If the special VLAN <code>ALL</code> is specified with the <code>state</code> value of <code>absent</code> then all VLANs will be removed.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>present</li></ul></td>
        <td><div>The state of the VLAN on the system. When <code>present</code>, guarantees that the VLAN exists with the provided attributes. When <code>absent</code>, removes the VLAN from the system.</div>        </td></tr>
                <tr><td>tag<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Tag number for the VLAN. The tag number can be any integer between 1 and 4094. The system automatically assigns a tag number if you do not specify a value.</div>        </td></tr>
                <tr><td>tagged_interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies a list of tagged interfaces and trunks that you want to configure for the VLAN. Use tagged interfaces or trunks when you want to assign a single interface or trunk to multiple VLANs.</div></br>
    <div style="font-size: small;">aliases: tagged_interface<div>        </td></tr>
                <tr><td>untagged_interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies a list of untagged interfaces and trunks that you want to configure for the VLAN.</div></br>
    <div style="font-size: small;">aliases: untagged_interface<div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create VLAN
      bigip_vlan:
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost

    - name: Set VLAN tag
      bigip_vlan:
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          tag: "2345"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost

    - name: Add VLAN 2345 as tagged to interface 1.1
      bigip_vlan:
          tagged_interface: 1.1
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          tag: "2345"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost

    - name: Add VLAN 1234 as tagged to interfaces 1.1 and 1.2
      bigip_vlan:
          tagged_interfaces:
              - 1.1
              - 1.2
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          tag: "1234"
          user: "admin"
          validate_certs: "no"
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
        <td> interfaces </td>
        <td> Interfaces that the VLAN is assigned to </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['1.1', '1.2'] </td>
    </tr>
            <tr>
        <td> partition </td>
        <td> The partition that the VLAN was created on </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> Common </td>
    </tr>
            <tr>
        <td> tag </td>
        <td> The ID of the VLAN </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2345 </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The description set on the VLAN </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> foo VLAN </td>
    </tr>
            <tr>
        <td> name </td>
        <td> The name of the VLAN </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> net1 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires BIG-IP versions >= 12.0.0
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.