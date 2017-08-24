.. _bigip_policy_rule:


bigip_policy_rule - Manage LTM policy rules on a BIG-IP.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* This module will manage LTM policy rules on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 1.5.0
  * BIG-IP >= v12.1.0


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
                <tr><td>actions<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The actions that you want the policy rule to perform</div>        </td></tr>
                <tr><td>conditions<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A list of attributes that describe the condition. The available attributes vary by the condition, however, each condition requires that a <code>type</code> be specified.</div><div>Available <code>type</code> values are <code>client-ssl</code>, <code>cpu-usage</code>, <code>geo-ip</code>, <code>http-basic-auth</code>, <code>http-cookie</code>, <code>http-header</code>, <code>http-host</code>, <code>http-method</code>, <code>http-referer</code>, <code>http-set-cookie</code>, <code>http-status</code>, <code>http-uri</code>, <code>http-user-agent</code>, <code>http-version</code>, <code>ssl-certificate</code>, <code>ssl-extension</code>, <code>tcp</code>, <code>web-socket</code>.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the rule.</div>        </td></tr>
                <tr><td>order<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A number, indicating the place in the list of a policy's rules.</div><div>When <code>order</code> is <code>0</code>, the rule will be placed first in the list, and all other rules will be moved down by one place.</div><div>When <code>order</code> is <code>-1</code>, the rule will be moved to the end of the list, and all other rules will be moved up by one place.</div><div>When <code>order</code> is any other number, if that order is currently occupied by an existing rule, then that exiting rule will be moved down and this new rule will take the existing rule's place.</div><div>When creating a new rule, the new rule will be placed at the end of any existing rules; a value of <code>-1</code>.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>policy<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the policy that you want to associate this rule with</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>present</code>, ensures that the key is uploaded to the device. When <code>absent</code>, ensures that the key is removed from the device. If the key is currently in use, the module will not be able to remove the key.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    vars:
        policy_rules:
            - name: rule1
              actions:
                  - forward: "yes"
                    select: "yes"
                    pool: "pool-svrs"
              conditions:
                  - http_uri: "yes"
                    path: "yes"
                    starts-with:
                        - /euro
              ordinal: 8
            - name: HomePage
              actions:
                  - forward: yes
                    select: yes
                    pool: "pool-svrs"
              conditions:
                  - http-uri: yes
                    path: yes
                    starts-with:
                        - /HomePage/
              ordinal: 4
    
    - name: Create policies
      bigip_policy:
          name: "Policy-Foo"
          state: present
      delegate_to: localhost
    
    - name: Add a rule to the new policy
      bigip_policy_rule:
          policy: "Policy-Foo"
          name: "ABC"
          ordinal: 11
          conditions:
              - http_uri: "yes"
                path: "yes"
                starts_with:
                    - "/ABC"
          actions:
              - forward: "yes"
                select: "yes"
                pool: "pool-svrs"
    
    - name: Add multiple rules to the new policy
      bigip_policy_rule:
          policy: "Policy-Foo"
          name: "{{ item.name }}"
          ordinal: "{{ item.ordinal }}"
          conditions: "{{ item.conditions }}"
          actions: "{{ item.actions }}"
      with_items:
          - policy_rules

Return Values
-------------

Common return values are documented here :doc:`common_return_values`, the following are the fields unique to this module:

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>

        <tr>
        <td> key_source_path </td>
        <td> Path on BIG-IP where the source of the key is stored </td>
        <td align=center> created </td>
        <td align=center> string </td>
        <td align=center> /var/config/rest/downloads/cert1.key </td>
    </tr>
            <tr>
        <td> key_filename </td>
        <td> ['The name of the SSL certificate key. The C(key_filename) and C(cert_filename) will be similar to each other, however the C(key_filename) will have a C(.key) extension.'] </td>
        <td align=center> created </td>
        <td align=center> string </td>
        <td align=center> cert1.key </td>
    </tr>
            <tr>
        <td> key_checksum </td>
        <td> SHA1 checksum of the key that was provided. </td>
        <td align=center> changed and created </td>
        <td align=center> string </td>
        <td align=center> cf23df2207d99a74fbe169e3eba035e633b65d94 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.