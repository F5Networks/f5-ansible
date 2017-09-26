.. _bigip_iapp_service:


bigip_iapp_service - Manages TCL iApp services on a BIG-IP.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages TCL iApp services on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk
  * deepdiff


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
                <tr><td>force<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Forces the updating of an iApp service even if the parameters to the service have not changed. This option is of particular importance if the iApp template that underlies the service has been updated in-place. This option is equivalent to re-configuring the iApp if that template has changed.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the iApp service that you want to deploy.</div>        </td></tr>
                <tr><td>parameters<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A hash of all the required template variables for the iApp template. If your parameters are stored in a file (the more common scenario) it is recommended you use either the `file` or `template` lookups to supply the expected parameters.</div>        </td></tr>
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
        <td><div>When <code>present</code>, ensures that the iApp service is created and running. When <code>absent</code>, ensures that the iApp service has been removed.</div>        </td></tr>
                <tr><td>template<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The iApp template from which to instantiate a new service. This template must exist on your BIG-IP before you can successfully create a service. This parameter is required if the <code>state</code> parameter is <code>present</code>.</div>        </td></tr>
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

    
    - name: Create HTTP iApp service from iApp template
      bigip_iapp_service:
          name: "foo-service"
          template: "f5.http"
          parameters: "{{ lookup('file', 'f5.http.parameters.json') }}"
          password: "secret"
          server: "lb.mydomain.com"
          state: "present"
          user: "admin"
      delegate_to: localhost
    
    - name: Upgrade foo-service to v1.2.0rc4 of the f5.http template
      bigip_iapp_service:
          name: "foo-service"
          template: "f5.http.v1.2.0rc4"
          password: "secret"
          server: "lb.mydomain.com"
          state: "present"
          user: "admin"
      delegate_to: localhost
    
    - name: Configure a service using parameters in YAML
      bigip_iapp_service:
          name: "tests"
          template: "web_frontends"
          password: "admin"
          server: "{{ inventory_hostname }}"
          server_port: "{{ bigip_port }}"
          validate_certs: "{{ validate_certs }}"
          state: "present"
          user: "admin"
          parameters:
              variables:
                  - name: "var__vs_address"
                    value: "1.1.1.1"
                  - name: "pm__apache_servers_for_http"
                    value: "2.2.2.1:80"
                  - name: "pm__apache_servers_for_https"
                    value: "2.2.2.2:80"
      delegate_to: localhost
    
    - name: Re-configure a service whose underlying iApp was updated in place
      bigip_iapp_service:
          name: "tests"
          template: "web_frontends"
          password: "admin"
          force: yes
          server: "{{ inventory_hostname }}"
          server_port: "{{ bigip_port }}"
          validate_certs: "{{ validate_certs }}"
          state: "present"
          user: "admin"
          parameters:
              variables:
                  - name: "var__vs_address"
                    value: "1.1.1.1"
                  - name: "pm__apache_servers_for_http"
                    value: "2.2.2.1:80"
                  - name: "pm__apache_servers_for_https"
                    value: "2.2.2.2:80"
      delegate_to: localhost


Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires the deepdiff Python package on the host. This is as easy as pip install f5-sdk.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.