.. _iworkflow_local_connector_node:


iworkflow_local_connector_node - Manages L2/L3 configuration of a BIG-IP via iWorkflow
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages L2/L3 configuration of a BIG-IP via iWorkflow. This module is useful in the event that you have a new BIG-IP that does not yet have VLANs and Self-IPs configured on it. You can use this module on a discovered, managed, device to configure those settings via iWorkflow. You **do not** need touse this module if you have an existing BIG-IP that has its L2/L3 configuration already complete. In that cae, it is sufficient to just use the ``iworkflow_managed_device`` module and iWorkflow will automatically discover the node information for you.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9
  * iWorkflow >= 2.1.0


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                <tr><td>connector<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the local connector to add the device(s) to.</div>        </td></tr>
                <tr><td>device<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Managed device to create node for.</div>        </td></tr>
                <tr><td>device_root_password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>If the <code>username_credential</code> is <code>root</code> but the <code>password_credential</code> is not the password of the root user, then this value should be provided. This parameter is only relevant when creating new nodes.</div>        </td></tr>
                <tr><td>hostname<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The hostname that you want to set on the remote managed BIG-IP.</div>        </td></tr>
                <tr><td>interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A list of network interface configuration details that iWorkflow should apply to the remote BIG-IP. This list must include the following keys; <code>local_address</code>, <code>subnet_address</code>. Also, optionally, the following keys can be provided <code>gateway_address</code>, <code>name</code>. One final key, <code>virtual_address</code>, can be provided in the event that the cloud provider you are configuring the device on sets a public IP address that forwards traffic to a NAT&#x27;d private address. <code>virtual_address</code> can be used in cases such as Azure public IPs, AWS Elastic IP paired with an ENI primary address, and OpenStack&#x27;s Floating IP. The first item in the list is <b>always</b> the management interface of the BIG-IP. All remaining items in the list apply to the interfaces in ascending order that they appear on the device (eth1, eth2, etc). This parameter is only required when <code>state</code> is <code>present</code>.</div>        </td></tr>
                <tr><td>key_content<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Private key content to use when iWorkflow attempts to communicate with the remote device. If your remote BIG-IP requires key based authentication (for example it is located in a public cloud), you can provide that value here. Either one of <code>key_src</code>, <code>key_content</code>, or <code>username_credential</code> must be provided.</div>        </td></tr>
                <tr><td>key_src<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Private key to use when iWorkflow attempts to communicate with the remote device. If your remote BIG-IP requires key based authentication (for example it is located in a public cloud), you can provide that value here. Either one of <code>key_src</code>, <code>key_content</code>, or <code>username_credential</code> must be provided.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td>password_credential<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Password of the user that you wish to connect to the remote BIG-IP with over SSH. The <code>password_credential</code> and <code>private_key</code> parameters are mutually exclusive. You may use one or the other.</div>        </td></tr>
                <tr><td rowspan="2">provider<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>A dict object containing connection details.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object provider</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>True</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>transport<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td>cli</td>
                <td><ul><li>rest</li><li>cli</li></ul></td>
                <td><div>Configures the transport connection to use when connecting to the remote device.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>present</code>, ensures that the cloud connector exists. When <code>absent</code>, ensures that the cloud connector does not exist.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>username_credential<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Username used to the remote BIG-IP with over its web API. This parameter is required when <code>state</code> is <code>present</code>.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create node from managed device
      iworkflow_local_connector_node:
          device: "10.144.128.137"
          password_credential: "secret"
          username_credential: "admin"
          state: "present"
          connector: "Private OpenStack"
          hostname: "lb1.example.com"
          interfaces:
              - local_address: "10.144.128.137"
                subnet_address: "10.144.128/24"
              - local_address: "10.2.0.81"
                subnet_address: "10.2.0.0/24"
                name: "internal"
          server: "iwf.mydomain.com"
          password: "secret"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost

    - name: Create node from managed device in Azure
      iworkflow_local_connector_node:
          device: "10.144.128.137"
          password_credential: "secret"
          username_credential: "admin"
          device_root_password: "default"
          state: "present"
          connector: "Public Azure West US"
          hostname: "lb1.example.com"
          interfaces:
              - local_address: "10.0.2.12"
                subnet_address: "10.0.2.0/24"
                virtual_address: "10.144.128.137"
              - local_address: "10.2.0.81"
                subnet_address: "10.2.0.0/24"
                name: "external"
          server: "iwf.mydomain.com"
          password: "secret"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost



Notes
-----

.. note::
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr.
    - This module does not support updating of existing nodes that were created with a ``cli_password_credential``. The onboarding process will change your device's ``cli_username_credential`` password, which will prevent you from using this module (without knowing the password) a second time.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.