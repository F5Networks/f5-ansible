Guidelines
==========

Follow these guidelines when developing F5 modules for Ansible.

Which API to use
----------------

Since Ansible 2.2, all new F5 modules must use the ``f5-sdk``.

Prior to 2.2, modules used ``bigsuds`` (SOAP) or ``requests`` (REST).

You can continue to extend modules that use ``bigsuds``, in order to maintain backward compatibility of older modules. ``bigsuds`` and ``f5-sdk`` can co-exist, but F5 recommends that you write all new features, and fix all bugs by using ``f5-sdk``.


Module naming convention
------------------------

Base the name of the module on the part of BIG-IP that the module manipulates. A good rule of thumb is to refer to the API the ``f5-sdk`` uses.

Don't further abbreviate names. If something is a well-known abbreviation because it is a major component of BIG-IP, you can use it, but don't create new ones independently (e.g., LTM, GTM, ASM, etc. are fine).

Adding new APIs
---------------

If a module you need does not exist yet, the REST API in the ``f5-sdk`` may not exist yet.

Refer to the following GitHub project to determine if the REST API exists:

- https://github.com/F5Networks/f5-common-python

If you want F5 to write an API, open an issue with this project.

Using the f5-sdk
----------------

Follow these guidelines for using the ``f5-sdk`` in the modules you develop. Here are the most common scenarios that you will encounter.

Importing
^^^^^^^^^

Wrap ``import`` statements in a try block and fail the module later if the import fails.

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


You might wonder why you are doing this.

The answer is that Ansible runs automated tests specifically against your module, and they use an environment that doesn't include your module's dependencies.

Therefore, without the appropriate exception handlers, your PR will fail to pass when Ansible runs these upstream tests.

Example tests include, but are not limited to:

- ansible-test sanity --test import --python 2.6
- ansible-test sanity --test import --python 2.7
- ansible-test sanity --test import --python 3.5
- ansible-test sanity --test import --python 3.6

Connecting to a BIG-IP
^^^^^^^^^^^^^^^^^^^^^^

Connecting to an F5 product is automatic. You can control which product you are communicating with by changing the appropriate value in your `ArgumentSpec` class.

For example, to specify that your module is one that communicates with a BIG-IP, here is the minimum viable `ArgumentSpec`:

.. code-block:: python

   class ArgumentSpec(object):
       def __init__(self):
           self.argument_spec = dict()
           self.f5_product_name = 'bigip'

Note the special key `f5_product_name`. By changing this value, you are able to change the `ManagementRoot` that your module uses.

The following is a list of allowed values for this key:

- bigip
- bigiq
- iworkflow

Inside your module, the `ManagementRoot` is in the `ModuleManager` under the `self.client.api` object.

Use the object in the same way that you normally use the `ManagementRoot` of an ``f5-sdk`` product.

For example, this code snippet illustrates a "normal" method of using the ``f5-sdk``:

.. code-block:: python

   mr = ManagementRoot("localhost", "admin", "admin", port='10443')
   vs = mr.tm.ltm.virtuals.virtual.load(name='asdf')

The equivalent Ansible module code is:

.. code-block:: python

   # Assumes you provided "bigip" in your ArgumentSpec
   vs = self.client.api.tm.ltm.virtuals.virtual.load(name='asdf')

Exception handling
^^^^^^^^^^^^^^^^^^

If the code throws an exception, it is up to you to decide how to handle it.

For raising exceptions, use the exception class, `F5ModuleError`, provided with the `f5-sdk`, exclusively.

.. code-block:: python

   # Module code
   ...

   try:
       result = self.want.api.tm.ltm.pools.pool.create(foo='bar')
   except iControlUnexpectedHTTPError as ex:
       raise F5ModuleError(str(ex))

   ...
   # End of module code

In all cases in which you encounter it, it is correct to catch internal exceptions and re-raise them (if necessary) with the `F5ModuleError` class.

Python compatibility
--------------------

The Python code underlying the Ansible modules should be compatible with both Python 2.7 and 3.

The Travis configuration contained in this repo will verify that your modules are compatible with both versions. Use the following cheat-sheet to write compatible code.

- http://python-future.org/compatible_idioms.html

Automated testing
-----------------

F5 recommends that you use the testing facilities paired with this repository. When you open PR's, F5's testing tools will run the PR against supported BIG-IP versions.

Because F5 has test harnesses, you do not need your own devices or VE instances to test (although if you do that's fine).

F5 currently has the following devices in the test harness:

- 12.0.0 (BIGIP-12.0.0.0.0.606)
- 12.1.0 (BIGIP-12.1.0.0.0.1434)
- 12.1.0-hf1 (BIGIP-12.1.0.1.0.1447-HF1)
- 12.1.0-hf2 (BIGIP-12.1.0.2.0.1468-HF2)
- 12.1.1 (BIGIP-12.1.1.0.0.184)
- 12.1.1-hf1 (BIGIP-12.1.1.1.0.196-HF1)
- 12.1.1-hf2 (BIGIP-12.1.1.2.0.204-HF2)
- 12.1.2 (BIGIP-12.1.2.0.0.249)
- 12.1.2-hf1 (BIGIP-12.1.2.1.0.264-HF1)
- 13.0.0 (BIGIP-13.0.0.0.0.1645)
- 13.0.0-hf1 (BIGIP-13.0.0.1.0.1668-HF1)
