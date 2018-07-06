ModuleParameters class
======================

The ``ModuleParameters`` class is one of two major Adapter-based classes that routinely appears
in the F5 Modules for Ansible. The job of this class is to act as a translation layer, or
adapter between the data received from the user (via Ansible) and the data used in the module.

For this tutorial, you should `navigate to the appropriate section`_ of the stable 2.5 source
code and copy it in to your working module at the same location that it exists in the stable
branch.

The rest of this section discusses implementation details of this class.

Internal methods
----------------

Adapter classes such as ``ModuleParameters`` may have any number of internal methods added to
them.

In this module's implementation, the class has several methods:

* ``_handle_http_uri_condition``
* ``_handle_forward_action``
* ``_handle_enable_action``

As mentioned in the :ref:`api-parameters-label` section, this is an encouraged behavior. Small
functions that handle assist the developer in meeting their goal, are encouraged.

@property methods
-----------------

Like the ``ApiParameters`` class, the ``ModuleParameters`` will also be composed of (module-specific) ``@property`` decorators. The purpose is completely the same as the
``ApiParameters``. This module is an implementation of the Adapter pattern, and therefore,
it should be used to adapt the values that are received from the Ansible module (i.e., the user)
into what is usable inside the module code.

Conclusion
----------

There is nothing specific about the ``ModuleParameters`` class that has not already been
covered in the ``ApiParameters`` content. In a module, the most likely adapter that you
will modify is the ``ModuleParameters`` class. This is because the Ansible
module will often offer arguments that do not map cleanly to the F5 product's API.

In the next section, the ``Difference`` class will be explored in greater detail.

.. _navigate to the appropriate section: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py#L327
