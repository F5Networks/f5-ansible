Design patterns
===============

These patterns should:

- Make your time spent developing new modules shorter
- Allow you to not need to decide "what to do"
- Allow for easier unit testing
- Allow for customizing the modules to meet edge cases easier
- Allow for customizing the modules to meet feature requests easier
- Allow for customizing the modules to address bug reports easier

If these patterns conflict with the above goals, the patterns should be re-evaluated and all modules changed to support the new patterns.

CRUDable
--------
- bigip_static_route

Only Updatable
--------------
- bigip_snmp

Executable
----------
- bigip_command

CRUDable Reference
------------------
- iworkflow_tenant_connector

List item as member
-------------------
- bigip_remote_syslog

Class variables
---------------

The following class variables are common attributes that each `Parameters` class needs to define.

updatables
``````````

Specifies a list of `Parameters` properties that the module considers updatable. Use this when doing `should_update()` comparisons and setting properties in `self.changes`.

api_attributes
``````````````

Specifies a list `Parameters` properties to provide to the `api_params()` method when generating valid sets of attributes for resources in the REST API.

You will likely need to write adapter methods that call the properties used internally by the module. For example:

.. code-block:: python

   def minSupportedBIGIPVersion(self):
       return self.min_bigip_version

Use this method instead of the map method when the value in `api_params()` is not a single property but a set of properties that you need to combine.

The `api_params` method uses this to generate a valid set of attributes to provide to the REST API. Typically this dictionary does NOT provide the `name` and `partition` parameters.

You should specify these values specifically in the `(create|update|delete)_on_device` methods.

returnables
```````````

Specifies a list of Parameters properties for the `to_return()` method to iterate over when supplying "changed" options back to the user.

api_map
```````

Sometimes you cannot write the API parameters as methods. For example, the `bigip_device_dns` APIs parameters include:

.. code-block:: python

   dns.proxy.__iter__

This attribute is mapped to `forwarders` in the Ansible module.

The pattern is to use methods decorated as properties in Python and then to call those methods when setting values and getting values.

For example, you would map the `dns.proxy.__iter__` API attribute to the `_values` key "forwarders". Normally you would set the API attributes directly in the dictionary. You would get those API-specific keys when you return the values to compare.

This makes the getters for the Module options look messy though.

You could make the API attributes have their own @property decorators, but this won't work in the "dns" case mentioned above.

NEED
a pattern for a single Ansible Option Parameter that returns 2 API attributes.
For example in the bigip_virtual_server module there is an option called
enabled vlans. This, however, actually sets two (possibly 3) values in the API:

- `vlans` (list)
- `vlansDisabled` (boolean True)
- `vlansEnabled` (boolean True)

what is a pattern that, that supports that?

The pattern is that the api_attributes is an arbitrary list of attributes that
you want to send to the API.

The api_params() method uses this list to iterate over the

param_api_map does not work for situations where the Ansible->API relationship
is 1->n (bigip_virtual_server with enabled_vlans) param_api_map only works
for 1->1

Requirements
- Easy attribute comparison in Ansible parameters format with BIG-IP API values
- Ability to consume API attributes that you cannot write as Python functions (dns.proxy.__iter__ for example)

.. code-block:: guess

   params_spec=dict(
            cache='dns.cache',
            forwarders='dns.proxy.__iter__',
            name_servers='nameServers',
            search='search',
            ip_version='include'
        )

        updatables = [
            'cache', 'forwarders', 'name_servers', 'search', 'ip_version'
        ]
    )


Common classes
--------------

Nearly every module (see exceptions) should have the following classes. These classes support the stated design patterns.

- Parameters
- Changes
- Difference
- ModuleManager
- ArgumentSpec

Exceptions to common classes
----------------------------

Exceptions to the above rules will happen when:

- The API that a particular module addresses changes between versions of the software.
- The resources or collections that the module is manipulating become too numerous.

Good examples of this include:

- `bigip_ssl_certificate`
- `bigip_gtm_wide_ip`

Defaulting to None
------------------

