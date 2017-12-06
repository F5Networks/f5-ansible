.. _bigip_software_facts:


bigip_software_facts - Collect software facts from BIG-IP devices
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Collect information about installed volumes, existing ISOs for images and hotfixes on the BIG-IP device.


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
                <tr><td>filter<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Filter responses based on the attribute and value provided. Valid filters are required to be in <code>key:value</code> format, with keys being one of the following; name, build, version, status, active.</div>        </td></tr>
                <tr><td>include<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>[u'all']</td>
        <td><ul><li>all</li><li>image</li><li>hotfix</li><li>volume</li></ul></td>
        <td><div>Type of information to collect.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Gather image facts filter on version
      bigip_software_facts:
        server: lb.mydomain.com
        user: admin
        password: secret
        include: image
        filter: version:12.1.1
      delegate_to: localhost


Return Values
-------------

Common return values are :doc:`documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`, the following are the fields unique to this module:

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
        <td> images </td>
        <td> List of base image ISOs that are present on the unit. </td>
        <td align=center> changed </td>
        <td align=center> list of dict </td>
        <td align=center> {'images': [{'product': 'BIG-IP', 'version': '12.1.1', 'name': 'BIGIP-12.1.1.0.0.184.iso', 'lastModified': 'Sun Oct  2 20:50:04 2016', 'fileSize': '1997 MB', 'build': '0.0.184'}]} </td>
    </tr>
            <tr>
        <td> hotfixes </td>
        <td> List of hotfix ISOs that are present on the unit. </td>
        <td align=center> changed </td>
        <td align=center> list of dict </td>
        <td align=center> {'hotfixes': [{'product': 'BIG-IP', 'version': '12.1.1', 'name': '12.1.1-hf2.iso', 'lastModified': 'Sun Oct  2 20:50:04 2016', 'fileSize': '1997 MB', 'build': '2.0.204'}]} </td>
    </tr>
            <tr>
        <td> volumes </td>
        <td> List the volumes present on device. </td>
        <td align=center> changed </td>
        <td align=center> list of dict </td>
        <td align=center> {'volumes': [{'status': 'complete', 'product': 'BIG-IP', 'version': '12.1.1', 'name': 'HD1.2', 'basebuild': '0.0.184', 'build': '0.0.184'}]} </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.