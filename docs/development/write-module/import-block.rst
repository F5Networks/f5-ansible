.. _import-block-label:

The import block
================

The next section of the module is the block of code where the imports happen.

This code usually just involves importing the ``module_utils`` helper libraries, but may
also include imports of other libraries if you are working with legacy code.

For this module, the import block is:

.. code-block:: python
   :linenos:

   from ansible.module_utils.basic import AnsibleModule
   from ansible.module_utils.basic import env_fallback
   from ansible.module_utils.six import iteritems

   HAS_DEVEL_IMPORTS = False

   try:
       # Sideband repository used for dev
       from library.module_utils.network.f5.bigip import HAS_F5SDK
       from library.module_utils.network.f5.bigip import F5Client
       from library.module_utils.network.f5.common import F5ModuleError
       from library.module_utils.network.f5.common import AnsibleF5Parameters
       from library.module_utils.network.f5.common import cleanup_tokens
       from library.module_utils.network.f5.common import fq_name
       from library.module_utils.network.f5.common import f5_argument_spec
       HAS_DEVEL_IMPORTS = True
   except ImportError:
       # Upstream Ansible
       from ansible.module_utils.network.f5.bigip import HAS_F5SDK
       from ansible.module_utils.network.f5.bigip import F5Client
       from ansible.module_utils.network.f5.common import F5ModuleError
       from ansible.module_utils.network.f5.common import AnsibleF5Parameters
       from ansible.module_utils.network.f5.common import cleanup_tokens
       from ansible.module_utils.network.f5.common import fq_name
       from ansible.module_utils.network.f5.common import f5_argument_spec

In 90% of cases, this code is boilerplate and you can ignore it when writing a module.
The ``f5ansible`` command takes care of this for you.

Let's take a moment to walk through some of the things you see here and explain their
purpose.

AnsibleModule import
--------------------

This import is at line #1 above.

.. code-block:: python

   from ansible.module_utils.basic import AnsibleModule

This import makes available to the module all of the utilities and convenience functions that Ansible provides to modules written in Python.

This module is defined `in Ansible here`_. This code will change over time, so you may need
to visit the file location itself on Ansible's ``devel`` branch.

All F5 modules should include this line because it is used in the body of the ``main()``
method of the module. Its purpose is to consume the module's ``ArgumentSpec`` class and
provide back to the module a list of parameters that have been parsed and verified to meet
the spec.

env_fallback import
-------------------

This import is at line #2 above.

This import is used by any modules that support a ``partition`` argument. Its purpose is to
provide access to environment variables for parameters to "fall back" to in the event that
the parameter is not provided directly to the module.

Normally, all of these environment fallbacks are defined in the F5 ``common.py`` module util
file. The partition one is the exception though, because it is **not** a common parameter.

Consider APIs of the BIG-IP that change system-level resources, like SSHD configuration or the
management IP of the BIG-IP. Modules like these have no reason to offer a ``partition``
parameter to the user. Therefore, ``partition`` is not common across *all* modules, and is
not included in the ``common.py`` module utils. Each module that can use a partition is
expected to define that parameter in its ``ArgumentSpec``.

Various helper import
---------------------

These imports are the other imports that remain outside of the import ``try`` block. In this
module, that means line #3.

Modules can make use of a number of helper libraries that ship with Ansible. This module
makes use of the ``iteritems`` function to provide dictionary iteration that is compatible
across both Python 2.x and 3.x.

This illustrates another concern that modules have; that they should support older and newer
Python versions.

This commitment enables the users of F5 modules to gradually move off of older Python versions
over time.

HAS_DEVEL_IMPORTS definition
----------------------------

This import happens on or around line #5. In this module's case, it happens exactly at
line #5.

When working with an Ansible module, there is a convention that constant-like things be
defined in all capital letters. This is seen in most situations when the module author is
interested in checking that an import happened, or did not happen.

The same thinking applies here.

The F5 module developers maintain a side-band repository that contains all of the F5 module
code. In fact, the documentation you're reading is maintained in there, and you cloned that
side-band repository to work on the module in this tutorial.

Due to the way the developers structure their code, they want to be able to do all of the
module development without requiring that they move all of their code directly to Ansible.

This variable is defined so that they can know (during debugging) that they are indeed
importing code from their side-band repository, and not from the Ansible installation that
is on their system.

By default, this value is ``False``. It assumes that you are *not* running from the
side-band codebase. This value is set to boolean ``True`` when you are. Which leads us
to the next import area.

The dev/prod import try block
-----------------------------

This series of imports start at, or around, line #7 and continues for some time. In this
module's case, it starts at line #7 and continues to line #33.

This large block of imports is actually a couple of things.

