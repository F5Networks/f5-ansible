:source: bigip_dns_zone.py

:orphan:

.. _bigip_dns_zone_module:


bigip_dns_zone - Manages DNS zones on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- This module manages DNS zones described in the iControl Management documentation



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- bigsuds
- distutils


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
                                                                        <div>A sequence of options for the view.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP password.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP host.</div>
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
                                                                        <div>Whether the record should exist.  When <code>absent</code>, removes the record.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP username.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: username</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>zone</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The name of the zone.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the bigsuds Python package on the remote host. This is as easy as pip install bigsuds
    - https://devcentral.f5.com/wiki/iControl.Management__Zone.ashx


Examples
--------

.. code-block:: yaml

    
    - name: Add a view, named "internal", to organization.com zone
      module: bigip_view:
        username: admin
        password: secret
        server: lb.mydomain.com
        zone_names:
          - organization.com
        state: present
        options:
          - domain_name: elliot.organization.com
            ip_address: 10.1.1.1





Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

