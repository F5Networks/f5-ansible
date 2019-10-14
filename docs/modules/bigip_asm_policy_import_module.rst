:source: bigip_asm_policy_import.py

:orphan:

.. _bigip_asm_policy_import_module:


bigip_asm_policy_import - Manage BIG-IP ASM policy imports
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage BIG-IP ASM policies policy imports.




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
                    <b>base64</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Indicates if imported policy string is encoded in base64.</div>
                                                    <div>Parameter only takes effect when using <code>inline</code> method of import.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>encoding</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>windows-874</li>
                                                                                                                                                                                                <li>utf-8</li>
                                                                                                                                                                                                <li>koi8-r</li>
                                                                                                                                                                                                <li>windows-1253</li>
                                                                                                                                                                                                <li>iso-8859-10</li>
                                                                                                                                                                                                <li>gbk</li>
                                                                                                                                                                                                <li>windows-1256</li>
                                                                                                                                                                                                <li>windows-1250</li>
                                                                                                                                                                                                <li>iso-8859-13</li>
                                                                                                                                                                                                <li>iso-8859-9</li>
                                                                                                                                                                                                <li>windows-1251</li>
                                                                                                                                                                                                <li>iso-8859-6</li>
                                                                                                                                                                                                <li>big5</li>
                                                                                                                                                                                                <li>gb2312</li>
                                                                                                                                                                                                <li>iso-8859-1</li>
                                                                                                                                                                                                <li>windows-1252</li>
                                                                                                                                                                                                <li>iso-8859-4</li>
                                                                                                                                                                                                <li>iso-8859-2</li>
                                                                                                                                                                                                <li>iso-8859-3</li>
                                                                                                                                                                                                <li>gb18030</li>
                                                                                                                                                                                                <li>shift_jis</li>
                                                                                                                                                                                                <li>iso-8859-8</li>
                                                                                                                                                                                                <li>euc-kr</li>
                                                                                                                                                                                                <li>iso-8859-5</li>
                                                                                                                                                                                                <li>iso-8859-7</li>
                                                                                                                                                                                                <li>windows-1255</li>
                                                                                                                                                                                                <li>euc-jp</li>
                                                                                                                                                                                                <li>iso-8859-15</li>
                                                                                                                                                                                                <li>windows-1257</li>
                                                                                                                                                                                                <li>iso-8859-16</li>
                                                                                                                                                                                                <li>auto-detect</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the desired application language of the imported policy.</div>
                                                    <div>The imported policy cannot be a <code>parent</code> type or attached to a <code>parent</code> policy when <code>auto-detect</code> encoding is set.</div>
                                                    <div>When importing policy to attach to a <code>parent</code> policy, the <code>encoding</code> of the imported policy if different must be set to to be the same value as <code>parent_policy</code>, otherwise import will fail.</div>
                                                    <div>This parameter is available on TMOS version 13.x and up and only takes effect when <code>inline</code> import method is used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>force</b>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When set to <code>yes</code> any existing policy with the same name will be overwritten by the new import.</div>
                                                    <div>Works for both inline and file imports, if the policy does not exist this setting is ignored.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>inline</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>When specified the ASM policy is created from a provided string.</div>
                                                    <div>Content needs to be provided in a valid XML format otherwise the operation will fail.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The ASM policy to create or override.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>parent_policy</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The parent policy to which the newly imported policy should be attached as child.</div>
                                                    <div>When <code>parent_policy</code> is specified the imported <code>policy_type</code> must not be <code>parent</code>.</div>
                                                    <div>This parameter is available on TMOS version 13.x and up and only takes effect when <code>inline</code> import method is used.</div>
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
                                                                        <div>Device partition to create policy on.</div>
                                                    <div>This parameter is also applied to indicate the partition of the <code>parent</code> policy.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>policy_type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>security</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>parent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The type of the policy to import.</div>
                                                    <div>When <code>policy_type</code> is <code>security</code> the policy is imported as an application security policy that you can apply to a virtual server.</div>
                                                    <div>When <code>policy_type</code> is <code>parent</code> the policy becomes a parent to which other Security policies attach inheriting its attributes. This policy type cannot be applied to Virtual Servers.</div>
                                                    <div>This parameter is available on TMOS version 13.x and up and only takes effect when <code>inline</code> import method is used.</div>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>auth_provider</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Configures the auth provider for to obtain authentication tokens from the remote device.</div>
                                                    <div>This option is really used when working with BIG-IQ devices.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>retain_inheritance_settings</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Indicate if an imported security type policy should retain settings when attached to parent policy.</div>
                                                    <div>This parameter is available on TMOS version 13.x and up and only takes effect when <code>inline</code> import method is used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>source</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Full path to a policy file to be imported into the BIG-IP ASM.</div>
                                                    <div>Policy files exported from newer versions of BIG-IP cannot be imported into older versions of BIG-IP. The opposite, however, is true; you can import older into newer.</div>
                                                    <div>The file format can be binary or XML.</div>
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

    
    - name: Import ASM policy
      bigip_asm_policy_import:
        name: new_asm_policy
        file: /root/asm_policy.xml
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Import ASM policy inline
      bigip_asm_policy_import:
        name: foo-policy4
        inline: <xml>content</xml>
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Override existing ASM policy
      bigip_asm_policy:
        name: new_asm_policy
        source: /root/asm_policy_new.xml
        force: yes
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
                    <b>base64</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Indicates if imported policy string is encoded in base64.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>encoding</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Thehe desired application language of the imported policy.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">utf-8</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>force</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Set when overwriting an existing policy.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>inline</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Contents of policy as an inline string.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">&lt;xml&gt;foobar contents&lt;/xml&gt;</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Name of the ASM policy to be created/overwritten.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Asm_APP1_Transparent</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>parent_policy</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The parent policy to which the newly imported policy should be attached as child.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/parent</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>policy_type</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The type of the policy to import.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">security</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>retain_inheritance_settings</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Indicate if an imported security type policy should retain settings when attached to parent policy.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>source</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Local path to an ASM policy file.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/root/some_policy.xml</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Wojciech Wypior (@wojtek0806)

