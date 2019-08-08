:source: bigip_asm_policy_signature_set.py

:orphan:

.. _bigip_asm_policy_signature_set_module:


bigip_asm_policy_signature_set - Manages Signature Sets on ASM policy
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages Signature Sets on ASM policy.




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
                    <b>alarm</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies if the security policy logs the request data in the Statistics screen, when a request matches a signature that is included in the signature set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>block</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Effective when the security policy`s enforcement mode is Blocking.</div>
                                                    <div>Determines how the system treats requests that match a signature included in the signature set.</div>
                                                    <div>When <code>yes</code> the system blocks all requests that match a signature, and provides the client with a support ID number.</div>
                                                    <div>When <code>no</code> the system accepts those requests.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>learn</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies if the security policy learns all requests that match a signature that is included in the signature set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the signature sets to apply on or remove from the ASM policy.</div>
                                                    <div>Apart from built-in signature sets that ship with the device, users can use user created signature sets.</div>
                                                    <div>When <code>All Response Signatures</code>, configures all signatures in the attack signature pool that can review responses.</div>
                                                    <div>When <code>All Signatures</code>, configures all attack signatures in the attack signature pool.</div>
                                                    <div>When <code>Apache Struts Signatures</code>, configures signatures that target attacks against the Apache Struts web servers. Only available in version 13.x and up.</div>
                                                    <div>When <code>Apache Tomcat Signatures</code>, configures signatures that target attacks against the Apache Tomcat web servers. Only available in version 13.x and up.</div>
                                                    <div>When <code>Cisco Signatures</code>, configures signatures that target attacks against Cisco systems. Only available in version 13.x and up.</div>
                                                    <div>When <code>Command Execution Signatures</code>, configures signatures involving attacks perpetrated by executing commands.</div>
                                                    <div>When <code>Cross Site Scripting Signatures</code>, configures signatures that target attacks caused by cross-site scripting techniques.</div>
                                                    <div>When <code>Directory Indexing Signatures</code>, configures signatures targeting attacks that browse directory listings.</div>
                                                    <div>When <code>Generic Detection Signatures</code>, configures signatures targeting well-known or common web and application attacks.</div>
                                                    <div>When <code>HTTP Response Splitting Signatures</code>, configures signatures targeting attacks that take advantage of responses for which input values have not been sanitized.</div>
                                                    <div>When <code>High Accuracy Detection Evasion Signatures</code>, configures signatures with a high level of accuracy that produce few false positives when identifying evasion attacks. Only available in version 13.x and up.</div>
                                                    <div>When <code>High Accuracy Signatures</code>, configures signatures with a high level of accuracy that produce few false positives when identifying evasion attacks.</div>
                                                    <div>When <code>IIS and Windows Signatures</code>, configures signatures that target attacks against IIS and Windows based systems. Only available in version 13.x and up.</div>
                                                    <div>When <code>Information Leakage Signatures</code>, configures signatures targeting attacks that are looking for system data or debugging information that shows where the system is vulnerable to attack.</div>
                                                    <div>When <code>Java Servlets/JSP Signatures</code>, configures signatures that target attacks against Java Servlets and Java Server Pages (JSP) based applications. Only available in version 13.x and up.</div>
                                                    <div>When <code>Low Accuracy Signatures</code>, configures signatures that may result in more false positives when identifying attacks.</div>
                                                    <div>When <code>Medium Accuracy Signatures</code>, configures signatures with a medium level of accuracy when identifying attacks.</div>
                                                    <div>When <code>OS Command Injection Signatures</code>, configures signatures targeting attacks that attempt to run system level commands through a vulnerable application.</div>
                                                    <div>When <code>OWA Signatures</code>, configures signatures that target attacks against the Microsoft Outlook Web Access (OWA) application.</div>
                                                    <div>When <code>Other Application Attacks Signatures</code>, configures signatures targeting miscellaneous attacks, including session fixation, local file access, injection attempts, header tampering and so on, affecting many applications.</div>
                                                    <div>When <code>Path Traversal Signatures</code>, configures signatures targeting attacks that attempt to access files and directories that are stored outside the web root folder.</div>
                                                    <div>When <code>Predictable Resource Location Signatures</code>, configures signatures targeting attacks that attempt to uncover hidden website content and functionality by forceful browsing, or by directory and file enumeration.</div>
                                                    <div>When <code>Remote File Include Signatures</code>, configures signatures targeting attacks that attempt to exploit a remote file include vulnerability that could enable a remote attacker to execute arbitrary commands on the server hosting the application.</div>
                                                    <div>When <code>SQL Injection Signatures</code>, configures signatures targeting attacks that attempt to insert (inject) a SQL query using the input data from a client to an application.</div>
                                                    <div>When <code>Server Side Code Injection Signatures</code>, configures signatures targeting code injection attacks on the server side.</div>
                                                    <div>When <code>WebSphere signatures</code>, configures signatures targeting attacks on many computing platforms that are integrated using WebSphere including general database, Microsoft Windows, IIS, Microsoft SQL Server, Apache, Oracle, Unix/Linux, IBM DB2, PostgreSQL, and XML.</div>
                                                    <div>When <code>XPath Injection Signatures</code>, configures signatures targeting attacks that attempt to gain access to data structures or bypass permissions when a web site uses user-supplied information to construct XPath queries for XML data.</div>
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
                                                                        <div>This parameter is only used when identifying ASM policy.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>policy_name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of an existing ASM policy to add or remove signature sets.</div>
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
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>present</code>, ensures that the resource exists.</div>
                                                    <div>When <code>absent</code>, ensures the resource is removed.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - This module is primarily used as a component of configuring ASM policy in Ansible Galaxy ASM Policy Role.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Add Signature Set to ASM Policy
      bigip_asm_policy_signature_set:
        name: IIS and Windows Signatures
        policy_name: FooPolicy
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost
    - name: Remove Signature Set to ASM Policy
      bigip_asm_policy_signature_set:
        name: IIS and Windows Signatures
        policy_name: FooPolicy
        state: absent
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
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
                    <b>alarm</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies whether the security policy logs the request data in the Statistics screen</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>block</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Determines how the system treats requests that match a signature included in the signature set</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>learn</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies if the policy learns all requests that match a signature that is included in the signature set</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of Signature Set added/removed on ASM policy</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Cisco Signatures</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>policy_name</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of the ASM policy</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">FooPolicy</div>
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

