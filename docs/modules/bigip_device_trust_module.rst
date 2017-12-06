.. _bigip_device_trust:


bigip_device_trust - Manage the trust relationships between BIG-IPs
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage the trust relationships between BIG-IPs. Devices, once peered, cannot be updated. If updating is needed, the peer must first be removed before it can be re-added to the trust.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk
  * netaddr


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
                <tr><td>peer_hostname<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The hostname that you want to associate with the device. This value will be used to easily distinguish this device in BIG-IP configuration. If not specified, the value of <code>peer_server</code> will be used as a default.</div>        </td></tr>
                <tr><td>peer_password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The password of the API username of the remote peer device that you are trusting. If this value is not specified, then the value of <code>password</code>, or the environment variable <code>F5_PASSWORD</code> will be used.</div>        </td></tr>
                <tr><td>peer_server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The peer address to connect to and trust for synchronizing configuration. This is typically the management address of the remote device, but may also be a Self IP.</div>        </td></tr>
                <tr><td>peer_user<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The API username of the remote peer device that you are trusting. Note that the CLI user cannot be used unless it too has an API account. If this value is not specified, then the value of <code>user</code>, or the environment variable <code>F5_USER</code> will be used.</div>        </td></tr>
                <tr><td>type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>peer</td>
        <td><ul><li>peer</li><li>subordinate</li></ul></td>
        <td><div>Specifies whether the device you are adding is a Peer or a Subordinate. The default is <code>peer</code>.</div><div>The difference between the two is a matter of mitigating risk of compromise.</div><div>A subordinate device cannot sign a certificate for another device.</div><div>In the case where the security of an authority device in a trust domain is compromised, the risk of compromise is minimized for any subordinate device.</div><div>Designating devices as subordinate devices is recommended for device groups with a large number of member devices, where the risk of compromise is high.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Add trusts for all peer devices to Active device
      bigip_device_trust:
        server: lb.mydomain.com
        user: admin
        password: secret
        peer_server: "{{ item.ansible_host }}"
        peer_hostname: "{{ item.inventory_hostname }}"
        peer_user: "{{ item.bigip_username }}"
        peer_password: "{{ item.bigip_password }}"
      with_items: hostvars
      when: inventory_hostname in groups['master']
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
        <td> peer_server </td>
        <td> The remote IP address of the trusted peer. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 10.0.2.15 </td>
    </tr>
            <tr>
        <td> peer_hostname </td>
        <td> The remote hostname used to identify the trusted peer. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> test-bigip-02.localhost.localdomain </td>
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