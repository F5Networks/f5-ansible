.. _bigip_license:


bigip_license - Manage license installation and activation on BIG-IP devices
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage license installation and activation on BIG-IP devices


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds
  * requests
  * suds
  * paramiko


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
    <td>dossier_file<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Path to file containing kernel dossier for your system</div></td></tr>
            <tr>
    <td>key<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The registration key to use to license the BIG-IP. This is required if the <code>state</code> is equal to <code>present</code> or <code>latest</code></div></td></tr>
            <tr>
    <td>license_file<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Path to file containing the license to use</div></td></tr>
            <tr>
    <td>license_options<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Dictionary of options to use when creating the license</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div></td></tr>
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
        <td><ul><li>absent</li><li>latest</li><li>present</li></ul></td>
        <td><div>The state of the license on the system. When <code>present</code>, only guarantees that a license is there. When <code>latest</code> ensures that the license is always valid. When <code>absent</code> removes the license on the system. <code>latest</code> is most useful internally. When using <code>absent</code>, the account accessing the device must be configured to use the advanced shell instead of Appliance Mode.</div></td></tr>
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
            <tr>
    <td>wsdl<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>WSDL file to use if you're receiving errors when downloading the WSDL file at run-time from the licensing servers</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: License BIG-IP using default license options
      bigip_license:
          server: "big-ip.domain.org"
          user: "admin"
          password: "MyPassword123"
          key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
      delegate_to: localhost
    
    - name: License BIG-IP, specifying license options
      bigip_license:
          server: "big-ip.domain.org"
          key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
          user: "admin"
          password: "MyPassword123"
          license_options:
              email: 'joe.user@myplace.com'
              firstname: 'Joe'
              lastname: 'User'
              company: 'My Place'
              phone: '630-555-1212'
              jobtitle: 'Systems Administrator'
              address: '207 N Rodeo Dr'
              city: 'Beverly Hills'
              state: 'CA'
              postalcode: '90210'
              country: 'US'
      delegate_to: localhost
    
    - name: Remove the license from the system
      bigip_license:
          server: "big-ip.domain.org"
          user: "admin"
          password: "MyPassword123"
          state: "absent"
      delegate_to: localhost
    
    - name: Update the current license of the BIG-IP
      bigip_license:
          server: "big-ip.domain.org"
          user: "admin"
          password: "MyPassword123"
          key: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"
          state: "latest"
      delegate_to: localhost


Notes
-----

.. note:: Requires the suds Python package on the host. This is as easy as pip install suds
.. note:: Requires the bigsuds Python package on the host. This is as easy as pip install bigsuds
.. note:: Requires the paramiko Python package on the host if using the ``state`` ``absent``. This is as easy as pip install paramiko
.. note:: Requires the requests Python package on the host if using the ``state`` ``absent``. This is as easy as pip install paramiko


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

