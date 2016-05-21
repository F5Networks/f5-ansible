.. _bigip_software:


bigip_software - Manage BIG-IP software versions and hotfixes
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage BIG-IP software versions and hotfixes


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds


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
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>yes</code> will upload the file every time and replace the file on the device. If <code>no</code>, the file will only be uploaded if it does not already exist. Generally should be <code>yes</code> only in cases where you have reason to believe that the image was corrupted during upload.</div><div>If <code>yes</code> with <code>reuse_inactive_volume</code> is specified and <code>volume</code> is not specified, Software will be installed / activated regardless of current running version to a new or an existing volume.</div></td></tr>
            <tr>
    <td>hotfix<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The path to an optional Hotfix to install. This parameter requires that the <code>software</code> parameter be specified.</div></br>
        <div style="font-size: small;">aliases: hotfix_image<div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>reuse_inactive_volume<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Automatically chooses the first inactive volume in alphanumeric order. If there is no inactive volume, new volume with incremented volume name will be created. For example, if HD1.1 is currently active and no other volume exists, then the module will create HD1.2 and install the software. If volume name does not end with numeric character, then add .1 to the current active volume name. When <code>volume</code> is specified, this option will be ignored.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>software<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The path to the software (base image) to install. The parameter must be provided if the <code>state</code> is either <code>installed</code> or <code>activated</code>.</div></br>
        <div style="font-size: small;">aliases: base_image<div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>activated</td>
        <td><ul><li>absent</li><li>activated</li><li>installed</li><li>present</li></ul></td>
        <td><div>When <code>installed</code>, ensures that the software is uploaded and installed, on the system. The device is not, however, rebooted into the new software. When <code>activated</code>, ensures that the software is uploaded, installed, and the system is rebooted to the new software. When <code>present</code>, ensures that the software is uploaded. When <code>absent</code>, only the uploaded image will be removed from the system</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
            <tr>
    <td>volume<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The volume to install the software and, optionally, the hotfix to. This parameter is only required when the <code>state</code> is either <code>activated</code> or <code>installed</code>.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Remove uploaded hotfix
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
          state: "absent"
      delegate_to: localhost
    
    - name: Upload hotfix
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
          state: "present"
      delegate_to: localhost
    
    - name: Remove uploaded base image
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          state: "absent"
      delegate_to: localhost
    
    - name: Upload base image
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          state: "present"
      delegate_to: localhost
    
    - name: Upload base image and hotfix
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
          state: "present"
      delegate_to: localhost
    
    - name: Remove uploaded base image and hotfix
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
          state: "absent"
      delegate_to: localhost
    
    - name: Install (upload, install) base image. Create volume if not exists
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          volume: "HD1.1"
          state: "installed"
      delegate_to: localhost
    
    - name: Install (upload, install) base image and hotfix. Create volume if not exists
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
          volume: "HD1.1"
          state: "installed"
    
    - name: Activate (upload, install, reboot) base image. Create volume if not exists
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          volume: "HD1.1"
          state: "activated"
      delegate_to: localhost
    
    - name: Activate (upload, install, reboot) base image and hotfix. Create volume if not exists
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
          volume: "HD1.1"
          state: "activated"
    
    - name: Activate (upload, install, reboot) base image and hotfix. Reuse inactive volume in volumes with prefix.
      bigip_software:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          software: "/root/BIGIP-11.6.0.0.0.401.iso"
          hotfix: "/root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso"
          reuse_inactive_volume: yes
          state: "activated"


Notes
-----

.. note:: Requires the bigsuds Python package on the host if using the iControl interface. This is as easy as pip install bigsuds
.. note:: Requires the lxml Python package on the host. This can be installed with pip install lxml
.. note:: https://devcentral.f5.com/articles/icontrol-101-06-file-transfer-apis


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

