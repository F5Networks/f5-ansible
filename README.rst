.. raw:: html

   <!--
   Copyright 2015-2019 F5 Networks Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   -->

F5 BIG-IP Imperative Collection for Ansible
===========================================

|travis badge| |shippable badge|

Important Warning
-----------------

Do not use Heroku App link for accessing F5 slack channel. It is not owned/maintained/used by F5 anymore.
You might be exposing yourself to security issues if you access this link thinking it to be the link to F5 slack channel. 

Introduction
------------

This repository is the source for F5 BIG-IP Imperative Collection for Ansible.
The architecture of the modules makes inherent use of the BIG-IP REST APIs as well as the tmsh API where required.

This repository is an **incubator** for Ansible imperative modules. The modules in this repository **may be
broken due to experimentation or refactoring**.

The F5 BIG-IP Modules for Ansible are freely provided to the open source community for automating BIG-IP device configurations.

If you want to download the stable modules, please install latest collection release found on galaxy: |f5_collection|.


Collections Daily Build
-----------------------

We offer a daily build of our most recent collection |dailybuild|. Please use this Collection to test the most
recent Ansible module updates between releases.

Installing the Daily Build
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

    ansible-galaxy collection install <collection name> -p ./collections
    e.g.
    ansible-galaxy collection install f5networks-f5_modules-devel.tar.gz -p ./collections

.. note::

   "-p" is the location in which the collection will be installed. This location should be defined in the path for
   ansible to search for collections. An example of this would be adding ``collections_paths = ./collections``
   to your **ansible.cfg**

Running latest devel in EE
~~~~~~~~~~~~~~~~~~~~~~~~~~
We also offer a new method of running the collection inside Ansible's Execution Environment container.
The advantage of such approach is that any required package dependencies and minimum supported Python versions are
installed in an isolated container which minimizes any environment related issues during runtime. More information on EE
can be found here [execenv]. Use the below requirements.yml file when building EE container:

.. code-block:: yaml

    collections:
      - name: ansible.netcommon
        version: ">=2.0.0"
      - name: f5networks.f5_modules
        source: https://github.com/F5Networks/f5-ansible-f5modules#ansible_collections/f5networks/f5_modules
        type: git
        version: devel

.. note::

   When running the **bigip_device_certificate** module one might see errors related to establishing ssh connection,
   one reason behind that could be ansible setting the ssh type to **libssh**, there are two ways to fix that,
   first, set the environemnt variable ``ANSIBLE_NETWORK_CLI_SSH_TYPE=paramiko`` while running the playbook.
   The second way is to add ``ssh_type = paramiko`` under section ``[persistent_connection]`` in **ansible.cfg**

Support
-------
F5 supports the F5 Imperative Collection for Ansible delivered in |ansible_galaxy|. Please refer to the |support_policy| for details.


Bugs, Issues
------------

Please file any bugs, questions, or enhancement requests by using |ansible_issues|. For details, see |ansiblegethelp|.

.. note:: **We no longer accept external code submissions.**

Documentation
-------------

All documentation is available on |ansiblehelp|.
Changelog information available on |changelog|.

Python Version Change
--------------------------
Collection only supports python 3.6 and above, however F5 recommends Python 3.9 and above.

Your ideas
----------

What types of modules do you want created? If you have a use case and can sufficiently describe the behavior you want to see, open an issue and we will hammer out the details.

If you've got the time, consider sending an email that introduces yourself and what you do. We love hearing about how you're using the F5 Modules for Ansible.

.. note:: **We no longer accept external code submissions.**

- Wojciech Wypior and the F5 team 

Copyright
---------

Copyright 2017-2023 F5 Networks Inc.


License
-------

GPL V3
~~~~~~

This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work.

See `License`_.


.. |travis badge| image:: https://travis-ci.com/F5Networks/f5-ansible.svg?branch=devel
    :target: https://travis-ci.com/F5Networks/f5-ansible
    :alt: Build Status

.. |shippable badge| image:: https://api.shippable.com/projects/57c88ded5a5c0d0f0012c53e/badge?branch=devel
    :target: https://app.shippable.com/github/F5Networks/f5-ansible
    :alt: Shippable Status

.. _License: https://github.com/F5Networks/f5-ansible/blob/devel/COPYING


.. |dailybuild| raw:: html

   <a href="https://f5-ansible.s3.amazonaws.com/collections/f5networks-f5_modules-devel.tar.gz" target="_blank">here</a>

.. |f5_collection| raw:: html

   <a href="https://galaxy.ansible.com/f5networks/f5_modules" target="_blank">F5 Ansible Modules Collection</a>

.. |ansible_galaxy| raw:: html

   <a href="https://galaxy.ansible.com/f5networks/f5_modules" target="_blank">Ansible Galaxy</a>

.. |support_policy| raw:: html

   <a href="https://f5.com/support/support-policies" target="_blank">F5 Ansible Support Policy</a>

.. |ansible_issues| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/issues" target="_blank">Github Issues</a>

.. |ansiblehelp| raw:: html

   <a href="http://clouddocs.f5.com/products/orchestration/ansible/devel/" target="_blank">clouddocs.f5.com</a>

.. |ansibleguidelines| raw:: html

   <a href="http://clouddocs.f5.com/products/orchestration/ansible/devel/development/guidelines.html" target="_blank">Guidelines</a>

.. |ansiblegethelp| raw:: html

   <a href="http://clouddocs.f5.com/products/orchestration/ansible/devel/usage/support.html" target="_blank">Get Help</a>

.. |changelog| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/blob/devel/ansible_collections/f5networks/f5_modules/CHANGELOG.rst" target="_blank">Changelogs</a>

