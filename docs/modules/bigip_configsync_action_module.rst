.. _bigip_configsync_action:


bigip_configsync_action - Perform different actions related to config-sync.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Allows one to run different config-sync actions. These actions allow you to manually sync your configuration across multiple BIG-IPs when those devices are in an HA pair.


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
                <tr><td>device_group<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The device group that you want to perform config-sync actions on.</div>        </td></tr>
                <tr><td>overwrite_config<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Indicates that the sync operation overwrites the configuration on the target.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>sync_device_to_group<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Specifies that the system synchronizes configuration data from this device to other members of the device group. In this case, the device will do a "push" to all the other devices in the group. This option is mutually exclusive with the <code>sync_group_to_device</code> option.</div>        </td></tr>
                <tr><td>sync_most_recent_to_device<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Specifies that the system synchronizes configuration data from the device with the most recent configuration. In this case, the device will do a "pull" from the most recently updated device. This option is mutually exclusive with the <code>sync_device_to_group</code> options.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Sync configuration from device to group
      bigip_configsync_actions:
          device_group: "foo-group"
          sync_device_to_group: yes
          server: "lb01.mydomain.com"
          user: "admin"
          password: "secret"
          validate_certs: no
      delegate_to: localhost
    
    - name: Sync configuration from most recent device to the current host
      bigip_configsync_actions:
          device_group: "foo-group"
          sync_most_recent_to_device: yes
          server: "lb01.mydomain.com"
          user: "admin"
          password: "secret"
          validate_certs: no
      delegate_to: localhost
    
    - name: Perform an initial sync of a device to a new device group
      bigip_configsync_actions:
          device_group: "new-device-group"
          sync_device_to_group: yes
          server: "lb01.mydomain.com"
          user: "admin"
          password: "secret"
          validate_certs: no
      delegate_to: localhost


Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires the objectpath Python package on the host. This is as easy as pip install objectpath.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.