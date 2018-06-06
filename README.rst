.. raw:: html

   <!--
   Copyright 2015-2016 F5 Networks Inc.

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

Ansible F5
==========

|slack badge| |travis badge|

Introduction
------------

This repository provides the foundation for working with the F5 Modules for Ansible.
The architecture of the modules makes inherent use of the BIG-IP SOAP and REST
APIs as well as the tmsh API where required.

This repository is an **incubator** for Ansible modules. The modules in this repository **may be
broken due to experimentation or refactoring**.

If you want to download the stable modules, they are shipped with Ansible
automatically. In-between major releases of Ansible, new |ansible_stablemodules|.

The F5 Modules for Ansible are freely provided to the open source community for automating
BIG-IP device configurations. 

Support
-------
F5 supports the F5 modules delivered in |ansible_distro|. Please refer to the |support_policy| for details.

Bugs, Issues
------------

Please file any bugs, questions, or enhancement requests by using |ansible_issues|. For details, see |ansiblegethelp|.

Documentation
-------------

All documentation is available on |ansiblehelp|.

When |writingmodules|, please refer to the |ansibleguidelines| document.

Your ideas
----------

What types of modules do you want created? If you have a use case and can sufficiently describe the behavior you want to see, open an issue and we will hammer out the details.

If you've got the time, consider sending an email that introduces yourself and what you do. We love hearing about how you're using the F5 Modules for Ansible.

- Tim Rupp and the F5 team - solutionsfeedback@f5.com

Copyright
---------

Copyright 2017-2018 F5 Networks Inc.


License
-------

GPL V3
~~~~~~

This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work.

See `License`_.

Contributor License Agreement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Individuals or business entities who contribute to this project must complete and submit the `F5 Contributor License Agreement <http://clouddocs.f5.com/products/orchestration/ansible/devel/development/cla-landing.html>`_ to Ansible_CLA@f5.com prior to their code submission being included in this project.


.. |travis badge| image:: https://travis-ci.org/F5Networks/f5-ansible.svg?branch=devel
    :target: https://travis-ci.org/F5Networks/f5-ansible
    :alt: Build Status

.. |slack badge| image:: https://f5cloudsolutions.herokuapp.com/badge.svg
    :target: https://f5cloudsolutions.herokuapp.com
    :alt: Slack Status


.. _License: https://github.com/F5Networks/f5-ansible/blob/devel/COPYING



.. |ansible_distro| raw:: html

   <a href="https://pypi.org/project/ansible/" target="_blank">Red Hat Ansible distributions</a>


.. |support_policy| raw:: html

   <a href="https://f5.com/support/support-policies" target="_blank">F5 Ansible Support Policy</a>



.. |ansible_stablemodules| raw:: html

   <a href="https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/f5" target="_blank">stable modules can be found here</a>

.. |ansible_issues| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/issues" target="_blank">Github Issues</a>

.. |ansiblehelp| raw:: html

   <a href="http://clouddocs.f5.com/products/orchestration/ansible/devel/" target="_blank">clouddocs.f5.com</a>

.. |writingmodules| raw:: html

   <a href="http://clouddocs.f5.com/products/orchestration/ansible/devel/development/writing-a-module.html" target="_blank">writing new modules</a>

.. |ansibleguidelines| raw:: html

   <a href="http://clouddocs.f5.com/products/orchestration/ansible/devel/development/guidelines.html" target="_blank">Guidelines</a>

.. |ansiblegethelp| raw:: html

   <a href="http://clouddocs.f5.com/products/orchestration/ansible/devel/usage/support.html" target="_blank">Get Help</a>


