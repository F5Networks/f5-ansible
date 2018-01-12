.. _bigip_sys_connection:


bigip_sys_connection - Run commands on F5 devices via api
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Run commands on F5 devices via api




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
                <tr><td>command<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Command to run</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP password</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP host</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP username</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Show connections to LTM virtual server
      local_action: >
          bigip_sys_connection
          server={{ f5_ltm_server }}
          user={{ f5_ltm_username }}
          password={{ f5_ltm_password }}
          command="tmsh show sys connection cs-server-addr {{ ip_address }}"



Notes
-----

.. note::
    - F5 developed module 'f5-sdk' required
    - Best run as a local_action in your playbook
    - Requires administrative privileges for user



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.