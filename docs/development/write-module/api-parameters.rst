.. _api-parameters-label:

ApiParameters class
===================

The ``ApiParameters`` class is one of two major Adapter-based classes that routinely appears
in the F5 Modules for Ansible. This class acts as a translation layer, or adapter
between the data received from the API and the data used in the module.

For this tutorial, you should `navigate to the appropriate section`_ of the stable 2.5 source
code and copy it into your working module at the same location that it exists in the stable
branch.

The rest of this section discusses implementation details of this class.

Internal methods
----------------

Adapter classes like ``ApiParameters`` may have any number of internal methods added to them.

In this module's implementation, the class has one method: ``_remove_internal_keywords``.
Adding new internal methods is a great way to tease out common functionality that you may want to reuse across a wide variety of modules.

The quintessential example is the ``fq_name`` method. You know it is common, because if you
remember back to the :doc:`import block <import-block>` section, it was included in one of the imports:

.. code-block:: python

   from ansible.module_utils.network.f5.common import fq_name

The history of this particular function goes back to the earliest days of the F5 module code.
In fact, its original implementation was not written by F5, but by customer contributors before
F5 ever became involved.

This method is used to combine a resource's name and its partition. This behavior is
common, and affects *every* resource on the device. Therefore, it was a great
candidate for inclusion in the common methods.

This same process of deducing what is common, and then re-using it across modules,
typically begins with internal methods.

Ansible's means of supporting this inclusion is through the ``module_utils`` area of Ansible.

What should you do in situations where your method may apply to a small subset of modules, but not all
modules? It turns out that Ansible can support that too. The ``module_utils`` directory contains
a number of sub-directories; one of them is delegated for use by F5.

Inside F5's directory (conveniently called ``f5``), module developers may add more files for
use in common subsets of modules. Examples might be "the GTM modules", or "the monitor modules."
The combinations may vary, but including them is all the same.

Suppose there was a common function used in all monitor-related modules. This
function is only relevant to monitors though. It makes no sense to include it in all
modules. The result is that the developer may create a new file in F5's ``module_utils``
directory called ``monitors.py`` and inside of that file, put the implementation of the
function.

Usage of this method could then be done in the monitor-related modules, like this.

.. code-block:: python

   from ansible.module_utils.network.f5.monitors import the_function

Where ``the_function`` is replaced with the name of the function.

Write as many internal methods as you need.

@property methods
-----------------

When it comes right down to it, the entirety of the functionality of the ``ApiParameters``
class is encapsulated in the numerous ``@property`` methods that it exposes.

These methods are used whenever you call the name of the property via the ``self.have`` object.
This object **is** the ``ApiParameters`` class. You should make sure that you have as many
properties as needed to make your development easier.

All ``ApiParameters`` inherit an additional, special, piece of functionality, which is,
they can be populated by the ``api_map``. If you'll remember back to the previous section
on the base ``Parameters`` class, one of the top-of-class variables was the ``api_map``
variable. The ``ApiParameters`` class is where this variable is most useful because it will
auto-map the API resource attribute name to the ``@property`` you specify.

Some modules implement additional ``@property`` methods that are neither mapped to the API
nor provided by the module user. The reason this is done (usually) is to get a simpler
view of data that either the API or the user provide. This simpler implementation is then used
for comparisons for validity checks.

Looking deeper into an @property method
---------------------------------------

To illustrate an example of a ``@property`` method, consider the ``actions`` property. The
implementation of this property is:

.. code-block:: python

   @property
   def actions(self):
       result = []
       if self._values['actions'] is None or 'items' not in self._values['actions']:
           return [dict(type='ignore')]
       for item in self._values['actions']['items']:
           action = dict()
           self._remove_internal_keywords(item)
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

Remember that the purpose of a the ``ApiParameters`` adapter is to take the content from the
API and translate it to something that is usable in the module.

The API representation of this action data is a list of dictionaries:

.. code-block:: javascript

   {
       "kind": "tm:ltm:policy:rules:actions:actionscollectionstate",
       "selfLink": "https://localhost/mgmt/tm/ltm/policy/~Common~sdfg/rules/foo/actions?ver=13.1.0",
       "items": [
           {
               "kind": "tm:ltm:policy:rules:actions:actionsstate",
               "name": "0",
               "fullPath": "0",
               "generation": 62,
               "selfLink": "https://localhost/mgmt/tm/ltm/policy/~Common~sdfg/rules/foo/actions/0?ver=13.1.0",
               "code": 0,
               "expirySecs": 0,
               "forward": true,
               "length": 0,
               "offset": 0,
               "pool": "/Common/dfgh",
               "poolReference": {
                   "link": "https://localhost/mgmt/tm/ltm/pool/~Common~dfgh?ver=13.1.0"
               },
               "port": 0,
               "request": true,
               "select": true,
               "status": 0,
               "timeout": 0,
               "vlanId": 0
           }
       ]
   }

The adapter needs to take this payload and turn it into something that the module can use.
A lot of thought needs to go into the "that the module can use" part, because there is no
prescribed way of handling data.

The developer of this module needed to know about what was stored in the API so that they could do an accurate comparison. These things were outlined back in
the ``DOCUMENTATION`` blob that you wrote. If you'll remember, that data was the following:

