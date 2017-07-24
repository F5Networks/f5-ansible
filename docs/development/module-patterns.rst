All properties should read from self._values[key]

All property.setters should write to self._values[key]

The 'key' in the self._values dictionary should match the API resource attribute.
This allows us to easily determine


Deprecating functionality
=========================

In a module, it may be necessary to raise warnings to the user due to deprecated
functionality.

Normally, deprecations are done in the ArgumentSpec, such as when using the
`removed_in_version` key shown below.

.. raw:: python

   type=dict(
       removed_in_version='2.4'
   )

but that is only relevant when the **parameter itself** is deprecated. There are
other deprecation scenarios for instance where the parameter is a list of choices
and the **choices themselves** are deprecated.

For example, consider the following parameter

.. raw:: python

   type=dict(
       choices=['foo_1', 'bar_2', 'baz_3']
   )

One may need to deprecate the values themselves in favor of other values.

.. raw:: python

   type=dict(
       choices=['foo-1', 'bar-2', 'baz-3']
   )

This may seem like a simple thing that one could add code to fix, but doing so would
also lead to an increase in technical debt. Having a mapping of old values to new
values should be considered an anti-pattern and something that is a candidate for
deprecation.

To announce deprecations (for all things) you can use the `removed_in_version` field
mentioned above, but you can also have more customized deprecations raised by your
module.

To do this, begin by amending the `__init__` method of your `Parameters` class to
define a `__warnings` variable.

.. raw:: python

   class Parameters(AnsibleF5Parameters):
       def __init__(self, params=None):
           super(Parameters, self).__init__(params)
           self._values['__warnings'] = []

Next, we need to add a new method to the `ModuleManager`, or, class specific manager
(such as those used when forking logic; ie, `bigip_gtm_pool`)

The definition of this method is the following

.. raw:: python

   def _announce_deprecations(self):
       warnings = []
       if self.want:
           warnings += self.want._values.get('__warnings', [])
       if self.have:
           warnings += self.have._values.get('__warnings', [])
       for warning in warnings:
           self.client.module.deprecate(
               msg=warning['msg'],
               version=warning['version']
           )

The third and final step is to actually make use of the deprecation code that you
set up previously. Do do that, you want to **append** to the aforementioned
`__warnings` field.

An example is show below.

.. raw:: python

   if lb_method in deprecated.keys():
       if self._values['__warnings'] is None:
           self._values['__warnings'] = []
       self._values['__warnings'].append(
           [
               dict(
                   msg='The provided lb_method is deprecated',
                   version='2.4'
               )
           ]
       )

pycodestyle
===========

Your modules should be flake free
    flake8

Your modules should conform to ansible's validate-modules code

Design Patterns
===============

These patterns are intended to

  * make your time spent developing new modules shorter
  * allow you to not need to decide "what to do"
  * allow for easier unit testing
  * allow for customizing the modules to meet edge cases easier
  * allow for customizing the modules to meet feature requests easier
  * allow for customizing the modules to address bug reports easier

If these patterns conflict with the above goals, the patterns should be
re-evaluated and all modules should be changed to support the new patterns.

CRUDable
--------
* bigip_static_route


Only Updatable
--------------
* bigip_snmp


Executable
----------
* bigip_command


CRUDable Reference
------------------
iworkflow_tenant_connector


List item as member
-------------------
* bigip_remote_syslog

Class variables
===============

The following class variables are common attributes that each `Parameters` class
needs to define.

updatables
----------

Specifies a list of `Parameters` properties to that are considered
updatable by the module. This is used when doing `should_update()``
comparisons and setting properties in `self.changes`.

api_attributes
--------------

Specifies a list `Parameters` properties to provide to the `api_params()``
method when generating valid sets of attributes for resources in the REST
API.

You will likely need to write adapter methods that call the properties
used internally by the module when writing these. For example

.. raw:: python

   def minSupportedBIGIPVersion(self):
       return self.min_bigip_version

The reason that we use this method instead of the map method is because
there may be cases where the value used in `api_params()` is not a single
property but a set of properties that need to be combined.

This is used by the `api_params` method to generate a valid set of
attributes to provide to the REST API. Typically this dictionary does
NOT provide the `name` and `partition` parameters. These values should
be specified specifically in the (create|update|delete)_on_device methods

returnables
-----------

    Specifies a list of Parameters properties for the `to_return()` method
    to iterate over when supplying "changed" options back to the user

api_map
-------

We need to have a dictionary or a list of some stuff because there are
times when the API parameters can not be written as methods. For example,
the `bigip_device_dns` APIs parameters include

.. raw:: python

   dns.proxy.__iter__

This attribute is mapped to `forwarders` in the Ansible module.

The pattern that I had been developing is to use methods decorated as
properties in python and then to call those methods when setting values
and getting values.

