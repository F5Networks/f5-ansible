Reporting Changes
=================

The second of the two ``Changes`` classes that can be encountered in a module's execution is
the ``ReportableChanges`` class. The implementation of this class for the module being developed
in this tutorial `can be found here`_.

Purpose
-------

As mentioned earlier, the general purpose of all the ``Changes`` classes is to serve as a place
for massaging data. The ``ReportableChanges`` class is responsible for massaging data that is
about to be sent back to the user.

This class implements an Adapter pattern, similar to the Adapter patterns that were implemented
by the ``ApiParameters`` and ``ModuleParameters`` classes. Since you have already worked with
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
       result = []
       if self._values['actions'] is None:
           return [dict(type='ignore')]
       for item in self._values['actions']:
           action = dict()
           if 'forward' in item:
               action.update(item)
               action['type'] = 'forward'
               del action['forward']
           elif 'enable' in item:
               action.update(item)
               action['type'] = 'enable'
               del action['enable']
           result.append(action)
       result = sorted(result, key=lambda x: x['name'])
       return result

Remember that earlier it was mentioned that the purpose of these classes is to adapt data
immediately before it returns to the user. This module made use of an ``actions`` property that
was observed in the different ``Parameters`` classes, and even the ``Difference`` class.

For the module to have done its work, it needed to create an internal representation of the data
to do things like comparison. It did this in the ``Parameters`` classes. Now that the comparison
is done though, it has to sent those updates to the BIG-IP. The data format used by the API
though is unlikely to be the same as the data format expected by the user.

Remember that, in the user's world view, they are unaware of:

* The F5 product API data format
* The internal Ansible module representation

The user is only familiar with the format of the parameters sent to the module. This classes
adaptation, therefore, needs to go towards making sure that what was sent to the API is translated
back to what the user is familiar with.

Therefore, this adapter for the ``actions`` property is tasked with converting the API
representation of the data back into a format that is capable of being recognized by the
Ansible user.

In the implementation here, you can see that key names are being changed to the ones that are
known to the user. Additionally, data is being deleted from the existing dictionaries so that
it is not accidentally sent to the user.

Received values
---------------

The values that are received by the ``ReportableChanges`` are those that were contained in the
``UsableChanges`` class. You can see this at work in the ``exec_module`` method of the
``ModuleManager`` class.

For example:

.. code-block:: python

   reportable = ReportableChanges(params=self.changes.to_return())
   changes = reportable.to_return()

Where ``self.changes`` is the ``UsableChanges`` object, and ``to_return`` is a method that
takes the ``returnables`` class variable into account.

Note that the ``returnables`` class variable is defined in the ``ReportableChanges`` class. It
is not always this way. Indeed, you will often find this variable defined in the base
``Parameters`` class. Because the ``ReportableChanges`` ultimately inherits from the base
``Parameters`` class, it is a matter of taste where you put it.

Conclusion
----------

You're now aware of its place in the pipeline, and prior to that knowledge, you already had
a firm understanding of the purpose of the various adapters in the module.

It's not always necessary to implement this class. Indeed, in a good API, you will never need
to be concerned with this class. Situations that warrant it usually involve complex data types
that needed to be converted to representations that the user is familiar with.

In the next section, we'll look at the ``main`` function.

.. _can be found here: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py#L442
