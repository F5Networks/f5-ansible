.. _bigip_qkview:


bigip_qkview - Manage qkviews on the device
+++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages creating and downloading qkviews from a BIG-IP. Various options can be provided when creating qkviews. The qkview is important when dealing with F5 support. It may be required that you upload this qkview to the supported channels during resolution of an SRs that you may have opened.


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
                <tr><td>asm_request_log<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>When <code>True</code>, includes the ASM request log data. When <code>False</code>, excludes the ASM request log data.</div>        </td></tr>
                <tr><td>complete_information<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Include complete information in the qkview.</div>        </td></tr>
                <tr><td>dest<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Destination on your local filesystem when you want to save the qkview.</div>        </td></tr>
                <tr><td>exclude<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>all</li><li>audit</li><li>secure</li><li>bash_history</li></ul></td>
        <td><div>Exclude various file from the qkview.</div>        </td></tr>
                <tr><td>exclude_core<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Exclude core files from the qkview.</div>        </td></tr>
                <tr><td>filename<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>localhost.localdomain.qkview</td>
        <td></td>
        <td><div>Name of the qkview to create on the remote BIG-IP.</div>        </td></tr>
                <tr><td>force<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, the file will only be transferred if the destination does not exist.</div>        </td></tr>
                <tr><td>max_file_size<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Max file size, in bytes, of the qkview to create. By default, no max file size is specified.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Fetch a qkview from the remote device
      bigip_qkview:
        asm_request_log: yes
        exclude:
          - audit
          - secure
        dest: /tmp/localhost.localdomain.qkview
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
        <td> stdout_lines </td>
        <td> The value of stdout split into a list </td>
        <td align=center> always </td>
        <td align=center> list </td>
        <td align=center> [['...', '...'], ['...'], ['...']] </td>
    </tr>
            <tr>
        <td> stdout </td>
        <td> The set of responses from the commands </td>
        <td align=center> always </td>
        <td align=center> list </td>
        <td align=center> ['...', '...'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - This module does not include the "max time" or "restrict to blade" options.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.