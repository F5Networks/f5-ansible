:source: modules/bigip_view.py

:orphan:

.. _bigip_view_module:


bigip_view - Manage ZoneRunner Views on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage ZoneRunner Views on a BIG-IP. ZoneRunner is a feature of the GTM module. Therefore, this module should only be used on BIG-IP systems that have the GTM module enabled. The SOAP connection has a number of known limitations when it comes to updating Views. It is only possible to



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- bigsuds


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                                                                                                                                                                                        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <b>options</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>A sequence of options for the view</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP password</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>port</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>BIG-IP web API port</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP host</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>present</code>, will ensure that the View exists with the correct zones in it. When <code>absent</code>, removes the View.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP username</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>view_name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The name of the view</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>view_order</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">0</div>
                                    </td>
                                                                <td>
                                                                        <div>The order of the view within the named.conf file. 0 = first in zone. 0xffffffff means to move the view to last. Any other number will move the view to that position, and bump up any view(s) by one (if necessary).</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>zones</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>A sequence of zones in this view</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the bigsuds Python package on the remote host. This is as easy as pip install bigsuds


Examples
--------

.. code-block:: yaml

    
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





Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

