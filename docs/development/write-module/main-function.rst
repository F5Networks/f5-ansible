Main module execution
=====================

At this point in the module's development, the module is largely complete. In this section, we'll
cover one of the boilerplate methods that ships with all the modules; the ``main`` function.

It is not necessary that you implement this function. We cover it here so that you are able to
combine the knowledge of how the module executes, with *where* its execution actually begins.

The main function
-----------------

In the module used for this tutorial, the ``main`` function is defined at the `bottom of the
source code`_.

The implementation of it is almost entirely boilerplate. Here it is.

.. code-block:: python

   def main():
       spec = ArgumentSpec()

       module = AnsibleModule(
           argument_spec=spec.argument_spec,
           supports_check_mode=spec.supports_check_mode
       )
       if not HAS_F5SDK:
           module.fail_json(msg="The python f5-sdk module is required")

       try:
           client = F5Client(**module.params)
           mm = ModuleManager(module=module, client=client)
           results = mm.exec_module()
           cleanup_tokens(client)
           module.exit_json(**results)
       except F5ModuleError as ex:
           cleanup_tokens(client)
           module.fail_json(msg=str(ex))

The operation of this function is as follows.

First, the ``ArgumentSpec`` and the ``AnsibleModule`` classes are initialized. You have seen both
of these in the past, so you should know their purpose.

* ``ArgumentSpec`` defines what the module can do
* ``AnsibleModule`` uses the ``ArgumentSpec`` to validate user input

Next, a series of validations are made on the available libraries used in this module. The
series above only includes one check, but others can be added as necessary. See the section
later in this document that discusses under what circumstances you would want to do this.

Next is the main ``try...except`` block. This exception handling is in place to catch all of the
known **F5 generated** errors. It very specifically does not catch the general Python ``Exception``
class. This is done this way because module developers want bugs reported that are not known to
them already. Handling ``Exception`` though, would prevent those bugs from raising.

The internals of the ``try`` block include the instantiation of the ``F5Client`` object. This
object will be used later for all communication with the F5 product.

.. note::

   When the ``F5Client`` class is instantiated, a connection is **not** immediately made to the
   remote F5 product. This is intentional, because some modules (like ``bigip_wait``) require that this does not
   happen.

The ``ModuleManager`` class is also instantiated here and is given the ``AnsibleModule`` object
as well as the ``F5Client`` object. These will be necessary later when the manager is busy
executing.

Execution of the manager is next using the ``exec_module`` method call. The return value of this
call is what will be returned to the user.

Before that return can take place, however, a function is called to clean up the authentication
tokens on the F5 device.

.. note::

   The ``cleanup_tokens`` method is **not** put in the ``ModuleManager`` because the manager
   can fail in a variety of places due to ``F5ModuleException``'s being raised by error checking
   code. This function must be run **after** manager execution.

Finally, the module cleanly exits with the ``exit_json`` method if everything has gone well.

If failure occurred at any time, the ``except`` block is invoked and a cleanup of authentication
tokens is done. The failing module reports back to Ansible with the ``fail_json`` method of
the ``AnsibleModule`` class.

When to change the main function
--------------------------------

The only time it would be necessary to change the ``main`` function is if you included other
module dependencies that needed to be checked for at runtime.

Note the two lines above, shown here.

.. code-block:: python

   if not HAS_F5SDK:
       module.fail_json(msg="The python f5-sdk module is required")

This series of conditionals would need to be changed if you were, for example, to include the
Python ``netaddr`` module in your work. Any dependencies of the module need to be checked for here
(and fail the module if they are not found) to ensure that the module runs correctly.

Executing main
--------------

The final two lines in your module inform Python to execute the module's code if the script
itself is executable.

.. code-block:: python

   if __name__ == '__main__':
       main()

Because of how Ansible works, when the ``main`` function contacts the remote device (or runs
locally), it is not called if you import the module.

You would import the module if you were using it outside of Ansible, or in some sort of test
environment where you do not want the module to actually run.

Conclusion
----------

This concludes the entirety of the core module development tutorial. If
you followed along and copied code correctly, you should have a functioning module.

In the remaining sections, we'll cover the business of testing: a requirement for F5 module
development.

.. _bottom of the source code: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py#L859
