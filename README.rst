.. raw:: html

   <!--
    Copyright 2015-2019 F5 Networks Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
   -->

Ansible F5
==========

|slack badge| |travis badge| |shippable badge|

Introduction
------------

This repository is the source for F5 Imperative Collection for Ansible.
The architecture of the modules makes inherent use of the BIG-IP REST APIs as well as the tmsh API where required.

This repository is an **incubator** for Ansible imperative modules. The modules in this repository **may be
broken due to experimentation or refactoring**.

The F5 Modules for Ansible are freely provided to the open source community for automating BIG-IP device configurations.

If you want to download the stable modules, please install latest collection release found on galaxy: |f5_collection|.


Collections Daily Build
-----------------------

We offer a daily build of our most recent collection |dailybuild|. Please use this Collection to test the most
recent Ansible module updates between releases.

Installing the Daily Build
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: shell

    ansible-galaxy collection install <collection name> -p ./collections
    e.g.
    ansible-galaxy collection install f5networks-f5_modules-devel.tar.gz -p ./collections

.. note::

   "-p" is the location in which the collection will be installed. This location should be defined in the path for
   ansible to search for collections. An example of this would be adding ``collections_paths = ./collections``
   to your **ansible.cfg**

Support
-------
F5 supports the F5 Imperative Collection for Ansible delivered in |ansible_galaxy|. Please refer to the |support_policy| for details.

Community Support
~~~~~~~~~~~~~~~~~
We encourage you to use our |slacklink| for discussion and assistance on F5 Ansible Modules (click the **ansible** channel). There are F5 employees who are members of this community who typically monitor the channel Monday-Friday 9-5 PST and will offer best-effort assistance. This slack channel community support should not be considered a substitute for F5 Technical Support.

Bugs, Issues
------------

Please file any bugs, questions, or enhancement requests by using |ansible_issues|. For details, see |ansiblegethelp|.

.. note:: **We no longer accept external code submissions.**

Documentation
-------------

All documentation is available on |ansiblehelp|.
Changelog information available on |changelog|.

Python Version Deprecation
--------------------------
Support for versions of Python earlier than 3.5 is being deprecated and will be removed at a future date.

Your ideas
----------

What types of modules do you want created? If you have a use case and can sufficiently describe the behavior you want to see, open an issue and we will hammer out the details.

If you've got the time, consider sending an email that introduces yourself and what you do. We love hearing about how you're using the F5 Modules for Ansible.

.. note:: **We no longer accept external code submissions.**

- Wojciech Wypior and the F5 team - solutionsfeedback@f5.com

Copyright
---------

Copyright 2017-2022 F5 Networks Inc.


License
-------

GPL V3
~~~~~~

This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work.

See `License`_.


.. |travis badge| image:: https://travis-ci.com/F5Networks/f5-ansible.svg?branch=devel
    :target: https://travis-ci.com/F5Networks/f5-ansible
    :alt: Build Status

.. |slack badge| image:: https://f5cloudsolutions.herokuapp.com/badge.svg
    :target: https://f5cloudsolutions.herokuapp.com
    :alt: Slack Status

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

.. |slacklink| raw:: html

   <a href="https://f5cloudsolutions.herokuapp.com/" target="_blank">Slack channel</a>

.. |changelog| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/blob/devel/ansible_collections/f5networks/f5_modules/CHANGELOG.rst" target="_blank">Changelogs</a>

