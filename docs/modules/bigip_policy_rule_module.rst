.. _bigip_policy_rule:


bigip_policy_rule - Manage LTM policy rules on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* This module will manage LTM policy rules on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.0
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
        <td><div>The actions that you want the policy rule to perform.</div><div>The available attributes vary by the action, however, each action requires that a <code>type</code> be specified.</div><div>Available <code>type</code> values are <code>forward</code>.</div>        </td></tr>
                <tr><td>append<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li><li>actions</li><li>conditions</li></ul></td>
        <td><div>When <code>yes</code>, will append all <code>conditions</code> and <code>actions</code> to the given rule if they do not already exist.</div><div>When <code>actions</code>, will only append the specified actions. If <code>conditions</code> are also provided, the existing conditions will be overwritten with the new list in the <code>conditions</code> parameter.</div><div>When <code>conditions</code>, will only append the specified conditions. If <code>actions</code> are also provided, the existing actions will be overwritten with the new list in the <code>actions</code> parameter.</div>        </td></tr>
                <tr><td rowspan="2">conditions<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>A list of attributes that describe the condition.</div><div>See suboptions for details on how to construct each list entry.</div><div>The ordering of this list is important, the module will ensure the order is kept when modifying the task.</div><div>The suboption options listed below are not required for all condition types, read the description for more details.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object conditions</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>type<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td><ul><li>http_uri</li></ul></td>
                <td><div>The condition type. This value controls what below options are required.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the rule.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>policy<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the policy that you want to associate this rule with.</div>        </td></tr>
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
        - type: forward
          pool: pool-svrs
      conditions:
        - type: http_uri
          path_starts_with: /euro
        - name: rule2
          actions:
        - type: forward
          pool: pool-svrs
      conditions:
        - type: http_uri
          path_starts_with: /HomePage/
    
    - name: Create policies
      bigip_policy:
        name: Policy-Foo
        state: present
      delegate_to: localhost
    
    - name: Add a rule to the new policy
      bigip_policy_rule:
        policy: Policy-Foo
        name: rule3
        conditions:
          - type: http_uri
            path_starts_with: /ABC
        actions:
          - type: forward
            pool: pool-svrs
    
    - name: Add multiple rules to the new policy
      bigip_policy_rule:
        policy: Policy-Foo
        name: "{{ item.name }}"
        conditions: "{{ item.conditions }}"
        actions: "{{ item.actions }}"
      with_items:
        - policy_rules


Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.