For example, the "dns.proxy.__iter__" API attribute would be mapped to the
`_values` key "forwarders". Normally I would set the set the API attributes
directly in the dictionary. I would need to get those API specific keys
however when I am returning the values to compare. this makes the getters
for the Module options look messy though.

Next I thought about having the API attributes have their own @property
decorators, but this won't work in the "dns" case mention above.



NEED
a pattern for a single Ansible Option Parameter that returns 2 API attributes.
For example in the bigip_virtual_server module there is an option called
enabled vlans. This, however, actually sets two (possibly 3) values in the API

    * vlans (list
    * vlansDisabled (boolean True)
    * vlansEnabled (boolean True)

what is a pattern that, that supports that?

The pattern is that the api_attributes is an arbitrary list of attributes that
you want to send to the API.

The api_params() method uses this list to iterate over the

param_api_map does not work for situations where the Ansible->API relationship
is 1->n (bigip_virtual_server with enabled_vlans) param_api_map only works
for 1->1

Requirements
  * easy attribute comparison in Ansible parameters format with BIG-IP API values
  * ability to consume API attributes that cannot be written as python functions (dns.proxy.__iter__ for example)

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
==============

Nearly every module (see exceptions) should have the following classes. These
classes are used to support the stated design patterns.

  * Parameters
  * ModuleManager
  * ArgumentSpec

Exceptions to common classes
----------------------------

Exceptions to the above rules will happen when,

  * the API that a particular module addresses, changes underneath it between versions of the software.
  * the resources or collections that the module is manipulating become too numerous

Good examples of this include

  * bigip_ssl_certificate
  * bigip_gtm_wide_ip

Defaulting to None
==================

It should be noted that you should never specify default values in your
`ArgumentSpec`. For example, the following is incorrect

.. raw:: python

   type=dict(
       required=False,
       default='foo'
   ),

But, shouldn't you be using the actual defaults?

  Answer: No

The reason that you provide no defaults is to support cases where the user does not
specify a value for a particular option. If that happens, then you should not step
on that parameter if it is preconfigured.

If a user had a setting that they want to keep and you specified a default value,
then in the first opportunity that they forgot to specify that value, you would
end up replacing that value with your default.

This is a bad idea.

Ansible defaults `required` to `False` and `default` to `None`. Therefore, there is
no need to specify these default values.

What is the layer of @property decorators all about?
====================================================

The ``@property` decorators you see represent an adapter pattern. Inside of the
`ModuleManager`, when data needs to be compared (what you have vs what you want),
that data is returned by these properties in a known format.

The API's resource attributes differ in structure and name from the options that
a user can provide to a module.

For example, an API resource may have an attribute called `minSupportedBIGIPVersion`.
The user facing portion of the module though, may refer to this attribute as
`min_bigip_version`. There are a number of reasons to do this.

  * it provides an abstraction of the API so the name of the thing being modified
    is not closely tied to the implementation of the API.
  * many times the API attribute names are vague, this abstraction makes them more
    clear
  * the Resource Attributes use camelCase variable naming, while some of python
    and nearly all of Ansible use snake_case variable naming.

For future developer clarity's sake, all of the attributes that we are interested
in are typically compared by the option name that they would have in Ansible and
not the Resource attribute name.

This allows a developer to look at the names of variables and match them to the
names of the options in the Ansible module.

While the names of properties usually mirror the names of the module options
available to the user, the values of those properties do not.

Values of the properties reflect the values that are accepted by the API resource.
This is done because, ultimately, the values that we need to deal with at the
values that are going to be used to update the API.

Therefore, when we receive options from the module, we transform them into the
values that would appropriate for the API. When we receive values from the API,
we might order them or cast some of their values to specific types so that
comparisons can occur, but otherwise we dont really touch them.

So,

1. property name reflects module option
2. property getter reflects the appropriate Resource attribute value

Why are they not all setters?
=============================

This is because there are some cases where you do not know ahead of time what
the value of that property should be. Often it takes two or more options be set
before another option can be known.

Consider a module that accepts an IP address option and a gateway mask option,
but needs to return a CIDR representation of those two values. Without getting
both values, we cannot produce the one value. That is who we calculate the
necessary value at time of getattr, and not at the time of setattr.

Use the module_utils test suite to verify AnsibleF5Parameters classes
=====================================================================

This is important in case there is a pattern we miss for adapting API
attributes and module params.

This test suite is found at the following location

  test/misc/test_module_utils.py

Never import *
==============

9 times out of 10 you are doing this because you are using one of the following
variables

* `BOOLEANS`
* `BOOLEANS_TRUE`
* `BOOLEANS_FALSE`

It is, however, an anti-pattern to import from * and it will be caught by the
Ansible unit tests. Instead, specifically include each thing that you want to use.

The Changes class
=================

In many cases, the values that you process from the user will match the values
that you send to BIG-IP.

For example, consider the following parameters to a module

.. raw:: yaml

   - name: This is an example
     bigip_device_sshd:
         banner: "enabled"
         banner_text: "banner text goes here"
         port: "1234"
         password: "secret"
         server: "lb.mydomain.com"
         user: "admin"

Above, the module code that implements this is a collection of different adapters
that collectively allow the module to convert the information the user provides
to it into a format that it is able to send to the BIG-IP and vice-versa.

This class is a way for the module developer to complete the cycle of

  User (params) -> Module -> REST -> Module -> User (changed params)

Due to most of the adapters being concerned with how they should be adapting
data to meet the format expect by the REST API, the `Changes` class is concerned
with how to adapt the data to meet the format expected by the end user.

If there is a need to change the value to something that is more "human" so that
the user can understand it, that job is undertaken by the `Changes` module.

An example of it in use is the `bigip_device_connectivity` module where it acts
as a way to translate BIG-IP's representation of "none" (`any6`) to the human
word "none"

Examples of modules that use the `Changes` class are,

* `bigip_gtm_datacenter`
* `bigip_device_connectivity`
* `bigip_device_group`

The Difference class
====================

When comparing values to detect changed-ness, there are situations where the
default comparison method will not be appropriate for you use. The default comparison
method essentially just does a simple comparison.

The source of this method illustrates its simplicity

.. raw:: python

   attr1 = getattr(self.want, key)
   attr2 = getattr(self.have, key)
   if attr1 != attr2:
       changed[key] = attr1

As you can see, it is quite simple and does not take into consideration anything
more complicated than simply the values being compared.

This differencing is not conducive to more complicated data structures or types of
data.

.. raw:: python

   int(5) == '5'

The above fails to satisfy this simple (albeit erroneous due to established
patterns) difference.

.. note::

   This is logically incorrect because the Adapter pattern that you should be using
   for the `Parameters` class mandates that `@property` values should return a
   specific data type (in the above case `int`) and should never be
   non-deterministic.

To check for differences in more complicated data structures, the module author
should make use of the `Difference` class.

The definition of the `Difference` class is the following

.. raw:: python

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

By default, it does nothing more than uses the simple comparison to diff the
parameters provided, and discovered, by the module.

To make use of it, you must do the following.

First, define this class in your module.

Second, add `@property` methods for each of the values that you want to compare.
Remember, the properties of the `Parameter` classes are the names that are exposed
to the module user and not the names of REST API parameters themselves (unless it
perfectly matches) because the REST API camel-cases all parameter names.

So, if we were interested in providing custom diffing for the `members` module
parameter, we may add this as a `@property` to the `Difference` class like so.

.. raw:: python

   @property
   def members(self):
       if self.want.members is None:
           return None
       if set(self.want.members) == set(self.have.members):
           return None
       if self.want.append is False:
           return self.want.members

       # Checking to see if the supplied list is a subset of the current
       # list is only relevant if the `append` parameter is provided.
       new_members = set(self.want.members)
       current_members = set(self.have.members)
       if new_members.issubset(current_members):
           return None
       result = list(set(self.have.members + self.want.members))
       return result

These `@property` methods **must** be named after the Parameter you want to compare.
Additionally, the return value of these `@property` definitions is one of two values.

- Python `None` if there is no difference
- The value of the difference if there is one. This value will later be reported as
  what was changed in the module invocation.

Finally, to make use of this new difference class, you must change the following
method in the `ModuleManager` code,

* `_update_changed_options`

The new value of this method must include the usage of the `Difference` class as a
new object. Example usage is provided below.

.. raw:: python

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
===============

This adapter pattern is useful for converting data values from user inputs
to REST outputs. It's definition is,

  The API Map Adapter pattern adapts a known REST attribute to a predefined
  `Parameters` method. The return value of this method is a correct payload for
  the REST attribute.

This pattern is frequently used as a way for the module developer to translate
the input provided to them by the user into a format that is consumable by the
REST API.

The following is an example of this kind of adapter.

.. raw:: python

   ...

   api_map = {
       ...

       'bannerText': 'banner_text',

       ...
   }


1-to-1 Adapter
==============

YAML represents the `banner`
parameter as a simple key with a simple value. The actual REST payload contains
an attribute called `banner` and it takes an actual value called `enabled`.
This is represented in code by the `ArgumentSpec` class.

This is considered to be the most simple form of a parameter definition by the
F5 Ansible modules because it is nearly a 1 to 1 translation of Ansible to F5.

The following is an example of this kind of adapter.

.. raw:: python

   ...
       banner_text=dict(
           required=False,
           default=None,
           choices=['enabled', 'disabled']
       ),
   ...
