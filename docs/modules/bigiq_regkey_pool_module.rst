:source: modules/bigiq_regkey_pool.py

.. _bigiq_regkey_pool:


bigiq_regkey_pool - Manages registration key pools on BIG-IQ
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages registration key (regkey) pools on a BIG-IQ. These pools function as a container in-which you will add lists of registration keys. To add registration keys, use the `bigiq_regkey_license` module.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- BIG-IQ >= 5.3.0
- f5-sdk >= 3.0.9


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
                            <b>description</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>A description to attach to the pool.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>name</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Specifies the name of the registration key pool.</div>
                                                            <div>You must be mindful to name your registration pools unique names. While BIG-IQ does not require this, this module does. If you do not do this, the behavior of the module is undefined and you may end up putting licenses in the wrong registration key pool.</div>
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
                            <b>state</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                                    <li>absent</li>
                                                                                                                                                                                                                        <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The state of the regkey pool on the system.</div>
                                                            <div>When <code>present</code>, guarantees that the pool exists.</div>
                                                            <div>When <code>absent</code>, removes the pool, and the licenses it contains, from the system.</div>
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
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as `pip install f5-sdk`.


Examples
--------

.. code-block:: yaml

    
    - name: Create a registration key (regkey) pool to hold individual device licenses
      bigiq_regkey_pool:
        name: foo-pool
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost




Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th class="head"><div class="cell-border">Key</div></th>
            <th class="head"><div class="cell-border">Returned</div></th>
            <th class="head" width="100%"><div class="cell-border">Description</div></th>
        </tr>
                    <tr class="return-value-column">
                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>description</b>
                            <br/><div style="font-size: small; color: red">string</div>
                        </div>
                    </div>
                </td>
                <td><div class="cell-border">changed</div></td>
                <td>
                    <div class="cell-border">
                                                    <div>New description of the regkey pool.</div>
                                                <br/>
                                                    <div style="font-size: smaller"><b>Sample:</b></div>
                                                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">My description</div>
                                            </div>
                </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

