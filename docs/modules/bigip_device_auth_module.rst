:source: bigip_device_auth.py

:orphan:

.. _bigip_device_auth_module:


bigip_device_auth - Manage system authentication on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.7

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage the system authentication configuration. This module can assist in configuring a number of different system authentication types. Note that this module can not be used to configure APM authentication types.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- f5-sdk >= 3.0.9


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
                    <b>authentication</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>use-first-server</li>
                                                                                                                                                                                                <li>use-all-servers</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the process the system employs when sending authentication requests.</div>
                                                    <div>When <code>use-first-server</code>, specifies that the system sends authentication attempts to only the first server in the list.</div>
                                                    <div>When <code>use-all-servers</code>, specifies that the system sends an authentication request to each server until authentication succeeds, or until the system has sent a request to all servers in the list.</div>
                                                    <div>This parameter is supported by the <code>tacacs</code> type.</div>
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
                    <b>protocol_name</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>lcp</li>
                                                                                                                                                                                                <li>ip</li>
                                                                                                                                                                                                <li>ipx</li>
                                                                                                                                                                                                <li>atalk</li>
                                                                                                                                                                                                <li>vines</li>
                                                                                                                                                                                                <li>lat</li>
                                                                                                                                                                                                <li>xremote</li>
                                                                                                                                                                                                <li>tn3270</li>
                                                                                                                                                                                                <li>telnet</li>
                                                                                                                                                                                                <li>rlogin</li>
                                                                                                                                                                                                <li>pad</li>
                                                                                                                                                                                                <li>vpdn</li>
                                                                                                                                                                                                <li>ftp</li>
                                                                                                                                                                                                <li>http</li>
                                                                                                                                                                                                <li>deccp</li>
                                                                                                                                                                                                <li>osicp</li>
                                                                                                                                                                                                <li>unknown</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the protocol associated with the value specified in <code>service_name</code>, which is a subset of the associated service being used for client authorization or system accounting.</div>
                                                    <div>Note that the majority of TACACS+ implementations are of protocol type <code>ip</code>, so try that first.</div>
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
                    <b>secret</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Secret key used to encrypt and decrypt packets sent or received from the server.</div>
                                                    <div><b>Do not</b> use the pound/hash sign in the secret for TACACS+ servers.</div>
                                                    <div>When configuring TACACS+ auth for the first time, this value is required.</div>
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
                    <b>servers</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a list of the IPv4 addresses for servers using the Terminal Access Controller Access System (TACACS)+ protocol with which the system communicates to obtain authorization data.</div>
                                                    <div>For each address, an alternate TCP port number may be optionally specified by specifying the <code>port</code> key.</div>
                                                    <div>If no port number is specified, the default port <code>49163</code> is used.</div>
                                                    <div>This parameter is supported by the <code>tacacs</code> type.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>address</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The IP address of the server.</div>
                                                    <div>This field is required, unless you are specifying a simple list of servers. In that case, the simple list can specify server IPs. See examples for more clarification.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>port</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">49163</div>
                                    </td>
                                                                <td>
                                                                        <div>The port of the server.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>service_name</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>slip</li>
                                                                                                                                                                                                <li>ppp</li>
                                                                                                                                                                                                <li>arap</li>
                                                                                                                                                                                                <li>shell</li>
                                                                                                                                                                                                <li>tty-daemon</li>
                                                                                                                                                                                                <li>connection</li>
                                                                                                                                                                                                <li>system</li>
                                                                                                                                                                                                <li>firewall</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the service that the user is requesting to be authorized to use.</div>
                                                    <div>Identifying what the user is asking to be authorized for, enables the TACACS+ server to behave differently for different types of authorization requests.</div>
                                                    <div>When configuring this form of system authentication, this setting is required.</div>
                                                    <div>Note that the majority of TACACS+ implementations are of service type <code>ppp</code>, so try that first.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The state of the authentication configuration on the system.</div>
                                                    <div>When <code>present</code>, guarantees that the system is configured for the specified <code>type</code>.</div>
                                                    <div>When <code>absent</code>, sets the system auth source back to <code>local</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>tacacs</li>
                                                                                                                                                                                                <li>local</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The authentication type to manage with this module.</div>
                                                    <div>Take special note that the parameters supported by this module will vary depending on the <code>type</code> that you are configuring.</div>
                                                    <div>This module only supports a subset, at this time, of the total available auth types.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>update_secret</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>always</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>on_create</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div><code>always</code> will allow to update secrets if the user chooses to do so.</div>
                                                    <div><code>on_create</code> will only set the secret when a <code>use_auth_source</code> is <code>yes</code> and TACACS+ is not currently the auth source.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>use_for_auth</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether or not this auth source is put in use on the system.</div>
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
                        </table>
    <br/>


Notes
-----

.. note::
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.


Examples
--------

.. code-block:: yaml

    
    - name: Set the system auth to TACACS+, default server port
      bigip_device_auth:
        type: tacacs
        authentication: use-all-servers
        protocol_name: ip
        secret: secret
        servers:
          - 10.10.10.10
          - 10.10.10.11
        service_name: ppp
        state: present
        use_for_auth: yes
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Set the system auth to TACACS+, override server port
      bigip_device_auth:
        type: tacacs
        authentication: use-all-servers
        protocol_name: ip
        secret: secret
        servers:
          - address: 10.10.10.10
            port: 1234
          - 10.10.10.11
        service_name: ppp
        use_for_auth: yes
        state: present
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
                    <b>authentication</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Process the system uses to serve authentication requests when using TACACS.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">use-all-servers</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>protocol_name</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Name of the protocol associated with <code>service_name</code> used for client authentication.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">ip</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>servers</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>List of servers used in TACACS authentication.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;1.2.2.1&#x27;, &#x27;4.5.5.4&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>service_name</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Name of the service the user is requesting to be authorized to use.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">ppp</div>
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

