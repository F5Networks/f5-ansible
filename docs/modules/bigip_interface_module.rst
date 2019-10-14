:source: bigip_interface.py

:orphan:

.. _bigip_interface_module:


bigip_interface - Module to manage BIG-IP physical interfaces.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.1

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Module to manage BIG-IP physical interfaces.




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
                    <b>bundle</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>not-supported</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables or disables bundle capability.</div>
                                                    <div>This option is only supported on selected hardware platforms and interfaces.</div>
                                                    <div>Attempting to enable this option on a <code>VE</code> or any other unsupported platform/interface will result in module run failure.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>bundle_speed</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>100G</li>
                                                                                                                                                                                                <li>40G</li>
                                                                                                                                                                                                <li>not-supported</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Sets the bundle speed, the setting is applicable only when the bundle is <code>yes</code>.</div>
                                                    <div>This option is only supported on selected hardware platforms and interfaces.</div>
                                                    <div>Attempting to enable this option on a <code>VE</code> or any other unsupported platform/interface will result in module run failure.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>User defined description.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the current status of the interface.</div>
                                                    <div>When <code>yes</code> enables the interface to pass traffic.</div>
                                                    <div>When <code>no</code> disables the interface from passing traffic.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>flow_control</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>none</li>
                                                                                                                                                                                                <li>rx</li>
                                                                                                                                                                                                <li>tx</li>
                                                                                                                                                                                                <li>tx-rx</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies how the system controls the sending of PAUSE frames.</div>
                                                    <div>When <code>tx-rx</code> the interface honors pause frames from its partner, and also generates pause frames when necessary.</div>
                                                    <div>When <code>tx</code> the interface ignores pause frames from its partner, and generates pause frames when necessary.</div>
                                                    <div>When <code>rx</code> the interface honors pause frames from its partner, but does not generate pause frames.</div>
                                                    <div>When (none) the flow control is disabled on the interface.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>force_gigabit_fiber</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables or disables forcing of gigabit fiber media.</div>
                                                    <div>When <code>yes</code> for a gigabit fiber interface, the media setting will be forced, and no auto-negotiation will be performed.</div>
                                                    <div>When <code>no</code> auto-negotiation will be performed with just a single gigabit fiber option advertised.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>forward_error_correction</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>not-supported</li>
                                                                                                                                                                                                <li>auto</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables or disables IEEE 802.3bm Clause 91 Reed-Solomon Forward Error Correction on 100G interfaces. Not valid for LR4 media.</div>
                                                    <div>This option is only supported on selected hardware platforms and interfaces.</div>
                                                    <div>Attempting to enable this option on a <code>VE</code> or any other unsupported platform/interface will result in module run failure.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>lldp_admin</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>disable</li>
                                                                                                                                                                                                <li>rxonly</li>
                                                                                                                                                                                                <li>txonly</li>
                                                                                                                                                                                                <li>txrx</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies LLDP settings on an interface level.</div>
                                                    <div>When <code>disabled</code> the interface neither transmits (sends) LLDP messages to nor receives LLDP messages from neighboring devices.</div>
                                                    <div>When <code>txonly</code> the interface transmits LLDP messages to neighbor devices but does not receive LLDP messages from neighbor devices.</div>
                                                    <div>When <code>rxonly</code> the interface receives LLDP messages from neighbor devices but does not transmit LLDP messages to neighbor devices.</div>
                                                    <div>When <code>txrx</code> the interface transmits LLDP messages to and receives LLDP messages from neighboring devices.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>lldp_tlvmap</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the content of an LLDP message being sent or received.</div>
                                                    <div>Each LLDP attribute that is specified with this setting is optional and is in the form of Type, Length, Value (TLV).</div>
                                                    <div>The three mandatory TLVs not taken into account when calculating this value are: <code>Chassis ID</code>, <code>Port ID</code>, and <code>TTL</code>.</div>
                                                    <div>The optional attributes that are possible to specify have a specific TLV numeric value mapped to them.</div>
                                                    <div>The <code>Port Description</code> attribute has a TLV value of <code>8</code>.</div>
                                                    <div>The <code>System Name</code> attribute has a TLV value of <code>16</code>.</div>
                                                    <div>The <code>System Description</code> attribute has a TLV value of <code>32</code>.</div>
                                                    <div>The <code>System Capabilities</code> attribute has a TLV value of <code>64</code>.</div>
                                                    <div>The <code>Management Address</code> attribute has a TLV value of <code>128</code>.</div>
                                                    <div>The <code>Port VLAN ID</code> attribute has a TLV value of <code>256</code>.</div>
                                                    <div>The <code>VLAN Name</code> attribute has a TLV value of <code>512</code>.</div>
                                                    <div>The <code>Port and Protocol VLAN ID</code> attribute has a TLV value of <code>1024</code>.</div>
                                                    <div>The <code>Protocol Identity</code> attribute has a TLV value of <code>2048</code>.</div>
                                                    <div>The <code>MAC/PHY Config Status</code> attribute has a TLV value of <code>4096</code>.</div>
                                                    <div>The <code>Link Aggregation</code> attribute has a TLV value of <code>8192</code>.</div>
                                                    <div>The <code>Max Frame Size</code> attribute has a TLV value of <code>32768</code>.</div>
                                                    <div>The <code>Product Model</code> attribute has a TLV value of <code>65536</code>.</div>
                                                    <div>The <code>lldp_tlvmap</code> is a numeric value that is a sum of all TLV values of selected attributes.</div>
                                                    <div>Setting <code>lldp_tlvmap</code> to <code>0</code> will remove all attributes from the interface.</div>
                                                    <div>Setting <code>lldp_tlvmap</code> to <code>114680</code> will add all attributes to the interface.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>media_fixed</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>100000-FD</li>
                                                                                                                                                                                                <li>100000LR4-FD</li>
                                                                                                                                                                                                <li>10000LR-FD</li>
                                                                                                                                                                                                <li>10000T-FD</li>
                                                                                                                                                                                                <li>1000SX-FD</li>
                                                                                                                                                                                                <li>100TX-FD</li>
                                                                                                                                                                                                <li>10T-HD</li>
                                                                                                                                                                                                <li>20000-FD</li>
                                                                                                                                                                                                <li>40000LR4-FD</li>
                                                                                                                                                                                                <li>100000AR4-FD</li>
                                                                                                                                                                                                <li>100000SR4-FD</li>
                                                                                                                                                                                                <li>10000SFPCU-FD</li>
                                                                                                                                                                                                <li>1000CX-FD</li>
                                                                                                                                                                                                <li>1000T-FD</li>
                                                                                                                                                                                                <li>100TX-HD</li>
                                                                                                                                                                                                <li>12000-FD</li>
                                                                                                                                                                                                <li>21000-FD</li>
                                                                                                                                                                                                <li>40000SR4-FD</li>
                                                                                                                                                                                                <li>100000CR4-FD</li>
                                                                                                                                                                                                <li>10000ER-FD</li>
                                                                                                                                                                                                <li>10000SR-FD</li>
                                                                                                                                                                                                <li>1000LX-FD</li>
                                                                                                                                                                                                <li>1000T-HD</li>
                                                                                                                                                                                                <li>10T-FD</li>
                                                                                                                                                                                                <li>16000-FD</li>
                                                                                                                                                                                                <li>40000-FD</li>
                                                                                                                                                                                                <li>42000-FD</li>
                                                                                                                                                                                                <li>auto</li>
                                                                                                                                                                                                <li>no-phy</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the settings for a fixed (non-pluggable) interface.</div>
                                                    <div>Use this option only with a combo port to specify the media type for the fixed interface, when it is not the preferred port.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>media_sfp</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>100000-FD</li>
                                                                                                                                                                                                <li>100000LR4-FD</li>
                                                                                                                                                                                                <li>10000LR-FD</li>
                                                                                                                                                                                                <li>10000T-FD</li>
                                                                                                                                                                                                <li>1000SX-FD</li>
                                                                                                                                                                                                <li>100TX-FD</li>
                                                                                                                                                                                                <li>10T-HD</li>
                                                                                                                                                                                                <li>20000-FD</li>
                                                                                                                                                                                                <li>40000LR4-FD</li>
                                                                                                                                                                                                <li>100000AR4-FD</li>
                                                                                                                                                                                                <li>100000SR4-FD</li>
                                                                                                                                                                                                <li>10000SFPCU-FD</li>
                                                                                                                                                                                                <li>1000CX-FD</li>
                                                                                                                                                                                                <li>1000T-FD</li>
                                                                                                                                                                                                <li>100TX-HD</li>
                                                                                                                                                                                                <li>12000-FD</li>
                                                                                                                                                                                                <li>21000-FD</li>
                                                                                                                                                                                                <li>40000SR4-FD</li>
                                                                                                                                                                                                <li>100000CR4-FD</li>
                                                                                                                                                                                                <li>10000ER-FD</li>
                                                                                                                                                                                                <li>10000SR-FD</li>
                                                                                                                                                                                                <li>1000LX-FD</li>
                                                                                                                                                                                                <li>1000T-HD</li>
                                                                                                                                                                                                <li>10T-FD</li>
                                                                                                                                                                                                <li>16000-FD</li>
                                                                                                                                                                                                <li>40000-FD</li>
                                                                                                                                                                                                <li>42000-FD</li>
                                                                                                                                                                                                <li>auto</li>
                                                                                                                                                                                                <li>no-phy</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the settings for an SFP (pluggable) interface.</div>
                                                    <div>Use this option only with a combo port to specify the media type for the SFP interface, when it is not the preferred port.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the interface to manage.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>port_fwd_mode</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>l3</li>
                                                                                                                                                                                                <li>passive</li>
                                                                                                                                                                                                <li>virtual-wire</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the operation mode.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>prefer_port</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>sfp</li>
                                                                                                                                                                                                <li>fixed</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Indicates which side of a combo port the interface uses, if both sides have the potential for an external link.</div>
                                                    <div>The default value for a combo port is sfp. Do not use this option for non-combo ports.</div>
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
                    <b>sflow</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies sFlow settings for the interface.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>poll_interval</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the maximum interval in seconds between two pollings.</div>
                                                    <div>For this setting to take effect, <code>poll_interval_global</code> must be set to <code>no</code>.</div>
                                                    <div>The valid range is 0 - 4294967295.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>poll_interval_global</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the global interface <code>poll_interval</code> setting overrides the object-level <code>poll_interval</code> setting.</div>
                                                    <div>When <code>yes</code> the <code>poll_interval</code> setting does not take effect.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>stp</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables or disables STP.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>stp_auto_edge_port</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Sets STP automatic edge port detection for the interface.</div>
                                                    <div>When <code>yes</code> the system monitors the interface for incoming STP, RSTP, or MSTP packets. If no such packets are received for a sufficient period of time (about three seconds), the interface is automatically given edge port status.</div>
                                                    <div>When <code>no</code>, the system never gives the interface edge port status automatically. Any STP setting set on a per-interface basis applies to all spanning tree instances.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>stp_edge_port</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the interface connects to an end station instead of another spanning tree bridge.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>stp_link_type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>auto</li>
                                                                                                                                                                                                <li>p2p</li>
                                                                                                                                                                                                <li>shared</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the STP link type for the interface.</div>
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

    
    - name: Update Interface Settings
      bigip_interface:
        name: 1.1
        stp: yes
        stp_auto_edge_port: no
        stp_edge_port: yes
        stp_link_type: shared
        description: my description
        flow_control: tx
        lldp_admin: txrx
        lldp_tlvmap: 8
        force_gigabit_fiber: no
        sflow:
          - poll_interval: 10
          - poll_interval_global: no
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Disable Interface
      bigip_interface:
        name: 1.1
        enabled: no
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Change sflow interface settings
      bigip_interface:
        name: 1.1
        sflow:
          - poll_interval: 0
          - poll_interval_global: yes
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
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="2">
                    <b>bundle</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables or disables bundle capability.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">not-supported</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>bundle_speed</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The bundle speed.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">100G</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>User defined description.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">my description</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The current status of the interface.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>flow_control</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies how the system controls the sending of PAUSE frames.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">tx</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>force_gigabit_fiber</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables or disables forcing of gigabit fiber media.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>forward_error_correction</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables or disables Forward Error Correction.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">auto</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>lldp_admin</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The LLDP settings on an interface level.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">txrx</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>lldp_tlvmap</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The content of an LLDP message being sent or received.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">136</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>media_fixed</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The settings for a fixed interface.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">100000-FD</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>media_sfp</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The settings for a SFP interface.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">100000-FD</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>port_fwd_mode</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The operation mode.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">passive</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>prefer_port</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The side of a combo port the interface uses.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">fixed</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>sflow</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies sFlow settings for the interface.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>poll_interval_global</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The global sFlow settings override.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>poll_interval</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The maximum interval in seconds between two pollings.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">128</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>stp</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enables or disables STP.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>stp_auto_edge_port</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Sets STP automatic edge port detection for the interface.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>stp_edge_port</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Specifies whether the interface connects to an end station instead of another spanning tree bridge.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>stp_link_type</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The STP link type for the interface.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">shared</div>
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

