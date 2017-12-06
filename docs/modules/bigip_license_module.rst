.. _bigip_license:


bigip_license - Manage license installation and activation on BIG-IP devices
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage license installation and activation on BIG-IP devices. This module provides two different ways to license a device. Either via a activation key (which requires a connection back to f5.com) or, with the content of a license and dossier that you have acquired manually.


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
                <tr><td>accept_eula<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Declares whether you accept the BIG-IP EULA or not. By default, this value is <code>no</code>. You must specifically declare that you have viewed and accepted the license. This module will not present you with that EULA though, so it is incumbent on you to re</div>        </td></tr>
                <tr><td>dossier_content<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Path to file containing kernel dossier for your system.</div>        </td></tr>
                <tr><td>key<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The registration key to use to license the BIG-IP. This is required if the <code>state</code> is equal to <code>present</code> or <code>latest</code>.</div>        </td></tr>
                <tr><td>license_content<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Path to file containing the license to use. In most cases you will want to use a <code>lookup</code> for this.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>latest</li><li>present</li></ul></td>
        <td><div>The state of the license on the system. When <code>present</code>, only guarantees that a license is there. When <code>latest</code> ensures that the license is always valid. When <code>absent</code> removes the license on the system. <code>latest</code> is most useful internally. When using <code>absent</code>, the account accessing the device must be configured to use the advanced shell instead of Appliance Mode.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: License BIG-IP using a key
      bigip_license:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
      delegate_to: localhost

    - name: License BIG-IP using a development key
      bigip_license:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
          license_server: "xxx.f5net.com"
      delegate_to: localhost

    - name: License BIG-IP using a pre-acquired license
      bigip_license:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          license_content: "{{ lookup('file', 'license.lic') }}"
          dossier_content: "{{ lookup('file', 'dossier.txt') }}"
      delegate_to: localhost

    - name: Remove the license from the system
      bigip_license:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "absent"
      delegate_to: localhost

    - name: Update the current license of the BIG-IP
      bigip_license:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
          state: "latest"
      delegate_to: localhost



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