.. _bigip_policy:


bigip_policy - Manage general policy configuration on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages general policy configuration on a BIG-IP. This module is best used in conjunction with the ``bigip_policy_rule`` module. This module can handle general configuration like setting the draft state of the policy, the description, and things unrelated to the policy rules themselves. It is also the first module that should be used when creating rules as the ``bigip_policy_rule`` module requires a policy parameter.


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
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The description to attach to the policy.</div><div>This parameter is only supported on versions of BIG-IP &gt;= 12.1.0. On earlier versions it will simply be ignored.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the policy to create.</div>        </td></tr>
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
                <tr><td>rules<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies a list of rules that you want associated with this policy. The order of this list is the order they will be evaluated by BIG-IP. If the specified rules do not exist (for example when creating a new policy) then they will be created.</div><div>The <code>conditions</code> for a default rule are <code>all</code>.</div><div>The <code>actions</code> for a default rule are <code>ignore</code>.</div><div>The <code>bigip_policy_rule</code> module can be used to create and edit existing and new rules.</div>        </td></tr>
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
        <td><ul><li>present</li><li>absent</li><li>draft</li></ul></td>
        <td><div>When <code>state</code> is <code>present</code>, ensures that the policy exists and is published. When <code>state</code> is <code>absent</code>, ensures that the policy is removed, even if it is currently drafted.</div><div>When <code>state</code> is <code>draft</code>, ensures that the policy exists and is drafted. When modifying rules, it is required that policies first be in a draft.</div><div>Drafting is only supported on versions of BIG-IP &gt;= 12.1.0. On versions prior to that, specifying a <code>state</code> of <code>draft</code> will raise an error.</div>        </td></tr>
                <tr><td>strategy<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>first</li><li>all</li><li>best</li></ul></td>
        <td><div>Specifies the method to determine which actions get executed in the case where there are multiple rules that match. When creating new policies, the default is <code>first</code>.</div><div>This module does not allow you to specify the <code>best</code> strategy to use. It will choose the system default (<code>/Common/best-match</code>) for you instead.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
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

    
    - name: Create policy which is immediately published
      bigip_policy:
        name: Policy-Foo
        state: present
      delegate_to: localhost

    - name: Add a rule to the new policy - Immediately published
      bigip_policy_rule:
        policy: Policy-Foo
        name: ABC
        conditions:
          - type: http_uri
            path_starts_with:
              - /ABC
              - foo
              - bar
            path_ends_with:
              - baz
        actions:
          - forward: yes
            select: yes
            pool: pool-svrs

    - name: Add multiple rules to the new policy - Added in the order they are specified
      bigip_policy_rule:
        policy: Policy-Foo
        name: "{{ item.name }}"
        conditions: "{{ item.conditions }}"
        actions: "{{ item.actions }}"
      with_items:
        - name: rule1
          actions:
            - type: forward
              pool: pool-svrs
          conditions:
            - type: http_uri
              path_starts_with: /euro
        - name: HomePage
          actions:
            - type: forward
              pool: pool-svrs
          conditions:
            - type: http_uri
              path_starts_with: /HomePage/

    - name: Create policy specify default rules - Immediately published
      bigip_policy:
        name: Policy-Bar
        state: present
        rules:
          - rule1
          - rule2
          - rule3

    - name: Create policy specify default rules - Left in a draft
      bigip_policy:
        name: Policy-Baz
        state: draft
        rules:
          - rule1
          - rule2
          - rule3


Return Values
-------------

Common return values are `documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`_, the following are the fields unique to this module:

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
        <td> rules </td>
        <td> List of the rules, and their order, applied to the policy. </td>
        <td align=center> changed and success </td>
        <td align=center> list </td>
        <td align=center> ['/Common/rule1', '/Common/rule2'] </td>
    </tr>
            <tr>
        <td> description </td>
        <td> ['The new description of the policy.', 'This value is only returned for BIG-IP devices >= 12.1.0.'] </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> This is my description </td>
    </tr>
            <tr>
        <td> strategy </td>
        <td> The new strategy set on the policy. </td>
        <td align=center> changed and success </td>
        <td align=center> int </td>
        <td align=center> first-match </td>
    </tr>
        
    </table>
    </br></br>

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