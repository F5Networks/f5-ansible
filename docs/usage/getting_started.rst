Getting started
===============

This document explains how to begin using the F5 Ansible modules.

**Note:** F5 Ansible modules are not currently supported by F5.

Install Python
--------------

Install the latest version of Python (2.7 minimum) if you do not already have it.

- |install_python|

Install Ansible
---------------

Then, install Ansible (2.2.0 minimum):

- |install_ansible|

F5 recommends that you install Ansible by using virtualenv/pip. For an example, see :doc:`virtualenv`.

- |install_ansible_pip|

Install Ansible Dependencies
----------------------------

In addition to Ansible, you should install a few additional Python modules.

- f5-sdk
- bigsuds
- netaddr
- deepdiff

At minimum, you should add `f5-sdk`.

You can install these by using pip (either globally or within a virtual environment). For example:

.. code-block:: bash

   (myansible) $ pip install f5-sdk bigsuds netaddr deepdiff

To view dependencies for a specific module, view the module's Documentation > Requirements section.




.. |install_python| raw:: html

   <a href="http://www.python.org/" target="_blank">http://www.python.org/</a>

.. |install_ansible| raw:: html

   <a href="http://docs.ansible.com/ansible/latest/intro_installation.html" target="_blank">http://docs.ansible.com/ansible/latest/intro_installation.html</a>

.. |install_ansible_pip| raw:: html

   <a href="http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-via-pip" target="_blank">http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-via-pip</a>

