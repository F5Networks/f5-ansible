CRUDable
========

* bigip_static_route


Only Updateable
===============
* bigip_snmp


Executable
==========
* bigip_command


CRUDable Reference
==================
iworkflow_tenant_connector


List item as member
===================
* bigip_remote_syslog


All properties should read from self._values[key]

All property.setters should write to self._values[key]

The 'key' in the self._values dictionary should match the API resource attribute.
This allows us to easily determine


The module parameters will always include the 'state'. You may not want this in
your returned changes though, so you can filter them with the following

def _filter_outliers(self, params):
    # These parameters are outliers because they have no API equivalent
    # but are still used in the modules to direct the behavior of the
    # module.
    #
    # Additionally, these parameters do not need to be returned to
    # the user if the module reports changes.
    outliers = ['state']
    for key in outliers:
        params.pop(key, None)
    return params



when needing to raise warnings

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
followed by this in the end of exec_module
    def _announce_deprecations(self, result):
        warnings = result.pop('__warnings', [])
        for warning in warnings:
            self.client.module.deprecate(
                msg=warning['msg'],
                version=warning['version']
            )


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

Class variables
===============

updatables:
    Specifies a list of `Parameters` properties to that are considered
    updatable by the module. This is used when doing `should_update()``
    comparisons and setting properties in `self.changes`.

api_attributes:
    Specifies a list `Parameters` properties to provide to the `api_params()``
    method when generating valid sets of attributes for resources in the REST
    API.

    You will likely need to write adapter methods that call the properties
    used internally by the module when writing these. For example

    ```
    def minSupportedBIGIPVersion(self):
        return self.min_bigip_version
    ```

    The reason that we use this method instead of the map method is because
    there may be cases where the value used in `api_params()` is not a single
    property but a set of properties that need to be combined.

    This is used by the api_params() method to generate a valid set of
    attributes to provide to the REST API. Typically this dictionary does
    NOT provide the `name` and `partition` parameters. These values should
    be specified specifically in the (create|update|delete)_on_device methods

returnables
    Specifies a list of Parameters properties for the `to_return()` method
    to iterate over when supplying "changed" options back to the user

param_api_map:
    We need to have a dictionary or a list of some stuff because there are
    times when the API parameters can not be written as methods. For example,
    the bigip_device_dns API's parameters include

        "dns.proxy.__iter__"

    this attributes is mapped to "forwarders" in the Ansible module.

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

Exceptions
~~~~~~~~~~

Exceptions to the above rules will happen when,

  * the API that a particular module addresses, changes underneath it between versions of the software.
  * the resources or collections that the module is manipulating become too numerous

Good examples of this include

  * bigip_ssl_certificate
  * bigip_gtm_wide_ip

Defaulting to None
==================

Why is it that I have to do a lot of this in my ArgumentSpec?

..raw: json

            type=dict(
                required=False,
                default=None
            ),

Shouldn't I be using the actual defaults?

Answer: No

The reason that you provide `default: None` is to support cases where the user
does not specify a value for a particular option.

If that happens, they you should not step on that parameter if it is preconfigured.
This is the reason to set `default: None`. If a user had a setting that they want
to keep and you specified a default value, then in the first opportunity that they
forgot to specify that value, you would end up replacing that value with your
default.

This is a bad idea, so use `None` (not the string "None", but the Python `None`)
to decide if a user has or has not specified something.

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
because there are some cases where you do not know ahead of time what the value of
that property should be. Often it takes two or more options be set before another
option can be known.

Consider a module that accepts an IP address option and a gateway mask option,
but needs to return a CIDR representation of those two values. Without getting
both values, we cannot produce the one value. That is who we calculate the
necessary value at time of getattr, and not at the time of setattr.

Use the module_utils test suite to verify AnsibleF5Parameters classes
=====================================================================

this is important in case there is a pattern we miss for adapting api
attributes and module params


Why is from ansible.module_utils.basic import * included in some modules?
=========================================================================

9 times out of 10 this is because you are using the BOOLEANS, BOOLEANS_TRUE,
or BOOLEANS_FALSE constants in the module.

The Changes class
=================

In many cases, the values that you process from the user will match the values
that you send to BIG-IP.

For example, consider the following parameters to a module

.. raw::yaml

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

.. raw::python

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

.. raw::python

   ...
       banner_text=dict(
           required=False,
           default=None,
           choices=['enabled', 'disabled']
       ),
   ...