You should never specify default values in your `ArgumentSpec`. For example, the following is incorrect:

.. code-block:: python

   type=dict(
       required=False,
       default='foo'
   ),

But, shouldn't you use the actual defaults?

Answer: No

You want to support cases where the user does not specify a value for a particular option. If that happens, then you should not step on that parameter if it is pre-configured.

If a user had a setting that they want to keep and you specified a default value, then the first time they forgot to specify that value, you would end up replacing that value with your default.

Ansible defaults `required` to `False` and `default` to `None`. Therefore, there is no need to specify these default values.

What is the layer of \@property decorators all about?
-----------------------------------------------------

The ``@property`` decorators represent an adapter pattern. Inside the `ModuleManager`, when you need to compare the data, these properties return that data in a known format.

The API's resource attributes differ in structure and name from the options that a user can provide to a module.

For example, an API resource may have an attribute called `minSupportedBIGIPVersion`. However, the user-facing portion of the module may refer to this attribute as `min_bigip_version`.

You should do this because:

- It provides an abstraction of the API so the name of the thing you're modifying is not closely tied to the implementation of the API.
- Many times the API attribute names are vague, and this abstraction makes them more clear.
- The Resource Attributes use camelCase variable naming, while some of Python and nearly all of Ansible use snake_case variable naming.

For clarity's sake, all of the attributes are typically compared by the option name in Ansible and not the Resource attribute name.

This allows you to look at the names of variables and match them to the names of the options in the Ansible module.

While the names of properties usually mirror the names of the module options available to the user, the values of those properties do not.

Values of the properties reflect the values that the API resource accepts. This is because, ultimately, the values you need to deal with are the values that will update the API.

Therefore, when you receive options from the module, you transform them into the values that would appropriate for the API. When you receive values from the API, you might order them or cast some of their values to specific types so that comparisons can occur, but otherwise you don't really touch them.

1. The property name reflects module option.
2. The property getter reflects the appropriate Resource attribute value.

Why are they not all setters?
-----------------------------

Sometimes you do not know ahead of time what the value of that property should be. Often you must set two or more options before you can know the value of another option.

Consider a module that accepts an IP address option and a gateway mask option, but needs to return a CIDR representation of those two values. Without getting both values, you cannot produce the one value.

That is why you calculate the necessary value at time of `getattr`, and not at the time of `setattr`.

Use the module_utils test suite to verify AnsibleF5Parameters classes
---------------------------------------------------------------------

This is important in case there is a pattern you miss for adapting API attributes and module params.

This test suite is here:

- test/misc/test_module_utils.py

Never import *
--------------

Most often, you do this because you are using one of the following variables:

- `BOOLEANS`
- `BOOLEANS_TRUE`
- `BOOLEANS_FALSE`

It is, however, an anti-pattern to import from * and the Ansible unit tests will catch it. Instead, specifically include each thing that you want to use.

The Changes class
-----------------

In many cases, the values that you process from the user will match the values that you send to BIG-IP.

For example, consider the following parameters:

.. code-block:: yaml

   - name: This is an example
     bigip_device_sshd:
         banner: "enabled"
         banner_text: "banner text goes here"
         port: "1234"
         password: "secret"
         server: "lb.mydomain.com"
         user: "admin"

The module code that implements this is a collection of different adapters. Collectively, they allow the module to convert the information the user provides into a format that can the BIG-IP can receive and send.

By using this class, you can complete the cycle:

User (params) -> Module -> REST -> Module -> User (changed params)

Most of the adapters adapt data to meet the format expect by the REST API. Use the `Changes` class to adapt the data to meet the format expected by the end user.

If there is a need to change the value to something that is more "human" so that the user can understand it, that job is undertaken by the `Changes` module.

An example is the `bigip_device_connectivity` module, where it acts as a way to translate BIG-IP's representation of "none" (`any6`) to the human word "none".

Examples of modules that use the `Changes` class are:

- `bigip_gtm_datacenter`
- `bigip_device_connectivity`
- `bigip_device_group`

The Difference class
--------------------

