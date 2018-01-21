.. _bigip_software:


bigip_software - Manage BIG-IP software versions and hotfixes
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage BIG-IP software versions and hotfixes.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9
  * isoparser


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
                <tr><td>force<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>yes</code> will upload the file every time and replace the file on the device. If <code>no</code>, the file will only be uploaded if it does not already exist. Generally should be <code>yes</code> only in cases where you have reason to believe that the image was corrupted during upload.</div><div>If <code>yes</code> with <code>reuse_inactive_volume</code> is specified and <code>volume</code> is not specified, Software will be installed / activated regardless of current running version to a new or an existing volume.</div>        </td></tr>
                <tr><td>hotfix<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The path to an optional Hotfix to install. This parameter requires that the <code>software</code> parameter be specified or the corresponding software image exists on the unit. If this parameter begins with either <code>http://</code> or <code>https://</code>, the path will be assumed to be a remote source.</div><div>When providing link to the hotfix ISO, if the ISO name is different than the one listed inside the <code>hotfix_md5</code> md5sum file. We will change it accordingly while saving the files on the device. This might lead to ISO names not matching the links provided in <code>hotfix</code>.</div></br>
    <div style="font-size: small;">aliases: hotfix_image<div>        </td></tr>
                <tr><td>hotfix_md5sum<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The link to an MD5 sum file of the remote hotfix ISO image, it is required when <code>hotfix</code> parameter is used and that parameter is a remote URL.</div><div>Parameter only used when and <code>state</code> is <code>installed</code>, <code>activated</code>, or <code>present</code>.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td rowspan="2">provider<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>A dict object containing connection details.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object provider</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>True</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>transport<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td>cli</td>
                <td><ul><li>rest</li><li>cli</li></ul></td>
                <td><div>Configures the transport connection to use when connecting to the remote device.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>remote_src<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>no</td>
        <td></td>
        <td><div>Parameter to enable remote source usage. When set to <code>yes</code> bigip will attempt to download and verify the images using the links provided in <code>software</code>, <code>hotfix</code>, <code>software_md5sum</code> and <code>hotfix_md5sum</code>.</div><div>This parameter also makes the <code>software_md5sum</code> and <code>hotfix_md5sum</code> mandatory when <code>state is C(present</code>, <code>activated</code> or <code>installed</code>.</div>        </td></tr>
                <tr><td>reuse_inactive_volume<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Automatically chooses the first inactive volume in alphanumeric order. If there is no inactive volume, new volume with incremented volume name will be created. For example, if HD1.1 is currently active and no other volume exists, then the module will create HD1.2 and install the software. If volume name does not end with numeric character, then add <code>.1</code> to the current active volume name. When <code>volume</code> is specified, this option will be ignored.</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>software<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The path to the software (base image) to install. The parameter must be provided if the <code>state</code> is either <code>installed</code> or <code>activated</code>. If this parameter begins with either <code>http://</code> or <code>https://</code>, the path will be assumed to be a remote source.</div><div>When providing link to the software ISO, if the ISO name is different than the one listed inside the <code>software_md5sum</code> md5sum file. We will change it accordingly when saving the files on the device. This might lead to ISO names not matching the links provided in <code>software</code>.</div></br>
    <div style="font-size: small;">aliases: base_image<div>        </td></tr>
                <tr><td>software_md5sum<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The link to an MD5 sum file of the remote software ISO image, it is required when <code>software</code> parameter is used and that parameter is a remote URL.</div><div>Parameter only used when and <code>state</code> is <code>installed</code>, <code>activated</code>, or <code>present</code>.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>activated</td>
        <td><ul><li>absent</li><li>activated</li><li>installed</li><li>present</li></ul></td>
        <td><div>When <code>present</code>, ensures that the software is uploaded/downloaded.</div><div>When <code>installed</code>, ensures that the software is uploaded/downloaded and installed on the system. The device is <b>not</b> rebooted into the new software.</div><div>When <code>activated</code>, ensures that the software is uploaded/downloaded, installed, and the system is rebooted to the new software.</div><div>When <code>absent</code>, only the uploaded/downloaded image will be removed from the system.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                <tr><td>volume<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The volume to install the software and, optionally, the hotfix to. This parameter is only required when the <code>state</code> is <code>activated</code> or <code>installed</code>.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Remove uploaded hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: /root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso
        state: absent
      delegate_to: localhost

    - name: Upload hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: /root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso
        state: present
      delegate_to: localhost

    - name: Remove uploaded base image
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        state: absent
      delegate_to: localhost

    - name: Upload base image
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        state: present
      delegate_to: localhost

    - name: Upload base image and hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        hotfix: /root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso
        state: present
      delegate_to: localhost

    - name: Remove uploaded base image and hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        hotfix: /root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso
        state: absent
      delegate_to: localhost

    - name: Install (upload, install) base image. Create volume if not exists
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        volume: HD1.1
        state: installed
      delegate_to: localhost

    - name: Install (upload, install) base image and hotfix. Create volume if not exists
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: "secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        hotfix: /root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso
        volume: HD1.1
        state: installed
      delegate_to: localhost

    - name: Activate (upload, install, reboot) base image. Create volume if not exists
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        volume: HD1.1
        state: activated
      delegate_to: localhost

    - name: Activate (upload, install, reboot) base image and hotfix. Create volume if not exists
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        hotfix: /root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso
        volume: HD1.1
        state: activated
      delegate_to: localhost

    - name: Activate (upload, install, reboot) base image and hotfix. Reuse inactive volume in volumes with prefix.
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: /root/BIGIP-11.6.0.0.0.401.iso
        hotfix: /root/Hotfix-BIGIP-11.6.0.3.0.412-HF3.iso
        reuse_inactive_volume: yes
        state: activated
      delegate_to: localhost

    - name: Activate (download, install, reboot, reuse_inactive_volume) base image and hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso"
        hotfix_md5sum: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5"
        software: "http://fake.com/BIGIP-12.1.2.0.0.249.iso"
        software_md5sum: "http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5"
        state: activated
        reuse_inactive_volume: True
      delegate_to: localhost

    - name: Download hotfix image
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso"
        hotfix_md5sum: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5"
        state: present
      delegate_to: localhost

    - name: Remove uploaded hotfix image
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso"
      delegate_to: localhost

    - name: Install (download, install) base image
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: "http://fake.com/BIGIP-12.1.2.0.0.249.iso"
        software_md5sum: "http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5"
        volume: HD1.1
        state: installed
      delegate_to: localhost

    - name: Install (download, install) base image and hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso"
        hotfix_md5sum: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5"
        software: "http://fake.com/BIGIP-12.1.2.0.0.249.iso"
        software_md5sum: "http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5"
        state: installed
        volume: HD1.2
       delegate_to: localhost

    - name: Download hotfix image (name mismatch)
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: "http://fake.com/12.1.2-HF1.iso"
        hotfix_md5sum: "http://fake.com/Hotfix-12.1.2HF1.md5"
        state: present
      delegate_to: localhost

    - name: Download software image (name mismatch)
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        software: "http://fake.com/BIGIP-12.1.2.iso"
        software_md5sum: "http://fake.com/12.1.2.md5"
        state: present
      delegate_to: localhost

    - name: Activate (download, install, reboot, reuse_inactive_volume) base image and hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso"
        hotfix_md5sum: "http://fake.com/Hotfix-12.1.2.1.0.271-HF1.iso.md5"
        software: /root/BIGIP-11.6.0.0.0.401.iso
        state: activated
        reuse_inactive_volume: True
      delegate_to: localhost

    - name: Activate (download, install, reboot, reuse_inactive_volume) base image and hotfix
      bigip_software:
        server: lb.mydomain.com
        user: admin
        password: secret
        hotfix: /root/Hotfix-12.1.2.1.0.271-HF1.iso
        software: "http://fake.com/BIGIP-12.1.2.0.0.249.iso"
        software_md5sum: "http://fake.com/BIGIP-12.1.2.0.0.249.iso.md5"
        state: activated
        reuse_inactive_volume: True
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
        <td> force </td>
        <td> Set when forcing the ISO upload/download. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> hotfix_md5 </td>
        <td> MD5 sum file for the remote hotfix ISO image. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> http://someweb.com/fake/hotfix.iso.md5 </td>
    </tr>
            <tr>
        <td> reuse_inactive_volume </td>
        <td> Create volume or reuse existing volume. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> False </td>
    </tr>
            <tr>
        <td> volume </td>
        <td> Volume to install desired image on </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> HD1.2 </td>
    </tr>
            <tr>
        <td> state </td>
        <td> Action performed on the target device. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> absent </td>
    </tr>
            <tr>
        <td> version </td>
        <td> Version of the remote ISO image. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 12.1.1 </td>
    </tr>
            <tr>
        <td> build </td>
        <td> Build of the remote ISO image. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 0.0.249 </td>
    </tr>
            <tr>
        <td> hotfix </td>
        <td> Local path, or remote link to the hotfix ISO image. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /root/hotfixes/hotfix.iso </td>
    </tr>
            <tr>
        <td> software_md5 </td>
        <td> MD5 sum file for the remote software ISO image. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> http://someweb.com/fake/software.iso.md5 </td>
    </tr>
            <tr>
        <td> software </td>
        <td> Local path, or remote link to the software ISO image. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> http://someweb.com/fake/software.iso </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the isoparser Python package on the host. This can be installed with pip install isoparser
    - Requires the lxml Python package on the host. This can be installed with pip install lxml
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.