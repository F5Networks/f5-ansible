Writing a module
================

The following tutorial explains how to create an F5 module for Ansible. During the course of
this tutorial, we will explore what is necessary to re-create the ``bigip_policy_rule``
module, as released in Ansible 2.5. This module is a core part of LTM Policy manipulation
and, therefore, a crucial component of BIG-IP automation.

This tutorial is split up into a number of different sections to keep the document
from becoming overwhelming. Feel free to jump to any section for a reference. Otherwise,
your next stop will be at the first item below.

The module that you will be re-creating is considered an advanced module. It is, however,
the one that illustrates using all pieces of the current coding conventions. So it is
useful to see the standards in their completeness instead of illustrating many different
modules.

.. toctree::
   :maxdepth: 1
   :includehidden:
   :caption: Writing a module

   requirements
   stubbing-module-fragments
   documentation-var
   examples-var
   import-block
   argument-spec
   module-manager
   parameters
   difference
   changes
   main-function
   testing

General module design
---------------------

Throughout this document, the subject of module development for F5 Modules for Ansible will
be discussed. As the tutorial probes deeper into what composes a module, it may become
difficult to follow code and visualize how things are connected.

To address this problem, please take note of the image below.

.. image:: f5-ansible-module-diagram.png

This image provides a 50,000 ft view of what is happening when a module executes. In general,
the module is a pipeline that moves from the left side of the diagram to the right side of
the diagram. It is recommended that you keep this diagram nearby as the tutorial moves on
to more code-heavy topics.
