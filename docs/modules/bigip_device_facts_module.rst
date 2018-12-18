:source: bigip_device_facts.py

:orphan:

.. _bigip_device_facts_module:


bigip_device_facts - Collect facts from F5 BIG-IP devices
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.7

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Collect facts from F5 BIG-IP devices.




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
                    <b>gather_subset</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>all</li>
                                                                                                                                                                                                <li>monitors</li>
                                                                                                                                                                                                <li>profiles</li>
                                                                                                                                                                                                <li>asm-policy-stats</li>
                                                                                                                                                                                                <li>asm-policies</li>
                                                                                                                                                                                                <li>asm-server-technologies</li>
                                                                                                                                                                                                <li>asm-signature-sets</li>
                                                                                                                                                                                                <li>client-ssl-profiles</li>
                                                                                                                                                                                                <li>devices</li>
                                                                                                                                                                                                <li>device-groups</li>
                                                                                                                                                                                                <li>external-monitors</li>
                                                                                                                                                                                                <li>fasthttp-profiles</li>
                                                                                                                                                                                                <li>fastl4-profiles</li>
                                                                                                                                                                                                <li>gateway-icmp-monitors</li>
                                                                                                                                                                                                <li>gtm-pools</li>
                                                                                                                                                                                                <li>gtm-servers</li>
                                                                                                                                                                                                <li>gtm-wide-ips</li>
                                                                                                                                                                                                <li>gtm-a-pools</li>
                                                                                                                                                                                                <li>gtm-a-wide-ips</li>
                                                                                                                                                                                                <li>gtm-aaaa-pools</li>
                                                                                                                                                                                                <li>gtm-aaaa-wide-ips</li>
                                                                                                                                                                                                <li>gtm-cname-pools</li>
                                                                                                                                                                                                <li>gtm-cname-wide-ips</li>
                                                                                                                                                                                                <li>gtm-mx-pools</li>
                                                                                                                                                                                                <li>gtm-mx-wide-ips</li>
                                                                                                                                                                                                <li>gtm-naptr-pools</li>
                                                                                                                                                                                                <li>gtm-naptr-wide-ips</li>
                                                                                                                                                                                                <li>gtm-srv-pools</li>
                                                                                                                                                                                                <li>gtm-srv-wide-ips</li>
                                                                                                                                                                                                <li>http-monitors</li>
                                                                                                                                                                                                <li>https-monitors</li>
                                                                                                                                                                                                <li>http-profiles</li>
                                                                                                                                                                                                <li>iapp-services</li>
                                                                                                                                                                                                <li>iapplx-packages</li>
                                                                                                                                                                                                <li>icmp-monitors</li>
                                                                                                                                                                                                <li>interfaces</li>
                                                                                                                                                                                                <li>internal-data-groups</li>
                                                                                                                                                                                                <li>irules</li>
                                                                                                                                                                                                <li>ltm-pools</li>
                                                                                                                                                                                                <li>nodes</li>
                                                                                                                                                                                                <li>oneconnect-profiles</li>
                                                                                                                                                                                                <li>partitions</li>
                                                                                                                                                                                                <li>provision-info</li>
                                                                                                                                                                                                <li>self-ips</li>
                                                                                                                                                                                                <li>server-ssl-profiles</li>
                                                                                                                                                                                                <li>software-volumes</li>
                                                                                                                                                                                                <li>software-images</li>
                                                                                                                                                                                                <li>software-hotfixes</li>
                                                                                                                                                                                                <li>ssl-certs</li>
                                                                                                                                                                                                <li>ssl-keys</li>
                                                                                                                                                                                                <li>system-db</li>
                                                                                                                                                                                                <li>system-info</li>
                                                                                                                                                                                                <li>tcp-monitors</li>
                                                                                                                                                                                                <li>tcp-half-open-monitors</li>
                                                                                                                                                                                                <li>tcp-profiles</li>
                                                                                                                                                                                                <li>traffic-groups</li>
                                                                                                                                                                                                <li>trunks</li>
                                                                                                                                                                                                <li>udp-profiles</li>
                                                                                                                                                                                                <li>vcmp-guests</li>
                                                                                                                                                                                                <li>virtual-addresses</li>
                                                                                                                                                                                                <li>virtual-servers</li>
                                                                                                                                                                                                <li>vlans</li>
                                                                                                                                                                                                <li>!all</li>
                                                                                                                                                                                                <li>!monitors</li>
                                                                                                                                                                                                <li>!profiles</li>
                                                                                                                                                                                                <li>!asm-policy-stats</li>
                                                                                                                                                                                                <li>!asm-policies</li>
                                                                                                                                                                                                <li>!asm-server-technologies</li>
                                                                                                                                                                                                <li>!asm-signature-sets</li>
                                                                                                                                                                                                <li>!client-ssl-profiles</li>
                                                                                                                                                                                                <li>!devices</li>
                                                                                                                                                                                                <li>!device-groups</li>
                                                                                                                                                                                                <li>!external-monitors</li>
                                                                                                                                                                                                <li>!fasthttp-profiles</li>
                                                                                                                                                                                                <li>!fastl4-profiles</li>
                                                                                                                                                                                                <li>!gateway-icmp-monitors</li>
                                                                                                                                                                                                <li>!gtm-pools</li>
                                                                                                                                                                                                <li>!gtm-servers</li>
                                                                                                                                                                                                <li>!gtm-wide-ips</li>
                                                                                                                                                                                                <li>!gtm-a-pools</li>
                                                                                                                                                                                                <li>!gtm-a-wide-ips</li>
                                                                                                                                                                                                <li>!gtm-aaaa-pools</li>
                                                                                                                                                                                                <li>!gtm-aaaa-wide-ips</li>
                                                                                                                                                                                                <li>!gtm-cname-pools</li>
                                                                                                                                                                                                <li>!gtm-cname-wide-ips</li>
                                                                                                                                                                                                <li>!gtm-mx-pools</li>
                                                                                                                                                                                                <li>!gtm-mx-wide-ips</li>
                                                                                                                                                                                                <li>!gtm-naptr-pools</li>
                                                                                                                                                                                                <li>!gtm-naptr-wide-ips</li>
                                                                                                                                                                                                <li>!gtm-srv-pools</li>
                                                                                                                                                                                                <li>!gtm-srv-wide-ips</li>
                                                                                                                                                                                                <li>!http-monitors</li>
                                                                                                                                                                                                <li>!https-monitors</li>
                                                                                                                                                                                                <li>!http-profiles</li>
                                                                                                                                                                                                <li>!iapp-services</li>
                                                                                                                                                                                                <li>!iapplx-packages</li>
                                                                                                                                                                                                <li>!icmp-monitors</li>
                                                                                                                                                                                                <li>!interfaces</li>
                                                                                                                                                                                                <li>!internal-data-groups</li>
                                                                                                                                                                                                <li>!irules</li>
                                                                                                                                                                                                <li>!ltm-pools</li>
                                                                                                                                                                                                <li>!nodes</li>
                                                                                                                                                                                                <li>!oneconnect-profiles</li>
                                                                                                                                                                                                <li>!partitions</li>
                                                                                                                                                                                                <li>!provision-info</li>
                                                                                                                                                                                                <li>!self-ips</li>
                                                                                                                                                                                                <li>!server-ssl-profiles</li>
                                                                                                                                                                                                <li>!software-volumes</li>
                                                                                                                                                                                                <li>!software-images</li>
                                                                                                                                                                                                <li>!software-hotfixes</li>
                                                                                                                                                                                                <li>!ssl-certs</li>
                                                                                                                                                                                                <li>!ssl-keys</li>
                                                                                                                                                                                                <li>!system-db</li>
                                                                                                                                                                                                <li>!system-info</li>
                                                                                                                                                                                                <li>!tcp-monitors</li>
                                                                                                                                                                                                <li>!tcp-half-open-monitors</li>
                                                                                                                                                                                                <li>!tcp-profiles</li>
                                                                                                                                                                                                <li>!traffic-groups</li>
                                                                                                                                                                                                <li>!trunks</li>
                                                                                                                                                                                                <li>!udp-profiles</li>
                                                                                                                                                                                                <li>!vcmp-guests</li>
                                                                                                                                                                                                <li>!virtual-addresses</li>
                                                                                                                                                                                                <li>!virtual-servers</li>
                                                                                                                                                                                                <li>!vlans</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When supplied, this argument will restrict the facts returned to a given subset.</div>
                                                    <div>Can specify a list of values to include a larger subset.</div>
                                                    <div>Values can also be used with an initial <code>!</code> to specify that a specific subset should not be collected.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: include</div>
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
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>rest</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>cli</li>
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
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Collect BIG-IP facts
      bigip_device_facts:
        gather_subset:
          - interfaces
          - vlans
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Collect all BIG-IP facts
      bigip_device_facts:
        gather_subset:
          - all
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Collect all BIG-IP facts except trunks
      bigip_device_facts:
        gather_subset:
          - all
          - "!trunks"
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost





Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)
- Wojciech Wypior (@wojtek0806)

