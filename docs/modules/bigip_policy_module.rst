.. _bigip_partition:


bigip_partition - Manage BIG-IP partitions
++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage BIG-IP partitions


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds
  * requests


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
            <tr>
    <td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The description to attach to the Partition</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div></td></tr>
            <tr>
    <td>route_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The default Route Domain to assign to the Partition. If no route domain is specified, then the default route domain for the system (typically zero) will be used only when creating a new partition. <code>route_domain</code> and <code>route_domain_id</code> are mutually exclusive.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the partition should exist or not</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    vars:
        policy_rules:
            - name: Eurobt
              actions:
                  - forward: "yes"
                    select: "yes"
                    pool: "drn-bondticker-eurobt-tomcat-lwc-svrs"
              conditions:
                  - http_uri: "yes"
                    path: "yes"
                    starts-with:
                        - /eurobt
              ordinal: 8
            - name: HomePage
              actions:
                  - forward: yes
                    select: yes
                    pool: "drn-bondticker-Homepage-lwc-svrs"
              conditions:
                  - http-uri: yes
                    path: yes
                    starts-with:
                        - /HomePage/
              ordinal: 4
          
    - name: Create policies
      bigip_policy:
          name: "Policy-Foo"
          controls:
              - forwarding
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
                pool: "drn-bondticker-etf-lwc-svrs"
    
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

.. note:: Requires the bigsuds Python package on the host if using the iControl interface. This is as easy as pip install bigsuds


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