.. code-block:: yaml

   actions:
     description:
       - The actions that you want the policy rule to perform.
       - The available attributes vary by the action, however, each action requires that
         a C(type) be specified.
       - These conditions can be specified in any order. Despite them being a list, the
         BIG-IP does not treat their order as anything special.
       - Available C(type) values are C(forward).
     suboptions:
       type:
         description:
           - The action type. This value controls what below options are required.
           - When C(type) is C(forward), will associate a given C(pool) with this rule.
           - When C(type) is C(enable), will associate a given C(asm_policy) with
             this rule.
           - When C(type) is C(ignore), will remove all existing actions from this
             rule.
         required: true
         choices: [ 'forward', 'enable', 'ignore' ]
       pool:
         description:
           - Pool that you want to forward traffic to.
           - This parameter is only valid with the C(forward) type.
       asm_policy:
         description:
           - ASM policy to enable.
           - This parameter is only valid with the C(enable) type.

This documentation tells us that the module intends to receive an ``actions`` argument.
Inside this argument will be a list. Each item in the list will be a dictionary containing
a required ``type`` key, and then one of the two other keys: either ``pool``, or
``asm_policy``.

So we know that the data we want to compare with should look something like this in terms
of its Python representation.

.. code-block:: python

   [
     {
       'type': '...',
       'pool': '...'
     },
   ]

   or

   [
     {
       'type': '...',
       'asm_policy': '...'
     },
   ]

Additionally, the data could possibly be a combination of the above, because policies allow
this. Perhaps something like this:

.. code-block:: python

   [
     {
       'type': '...',
       'pool': '...'
     },
     {
       'type': '...',
       'asm_policy': '...'
     },
   ]

Python lets us compare dictionaries pretty easily using their tuple representations, so
let's assume that we want to make the API data reflect the data structure shown above.

To do this, we need to know the ``type``, and one of two values: either the ``pool`` or
``asm_policy``. It turns out that the action payload shown earlier actually contains this
information. Furthermore, we can see that the ``actions`` ``@property`` converts the JSON
payload to a dict that resembles the intended data structure above.

First, because the module data structure wants a list, the method sets the ``result`` local
variable to a Python empty list. This allows the method to then add values to the list later.

Next, the method checks to see if either of two conditions are true:

- Is the ``actions`` attribute of the LTM policy rule missing? If it is, its value will be
  Python's ``None`` value.
- Is the ``actions`` attribute missing the ``items`` key? Earlier, in the JSON payload, you
  saw that the actions payload will have three top-level keys: ``kind``, ``selfLink``, and
  ``items``. If the ``items`` value is missing, then there are no actions to be taken.

If either of the above conditions are met, the method immediately returns a single item list
with the one item being set to a dictionary with a ``type`` key whose value is ``ignore``.
This is the internal representation for how the module detects an ``ignore`` type.

If the above does not happen, the method can safely assume that it has a number of actions
that need to be discovered and formatted into usable dictionaries.

On the ``for item...`` line, it iterates over each of these ``items``.

During iteration, the method will be determining the ``actions`` that can be deduced from
the original JSON payload. Therefore, it creates a new local variable named ``actions`` and
sets its value to an empty dictionary. If it is able to intuit actions from this payload,
they will go in this variable.

Next, the module removes any keywords that it deems internal, from the current action in
the ``items`` list.

After removing internal (i.e., useless to the module) keywords, the method makes a judgement
call about the ``type``. This judgement call also says a lot about which ``type``s the module
supports.

The two decisions are:

- Does the current action have an attribute named ``forward``?
- Does the current action have an attribute named ``enable``?

If either of those two rules is met, then the current action is added to the local ``action``
variable, a ``type`` key is added that is specific to the ``type`` that the method found,
and the original key that was used to determine the type is deleted from the local action
variable. The last step is done to prevent any polluting of what is returned by the method.

Finally, the local action variable is appended to the local ``result`` list.

The final action of the method before returning the result to the caller is that it sorts
all of the entries in the local ``result`` variable by the ``name`` key of the item in the
``result`` list.

This is a **very important** step because it ensures that any future comparisons will be
done on lists that are in the same order. When determining "difference," it is not enough
to assume that all items in a list have the same value. *Order* of that list is just as
important in certain circumstances. Those circumstances are usually when the data on the
BIG-IP itself is *un*ordered.

If BIG-IP does not consider order important for a particular resource, then the module
developer **must** consider it important. This is because when there is no order, the users
are not expecting there to be any order, and therefore, can arrange things in any way they
want. For the module developer, this is a problem because all of the following are technically
the same:

.. code-block:: python

   [1, 2, 3, 4]
   [2, 3, 1, 4]
   [4, 3, 2, 1]

The module then, is responsible for assuming that all values can possibly be unordered, and
ordering them sanely for comparison.

Contrast this with a situation where the above **is** ordered. Then, each one of those lists
is a different value. And a comparison of one order would fail against another order-- i.e., if
the customer changes the order of an ordered list, it implies their desire to change the
order of the values in the BIG-IP.

Rules in a policy are a great example of this. The *rules* have order. However the *actions*
and *conditions* in that rule have no order.

Conclusion
----------

Understanding and using the ``ApiParameters`` class is a core tenant of understanding
the F5 Modules for Ansible. From here, you may want to go back and consider exploring the
twin of this class (but which operates on the user's side): the ``ModuleParameters`` class.

.. _navigate to the appropriate section: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py#L271
