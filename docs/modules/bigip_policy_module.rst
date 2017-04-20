.. _bigip_policy:


bigip_policy - Manage general policy configuration on a BIG-IP.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages general policy configuration on a BIG-IP. This module is best used in conjunction with the ``bigip_policy_rule`` module. This module can handle general configuration like setting the draft state of the policy, the description, and things unrelated to the policy rules themselves. It is also the first module that should be used when creating rules as the ``bigip_policy_rule`` module requires a policy parameter.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk


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
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>The description to attach to the Partition.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the policy to create.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
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
        <td><ul><li>present</li><li>absent</li><li>draft</li></ul></td>
        <td><div>When <code>state</code> is <code>present</code>, ensures that the policy exists and is published. When <code>state</code> is <code>absent</code>, ensures that the policy is removed, even if it is currently drafted. When <code>state</code> is <code>draft</code>, ensures that the policy exists and is drafted.</div>        </td></tr>
                <tr><td>strategy<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>first</li><li>all</li><li>best</li><li>Custom strategy</li></ul></td>
        <td><div>Specifies the method to determine which actions get executed in the case where there are multiple rules that match. When creating new policies, the default is <code>first</code>.</div>        </td></tr>
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


Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.