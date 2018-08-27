:source: bigip_software.py

:orphan:

.. _bigip_software_module:


bigip_software - Manage BIG-IP software versions and hotfixes
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage BIG-IP software versions and hotfixes.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- f5-sdk >= 3.0.9
- isoparser


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                    <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="2">
                    <b>force</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                                                                                    <li>yes</li>
                                                                                                                                                                                                                                                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">no</div>
                                    </td>
                                                                <td>
                                                                        <div>If <code>yes</code> will upload the file every time and replace the file on the device. If <code>no</code>, the file will only be uploaded if it does not already exist. Generally should be <code>yes</code> only in cases where you have reason to believe that the image was corrupted during upload.</div>
                                                    <div>If <code>yes</code> with <code>reuse_inactive_volume</code> is specified and <code>volume</code> is not specified, Software will be installed / activated regardless of current running version to a new or an existing volume.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>hotfix</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The path to an optional Hotfix to install. This parameter requires that the <code>software</code> parameter be specified or the corresponding software image exists on the unit. If this parameter begins with either <code>http://</code> or <code>https://</code>, the path will be assumed to be a remote source.</div>
                                                    <div>When providing link to the hotfix ISO, if the ISO name is different than the one listed inside the <code>hotfix_md5</code> md5sum file. We will change it accordingly while saving the files on the device. This might lead to ISO names not matching the links provided in <code>hotfix</code>.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: hotfix_image</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>hotfix_md5sum</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The link to an MD5 sum file of the remote hotfix ISO image, it is required when <code>hotfix</code> parameter is used and that parameter is a remote URL.</div>
                                                    <div>Parameter only used when and <code>state</code> is <code>installed</code>, <code>activated</code>, or <code>present</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>provider</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>A dict object containing connection details.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>server_port</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>validate_certs</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">10</div>
                                    </td>
                                                                <td>
                                                                        <div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>ssh_keyfile</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>transport</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>rest</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>cli</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>remote_src</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">no</div>
                                    </td>
                                                                <td>
                                                                        <div>Parameter to enable remote source usage. When set to <code>yes</code> bigip will attempt to download and verify the images using the links provided in <code>software</code>, <code>hotfix</code>, <code>software_md5sum</code> and <code>hotfix_md5sum</code>.</div>
                                                    <div>This parameter also makes the <code>software_md5sum</code> and <code>hotfix_md5sum</code> mandatory when <code>state is C(present</code>, <code>activated</code> or <code>installed</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>reuse_inactive_volume</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Automatically chooses the first inactive volume in alphanumeric order. If there is no inactive volume, new volume with incremented volume name will be created. For example, if HD1.1 is currently active and no other volume exists, then the module will create HD1.2 and install the software. If volume name does not end with numeric character, then add <code>.1</code> to the current active volume name. When <code>volume</code> is specified, this option will be ignored.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>server_port</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>software</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The path to the software (base image) to install. The parameter must be provided if the <code>state</code> is either <code>installed</code> or <code>activated</code>. If this parameter begins with either <code>http://</code> or <code>https://</code>, the path will be assumed to be a remote source.</div>
                                                    <div>When providing link to the software ISO, if the ISO name is different than the one listed inside the <code>software_md5sum</code> md5sum file. We will change it accordingly when saving the files on the device. This might lead to ISO names not matching the links provided in <code>software</code>.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: base_image</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>software_md5sum</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The link to an MD5 sum file of the remote software ISO image, it is required when <code>software</code> parameter is used and that parameter is a remote URL.</div>
                                                    <div>Parameter only used when and <code>state</code> is <code>installed</code>, <code>activated</code>, or <code>present</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>activated</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>installed</li>
                                                                                                                                                                                                <li>present</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>present</code>, ensures that the software is uploaded/downloaded.</div>
                                                    <div>When <code>installed</code>, ensures that the software is uploaded/downloaded and installed on the system. The device is <b>not</b> rebooted into the new software.</div>
                                                    <div>When <code>activated</code>, ensures that the software is uploaded/downloaded, installed, and the system is rebooted to the new software.</div>
                                                    <div>When <code>absent</code>, only the uploaded/downloaded image will be removed from the system.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>validate_certs</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.0)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>volume</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The volume to install the software and, optionally, the hotfix to. This parameter is only required when the <code>state</code> is <code>activated</code> or <code>installed</code>.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the isoparser Python package on the host. This can be installed with pip install isoparser
    - Requires the lxml Python package on the host. This can be installed with pip install lxml
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.


Examples
--------

.. code-block:: yaml

    
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
        password: secret
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
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                                                                                                                                                                                                        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <b>build</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Build of the remote ISO image.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">0.0.249</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>force</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Set when forcing the ISO upload/download.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>hotfix</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Local path, or remote link to the hotfix ISO image.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/root/hotfixes/hotfix.iso</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>hotfix_md5</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>MD5 sum file for the remote hotfix ISO image.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">http://someweb.com/fake/hotfix.iso.md5</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>reuse_inactive_volume</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Create volume or reuse existing volume.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>software</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Local path, or remote link to the software ISO image.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">http://someweb.com/fake/software.iso</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>software_md5</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>MD5 sum file for the remote software ISO image.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">http://someweb.com/fake/software.iso.md5</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>state</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Action performed on the target device.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">absent</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>version</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Version of the remote ISO image.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">12.1.1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>volume</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Volume to install desired image on</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">HD1.2</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)
- Wojciech Wypior (@wojtek0806)

