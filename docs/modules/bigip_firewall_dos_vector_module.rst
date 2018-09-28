:source: bigip_firewall_dos_vector.py

:orphan:

.. _bigip_firewall_dos_vector_module:


bigip_firewall_dos_vector - Manage attack vector configuration in an AFM DoS profile
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage attack vector configuration in an AFM DoS profile. In addition to the normal AFM DoS profile vectors, this module can manage the device-configuration vectors. See the module documentation for details about this method.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- BIG-IP >= v13.0.0
- f5-sdk >= 3.0.16


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
                    <b>name</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>ext-hdr-too-large</li>
                                                                                                                                                                                                <li>hop-cnt-low</li>
                                                                                                                                                                                                <li>host-unreachable</li>
                                                                                                                                                                                                <li>icmp-frag</li>
                                                                                                                                                                                                <li>icmpv4-flood</li>
                                                                                                                                                                                                <li>icmpv6-flood</li>
                                                                                                                                                                                                <li>ip-frag-flood</li>
                                                                                                                                                                                                <li>ip-low-ttl</li>
                                                                                                                                                                                                <li>ip-opt-frames</li>
                                                                                                                                                                                                <li>ipv6-frag-flood</li>
                                                                                                                                                                                                <li>opt-present-with-illegal-len</li>
                                                                                                                                                                                                <li>sweep</li>
                                                                                                                                                                                                <li>tcp-bad-urg</li>
                                                                                                                                                                                                <li>tcp-half-open</li>
                                                                                                                                                                                                <li>tcp-opt-overruns-tcp-hdr</li>
                                                                                                                                                                                                <li>tcp-psh-flood</li>
                                                                                                                                                                                                <li>tcp-rst-flood</li>
                                                                                                                                                                                                <li>tcp-syn-flood</li>
                                                                                                                                                                                                <li>tcp-syn-oversize</li>
                                                                                                                                                                                                <li>tcp-synack-flood</li>
                                                                                                                                                                                                <li>tcp-window-size</li>
                                                                                                                                                                                                <li>tidcmp</li>
                                                                                                                                                                                                <li>too-many-ext-hdrs</li>
                                                                                                                                                                                                <li>udp-flood</li>
                                                                                                                                                                                                <li>unk-tcp-opt-type</li>
                                                                                                                                                                                                <li>a</li>
                                                                                                                                                                                                <li>aaaa</li>
                                                                                                                                                                                                <li>any</li>
                                                                                                                                                                                                <li>axfr</li>
                                                                                                                                                                                                <li>cname</li>
                                                                                                                                                                                                <li>dns-malformed</li>
                                                                                                                                                                                                <li>ixfr</li>
                                                                                                                                                                                                <li>mx</li>
                                                                                                                                                                                                <li>ns</li>
                                                                                                                                                                                                <li>other</li>
                                                                                                                                                                                                <li>ptr</li>
                                                                                                                                                                                                <li>qdcount</li>
                                                                                                                                                                                                <li>soa</li>
                                                                                                                                                                                                <li>srv</li>
                                                                                                                                                                                                <li>txt</li>
                                                                                                                                                                                                <li>ack</li>
                                                                                                                                                                                                <li>bye</li>
                                                                                                                                                                                                <li>cancel</li>
                                                                                                                                                                                                <li>invite</li>
                                                                                                                                                                                                <li>message</li>
                                                                                                                                                                                                <li>notify</li>
                                                                                                                                                                                                <li>options</li>
                                                                                                                                                                                                <li>other</li>
                                                                                                                                                                                                <li>prack</li>
                                                                                                                                                                                                <li>publish</li>
                                                                                                                                                                                                <li>register</li>
                                                                                                                                                                                                <li>sip-malformed</li>
                                                                                                                                                                                                <li>subscribe</li>
                                                                                                                                                                                                <li>uri-limit</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the vector to modify.</div>
                                                    <div>Vectors that ship with the device are &quot;hard-coded&quot; so-to-speak in that the list of vectors is known to the system and users cannot add new vectors. Users only manipulate the existing vectors; all of which are disabled by default.</div>
                                                    <div>When <code>ext-hdr-too-large</code>, configures the &quot;IPv6 extension header too large&quot; Network Security vector.</div>
                                                    <div>When <code>hop-cnt-low</code>, configures the &quot;IPv6 hop count &lt;= &lt;tunable&gt;&quot; Network Security vector.</div>
                                                    <div>When <code>host-unreachable</code>, configures the &quot;Host Unreachable&quot; Network Security vector.</div>
                                                    <div>When <code>icmp-frag</code>, configures the &quot;ICMP Fragment&quot; Network Security vector.</div>
                                                    <div>When <code>icmpv4-flood</code>, configures the &quot;ICMPv4 flood&quot; Network Security vector.</div>
                                                    <div>When <code>icmpv6-flood</code>, configures the &quot;ICMPv6 flood&quot; Network Security vector.</div>
                                                    <div>When <code>ip-frag-flood</code>, configures the &quot;IP Fragment Flood&quot; Network Security vector.</div>
                                                    <div>When <code>ip-low-ttl</code>, configures the &quot;TTL &lt;= &lt;tunable&gt;&quot; Network Security vector.</div>
                                                    <div>When <code>ip-opt-frames</code>, configures the &quot;IP Option Frames&quot; Network Security vector.</div>
                                                    <div>When <code>ipv6-ext-hdr-frames</code>, configures the &quot;IPv6 Extended Header Frames&quot; Network Security vector.</div>
                                                    <div>When <code>ipv6-frag-flood</code>, configures the &quot;IPv6 Fragment Flood&quot; Network Security vector.</div>
                                                    <div>When <code>opt-present-with-illegal-len</code>, configures the &quot;Option Present With Illegal Length&quot; Network Security vector.</div>
                                                    <div>When <code>sweep</code>, configures the &quot;Sweep&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-bad-urg</code>, configures the &quot;TCP Flags-Bad URG&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-half-open</code>, configures the &quot;TCP Half Open&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-opt-overruns-tcp-hdr</code>, configures the &quot;TCP Option Overruns TCP Header&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-psh-flood</code>, configures the &quot;TCP PUSH Flood&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-rst-flood</code>, configures the &quot;TCP RST Flood&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-syn-flood</code>, configures the &quot;TCP SYN Flood&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-syn-oversize</code>, configures the &quot;TCP SYN Oversize&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-synack-flood</code>, configures the &quot;TCP SYN ACK Flood&quot; Network Security vector.</div>
                                                    <div>When <code>tcp-window-size</code>, configures the &quot;TCP Window Size&quot; Network Security vector.</div>
                                                    <div>When <code>tidcmp</code>, configures the &quot;TIDCMP&quot; Network Security vector.</div>
                                                    <div>When <code>too-many-ext-hdrs</code>, configures the &quot;Too Many Extension Headers&quot; Network Security vector.</div>
                                                    <div>When <code>udp-flood</code>, configures the &quot;UDP Flood&quot; Network Security vector.</div>
                                                    <div>When <code>unk-tcp-opt-type</code>, configures the &quot;Unknown TCP Option Type&quot; Network Security vector.</div>
                                                    <div>When <code>a</code>, configures the &quot;DNS A Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>aaaa</code>, configures the &quot;DNS AAAA Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>any</code>, configures the &quot;DNS ANY Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>axfr</code>, configures the &quot;DNS AXFR Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>cname</code>, configures the &quot;DNS CNAME Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>dns-malformed</code>, configures the &quot;dns-malformed&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>ixfr</code>, configures the &quot;DNS IXFR Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>mx</code>, configures the &quot;DNS MX Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>ns</code>, configures the &quot;DNS NS Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>other</code>, configures the &quot;DNS OTHER Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>ptr</code>, configures the &quot;DNS PTR Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>qdcount</code>, configures the &quot;DNS QDCOUNT Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>soa</code>, configures the &quot;DNS SOA Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>srv</code>, configures the &quot;DNS SRV Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>txt</code>, configures the &quot;DNS TXT Query&quot; DNS Protocol Security vector.</div>
                                                    <div>When <code>ack</code>, configures the &quot;SIP ACK Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>bye</code>, configures the &quot;SIP BYE Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>cancel</code>, configures the &quot;SIP CANCEL Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>invite</code>, configures the &quot;SIP INVITE Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>message</code>, configures the &quot;SIP MESSAGE Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>notify</code>, configures the &quot;SIP NOTIFY Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>options</code>, configures the &quot;SIP OPTIONS Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>other</code>, configures the &quot;SIP OTHER Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>prack</code>, configures the &quot;SIP PRACK Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>publish</code>, configures the &quot;SIP PUBLISH Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>register</code>, configures the &quot;SIP REGISTER Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>sip-malformed</code>, configures the &quot;sip-malformed&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>subscribe</code>, configures the &quot;SIP SUBSCRIBE Method&quot; SIP Protocol Security vector.</div>
                                                    <div>When <code>uri-limit</code>, configures the &quot;uri-limit&quot; SIP Protocol Security vector.</div>
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
                    <b>profile</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the profile to manage vectors in.</div>
                                                    <div>The reserved name <code>device-config</code> represents the vec</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>provider</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
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
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Create a ...
      bigip_firewall_dos_vector:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
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
                    <b>param1</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new param1 value of the resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>param2</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new param2 value of the resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Foo is bar</div>
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

