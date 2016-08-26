.. _bigip_ssl_certificate:


bigip_ssl_certificate - Import/Delete certificates from BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module will import/delete SSL certificates on BIG-IP LTM. Certificates can be imported from certificate and key files on the local disk, in PEM format.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 1.3.1
  * BigIP >= v12


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
    <td>cert_content<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>When used instead of 'cert_src', sets the contents of a certificate directly to the specified value. This is used with lookup plugins or for anything with formatting or templating. Either one of <code>key_src</code>, <code>key_content</code>, <code>cert_src</code> or <code>cert_content</code> must be provided when <code>state</code> is <code>present</code>.</div></td></tr>
            <tr>
    <td>cert_src<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>This is the local filename of the certificate. Either one of <code>key_src</code>, <code>key_content</code>, <code>cert_src</code> or <code>cert_content</code> must be provided when <code>state</code> is <code>present</code>.</div></td></tr>
            <tr>
    <td>key_content<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>When used instead of 'key_src', sets the contents of a certificate key directly to the specified value. This is used with lookup plugins or for anything with formatting or templating. Either one of <code>key_src</code>, <code>key_content</code>, <code>cert_src</code> or <code>cert_content</code> must be provided when <code>state</code> is <code>present</code>.</div></td></tr>
            <tr>
    <td>key_src<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>This is the local filename of the private key. Either one of <code>key_src</code>, <code>key_content</code>, <code>cert_src</code> or <code>cert_content</code> must be provided when <code>state</code> is <code>present</code>.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>SSL Certificate Name.  This is the cert/key pair name used when importing a certificate/key into the F5. It also determines the filenames of the objects on the LTM (:Partition:name.cer_11111_1 and :Partition_name.key_11111_1).</div></td></tr>
            <tr>
    <td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td><ul></ul></td>
        <td><div>BIG-IP partition to use when adding/deleting certificate.</div></td></tr>
            <tr>
    <td>passphrase<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Passphrase on certificate private key</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The BIG-IP host.</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>The BIG-IP server port.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Certificate and key state. This determines if the provided certificate and key is to be made <code>present</code> on the device or <code>absent</code>.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Import PEM Certificate from local disk
      bigip_ssl_certificate:
          name: "certificate-name"
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          cert_src: "/path/to/cert.crt"
          key_src: "/path/to/key.key"
      delegate_to: localhost
    
    - name: Use a file lookup to import PEM Certificate
      bigip_ssl_certificate:
          name: "certificate-name"
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          cert_content: "{{ lookup('file', '/path/to/cert.crt') }}"
          key_content: "{{ lookup('file', '/path/to/key.key') }}"
      delegate_to: localhost
    
    - name: "Delete Certificate"
      bigip_ssl_certificate:
          name: "certificate-name"
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "absent"
      delegate_to: localhost


Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
.. note:: Requires the netaddr Python package on the host.
.. note:: If you use this module, you will not be able to remove the certificates and keys that are managed, via the web UI. You can only remove them via tmsh or these modules.


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

