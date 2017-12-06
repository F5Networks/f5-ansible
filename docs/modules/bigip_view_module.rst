.. _bigip_view:


bigip_view - Manage ZoneRunner Views on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage ZoneRunner Views on a BIG-IP. ZoneRunner is a feature of the GTM module. Therefore, this module should only be used on BIG-IP systems that have the GTM module enabled. The SOAP connection has a number of known limitations when it comes to updating Views. It is only possible to


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
                <tr><td>options<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A sequence of options for the view</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP password</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>BIG-IP web API port</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP host</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>present</code>, will ensure that the View exists with the correct zones in it. When <code>absent</code>, removes the View.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP username</div>        </td></tr>
                <tr><td>view_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the view</div>        </td></tr>
                <tr><td>view_order<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The order of the view within the named.conf file. 0 = first in zone. 0xffffffff means to move the view to last. Any other number will move the view to that position, and bump up any view(s) by one (if necessary).</div>        </td></tr>
                <tr><td>zones<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>A sequence of zones in this view</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a view foo.local
      local_action:
          module: "bigip_view"
          user: "admin"
          password: "admin"
          name: "foo.local"

    - name: Assign zone "bar" to view "foo.local"
      local_action:
          module: "bigip_view"
          user: "admin"
          password: "admin"
          name: "foo.local"
          zones:
              - "bar"



Notes
-----

.. note::
    - Requires the bigsuds Python package on the remote host. This is as easy as pip install bigsuds



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.