Detecting Configuration Differences
===================================

When it comes to deciding what changes to make to a remote BIG-IP, the majority of the job
falls on the shoulders of the ``Difference`` class (or suite of ``Difference`` classes).
Rectifying an existing config with a provided config can be the most difficult
part of module development.

This section explores the implementation of the ``Difference`` class that is used for the
module we've been working with. We'll also see the module execution that leads up to the
usage of the ``Difference`` class.

You may hear the ``Difference`` class referred to as the ``Difference`` "engine."

Difference class implementation
-------------------------------

The implementation for the module under `development begins here`_. Open this content in a new tab
and begin re-implementing it in the module under development.

The ``Difference`` class will be comparing the *internal module* representations of the
attributes you are interested in. Therefore, it is the *output* of the different adapter
classes. Keep this in mind.

What follows is a deeper dive into the components that make up the ``Difference`` class.

The common methods
------------------

This ``Difference`` class includes a couple of common methods. The base ``Difference`` class
is capable of doing simple, non-typed, key/value comparisons. If this satisfies all of your
needs, then you do not need to implement any further code in this class.

The __init__ method
```````````````````

The first method that a developer will encounter is the ``__init__`` method. There is no
need to change any of the code in this method.

The purpose of the method is to initialize a ``Difference`` object from the class itself.
This method performs a well-defined set of work, respective to this class. In
particular, it sets two instance variables to the values that are passed to the class.

The variables are:

* ``self.want``
* ``self.have``

These names should be familiar, as they are the same ``self.want`` and ``self.have`` that
are used throughout the ``ModuleManager`` class that was explored earlier. When used in the
``Difference`` class, these methods will be the conduit from which you will do comparisons.

The compare method
``````````````````

This method is responsible for deciding whether a comparison should be done by using predefined properties or the default comparison method.

The default comparison method is a simple ``if foo != bar: return foo`` comparison. It does
not take into consideration things like datatypes, where a comparison such as the one done
above might fail.

.. note::

   This underscores an important point about the earlier adapter patterns that were discussed
   in the ``ApiParameters`` and ``ModuleParameters`` classes. When writing the properties in
   these methods, it is imperative that you take comparison into consideration. Doing simple
   things like sorting or type casting your return values can go a **long** way in minimizing
   the problems you would otherwise have when implementing the ``Difference`` class.

For more complex comparisons, implement your own comparison method instead of using the default method. To do this, follow the same methodology that you
followed when writing the ``ApiParameters`` and ``ModuleParameters`` adapters: using the
``@property`` decorator on methods.

You can see this implementation at work in the following method.

.. code-block:: python

   @property
   def actions(self):
       result = self._diff_complex_items(self.want.actions, self.have.actions)
       if self._conditions_missing_default_rule_for_asm(result):
           raise F5ModuleError(
               "The 'all_traffic' condition is required when using an ASM policy in a rule's 'enable' action."
           )
       return result

The above method is concerned with comparing a non-trivial comparison of the ``actions``
property of the ``ApiParameters`` and ``ModuleParameters`` classes. Its implementation
looks pretty simple because most of the heavy lifting is done in other functions. The basic
idea though should drive the point home.

The __default method
````````````````````

This method is the fallback method that is called in the event that there is no user-defined
method with a ``@property`` decorator that matches the property being compared. This
fallback method allows you to avoid common situations involving comparison. For example,
consider the comparison of one description to another. This is clearly a simple task and,
therefore, does not need to have a customer ``@property`` decorated method written for it.

How change is affected
----------------------

How does the ``Difference`` class affect what is returned and used by the module when
updating an API? The answer to that has three components.

First, the return value of any ``@property`` decorated method in the ``Difference``
class should return the value for the API attribute that it wants to change. Any value
these methods return is considered by the Ansible module to be **the** value for the
attribute in the API. The only exception is ``None``. If you return ``None``,
then the API attribute will be filtered out from any further operations.

The second part of the tool chain is handled by the ``_update_changed_options`` method
of the ``ModuleManager``. This method initiates the ``Difference`` object, and also is
responsible for making the calls to ``compare`` to compare. There is a fragment of the
``_update_changed_options`` code that is responsible for checking the return value of the
``compare`` method. The behavior is defined as such:

* If the returned value is a ``dict``, then merge it into the dictionary of ``changed`` properties
* Else, set the ``changed`` dictionary at key ``k`` to the returned value.

This behavior implies that you are able to change *multiple* properties
with a single return value. Furthermore, you can return properties that are not even named
after the key being compared.

Consider the following:

**Simple return**

.. code-block:: python

   # Difference
   @property
   def description(self):
       return "foo"

The above example would result in a ``changed`` dictionary that looks like this.

.. code-block:: python

   changed = {
      'description': 'foo'
   }

**Dictionary return**

.. code-block:: python

   # Difference
   @property
   def description(self):
       return {
          'baz': 1234,
          'bar': '5678'
       }

The above example would result in a ``changed`` dictionary that looks like this.

.. code-block:: python

   changed = {
      'baz': 1234,
      'bar': '5678'
   }

The third part of the tool change is the ``UsableChanges`` class. This will be discussed
further in later sections.

Complex comparison
------------------

For any situation in which the comparison of properties is more complicated than ``x == y``,
the module developer will definitely need to implement their own comparison check.

Consider a property that contains dictionaries. In Python, it is not possible to compare two
dictionaries in their native state. The reason is because dictionaries inherently
have no order.

To perform this comparison, a ``@property`` should be defined in the ``Difference`` class.
The name of the ``@property`` must match the name of the property being compared, as shown in
earlier sections.

It is then the responsibility of the module developer to figure out how to carry out the
differentiation between the two values. Below is a comparison of two dicts
and other comparisons to take into consideration when diff'ing two values.

.. code-block:: python
   :linenos:

   @property
   def records(self):
       # External data groups are compared by their checksum, not their records. This
       # is because the BIG-IP does not store the actual records in the API. It instead
       # stores the checksum of the file. External DGs have the possibility of being huge
       # and we would never want to do a comparison of such huge files.
       #
       # Therefore, comparison is no-op if the DG being worked with is an external DG.
       if self.want.internal is False:
           return None
       if self.have.records is None and self.want.records == []:
           return None
       if self.have.records is None:
           return self.want.records
       result = compare_dictionary(self.want.records, self.have.records)
       return result

This comparison in particular comes from the ``bigip_data_group`` module. Let's take a moment
to go line-by-line through the comparison. This will be a good opportunity to get a sense of
what can, and should, be done in a comparison method.

Ignore the comments at the top and begin at line 9.

.. code-block:: python

   if self.want.internal is False:

This comparison function begins by checking a ``self.want`` variable. In this module's case,
the reason is described in the comment block above the comparison. Remember that
``self.want`` is the data that the user provided to the Ansible module.

Line 10 brings you to a feature of the ``Difference`` class's properties.

.. code-block:: python

   return None

By returning ``None``, the particular property will not be made available to the
``UsableChanges`` class (and, subsequently, won't be sent to the API). The lesson here is that
you should return ``None`` when there is **no change** in the values being compared.

Line 11 contains another comparison, but this comparison is done for a completely different
reason.

.. code-block:: python

   if self.have.records is None and self.want.records == []:

This comparison checks to see if there are:

- No existing records
- No records specified by the user to the module

The equality check with an empty list (``[]``) may be a bit confusing. The reason for a comparison
like this is because the ```ModuleParameters`` returns an empty list when the user specifies
a single empty item in the Ansible module. For example, something like this:

