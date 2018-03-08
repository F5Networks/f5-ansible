F5 Modules for Ansible
======================

This project implements a set of Ansible modules for the BIG-IP platform from F5 Networks.

You can use these modules to create, edit, update, and delete configuration objects on BIG-IP.

The code is open source and |f5_ansible_github|. Additionally, some modules have been promoted to the |ansible_core| and |ansible_extras|.

.. toctree::
   :maxdepth: 2
   :includehidden:
   :caption: Support Details
   :glob:

   /usage/supported-versions

.. toctree::
   :maxdepth: 2
   :includehidden:
   :caption: User's Guide
   :glob:

   /usage/getting_started
   /usage/playbook_tutorial
   /usage/connection-local-or-delegate-to
   /usage/support
   /usage/installing-modules

.. toctree::
   :maxdepth: 2
   :caption: Module Reference

   /modules/modules_by_category

.. toctree::
   :maxdepth: 2
   :caption: Developer's Guide

   /development/cla-landing
   /development/getting-involved
   /development/guidelines
   /development/write-module/index
   /development/code-conventions
   /development/parameters
   /development/module-patterns
   /development/ssh-functionality-for-modules
   /development/tests
   /development/upstreaming
   /development/securing-sensitive-information
   /development/playbook-metadata
   /development/deprecating-code

.. |f5_ansible_github| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible" target="_blank">available on github</a>

.. |ansible_core| raw:: html

   <a href="https://github.com/ansible/ansible-modules-core" target="_blank">Ansible core product</a>

.. |ansible_extras| raw:: html

   <a href="https://github.com/ansible/ansible-modules-extras" target="_blank">Ansible extras</a>
