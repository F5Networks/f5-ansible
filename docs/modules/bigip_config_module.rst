.. _bigip_config:


bigip_config - Manage BIG-IP configuration sections
+++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages a BIG-IP configuration by allowing TMSH commands that modify running configuration, or merge SCF formatted files into the running configuration. Additionally, this module is of significant importance because it allows you to save your running configuration to disk. Since the F5 module only manipulate running configuration, it is important that you utilize this module to save that running config.


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
                <tr><td>merge_content<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Loads the specified configuration that you want to merge into the running configuration. This is equivalent to using the <code>tmsh</code> command <code>load sys config from-terminal merge</code>. If you need to read configuration from a file or template, use Ansible's <code>file</code> or <code>template</code> lookup plugins respectively.</div>        </td></tr>
                <tr><td>reset<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Loads the default configuration on the device. If this option is specified, the default configuration will be loaded before any commands or other provided configuration is run.</div>        </td></tr>
                <tr><td>save<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>The <code>save</code> argument instructs the module to save the running-config to startup-config. This operation is performed after any changes are made to the current running config. If no changes are made, the configuration is still saved to the startup config. This option will always cause the module to return changed.</div>        </td></tr>
                <tr><td>verify<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Validates the specified configuration to see whether they are valid to replace the running configuration. The running configuration will not be changed.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Save the running configuration of the BIG-IP
      bigip_config:
        save: yes
        server: lb.mydomain.com
        password: secret
        user: admin
        validate_certs: no
      delegate_to: localhost

    - name: Reset the BIG-IP configuration, for example, to RMA the device
      bigip_config:
        reset: yes
        save: yes
        server: lb.mydomain.com
        password: secret
        user: admin
        validate_certs: no
      delegate_to: localhost

    - name: Load an SCF configuration
      bigip_config:
        merge_content: "{{ lookup('file', '/path/to/config.scf') }}"
        server: lb.mydomain.com
        password: secret
        user: admin
        validate_certs: no
      delegate_to: localhost


Return Values
-------------

Common return values are `documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`_, the following are the fields unique to this module:

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
        <td> The set of responses from the options </td>
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
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.