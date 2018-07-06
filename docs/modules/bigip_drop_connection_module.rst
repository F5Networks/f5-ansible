:source: modules/bigip_drop_connection.py

:orphan:

.. _bigip_sys_connection_module:


bigip_sys_connection - Run commands on F5 devices via api
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Run commands on F5 devices via api




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
                    <b>command</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Command to run</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>BIG-IP password</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>BIG-IP host</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>BIG-IP username</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - F5 developed module 'f5-sdk' required
    - Best run as a local_action in your playbook
    - Requires administrative privileges for user


Examples
--------

.. code-block:: yaml

    
    - name: Show connections to LTM virtual server
      local_action: >
          bigip_sys_connection
          server={{ f5_ltm_server }}
          user={{ f5_ltm_username }}
          password={{ f5_ltm_password }}
          command="tmsh show sys connection cs-server-addr {{ ip_address }}"





Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Michael Perzel

