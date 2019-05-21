F5 Modules for Ansible
======================

Welcome to the F5 Modules for Ansible documentation.

Use these modules to create, edit, update, and delete configuration objects on BIG-IP 12.0.0 and later, and BIG-IQ 5.4.0 and later.

The code is open source and |f5_ansible_github|. Additionally, some modules have been promoted to the |ansible_core| and |ansible_extras|.


Set Up
------

:doc:`Install </usage/getting_started>`  (connection vs delegation sub-topic (not in table of contents))

Get Started
-----------

:doc:`Run your first playbook </usage/playbook_tutorial>`

Work with the Modules
---------------------

- Work with output (jinja filters)

- Use F5 aggregate functionality

- Use galaxy role

- Use modules with tower

Tutorials
---------

https://github.com/F5Networks/f5-ansible/tree/devel/examples


Module Reference
----------------

:doc:`Module Index </modules/modules_by_category>`


Get Help
--------

Supported versions--
How to get help for the supported versions

|
|

.. toctree::
   :maxdepth: 2
   :caption: Set Up
   :glob:
   :hidden:

   /usage/getting_started
   /usage/connection-local-or-delegate-to

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Get Started
   :glob:

   /usage/playbook_tutorial

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Work with the Modules
   :glob:

   /usage/module-usage-with-tower

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Tutorials
   :glob:

   https://github.com/F5Networks/f5-ansible/tree/devel/examples

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Module Reference

   /modules/modules_by_category


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Get Help
   :glob:

   /usage/supported-versions
   /usage/support



.. |f5_ansible_github| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible" target="_blank">available on github</a>

.. |ansible_core| raw:: html

   <a href="https://github.com/ansible/ansible-modules-core" target="_blank">Ansible core product</a>

.. |ansible_extras| raw:: html

   <a href="https://github.com/ansible/ansible-modules-extras" target="_blank">Ansible extras</a>
