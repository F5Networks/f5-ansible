.. _bigip_data_group:


bigip_data_group - Manage data groups on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.6


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Allows for managing data groups on a BIG-IP. Data groups provide a way to store collections of values on a BIG-IP for later use in things such as LTM rules, iRules, and ASM policies.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9


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
                <tr><td>delete_data_group_file<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>When <code>yes</code>, will ensure that the remote data group file is deleted.</div><div>This parameter is only relevant when <code>state</code> is <code>absent</code> and <code>internal</code> is <code>no</code>.</div>        </td></tr>
                <tr><td>external_file_name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>When creating a new data group, this specifies the file name that you want to give an external data group file on the BIG-IP.</div><div>This parameter is ignored when <code>internal</code> is <code>yes</code>.</div><div>This parameter can be used to select an existing data group file to use with an existing external data group.</div><div>If this value is not provided, it will be given the value specified in <code>name</code> and, therefore, match the name of the data group.</div><div>This value may only contain letters, numbers, underscores, dashes, or a period.</div>        </td></tr>
                <tr><td>internal<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>The type of this data group.</div><div>You should only consider setting this value in cases where you know exactly what you&#x27;re doing, <b>or</b>, you are working with a pre-existing internal data group.</div><div>Be aware that if you deliberately force this parameter to <code>yes</code>, and you have a either a large number of records or a large total records size, this large amount of data will be reflected in your BIG-IP configuration. This can lead to <b>long</b> system configuration load times due to needing to parse and verify the large configuration.</div><div>There is a limit of either 4 megabytes or 65,000 records (whichever is more restrictive) for uploads when this parameter is <code>yes</code>.</div><div>This value cannot be changed once the data group is created.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Specifies the name of the data group.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
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
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>yes</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>transport<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td>cli</td>
                <td><ul><li>rest</li><li>cli</li></ul></td>
                <td><div>Configures the transport connection to use when connecting to the remote device.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td rowspan="2">records<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>Specifies the records that you want to add to a data group.</div><div>If you have a large number of records, it is recommended that you use <code>records_content</code> instead of typing all those records here.</div><div>The technical limit of either 1. the number of records, or 2. the total size of all records, varies with the size of the total resources on your system; in particular, RAM.</div><div>When <code>internal</code> is <code>no</code>, at least one record must be specified in either <code>records</code> or <code>records_content</code>.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object records</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>key<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The key describing the record in the data group.</div><div>Your key will be used for validation of the <code>type</code> parameter to this module.</div>        </td></tr>
                    <tr><td>value<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>The value of the key describing the record in the data group.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>records_src<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Path to a file with records in it.</div><div>The file should be well-formed. This means that it includes records, one per line, that resemble the following format &quot;key separator value&quot;. For example, <code>foo := bar</code>.</div><div>BIG-IP is strict about this format, but this module is a bit more lax. It will allow you to include arbitrary amounts (including none) of empty space on either side of the separator. For an illustration of this, see the Examples section.</div><div>Record keys are limited in length to no more than 65520 characters.</div><div>Values of record keys are limited in length to no more than 65520 characters.</div><div>The total number of records you can have in your BIG-IP is limited by the memory of the BIG-IP.</div><div>The format of this content is slightly different depending on whether you specify a <code>type</code> of <code>address</code>, <code>integer</code>, or <code>string</code>. See the examples section for examples of the different types of payload formats that are expected in your data group file.</div><div>When <code>internal</code> is <code>no</code>, at least one record must be specified in either <code>records</code> or <code>records_content</code>.</div>        </td></tr>
                <tr><td>separator<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>When specifying <code>records_content</code>, this is the string of characters that will be used to break apart entries in the <code>records_content</code> into key/value pairs.</div><div>By default, this parameter&#x27;s value is <code>:=</code>.</div><div>This value cannot be changed once it is set.</div><div>This parameter is only relevant when <code>internal</code> is <code>no</code>. It will be ignored otherwise.</div>        </td></tr>
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
    <td></td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>state</code> is <code>present</code>, ensures the data group exists.</div><div>When <code>state</code> is <code>absent</code>, ensures that the data group is removed.</div>        </td></tr>
                <tr><td>type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>string</td>
        <td><ul><li>address</li><li>string</li><li>integer</li></ul></td>
        <td><div>The type of records in this data group.</div><div>This parameter is especially important because it causes BIG-IP to store your data in different ways so-as to optimize access to it. For example, it would be wrong to specify a list of records containing IP addresses, but label them as a <code>string</code> type.</div><div>This value cannot be changed once the data group is created.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>yes</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a data group of addresses
      bigip_data_group:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
        records:
          - key: 0.0.0.0/32
            value: External_NAT
          - key: 10.10.10.10
            value: No_NAT
        type: address
      delegate_to: localhost

    - name: Create a data group of strings
      bigip_data_group:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
        records:
          - key: caddy
            value: ""
          - key: cafeteria
            value: ""
          - key: cactus
            value: ""
        type: string
      delegate_to: localhost

    - name: Create a data group of IP addresses from a file
      bigip_data_group:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
        records_src: /path/to/dg-file
        type: address
      delegate_to: localhost

    - name: Update an existing internal data group of strings
      bigip_data_group:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        internal: yes
        user: admin
        records:
          - key: caddy
            value: ""
          - key: cafeteria
            value: ""
          - key: cactus
            value: ""
      delegate_to: localhost

    - name: Show the data format expected for records_content - address 1
      copy:
        dest: /path/to/addresses.txt
        content: |
          network 10.0.0.0 prefixlen 8 := "Network1",
          network 172.16.0.0 prefixlen 12 := "Network2",
          network 192.168.0.0 prefixlen 16 := "Network3",
          network 2402:9400:1000:0:: prefixlen 64 := "Network4",
          host 192.168.20.1 := "Host1",
          host 172.16.1.1 := "Host2",
          host 172.16.1.1/32 := "Host3",
          host 2001:0db8:85a3:0000:0000:8a2e:0370:7334 := "Host4",
          host 2001:0db8:85a3:0000:0000:8a2e:0370:7334/128 := "Host5"

    - name: Show the data format expected for records_content - address 2
      copy:
        dest: /path/to/addresses.txt
        content: |
          10.0.0.0/8 := "Network1",
          172.16.0.0/12 := "Network2",
          192.168.0.0/16 := "Network3",
          2402:9400:1000:0::/64 := "Network4",
          192.168.20.1 := "Host1",
          172.16.1.1 := "Host2",
          172.16.1.1/32 := "Host3",
          2001:0db8:85a3:0000:0000:8a2e:0370:7334 := "Host4",
          2001:0db8:85a3:0000:0000:8a2e:0370:7334/128 := "Host5"

    - name: Show the data format expected for records_content - string
      copy:
        dest: /path/to/strings.txt
        content: |
          a := alpha,
          b := bravo,
          c := charlie,
          x := x-ray,
          y := yankee,
          z := zulu,

    - name: Show the data format expected for records_content - integer
      copy:
        dest: /path/to/integers.txt
        content: |
          1 := bar,
          2 := baz,
          3,
          4,



Notes
-----

.. note::
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