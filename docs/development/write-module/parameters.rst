Parameters
==========

The ``Parameters`` topic is more broad than just a single class. Therefore, in this section,
only the ``Parameters`` base class will be discussed. There are concrete classes that inherit
from this base class and they are discussed in the sections listed below.

.. toctree::
   :maxdepth: 1
   :includehidden:
   :caption: Concrete Parameters

   api-parameters
   module-parameters

The Parameters base class
-------------------------

Each module has a class named ``Parameters``. This class is a base class
for the more specialized ``ApiParameters`` and ``ModuleParameters`` classes. The purpose of
this base class is to provide functionality and data that is used in both of the specialized
classes.

The ``Parameters`` classes implementation is a little boiler plate mixed with several module-specific changes. This means that for this tutorial (and for any custom modules that you
may write in the future) it is almost certain that you will be changing parts of it.

For the tutorial's module, please refer `to this link`_ for the correct source code for the
module's ``Parameters`` class. Replicate this implementation in the tutorial's module.

The Parameters class boilerplate
--------------------------------

The implementation of the ``Parameters`` class contains some boilerplate code. Let's look
at that boilerplate and what it means.

The top-of-class variables
``````````````````````````

Each ``Parameters`` class defines several class variables.

+------------------+-------------------------------------------------------------------------+
| Variable         | Purpose                                                                 |
+==================+=========================================================================+
| api_map          | This is a dictionary (use ``{ ... }`` form) that maps API Parameter     |
|                  | attribute names to property names used internally by the module.        |
|                  | This functions as a quick way for the module developer to define a      |
|                  | series of ``property`` variables that require no form of manipulation   |
|                  | when they are received from the API. There are many resource attributes |
|                  | that play well with the user of the API, but they vary from API to API. |
+------------------+-------------------------------------------------------------------------+
| api_attributes   | This is a list of attributes for the resource being modified **as they  |
|                  | are named in the API**. This is used when generating the return value   |
|                  | that the ``api_params`` method returns. Nearly every module should have |
|                  | this class parameter defined. The value of this list will vary with the |
|                  | module. ``name`` and ``partition`` attributes are not defined here.     |
+------------------+-------------------------------------------------------------------------+
| updatables       | This is a list of attributes that should be updatable. The list         |
|                  | contains **internal** attribute names; i.e., the ``property`` values    |
|                  | that the developer uses within the module. This list is also used by    |
|                  | the ``Difference`` class to determine which attributes should be        |
|                  | compared during an update.                                              |
+------------------+-------------------------------------------------------------------------+
| returnables      | This is a list of properties that you want to return to the user after  |
|                  | the module finishes running. The names in this list are sent to the     |
|                  | ``ReportableChanges`` class, as well as received back from that class   |
|                  | (after appropriate formatting).                                         |
+------------------+-------------------------------------------------------------------------+

The top-of-class variables should always be defined (even if they are empty) because they are
used through the module.

Common properties
`````````````````

This module's ``Parameters`` class has several ``@property`` definitions included in it. These
are **not** a requirement for all modules. Instead, putting the properties here allows those
properties (and their return values) to be used in both the ``ApiParameters`` and
``ModuleParameters`` automatically.

.. note::

   Be sure to *only* put properties here that are 100% common to the API and Module parameters
   classes. Even a slight deviation in return values among code in the different parameters
   classes can cause issues.

Some of the common properties that *this* module has (but that others may not) are:

* ``name``
* ``description``
* ``policy``

Conclusion
----------

The general ``Parameters`` should only be used for the things that are truly generic between
the ``ApiParameters`` and ``ModuleParameters`` classes. The most common of these are the
top-of-class variables. Links to deeper dives on the concrete classes are listed at the top
of this topic. Use them as an introduction to those classes and their purpose in the module.

.. _to this link: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py#L231
