F5 Ansible Docs
===============

This project implements a set of Ansible modules for the F5 Networks® BIG-IP®
Users of these modules can create, edit, update, and delete configuration
objects on a BIG-IP®. For more information on the basic principals that the
modules use, see the :doc:`usage/index`.

The code is open source, and `available on github`_. Additionally, some modules
have been promoted to the `Ansible core product`_ and `Ansible extras`_.

.. _available on github: https://github.com/F5Networks/f5-ansible
.. _Ansible core product: https://github.com/ansible/ansible-modules-core
.. _Ansible extras: https://github.com/ansible/ansible-modules-extras

The main documentation for the modules is organized into several sections
listed below.

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   usage/getting_started
   usage/connection-local-or-delegate-to
   usage/installing-modules
   usage/versions
   usage/support

.. toctree::
   :maxdepth: 2
   :caption: Module Documentation

   general
   modules/modules_by_category

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   development/cla-landing
   development/getting-involved
   development/install
   development/guidelines
   development/tests
   development/architecture
   development/code-conventions
   development/upstreaming
   development/writing-a-module
   development/deprecating_code.rst
   development/design-decisions.rst
   development/dealing-with-replace-all.rst
   development/module-patterns.rst
   development/testing-pipeline.rst
   development/securing-sensitive-information.rst
   development/ssh-functionality-for-modules.rst
   development/issue-management.rst
