F5 Ansible Docs
===============

This project implements a set of Ansible modules for the BIG-IP platform from F5 Networks.

You can use these modules to create, edit, update, and delete configuration objects on a BIG-IP.

The code is open source, and |f5_ansible_github|. Additionally, some modules have been promoted to the |ansible_core| and |ansible_extras|.


.. |f5_ansible_github| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible" target="_blank">available on github</a>

.. |ansible_core| raw:: html

   <a href="https://github.com/ansible/ansible-modules-core" target="_blank">Ansible core product</a>

.. |ansible_extras| raw:: html

   <a href="https://github.com/ansible/ansible-modules-extras" target="_blank">Ansible extras</a>


.. toctree::
   :maxdepth: 1
   :includehidden:
   :caption: User Documentation

   usage/getting_started.rst
   usage/installing-modules.rst
   usage/versions.rst
   usage/support.rst
   usage/playbook_tutorial.rst
   usage/connection-local-or-delegate-to.rst
   usage/filing-issues.rst


.. toctree::
   :maxdepth: 2
   :caption: Module Documentation

   modules/modules_by_category

.. toctree::
   :maxdepth: 1
   :caption: Developer Documentation

   development/cla-landing.rst
   development/getting-involved.rst
   development/guidelines.rst
   development/tests.rst
   development/architecture.rst
   development/code-conventions.rst
   development/upstreaming.rst
   development/writing-a-module.rst
   development/deprecating_code.rst
   development/design-decisions.rst
   development/dealing-with-replace-all.rst
   development/module-patterns.rst
   development/testing-pipeline.rst
   development/securing-sensitive-information.rst
   development/ssh-functionality-for-modules.rst
   development/issue-management.rst
