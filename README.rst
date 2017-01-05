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
##########

|slack badge|

Introduction
************

This repository provides the foundation for working with F5 devices and Ansible.
The architecture of the modules makes inherent use of the BIG-IP SOAP and REST
APIs as well as the tmsh API where required.

These modules are freely provided to the open source community for automating
BIG-IP device configurations using Ansible. Support for the modules is provided
on a best effort basis by the F5 community. Please file any bugs, questions or
enhancement requests using |Github Issues|

Requirements
============

* [Ansible 2.2.0 or greater][installing]
* Advanced shell for user account enabled
* [bigsuds Python Client 1.0.4 or later][bigsuds]
* [f5-sdk Python Client, latest available][f5-sdk]

Documentation
=============

All documentation is hosted on [ReadTheDocs][readthedocs].

When [writing new modules][writingnew], please refer to the
[Guidelines][guidelines] document.

Purpose
=======

The purpose of this repository is to serve as a **staging ground** for Ansible
modules that we would prefer to have upstreamed over the course of time.

The modules in this repository **may be broken** due to experimentation
or refactoring

Your ideas
==========

We are curious to know what sort of modules you want to see created. If you have
a use case and can sufficiently describe the behavior you want to see, open
an issue here and we will hammer out the details.

Support
=======

See `Support <SUPPORT.rst>`_.

Enjoy!

.. |bigsuds|
    :target: https://pypi.python.org/pypi/bigsuds/
    :alt: bigsuds

.. |f5-sdk|
    :target: https://pypi.python.org/pypi/f5-sdk/
    :alt: f5-sdk

.. |readthedocs|
    :target: https://f5-ansible.readthedocs.io/en/latest/
    :alt: ReadTheDocs

.. |guidelines|
    :target: https://f5-ansible.readthedocs.io/en/latest/development/guidelines.html
    :alt: Guidelines

.. |writingnew|
    :target: https://f5-ansible.readthedocs.io/en/latest/development/writing-a-module.html
    :alt: Writing a module

.. |installing|
    :target: https://f5-ansible.readthedocs.io/en/latest/usage/getting_started.html#installing-ansible
    :alt: Installing the modules

.. |slack badge| image:: https://f5-openstack-slack.herokuapp.com/badge.svg
    :target: https://f5-openstack-slack.herokuapp.com/
    :alt: Slack

.. |Github Issues|
    :target: https://github.com/F5Networks/f5-ansible/issues
    :alt: Github Issues