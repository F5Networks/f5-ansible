RETURN variable
===============

When a module finishes running, F5 usually wants to report back to the user with the new state
of the module and anything that may be relevant to them.

The general rule of thumb is to return data that is in the same format that the user supplied to the module.

Why is this important?

Parameter consistency and validity
----------------------------------

Imagine, if you will, a scenario where you go to your bank to have a $20 bill broken up
into a smaller denomination of money. For example:

* A $10 bill
* A $5 bill
* And five $1 bills

When you reach the teller and hand them your money, they instead give you back:

* A duck
* A chicken
* A crow

Technically, these are all birds, but combined, they have no relevance to what you put *in*
to the transaction. If you put money in, you expected money out; not various fowl.

The same principal applies with to the F5 Modules for Ansible. If you put in a list of dictionaries,
such as the example below:

.. code-block:: yaml

   actions:
     - type: forward
       pool: pool-svrs

Then it would make sense that after the module completes and makes any changes it deems
necessary, you should receive data back out that is in the same usable form.

Exceptions to the rule
----------------------

Not all information that the user puts in is information that is relevant on its way back
out. For example, the ``state`` variable usually contains information that is not typically
re-used in Ansible.

There are some instances though when the ``state`` is "more" relevant, such as when it contains
more than just ``absent`` and ``present``, such as in the ``bigip_virtual_server`` module.

Another example would be when the module consumes otherwise sensitive information. For example,
the ``bigip_ssl_certificate`` and ``bigip_ssl_key`` modules consume parameters that you
probably do not want echoed back out (like keys and certs). Therefore, we suppress that in
the return value.

One more example is in situations where modules can consume a whole lot of data. For example,
the ``bigip_data_group`` module can consume megabytes or more of data. It makes no sense to
echo all this back out to the user.

RETURN variable for the example module
--------------------------------------

With the above made known, here is the content of the ``RETURN`` variable as it applies to
the module we are in the process of writing.

.. code-block:: python

   RETURN = r'''
   actions:
     description: The new list of actions applied to the rule
     returned: changed
     type: complex
     contains:
       type:
         description: The action type
         returned: changed
         type: string
         sample: forward
       pool:
         description: Pool for forward to
         returned: changed
         type: string
         sample: foo-pool
     sample: hash/dictionary of values
   conditions:
     description: The new list of conditions applied to the rule.
     returned: changed
     type: complex
     contains:
       type:
         description: The condition type
         returned: changed
         type: string
         sample: http_uri
       path_begins_with_any:
         description: List of strings that the URI begins with.
         returned: changed
         type: list
         sample: [foo, bar]
     sample: hash/dictionary of values
   description:
     description: The new description of the rule.
     returned: changed
     type: string
     sample: My rule
   '''

Conclusion
----------

When the Ansible module documentation is generated, these values are output in a table.
You can see an example of the kind of `table that is created here`_. This is the final
documentation-related blob that will be added to the module. Up next, we will cover the
``import`` block.

.. _table that is created here: http://docs.ansible.com/ansible/latest/modules/bigip_pool_module.html#return-values
