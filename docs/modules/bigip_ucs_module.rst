.. _bigip_ucs:


bigip_ucs - Manage UCS files.
+++++++++++++++++++++++++++++

.. versionadded:: 2.0


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage UCS files.


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds
  * requests
  * paramiko


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
            <tr>
    <td>force<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>yes</code> will upload the file every time and replace the file on the device. If <code>no</code>, the file will only be uploaded if it does not already exist. Generally should be <code>yes</code> only in cases where you have reason to believe that the image was corrupted during upload.</div></td></tr>
            <tr>
    <td>include_chassis_level_config<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>During restore of the UCS file, include chassis level configuration that is shared among boot volume sets. For example, cluster default configuration.</div></td></tr>
            <tr>
    <td>no_license<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Performs a full restore of the UCS file and all the files it contains, with the exception of the license file. The option must be used to restore a UCS on RMA devices (Returned Materials Authorization).</div></td></tr>
            <tr>
    <td>no_platform_check<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Bypasses the platform check and allows a UCS that was created using a different platform to be installed. By default (without this option), a UCS created from a different platform is not allowed to be installed.</div></td></tr>
            <tr>
    <td>passphrase<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Specifies the passphrase that is necessary to load the specified UCS file</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>reset_trust<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>When specified, the device and trust domain certs and keys are not loaded from the UCS. Instead, a new set is regenerated.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The BIG-IP host.</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>The BIG-IP server port.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>installed</td>
        <td><ul><li>absent</li><li>installed</li><li>present</li></ul></td>
        <td><div>When <code>installed</code>, ensures that the UCS is uploaded and installed, on the system. When <code>present</code>, ensures that the UCS is uploaded. When <code>absent</code>, the UCS will be removed from the system.</div></td></tr>
            <tr>
    <td>ucs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The path to the UCS file to install. The parameter must be provided if the <code>state</code> is either <code>installed</code> or <code>activated</code>.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Upload UCS
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          ucs: "/root/bigip.localhost.localdomain.ucs"
          state: "present"
      delegate_to: localhost
    
    - name: Install (upload, install) UCS.
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          ucs: "/root/bigip.localhost.localdomain.ucs"
          state: "installed"
      delegate_to: localhost
    
    - name: Install (upload, install) UCS without installing the license portion
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          ucs: "/root/bigip.localhost.localdomain.ucs"
          state: "installed"
          no_license: "yes"
      delegate_to: localhost
    
    - name: Install (upload, install) UCS except the license, and bypassing the platform check
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          ucs: "/root/bigip.localhost.localdomain.ucs"
          state: "installed"
          no_license: "yes"
          no_platform_check: "yes"
      delegate_to: localhost
    
    - name: Install (upload, install) UCS using a passphrase necessary to load the UCS
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          ucs: "/root/bigip.localhost.localdomain.ucs"
          state: "installed"
          passphrase: "MyPassphrase1234"
      delegate_to: localhost
    
    - name: Remove uploaded UCS file
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          ucs: "/root/bigip.localhost.localdomain.ucs"
          state: "absent"
      delegate_to: localhost


Notes
-----

.. note:: Requires the bigsuds Python package on the host if using the iControl interface. This is as easy as pip install bigsuds
.. note:: Requires the paramiko Python package on the host for UCS load commands that are not available through the REST or SOAP APIs
.. note:: Only the most basic checks are performed by this module. Other checks and considerations need to be taken into account. See the following URL. https://support.f5.com/kb/en-us/solutions/public/11000/300/sol11318.html
.. note:: This module requires SSH access to the remote BIG-IP and will use the ``user`` and ``password`` values specified by default. The web UI credentials typically differ from the SSH credentials so it is recommended that you use the bigip_user module to enable terminal access for the Web UI user
.. note:: This module does not handle devices with the FIPS 140 HSM
.. note:: This module does not handle BIG-IPs systems on the 6400, 6800, 8400, or 8800 hardware platform.
.. note:: This module does not verify that the new or replaced SSH keys from the UCS file are synchronized between the BIG-IP system and the SCCP
.. note:: This module does not support the 'rma' option
.. note:: This module does not support restoring a UCS archive on a BIG-IP 1500, 3400, 4100, 6400, 6800, or 8400 hardware platform other than the system from which the backup was created
.. note:: This module does not support restoring a UCS archive using the bigpipe utility
.. note:: The UCS restore operation restores the full configuration only if the hostname of the target system matches the hostname on which the UCS archive was created. If the hostname does not match, only the shared configuration is restored. You can ensure hostnames match by using the bigip_hostname Ansible module in a task before using this module.
.. note:: This module does not support re-licensing a BIG-IP restored from a UCS
.. note:: This module does not support restoring encrypted archives on replacement RMA units.
.. note:: This module will attempt to auto-recover a failed UCS load by using the iControl API to load the default backup UCS file (cs_backup.ucs)


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

