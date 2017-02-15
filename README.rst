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

|slack badge|

Introduction
------------

This repository provides the foundation for working with F5 devices and Ansible.
The architecture of the modules makes inherent use of the BIG-IP SOAP and REST
APIs as well as the tmsh API where required.

These modules are freely provided to the open source community for automating
BIG-IP device configurations using Ansible. Support for the modules is provided
on a best effort basis by the F5 community. Please file any bugs, questions or
enhancement requests using `Github Issues`_

Requirements
------------

* `Ansible 2.2.0 or greater`_
* Advanced shell for user account enabled
* `bigsuds Python Client 1.0.4 or later`_
* `f5-sdk Python Client, latest available`_

Documentation
-------------

All documentation is hosted on `ReadTheDocs`_.

When `writing new modules`_, please refer to the
`Guidelines`_ document.

Purpose
-------

The purpose of this repository is to serve as a **staging ground** for Ansible
modules that we would prefer to have upstreamed over the course of time.

The modules in this repository **may be broken** due to experimentation
or refactoring

Your ideas
----------

We are curious to know what sort of modules you want to see created. If you have
a use case and can sufficiently describe the behavior you want to see, open
an issue here and we will hammer out the details.

Copyright
---------

Copyright 2015-2016 F5 Networks Inc.


Support
-------

See `Support <SUPPORT.rst>`_.

License
-------

GPL V3
~~~~~~
See `License`_

Contributor License Agreement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Individuals or business entities who contribute to this project must
have completed and submitted the `F5 Contributor License
Agreement <http://f5-ansible.readthedocs.org/en/latest/development/cla_landing.html>`_
to Ansible_CLA@f5.com prior to their code submission being included
in this project.


.. |slack badge| image:: https://f5ansible.herokuapp.com/badge.svg
    :target: https://f5ansible.herokuapp.com/
    :alt: Slack

.. _Guidelines: https://f5-ansible.readthedocs.io/en/latest/development/guidelines.html
.. _writing new modules: https://f5-ansible.readthedocs.io/en/latest/development/writing-a-module.html
.. _ReadTheDocs: https://f5-ansible.readthedocs.io/en/latest/
.. _bigsuds Python Client 1.0.4 or later: https://pypi.python.org/pypi/bigsuds/
.. _f5-sdk Python Client, latest available: https://pypi.python.org/pypi/f5-sdk/
.. _Ansible 2.2.0 or greater: https://f5-ansible.readthedocs.io/en/latest/usage/getting_started.html#installing-ansible
.. _Github Issues: https://github.com/F5Networks/f5-ansible/issues
.. _License: https://github.com/F5Networks/f5-ansible/blob/master/LICENSE