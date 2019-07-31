:source: bigip_ipsec_policy.py

:orphan:

.. _bigip_ipsec_policy_module:


bigip_ipsec_policy - Manage IPSec policies on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage IPSec policies on a BIG-IP.




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
                    <b>auth_algorithm</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>sha1</li>
                                                                                                                                                                                                <li>sha256</li>
                                                                                                                                                                                                <li>sha384</li>
                                                                                                                                                                                                <li>sha512</li>
                                                                                                                                                                                                <li>aes-gcm128</li>
                                                                                                                                                                                                <li>aes-gcm192</li>
                                                                                                                                                                                                <li>aes-gcm256</li>
                                                                                                                                                                                                <li>aes-gmac128</li>
                                                                                                                                                                                                <li>aes-gmac192</li>
                                                                                                                                                                                                <li>aes-gmac256</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the algorithm to use for IKE authentication.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Description of the policy</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>encrypt_algorithm</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>none</li>
                                                                                                                                                                                                <li>3des</li>
                                                                                                                                                                                                <li>aes128</li>
                                                                                                                                                                                                <li>aes192</li>
                                                                                                                                                                                                <li>aes256</li>
                                                                                                                                                                                                <li>aes-gmac256</li>
                                                                                                                                                                                                <li>aes-gmac192</li>
                                                                                                                                                                                                <li>aes-gmac128</li>
                                                                                                                                                                                                <li>aes-gcm256</li>
                                                                                                                                                                                                <li>aes-gcm192</li>
                                                                                                                                                                                                <li>aes-gcm256</li>
                                                                                                                                                                                                <li>aes-gcm128</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the algorithm to use for IKE encryption.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ipcomp</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>none</li>
                                                                                                                                                                                                <li>null</li>
                                                                                                                                                                                                <li>deflate</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether to use IPComp encapsulation.</div>
                                                    <div>When <code>none</code>, specifies that IPComp is disabled.</div>
                                                    <div>When <code>deflate</code>, specifies that IPComp is enabled and uses the Deflate compression algorithm.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ipv4_interface</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.9)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>mode</code> is <code>interface</code> indicate if the IPv4 <code>any</code> address should be used. By default <code>BIG-IP</code> assumes <code>any6</code> address for tunnel addresses when <code>mode</code> is <code>interface</code>.</div>
                                                    <div>This option takes effect only when <code>mode</code> is set to <code>interface</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>kb_lifetime</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the length of time, in kilobytes, before the IKE security association expires.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>lifetime</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the length of time, in minutes, before the IKE security association expires.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>mode</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>transport</li>
                                                                                                                                                                                                <li>interface</li>
                                                                                                                                                                                                <li>isession</li>
                                                                                                                                                                                                <li>tunnel</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the processing mode.</div>
                                                    <div>When <code>transport</code>, specifies a mode that encapsulates only the payload (adding an ESP header, trailer, and authentication tag).</div>
                                                    <div>When <code>tunnel</code>, specifies a mode that includes encapsulation of the header as well as the payload (adding a new IP header, in addition to adding an ESP header, trailer, and authentication tag). If you select this option, you must also provide IP addresses for the local and remote endpoints of the IPsec tunnel.</div>
                                                    <div>When <code>isession</code>, specifies the use of iSession over an IPsec tunnel. To use this option, you must also configure the iSession endpoints with IPsec in the Acceleration section of the user interface.</div>
                                                    <div>When <code>interface</code>, specifies that the IPsec policy can be used in the tunnel profile for network interfaces.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the IPSec policy.</div>
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
                    <b>perfect_forward_secrecy</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>none</li>
                                                                                                                                                                                                <li>modp768</li>
                                                                                                                                                                                                <li>modp1024</li>
                                                                                                                                                                                                <li>modp1536</li>
                                                                                                                                                                                                <li>modp2048</li>
                                                                                                                                                                                                <li>modp3072</li>
                                                                                                                                                                                                <li>modp4096</li>
                                                                                                                                                                                                <li>modp6144</li>
                                                                                                                                                                                                <li>modp8192</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the Diffie-Hellman group to use for IKE Phase 2 negotiation.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>protocol</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>esp</li>
                                                                                                                                                                                                <li>ah</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the IPsec protocol</div>
                                                    <div>Options include ESP (Encapsulating Security Protocol) or AH (Authentication Header).</div>
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
                    <b>route_domain</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the route domain, when <code>interface</code> is selected for the <code>mode</code> setting.</div>
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
                                <tr>
                                                                <td colspan="2">
                    <b>tunnel_local_address</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the local endpoint IP address of the IPsec tunnel.</div>
                                                    <div>This parameter is only valid when <code>mode</code> is <code>tunnel</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>tunnel_remote_address</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the remote endpoint IP address of the IPsec tunnel.</div>
                                                    <div>This parameter is only valid when <code>mode</code> is <code>tunnel</code>.</div>
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

    
    - name: Create a IPSec policy
      bigip_ipsec_policy:
        name: policy1
        mode: tunnel
        tunnel_local_address: 1.1.1.1
        tunnel_remote_address: 2.2.2.
        auth_algorithm: sha1
        encrypt_algorithm: 3des
        protocol: esp
        perfect_forward_secrecy: modp1024
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
                    <b>auth_algorithm</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IKE Phase 2 Authentication Algorithm value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">sha512</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new description value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">My policy</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>encrypt_algorithm</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IKE Phase 2 Encryption Algorithm value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">aes256</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>ipcomp</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IKE Phase 2 IPComp value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">deflate</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>kb_lifetime</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IKE Phase 2 KB Lifetime value.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>lifetime</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IKE Phase 2 Lifetime value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1440</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>mode</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Mode value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">tunnel</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>perfect_forward_secrecy</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IKE Phase 2 Perfect Forward Secrecy value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">modp2048</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>protocol</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IPsec Protocol value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">ah</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>route_domain</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Route Domain value when in Tunnel mode.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>tunnel_local_address</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Tunnel Local Address value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1.2.2.1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>tunnel_remote_address</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Tunnel Remote Address value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2.1.1.2</div>
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

