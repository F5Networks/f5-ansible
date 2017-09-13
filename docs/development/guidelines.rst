Guidelines
==========

Guidelines are written for you, the contributor, to understand what we expect
from our contributors and to provide guidance on the direction we are taking
the modules.

Getting Started
---------------

Since Ansible 2.2, it is a requirement that all new F5 modules are written to
use the ``f5-sdk``.

Prior to 2.2, modules may of been written in ``bigsuds`` or ``requests`` (for
SOAP and REST respectively). Modules written using ``bigsuds`` can continue to
be extended using it.

Backward compatibility of older modules should be maintained, but because
``bigsuds`` and ``f5-sdk`` can co-exist, it is recommended that all future
features be written using ``f5-sdk``.

BIG-IP's have two API interfaces; SOAP and REST. As a general rule of thumb,
the SOAP API should be considered deprecated. While this is not an official
stance from F5, there is clearly more of a push in the REST direction than
the SOAP direction.

New functionality to the SOAP interface continues to be added, but only
under certain circumstances.

Bug fixing
----------

If you are writing a bugfix for a module that uses ``bigsuds``, you should
continue to use ``bigsuds`` to maintain backward compatibility.

If you are adding new functionality to an existing module that uses ``bigsuds``
but the new functionality requires ``f5-sdk``, you may add it using ``f5-sdk``.

Naming your module
^^^^^^^^^^^^^^^^^^

Base the name of the module on the part of BIG-IP that the modules
manipulates. (A good rule of thumb is to refer to the API being used in the
``f5-sdk``).

Don't further abbreviate names - if something is a well known abbreviation
due to it being a major component of BIG-IP, that's fine, but don't create
new ones independently (e.g. LTM, GTM, ASM, etc. are fine)

Adding new features
-------------------

If a module that you need does not yet exist, it is equally likely that the
REST API in the f5-sdk has also not yet been developed. Please refer to the
following github project

* https://github.com/F5Networks/f5-common-python

Open an Issue with that project to add the necessary APIs so that a proper
Ansible module can be written to use them.

Using f5-sdk
------------

The following guidelines pertain to how you should use the f5-sdk in the
modules that you develop. We'll focus on the most common scenarios that
you will encounter.

Importing
^^^^^^^^^

Wrap ``import`` statements in a try block and fail the module later if the
import fails.

f5-sdk
""""""

.. code-block:: python

   try:
       from f5.bigip import ManagementRoot
       from f5.bigip.contexts import TransactionContextManager
       HAS_F5SDK = True
   except ImportError:
       HAS_F5SDK = False

   def main():

      if not HAS_F5SDK:
         module.fail_json(msg='f5-sdk required for this module')

You might ask yourself "Why am I doing this?".

The answer is because of the way that Ansible tests PRs that are made against
their source. There are automated tests that run specifically against your module,
using an environment where none of your module's dependencies are installed.

Therefore, without the appropriate exception handlers, your PR will fail to
pass when these upstream tests are run.

Example tests include, but are not limited to,

* ansible-test sanity --test import --python 2.6
* ansible-test sanity --test import --python 2.7
* ansible-test sanity --test import --python 3.5
* ansible-test sanity --test import --python 3.6

Connecting to a BIG-IP
^^^^^^^^^^^^^^^^^^^^^^

Connecting to an F5 product is handled for you automatically. You can control
which product you are communicating with by changing the appropriate value in
your `ArgumentSpec` class.

For example, to specify that your module is one that communicates with a BIG-IP,
The minimum viable `ArgumentSpec` you can write is illustrated below.

.. code-block:: python

   class ArgumentSpec(object):
       def __init__(self):
           self.argument_spec = dict()
           self.f5_product_name = 'bigip'

Note the special key `f5_product_name`. By changing this value, you are able to
change the `ManagementRoot` which will be provided to your module.

The following is a list of allowed values for this key

* bigip
* bigiq
* iworkflow

Inside your module, the `ManagementRoot` is contained in the `ModuleManager`
under the `self.client.api` object.

Use of the object is done in the same way that you work normally use the
`ManagementRoot` of an F5-SDK product.

For example, the code snippet below illustrates a "normal" method of using the
F5-SDK

.. code-block:: python

   mr = ManagementRoot("localhost", "admin", "admin", port='10443')
   vs = mr.tm.ltm.virtuals.virtual.load(name='asdf')

The equivalent Ansible module code is shown below

.. code-block:: python

   # Assumes you provided "bigip" in your ArgumentSpec
   vs = self.client.api.tm.ltm.virtuals.virtual.load(name='asdf')

Exception Handling
^^^^^^^^^^^^^^^^^^

If an exception is thrown, it is up to you decide how to handle it.

For raising exceptions the exception class, `F5ModuleError`, provided with the
`f5-sdk` is used exclusively. It can be used as such.

.. code-block:: python

   # Module code
   ...

   try:
       result = self.want.api.tm.ltm.pools.pool.create(foo='bar')
   except iControlUnexpectedHTTPError as ex:
       raise F5ModuleError(str(ex))

   ...
   # End of module code

In all cases which you encounter it, it is correct to catch internal exceptions
and re-raise them (if necessary) with the `F5ModuleError` class.

Code compatibility
------------------

The python code underlying the Ansible modules should be written to be
compatible with both Python 2.7 and 3.

The travis configuration contained in this repo will verify that your modules
are compatible with both versions. Use the following cheat-sheet to write
compatible code.

* http://python-future.org/compatible_idioms.html

Automated testing
-----------------

It is recommended that you use the testing facilities that we have paired with
this repository. When you open PR's, our testing tools will run the PR against
supported BIG-IP versions in our testing facilities.

By doing using our test harnesses, you do not need to have your own devices or
VE instances to do your testing (although if you do that's fine).

We currently have the following devices in our test harness

* 12.0.0 (BIGIP-12.0.0.0.0.606)
* 12.1.0 (BIGIP-12.1.0.0.0.1434)
* 12.1.0-hf1 (BIGIP-12.1.0.1.0.1447-HF1)
* 12.1.0-hf2 (BIGIP-12.1.0.2.0.1468-HF2)
* 12.1.1 (BIGIP-12.1.1.0.0.184)
* 12.1.1-hf1 (BIGIP-12.1.1.1.0.196-HF1)
* 12.1.1-hf2 (BIGIP-12.1.1.2.0.204-HF2)
* 12.1.2 (BIGIP-12.1.2.0.0.249)
* 12.1.2-hf1 (BIGIP-12.1.2.1.0.264-HF1)
* 13.0.0 (BIGIP-13.0.0.0.0.1645)
* 13.0.0-hf1 (BIGIP-13.0.0.1.0.1668-HF1)

The above list runs the risk of becoming outdated because the actual source of
truth can be found here
