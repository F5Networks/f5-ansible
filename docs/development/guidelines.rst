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

## Naming your module

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

```python
try:
    from f5.bigip import ManagementRoot
    from f5.bigip.contexts import TransactionContextManager
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

def main():

    if not HAS_F5SDK:
        module.fail_json(msg='f5-sdk required for this module')
```

Connecting to a BIG-IP
^^^^^^^^^^^^^^^^^^^^^^

To connect to a BIG-IP, you should use the instantiate a `ManagementRoot`
object, providing the credentials and options you wish to use for connecting.

#### REST

An example of connecting to big-ip01.internal is shown below.

```python

from f5.bigip import ManagementRoot
from f5.bigip.contexts import TransactionContextManager

mr = ManagementRoot("localhost", "admin", "admin", port='10443')
tx = mr.tm.transactions.transaction

with TransactionContextManager(tx) as api:
    virt = api.tm.ltm.virtuals.virtual.load(name='asdf')
    tcp = virt.profiles_s.profiles.load(name='tcp')
    tcp.delete()
    virt.profiles_s.profiles.create(name='wom-tcp-wan-optimized')
```

Exception Handling
^^^^^^^^^^^^^^^^^^

You should wrap any f5-sdk call in a try block. If an exception is thrown,
it is up to you decide how to handle it but usually calling fail_json
with the error message will suffice.

For raising exceptions you can include the exception class provided with
the f5-sdk. It can be used as such.

```python
try:
    from f5.sdk_exception import F5SDKError
    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False

# Connect to BIG-IP
...

# Make a call to BIG-IP
try:
    result = api.tm.ltm.pools.pool.create(foo='bar')
except F5SDKError, e:
    module.fail_json(msg=e.message)
```

Helper functions
^^^^^^^^^^^^^^^^

The helper functions available to you are included in the Ansible f5.py
module_utils.

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

  * BIG-IP VE 11.6.0
  * BIG-IP VE 12.0.0
  * BIG-IP VE 12.1.0