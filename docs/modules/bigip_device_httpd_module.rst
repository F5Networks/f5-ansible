.. _bigip_device_httpd:


bigip_device_httpd - Manage HTTPD related settings on BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages HTTPD related settings on the BIG-IP. These settings are interesting to change when you want to set GUI timeouts and other TMUI related settings.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.4


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
                <tr><td>auth_name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the BIG-IP authentication realm name</div>        </td></tr>
                <tr><td>auth_pam_dashboard_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>on</li><li>off</li></ul></td>
        <td><div>Sets whether or not the BIG-IP dashboard will timeout.</div>        </td></tr>
                <tr><td>auth_pam_idle_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the GUI timeout for automatic logout, in seconds.</div>        </td></tr>
                <tr><td>auth_pam_validate_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>on</li><li>off</li></ul></td>
        <td><div>Sets the authPamValidateIp setting.</div>        </td></tr>
                <tr><td>fast_cgi_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the timeout of FastCGI.</div>        </td></tr>
                <tr><td>hostname_lookup<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>on</li><li>off</li></ul></td>
        <td><div>Sets whether or not to display the hostname, if possible.</div>        </td></tr>
                <tr><td>log_level<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>alert</li><li>crit</li><li>debug</li><li>emerg</li><li>error</li><li>info</li><li>notice</li><li>warn</li></ul></td>
        <td><div>Sets the minimum httpd log level.</div>        </td></tr>
                <tr><td>max_clients<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Sets the maximum number of clients that can connect to the GUI at once.</div>        </td></tr>
                <tr><td>redirect_http_to_https<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Whether or not to redirect http requests to the GUI to https.</div>        </td></tr>
                <tr><td>ssl_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The HTTPS port to listen on.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Set the BIG-IP authentication realm name
      bigip_device_httpd:
        auth_name: BIG-IP
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Set the auth pam timeout to 3600 seconds
      bigip_device_httpd:
        auth_pam_idle_timeout: 1200
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost

    - name: Set the validate IP settings
      bigip_device_httpd:
        auth_pam_validate_ip: on
        password: secret
        server: lb.mydomain.com
        user: admin
      delegate_to: localhost


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
        <td> auth_pam_idle_timeout </td>
        <td> The new number of seconds for GUI timeout. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 1200 </td>
    </tr>
        
    </table>
    </br></br>

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

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.