.. code-block:: yaml

   records: ""

This allows the user of the module to zero out the values of records. So this comparison is
essentially checking that there are no existiing records, and that the user specified a single
empty record. Therefore, a no-op, or no change, and the comparison returns what is seen on line
12: ``None``.

On line 13, there is a shortcut in logic for this comparison method.

.. code-block:: python

   if self.have.records is None:

The shortcut is that, if the module has reached this point, and there are no existing records,
no comparison even needs to take place, just return whatever the user specified to the module.

This is a common operation to make when checking parameter difference. There is no reason to
do a comparison in this case because there are no existing records to compare with. The current
order of ``if`` statements to get to this point though, is important. Line 14 is the shortcut
in practice, returning what the user wants.

Finally, on line 15, a serious comparison takes place.

.. code-block:: python

   result = compare_dictionary(self.want.records, self.have.records)

This line illustrates a true comparison of dictionaries. In this case, the module is using a
method called ``compare_dictionary``, found in ``ansible.module_utils.network.f5.common``.
This method allows you to compare dictionaries to find out if there are the same
or different.

Finally, the method here returns the return value from the ``compare_dictionary`` function.
For your information, the return value is the content of ``self.want`` for the property being
compared. In this case, the records the user *wants* will be returned if the
two values differ.

Conclusion
----------

The ``Difference`` class is a core piece of functionality in the F5 Modules for Ansible. It is
responsible for much of the heavy lifting when doing an update of an existing resource. The work
it does, however, can be complicated and prone to error because of this complexity. It is
highly recommended that you utilize unit tests when working on your module's own implementation.

You received a taste of what a more complicated comparison looks like. Future modules will surely
push the limits of what it means to be complicated when comparing values. Over time, it is
expected that patterns and common methods will emerge that makes the process of comparison much
easier for the lay-developer.

In the next section, we'll touch upon the ``Changes`` classes that you will encounter in modules.

.. _development begins here: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py#L522
