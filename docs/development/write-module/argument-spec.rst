The ArgumentSpec
================

The ``ArgumentSpec`` defines which arguments your module will accept.

Earlier, when you were writing the ``DOCUMENTATION`` variable, you identified the arguments to the module and the values those arguments took.

Now is the time you would concern yourself with implementing the code that reflects this documentation.

The ``ArgumentSpec`` is your opportunity to turn documentation into code that you will provide to Ansible.

Ansible has the ability to parse these arguments and provide a small set of enforcement
checks to them. It determines what needs to be checked by virtue of the ``ArgumentSpec`` class
you provide to it.

First, here is a look at the ``ArgumentSpec`` class for this module.

.. code-block:: python

   class ArgumentSpec(object):
       def __init__(self):
           self.supports_check_mode = True
           argument_spec = dict(
               description=dict(),
               actions=dict(
                   type='list',
                   elements='dict',
                   options=dict(
                       type=dict(
                           choices=[
                               'forward',
                               'enable',
                               'ignore'
                           ],
                           required=True
                       ),
                       pool=dict(),
                       asm_policy=dict()
                   ),
                   mutually_exclusive=[
                       ['pool', 'asm_policy']
                   ]
               ),
               conditions=dict(
                   type='list',
                   options=dict(
                       type=dict(
                           choices=[
                               'http_uri',
                               'all_traffic'
                           ],
                           required=True
                       )
                   ),
                   path_begins_with_any=dict()
               ),
               name=dict(required=True),
               policy=dict(required=True),
               state=dict(
                   default='present',
                   choices=['absent', 'present']
               ),
               partition=dict(
                   default='Common',
                   fallback=(env_fallback, ['F5_PARTITION'])
               )
           )
           self.argument_spec = {}
           self.argument_spec.update(f5_argument_spec)
           self.argument_spec.update(argument_spec)

The ArgumentSpec class
----------------------

The class is located near the bottom of the module. It is by convention that the F5 module
developers put it there. This location is not a technical requirement, but you are required
to follow it per the coding conventions that F5 has established.

Looking at the body of this class, you'll note that it only consists of an ``__init__()``
method. This class has no purpose outside of encapsulating the requirements that it will
deliver to Ansible. Therefore, it typically has no real functionality.

The order in which the code is written, however, is of deep importance. Let's take a look
at that.

The check_mode declaration
--------------------------

Typically, the first thing you find in an ``ArgumentSpec`` class is the creation of an
instance variable named ``supports_check_mode``. This is *almost always* ``True``.

Check mode lets the Ansible user ask a module to run without doing anything to a device. It's a way for the user to know (before they run Ansible in non-check mode) that the module is going to change something on their system.

A deficiency of this feature though, is that it is not implemented in Ansible core. It is
instead left to the will of the module developer whether or not to support this functionality.

The end result is that most modules do not use it, and therefore, it is not a feature you can rely on.

This doesn't mean that F5 needs to perpetuate the problem though. The F5 module
developers, by default, expect that a module should support check mode. There are very few
cases where it is impossible, or impractical, to support it.

This instance variable is how the module declares that it will support it. Later on in the
module, the F5 developers will add the implementation of the support.

The argument_spec
-----------------

The ``argument_spec`` is the body of what defines the arguments your module can accept. You'll
notice that is is nearly a complete reflection of what was specified in the ``DOCUMENTATION``
variable earlier.

.. note::

   This variable is *not* an instance variable; it has no ``self.`` attached to
   it. This is important for unit testing. When unit tests are written and run, they
   usually begin with an ``import`` of the ``ArgumentSpec`` class from the appropriate
   module being tested.

   If the module were only ever declaring and updating an instance variable, then the unit
   tests would begin failing.

   For example, when running many module unit tests, the developer might see the first module's
   tests pass, but then the second module's tests fail with errors that mention that
   a mutual exclusivity is being violated. This may sound weird, but is actually very common.

   The cause is the global instance of the ``ArgumentSpec`` class being re-used. And this
   problem manifests itself in particular when you are maintaining an instance variable.

   One test may use one of the mutually-exclusive properties; it sets it in the
   ``ArgumentSpec``. The next test tries to use the other, but since the ``ArgumentSpec``
   is re-used, the first property was never cleared. Now you have both properties (which
   are mutually exclusive) being set to a value. This is an error, and your tests will
   fail.

   Putting the arguments in a local variable prevents this, because that variable is
   destroyed between runs of the tests and usage of the ``ArgumentSpec``.

After the argument spec is locally defined, another variable is created and set to an
empty dictionary value.

This variable is named identically to the first, except this time it is an instance
variable. The module always sets this to an empty ``dict`` to ensure that no collisions
happen between unit tests.

Next, this instance variable is updated with all of the parameters in the base argument
spec that was imported at the top of the module. This gives the ``ArgumentSpec`` all of
the common parameters such as ``user``, ``password``, and ``server``.

Finally, the instance variable is updated with **this** module's arguments. The order to
this updating is important, because it gives the module authors the ability to override
any of the parameters that are defined in the base parameter configuration.

Conclusion
----------

This is one of the easier classes to write because you have largely done all the work when
you wrote the ``DOCUMENTATION`` variable earlier.

With this class out of the way, the next class to explore is the ``ModuleManager``
class. This class is the traffic cop of the module. The stubbing tool provides a boilerplate
version of this class to you. You, as the developer, are expected to replace certain key
instances of API calls in it.
