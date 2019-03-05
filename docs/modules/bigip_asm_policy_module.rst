:source: _bigip_asm_policy.py

:orphan:

.. _bigip_asm_policy_module:


bigip_asm_policy - Manage BIG-IP ASM policies
+++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5

.. contents::
   :local:
   :depth: 2

DEPRECATED
----------
:Removed in Ansible: version: 2.12
:Why: The bigip_asm_policy module has been split into three new modules to handle import, export and general policy management. This will allow scalability of the asm policy management as well as ease of maintenance. Additionally to further reduce the burden of having multiple smaller module F5 has created asm_policy role in Ansible Galaxy for a more declarative way of ASM policy management.

:Alternative: bigip_asm_policy_manage



Synopsis
--------
- Manage BIG-IP ASM policies.




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
                    <b>active</b>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>yes</code> will apply and activate existing inactive policy. If <code>no</code>, it will deactivate existing active policy. Generally should be <code>yes</code> only in cases where you want to activate new or existing policy.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>file</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Full path to a policy file to be imported into the BIG-IP ASM.</div>
                                                    <div>Policy files exported from newer versions of BIG-IP cannot be imported into older versions of BIG-IP. The opposite, however, is true; you can import older into newer.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The ASM policy to manage or create.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>partition</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">Common</div>
                                    </td>
                                                                <td>
                                                                        <div>Device partition to manage resources on.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password for the user account used to connect to the BIG-IP.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_PASSWORD</code>.</div>
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
                                                                        <div>The password for the user account used to connect to the BIG-IP.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_PASSWORD</code>.</div>
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
                                                                        <div>The BIG-IP host.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER</code>.</div>
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
                                                                        <div>The BIG-IP server port.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER_PORT</code>.</div>
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
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_USER</code>.</div>
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
                                                                        <div>If <code>no</code>, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_VALIDATE_CERTS</code>.</div>
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
                                                                        <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports.</div>
                                                    <div>You may omit this option by setting the environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>transport</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>cli</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>rest</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER</code>.</div>
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
                                                                        <div>The BIG-IP server port.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER_PORT</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>state</code> is <code>present</code>, and <code>file</code> or <code>template</code> parameter is provided, new ASM policy is imported and created with the given <code>name</code>.</div>
                                                    <div>When <code>state</code> is present and no <code>file</code> or <code>template</code> parameter is provided new blank ASM policy is created with the given <code>name</code>.</div>
                                                    <div>When <code>state</code> is <code>absent</code>, ensures that the policy is removed, even if it is currently active.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>template</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>ActiveSync v1.0 v2.0 (http)</li>
                                                                                                                                                                                                <li>ActiveSync v1.0 v2.0 (https)</li>
                                                                                                                                                                                                <li>Comprehensive</li>
                                                                                                                                                                                                <li>Drupal</li>
                                                                                                                                                                                                <li>Fundamental</li>
                                                                                                                                                                                                <li>Joomla</li>
                                                                                                                                                                                                <li>LotusDomino 6.5 (http)</li>
                                                                                                                                                                                                <li>LotusDomino 6.5 (https)</li>
                                                                                                                                                                                                <li>OWA Exchange 2003 (http)</li>
                                                                                                                                                                                                <li>OWA Exchange 2003 (https)</li>
                                                                                                                                                                                                <li>OWA Exchange 2003 with ActiveSync (http)</li>
                                                                                                                                                                                                <li>OWA Exchange 2003 with ActiveSync (https)</li>
                                                                                                                                                                                                <li>OWA Exchange 2007 (http)</li>
                                                                                                                                                                                                <li>OWA Exchange 2007 (https)</li>
                                                                                                                                                                                                <li>OWA Exchange 2007 with ActiveSync (http)</li>
                                                                                                                                                                                                <li>OWA Exchange 2007 with ActiveSync (https)</li>
                                                                                                                                                                                                <li>OWA Exchange 2010 (http)</li>
                                                                                                                                                                                                <li>OWA Exchange 2010 (https)</li>
                                                                                                                                                                                                <li>Oracle 10g Portal (http)</li>
                                                                                                                                                                                                <li>Oracle 10g Portal (https)</li>
                                                                                                                                                                                                <li>Oracle Applications 11i (http)</li>
                                                                                                                                                                                                <li>Oracle Applications 11i (https)</li>
                                                                                                                                                                                                <li>PeopleSoft Portal 9 (http)</li>
                                                                                                                                                                                                <li>PeopleSoft Portal 9 (https)</li>
                                                                                                                                                                                                <li>Rapid Deployment Policy</li>
                                                                                                                                                                                                <li>SAP NetWeaver 7 (http)</li>
                                                                                                                                                                                                <li>SAP NetWeaver 7 (https)</li>
                                                                                                                                                                                                <li>SharePoint 2003 (http)</li>
                                                                                                                                                                                                <li>SharePoint 2003 (https)</li>
                                                                                                                                                                                                <li>SharePoint 2007 (http)</li>
                                                                                                                                                                                                <li>SharePoint 2007 (https)</li>
                                                                                                                                                                                                <li>SharePoint 2010 (http)</li>
                                                                                                                                                                                                <li>SharePoint 2010 (https)</li>
                                                                                                                                                                                                <li>Vulnerability Assessment Baseline</li>
                                                                                                                                                                                                <li>Wordpress</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>An ASM policy built-in template. If the template does not exist we will raise an error.</div>
                                                    <div>Once the policy has been created, this value cannot change.</div>
                                                    <div>The <code>Comprehensive</code>, <code>Drupal</code>, <code>Fundamental</code>, <code>Joomla</code>, <code>Vulnerability Assessment Baseline</code>, and <code>Wordpress</code> templates are only available on BIG-IP versions &gt;= 13.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_USER</code>.</div>
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
                                                                        <div>If <code>no</code>, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_VALIDATE_CERTS</code>.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Import and activate ASM policy
      bigip_asm_policy:
        name: new_asm_policy
        file: /root/asm_policy.xml
        active: yes
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Import ASM policy from template
      bigip_asm_policy:
        name: new_sharepoint_policy
        template: SharePoint 2007 (http)
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Create blank ASM policy
      bigip_asm_policy:
        name: new_blank_policy
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Create blank ASM policy and activate
      bigip_asm_policy:
        name: new_blank_policy
        active: yes
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Activate ASM policy
      bigip_asm_policy:
        name: inactive_policy
        active: yes
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Deactivate ASM policy
      bigip_asm_policy:
        name: active_policy
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Import and activate ASM policy in Role
      bigip_asm_policy:
        name: new_asm_policy
        file: "{{ role_path }}/files/asm_policy.xml"
        active: yes
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Import ASM binary policy
      bigip_asm_policy:
        name: new_asm_policy
        file: "/root/asm_policy.plc"
        active: yes
        state: present
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
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
                    <b>active</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Set when activating/deactivating ASM policy</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>file</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Local path to ASM policy file.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/root/some_policy.xml</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Name of the ASM policy to be managed/created</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Asm_APP1_Transparent</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>state</b>
                    <br/><div style="font-size: small; color: red">str</div>
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
                    <b>template</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Name of the built-in ASM policy template</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">OWA Exchange 2007 (https)</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------

This module is **deprecated** and will be removed in version 2.12. For more information see `DEPRECATED`_.


Author
~~~~~~

- Wojciech Wypior (@wojtek0806)
- Tim Rupp (@caphrim007)