When you compare values to detect changes, sometimes the default comparison method will not be appropriate. The default comparison method essentially just does a simple comparison.

The source of this method illustrates its simplicity:

.. code-block:: python

   attr1 = getattr(self.want, key)
   attr2 = getattr(self.have, key)
   if attr1 != attr2:
       changed[key] = attr1

As you can see, it is quite simple and does not take into consideration anything more complicated than simply comparing the values.

This difference is not conducive to more complicated data structures or types of data.

.. code-block:: python

   int(5) == '5'

The above fails to satisfy this simple (albeit erroneous due to established patterns) difference.

.. note::

   This is logically incorrect because the Adapter pattern you should use for the `Parameters` class mandates that `@property` values return a specific data type (in the above case `int`) and should never be non-deterministic.

To check for differences in more complicated data structures, use of the `Difference` class.

The definition of the `Difference` class is:

.. code-block:: python

   class Difference(object):
       def __init__(self, want, have=None):
           self.want = want
           self.have = have

       def compare(self, param):
           try:
               result = getattr(self, param)
               return result
           except AttributeError:
               return self.__default(param)

       def __default(self, param):
           attr1 = getattr(self.want, param)
           try:
               attr2 = getattr(self.have, param)
               if attr1 != attr2:
                   return attr1
           except AttributeError:
               return attr1

By default, it uses the simple comparison to diff the parameters provided, and discovered, by the module.

To make use of it, you must do the following.

First, define this class in your module.

Second, add `@property` methods for each of the values you want to compare.

Remember, the properties of the `Parameter` classes are the names exposed to the module user and not the names of REST API parameters themselves (unless it perfectly matches), because the REST API camel-cases all parameter names.

To provide custom diffing for the `members` module parameter, you can add this as a `@property` to the `Difference` class:

.. code-block:: python

   @property
   def members(self):
       if self.want.members is None:
           return None
       if set(self.want.members) == set(self.have.members):
           return None
       if self.want.append is False:
           return self.want.members

       # Checking to see if the supplied list is a subset of the current
       # list is only relevant if user provides the `append` parameter
       new_members = set(self.want.members)
       current_members = set(self.have.members)
       if new_members.issubset(current_members):
           return None
       result = list(set(self.have.members + self.want.members))
       return result

These `@property` methods **must** be named after the Parameter you want to compare.

Additionally, the return value of these `@property` definitions is one of two values.

- Python `None` if there is no difference.
- The value of the difference if there is one. Later, the module reports this value as what changed when the module ran.

Finally, to make use of this new difference class, you must change the following method in the `ModuleManager` code:

- `_update_changed_options`

The new value of this method must include the usage of the `Difference` class as a new object. For example:

.. code-block:: python

   def _update_changed_options(self):
       diff = Difference(self.want, self.have)
       updatables =  Parameters.updatables
       changed = dict()
       for k in updatables:
           change = diff.compare(k)
           if change is None:
               continue
           else:
               changed[k] = change
       if changed:
           self.changes = Parameters(changed)
           return True
       return False

API Map Adapter
---------------

This adapter pattern is useful for converting data values from user inputs to REST outputs.

The API Map Adapter pattern adapts a known REST attribute to a predefined `Parameters` method. The return value of this method is a correct payload for the REST attribute.

This pattern is frequently used so you can translate the input provided by the user into a format that the REST API can consume.

Here is an example of this kind of adapter.

.. code-block:: python

   ...

   api_map = {
       ...

       'bannerText': 'banner_text',

       ...
   }


1-to-1 Adapter
--------------

YAML represents the `banner` parameter as a simple key with a simple value. The actual REST payload contains an attribute called `banner` and it takes an actual value called `enabled`.

In code, the `ArgumentSpec` class represents this.

This is the most simple form of a parameter definition by the F5 Ansible modules because it is nearly a 1 to 1 translation of Ansible to F5.

The following is an example of this kind of adapter.

.. code-block:: python

   ...
       banner_text=dict(
           required=False,
           default=None,
           choices=['enabled', 'disabled']
       ),
   ...
