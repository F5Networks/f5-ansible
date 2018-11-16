:source: bigip_imish_config.py

:orphan:

.. _bigip_imish_config_module:


bigip_imish_config - Manage BIG-IP advanced routing configuration sections
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- This module provides an implementation for working with advanced routing configuration sections in a deterministic way.




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
                    <b>after</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The ordered set of commands to append to the end of the command stack if a change needs to be made.</div>
                                                    <div>Just like with <em>before</em> this allows the playbook designer to append a set of commands to be executed after the command set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>backup</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This argument will cause the module to create a full backup of the current <code>running-config</code> from the remote device before any changes are made.</div>
                                                    <div>The backup file is written to the <code>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>before</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The ordered set of commands to push on to the command stack if a change needs to be made.</div>
                                                    <div>This allows the playbook designer the opportunity to perform configuration commands prior to pushing any changes without affecting how the set of commands are matched against the system.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>diff_against</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>startup</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>intended</li>
                                                                                                                                                                                                <li>running</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When using the <code>ansible-playbook --diff</code> command line argument the module can generate diffs against different sources.</div>
                                                    <div>When this option is configure as <em>startup</em>, the module will return the diff of the running-config against the startup-config.</div>
                                                    <div>When this option is configured as <em>intended</em>, the module will return the diff of the running-config against the configuration provided in the <code>intended_config</code> argument.</div>
                                                    <div>When this option is configured as <em>running</em>, the module will return the before and after diff of the running-config with respect to any changes made to the device configuration.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>diff_ignore_lines</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Use this argument to specify one or more lines that should be ignored during the diff.</div>
                                                    <div>This is used for lines in the configuration that are automatically updated by the system.</div>
                                                    <div>This argument takes a list of regular expressions or exact line matches.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>intended_config</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The <code>intended_config</code> provides the master configuration that the node should conform to and is used to check the final running-config against.</div>
                                                    <div>This argument will not modify any settings on the remote device and is strictly used to check the compliance of the current device&#x27;s configuration against.</div>
                                                    <div>When specifying this argument, the task should also modify the <code>diff_against</code> value and set it to <em>intended</em>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>lines</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The ordered set of commands that should be configured in the section.</div>
                                                    <div>The commands must be the exact same commands as found in the device running-config.</div>
                                                    <div>Be sure to note the configuration command syntax as some commands are automatically modified by the device config parser.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: commands</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>match</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>line</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>strict</li>
                                                                                                                                                                                                <li>exact</li>
                                                                                                                                                                                                <li>none</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Instructs the module on the way to perform the matching of the set of commands against the current device config.</div>
                                                    <div>If match is set to <em>line</em>, commands are matched line by line.</div>
                                                    <div>If match is set to <em>strict</em>, command lines are matched with respect to position.</div>
                                                    <div>If match is set to <em>exact</em>, command lines must be an equal match.</div>
                                                    <div>Finally, if match is set to <em>none</em>, the module will not attempt to compare the source configuration with the running configuration on the remote device.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>parents</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The ordered set of parents that uniquely identify the section or hierarchy the commands should be checked against.</div>
                                                    <div>If the <code>parents</code> argument is omitted, the commands are checked against the set of top level or global commands.</div>
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
                    <b>replace</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>line</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>block</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Instructs the module on the way to perform the configuration on the device.</div>
                                                    <div>If the replace argument is set to <em>line</em> then the modified lines are pushed to the device in configuration mode.</div>
                                                    <div>If the replace argument is set to <em>block</em> then the entire command block is pushed to the device in configuration mode if any line is not correct.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>running_config</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The module, by default, will connect to the remote device and retrieve the current running-config to use as a base for comparing against the contents of source.</div>
                                                    <div>There are times when it is not desirable to have the task get the current running-config for every task in a playbook.</div>
                                                    <div>The <em>running_config</em> argument allows the implementer to pass in the configuration to use as the base config for comparison.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: config</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>save_when</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>always</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>never</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>modified</li>
                                                                                                                                                                                                <li>changed</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When changes are made to the device running-configuration, the changes are not copied to non-volatile storage by default.</div>
                                                    <div>If the argument is set to <em>always</em>, then the running-config will always be copied to the startup-config and the <em>modified</em> flag will always be set to <code>True</code>.</div>
                                                    <div>If the argument is set to <em>modified</em>, then the running-config will only be copied to the startup-config if it has changed since the last save to startup-config.</div>
                                                    <div>If the argument is set to <em>never</em>, the running-config will never be copied to the startup-config.</div>
                                                    <div>If the argument is set to <em>changed</em>, then the running-config will only be copied to the startup-config if the task has made a change.</div>
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
                    <b>src</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The <em>src</em> argument provides a path to the configuration file to load into the remote system.</div>
                                                    <div>The path can either be a full system path to the configuration file if the value starts with / or relative to the root of the implemented role or playbook.</div>
                                                    <div>This argument is mutually exclusive with the <em>lines</em> and <em>parents</em> arguments.</div>
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
    - Abbreviated commands are NOT idempotent, see `Network FAQ <../network/user_guide/faq.html#why-do-the-config-modules-always-return-changed-true-with-abbreviated-commands>`_.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: configure top level configuration and save it
      bigip_imish_config:
        lines: bfd slow-timer 2000
        save_when: modified

    - name: diff the running-config against a provided config
      bigip_imish_config:
        diff_against: intended
        intended_config: "{{ lookup('file', 'master.cfg') }}"

    - name: Add config to a parent block
      bigip_imish_config:
        lines:
          - bgp graceful-restart restart-time 120
          - redistribute kernel route-map rhi
          - neighbor 10.10.10.11 remote-as 65000
          - neighbor 10.10.10.11 fall-over bfd
          - neighbor 10.10.10.11 remote-as 65000
          - neighbor 10.10.10.11 fall-over bfd
        parents: router bgp 64664
        match: exact

    - name: Remove an existing acl before writing it
      bigip_imish_config:
        lines:
          - access-list 10 permit 20.20.20.20
          - access-list 10 permit 20.20.20.21
          - access-list 10 deny any
        before: no access-list 10

    - name: for idempotency, use full-form commands
      bigip_imish_config:
        lines:
          # - desc My interface
          - description My Interface
        # parents: int ANYCAST-P2P-2
        parents: interface ANYCAST-P2P-2




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
                    <b>backup_path</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>when backup is yes</td>
                <td>
                                            <div>The full path to the backup file</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/playbooks/ansible/backup/bigip_imish_config.2016-07-16@22:28:34</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>commands</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>always</td>
                <td>
                                            <div>The set of commands that will be pushed to the remote device</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface ANYCAST-P2P-2&#x27;, &#x27;neighbor 20.20.20.21 remote-as 65000&#x27;, &#x27;neighbor 20.20.20.21 fall-over bfd&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>updates</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>always</td>
                <td>
                                            <div>The set of commands that will be pushed to the remote device</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface ANYCAST-P2P-2&#x27;, &#x27;neighbor 20.20.20.21 remote-as 65000&#x27;, &#x27;neighbor 20.20.20.21 fall-over bfd&#x27;]</div>
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

