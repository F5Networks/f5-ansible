:source: modules/bigip_device_facts.py

.. _bigip_device_facts:


bigip_device_facts - Collect facts from F5 BIG-IP devices
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.7

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Collect facts from F5 BIG-IP devices.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- f5-sdk >= 3.0.9
- netaddr


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                <tr>
            <th class="head"><div class="cell-border">Parameter</div></th>
            <th class="head"><div class="cell-border">Choices/<font color="blue">Defaults</font></div></th>
                        <th class="head" width="100%"><div class="cell-border">Comments</div></th>
        </tr>
                    <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>gather_subset</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                                    <li>internal-data-groups</li>
                                                                                                                                                                                                                        <li>client-ssl-profiles</li>
                                                                                                                                                                                                                        <li>fasthttp-profiles</li>
                                                                                                                                                                                                                        <li>devices</li>
                                                                                                                                                                                                                        <li>device-groups</li>
                                                                                                                                                                                                                        <li>interfaces</li>
                                                                                                                                                                                                                        <li>ssl-certs</li>
                                                                                                                                                                                                                        <li>ssl-keys</li>
                                                                                                                                                                                                                        <li>nodes</li>
                                                                                                                                                                                                                        <li>ltm-pools</li>
                                                                                                                                                                                                                        <li>provision-info</li>
                                                                                                                                                                                                                        <li>irules</li>
                                                                                                                                                                                                                        <li>self-ips</li>
                                                                                                                                                                                                                        <li>software-volumes</li>
                                                                                                                                                                                                                        <li>system-info</li>
                                                                                                                                                                                                                        <li>traffic-groups</li>
                                                                                                                                                                                                                        <li>trunks</li>
                                                                                                                                                                                                                        <li>virtual-addresses</li>
                                                                                                                                                                                                                        <li>virtual-servers</li>
                                                                                                                                                                                                                        <li>vlans</li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>When supplied, this argument will restrict the facts returned to a given subset.</div>
                                                            <div>Can specify a list of values to include a larger subset.</div>
                                                            <div>Values can also be used with an initial <code>!</code> to specify that a specific subset should not be collected.</div>
                                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: include</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>password</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>provider</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>A dict object containing connection details.</div>
                                                                                                </div>
                </td>
            </tr>
                                                            <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>password</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                            </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>server</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>server_port</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">443</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>user</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>validate_certs</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                                    <li>no</li>
                                                                                                                                                                                                                        <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>timeout</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">10</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>ssh_keyfile</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                    <div class="elbow-placeholder">&nbsp;</div>
                                                <div class="elbow-key">
                            <b>transport</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                                    <li>rest</li>
                                                                                                                                                                                                                        <li><div style="color: blue"><b>cli</b>&nbsp;&larr;</div></li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                                </div>
                </td>
            </tr>
                    
                                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>server</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>server_port</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">443</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>user</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>validate_certs</b>
                                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.0)</div>                        </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                                    <li>no</li>
                                                                                                                                                                                                                        <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                                </div>
                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as `pip install f5-sdk`.


Examples
--------

.. code-block:: yaml

    
    - name: Collect BIG-IP facts
      bigip_facts:
        server: lb.mydomain.com
        user: admin
        password: secret
        gather_subset:
          - interface
          - vlans
      delegate_to: localhost

    - name: Collect all BIG-IP facts
      bigip_facts:
        server: lb.mydomain.com
        user: admin
        password: secret
        gather_subset:
          - all
      delegate_to: localhost

    - name: Collect all BIG-IP facts except trunks
      bigip_facts:
        server: lb.mydomain.com
        user: admin
        password: secret
        gather_subset:
          - all
          - "!trunks"
      delegate_to: localhost





Status
------



This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

