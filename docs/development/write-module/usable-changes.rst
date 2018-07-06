Usable Changes
==============

The first of the two ``Changes`` classes that can be encountered in a module's execution is
the ``UsableChanges`` class. The implementation of this class for the module being developed
in this tutorial `can be found here`_.

Purpose
-------

The general purpose of all the ``Changes`` classes is to serve as a place for massaging data.
The ``UsableChanges`` class is responsible for massaging data that is about to be sent to the API.

This class implements an Adapter pattern, similar to the Adapter patterns that were implemented
by the ``ApiParameters`` and ``ModuleParameters`` classes. Because you have already worked with
those classes, you should be more than familiar with what needs to happen in this class.

Additionally, because this class is nothing more than another Adapter, its implementation is
completely optional. It will exist as a stub in your module by default. It is your responsibility
to implement it as needed.

What sort of data do you need to adapt at this point in the module?

Consider the implementation that is found in the module that is being studied here.

Implementation
--------------

Let's look at one of the adapted properties in this class. The other is largely similar in purpose
and function, so we'll skip it. You should, however, implement it for completeness in your copy of
the module.

.. code-block:: python

   @property
   def actions(self):
       if self._values['actions'] is None:
           return None
       result = []
       for action in self._values['actions']:
           if 'type' not in action:
               continue
           if action['type'] == 'forward':
               action['forward'] = True
               del action['type']
           elif action['type'] == 'enable':
               action['enable'] = True
               del action['type']
           elif action['type'] == 'ignore':
               result = []
               break
           result.append(action)
       return result

Remember that earlier it was mentioned that the purpose of these classes is to adapt data
immediately before it hits the wire. This module made use of an ``actions`` property that was
observed in the different ``Parameters`` classes, and even the ``Difference`` class.

For the module to have done its work, it needed to create an internal representation of the data
to do things like comparison. It did this in the ``Parameters`` classes. Now that the comparison
is done though, it needs to send those updates to the BIG-IP. The internal data format, though, is
unlikely to be the same as the data format expected by BIG-IP.

Therefore, this adapter for the ``actions`` property is tasked with converting the internal
representation of the data back into a format that is capable of being handled by the F5 device.

In the implementation here, you can see that key names are being changed to the ones that are known
to the API. Additionally, data is being deleted from the existing dictionaries so that it is not
accidentally sent to the API. Were it sent, the API would raise an exception and the module would
fail.

Received values
---------------

The values that are received by the ``UsableChanges`` are those that were output by the
``Difference`` class. You can see this at work in the ``_update_changed_options`` method of the
``ModuleManager`` class.

For example:

.. code-block:: python

   if changed:
       self.changes = UsableChanges(params=changed)

Where ``changed`` is the dictionary produced by multiple calls to the ``Difference`` class's
``compare`` method.

Conclusion
----------

You're now aware of this class's place in the pipeline, and prior to that knowledge, you already
had a firm understanding of the purpose of the various adapters in the module.

It's not always necessary to implement this class. Indeed, in a good API, you will never need
to be concerned with this class. Situations that warrant it usually involve complex data types
that needed to be compared.

In the next section, we'll look at the ``UsableChanges`` counter-class, the ``ReportableChanges``.

.. _can be found here: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py#L483