First, remember back to the previous section where the ``HAS_DEVEL_IMPORTS`` was first
defined. The first set of imports in this ``try`` block is the module's attempts to load
those.

The reason that the modules tries its development libraries first is that, were the developers
to try to import the second block, the second block would **always** succeed. This is because
the second block's imports are always defined; they are part of Ansible.

However, the developers need to test and do their development. So the module tries to
import the development code (part of the side-band repository) first. This allows the
developers to do their work without messing up anything in their installed copy of Ansible.
It also allows them to do work in their own side-band source repository. Otherwise, they
would need to do development directly in the Ansible repository.

When Ansible ships, this code will fail to import, but that's not a problem. The module
will catch this failing behavior, and instead, try to import what it considers to be the
*production* imports. In other words, what comes installed with Ansible. This is nearly
always guaranteed to succeed.

.. note::

   This may fail when a newer copy of the module is run on an older copy of
   Ansible. In this case, the older copy may be missing things that were defined in the
   newer Ansible. The F5 modules should always be run on the newest version of Ansible
   to prevent this from occurring.

What is imported in the try block?
----------------------------------

These try blocks are a mixture of support libraries that the Ansible module will use.
Most of these libraries are standard across all F5 modules. Also, you'll notice that
the actual imported things are nearly identical, except for the path leading up to them.

For example:

.. code-block:: python

   from library.module_utils.network.f5.bigip import HAS_F5SDK

versus:

.. code-block:: python

   from ansible.module_utils.network.f5.bigip import HAS_F5SDK

In both cases, the ``HAS_F5SDK`` variable is attempted to be imported. It is the location
of this variable that changes. The first attempt is in the side-band repository. The
second attempt is in Ansible core.

Key imports to recognize
------------------------

Some of the imports that are made are *crucial* for the module to execute correctly. The
imports and their purposes are outlined below.

+-------------------------+---------------------------------------------------------------------+
| Imported item           | Comment                                                             |
+=========================+=====================================================================+
| ``HAS_F5SDK``           | This variable that tells the module if the f5-sdk was found on your |
|                         | Ansible controller. This variable may be overridden shortly in a    |
|                         | subsequent import check.                                            |
+-------------------------+---------------------------------------------------------------------+
| ``F5Client``            | This variable contains a connection to your F5 device (BIG-IP,      |
|                         | BIG-IQ, etc).                                                       |
+-------------------------+---------------------------------------------------------------------+
| ``F5ModuleError``       | This is a general purpose ``Exception`` class that all F5 modules   |
|                         | use when something "bad" happens in them. It is raised for          |
|                         | situations when F5 is aware that something troubling can happen.    |
|                         | F5 does not catch, nor raise, Python's base ``Exception`` exception |
|                         | because this may suppress problems that occur that we are *not*     |
|                         | aware of. The developers want to be identified of those unknowns.   |
+-------------------------+---------------------------------------------------------------------+
| ``AnsibleF5Parameters`` | This is a base class for the ``Parameters`` class that is used by   |
|                         | all modules. This class includes methods for handling common F5     |
|                         | things such as the method by which the ``Parameters`` class         |
|                         | auto-creates properties for you.                                    |
+-------------------------+---------------------------------------------------------------------+
| ``cleanup_tokens``      | This method is used by all modules to clean up the authentication   |
|                         | tokens that are created during a module's run. If token cleanup is  |
|                         | not done, this can wedge your BIG-IP after hundreds of tokens have  |
|                         | accumulated.                                                        |
+-------------------------+---------------------------------------------------------------------+
| ``fq_name``             | This is a convenience method. Give a ``partition`` and a ``name``.  |
|                         | It will return a ``name`` that is "fully qualified," i.e., includes |
|                         | the partition. This is helpful in situations where users can        |
|                         | specify a name which, itself, is a fully qualified name. For        |
|                         | example, inputs of ``foo`` and ``/Common/foo`` would both return    |
|                         | ``/Common/foo``.                                                    |
+-------------------------+---------------------------------------------------------------------+
| ``f5_argument_spec``    | This returns the base set of arguments that all modules can consume.|
|                         | This is usually combined with module specific arguments to form the |
|                         | final ``ArgumentSpec``.                                             |
+-------------------------+---------------------------------------------------------------------+

Conclusion
----------

The import block at the top of each module has a number of useful things injected into the module.

The next section skips down to the bottom of the file and begins exploring some of the common classes of a module. ``ArgumentSpec`` will be the first class we visit.

.. _in Ansible here: https://github.com/ansible/ansible/blob/2f36b9e5ce0ec41a822752845d3b7c4afdf7eee9/lib/ansible/module_utils/basic.py#L801
