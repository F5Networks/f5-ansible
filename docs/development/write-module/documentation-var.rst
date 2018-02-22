DOCUMENTATION variable
======================

The first chunk of code that you will insert describes the module. It names which
parameters it accepts, who the authors/maintainers are, its dependencies, and a variety
of other things.

.. note::

   This area of the module is near the top, but note that you were not instructed to
   change anything else near the top. This is because when fleshing out a stub, there
   is a lot of boilerplate included for you automatically.

   This actually makes writing modules easier! You no longer need to concern yourself
   with writing this boilerplate; only changing it as necessary. This can really shorten
   your development time for a module that uses a good API.

The ``f5ansible`` tool created all of what you see, but you are concerned right now with
only documenting this module. The stub includes some of that work for you. For example,

.. code-block:: python

   DOCUMENTATION = r'''
   ---
   module: {{ module }}
   short_description: __SHORT_DESCRIPTION__
   description:
     - __LONG DESCRIPTION__.
   version_added: 2.6
   options:
     name:
       description:
         - Specifies the name of the ... .
       required: True
   extends_documentation_fragment: f5
   author:
     - Tim Rupp (@caphrim007)
   '''

While this is a good start (and even completely valid) it is not helpful at all. Earlier
I mentioned that you do not need to pay attention to the document file that was created
by the ``f5ansible`` tool. The reason why is because **this** documentation you see here
is what is going to be used to generate the online docs.

It's critical that this documentation here reflect what the module is intended to do, as
well as what it actually does.

Below is a paste of all of the code that you should enter into your own copy of the
``bigip_policy_rule`` module. We'll cover its different sections once you have completed
that.

.. code-block:: python

   DOCUMENTATION = r'''
   ---
   module: bigip_policy_rule
   short_description: Manage LTM policy rules on a BIG-IP
   description:
     - This module will manage LTM policy rules on a BIG-IP.
   version_added: 2.5
   options:
     description:
       description:
         - Description of the policy rule.
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
     policy:
       description:
         - The name of the policy that you want to associate this rule with.
       required: True
     name:
       description:
         - The name of the rule.
       required: True
     conditions:
       description:
         - A list of attributes that describe the condition.
         - See suboptions for details on how to construct each list entry.
         - The ordering of this list is important, the module will ensure the order is
           kept when modifying the task.
         - The suboption options listed below are not required for all condition types,
           read the description for more details.
         - These conditions can be specified in any order. Despite them being a list, the
           BIG-IP does not treat their order as anything special.
       suboptions:
         type:
           description:
             - The condition type. This value controls what below options are required.
             - When C(type) is C(http_uri), will associate a given C(path_begins_with_any)
               list of strings with which the HTTP URI should begin with. Any item in the
               list will provide a match.
             - When C(type) is C(all_traffic), will remove all existing conditions from
               this rule.
           required: true
           choices: [ 'http_uri', 'all_traffic' ]
         path_begins_with_any:
           description:
             - A list of strings of characters that the HTTP URI should start with.
             - This parameter is only valid with the C(http_uri) type.
     state:
       description:
         - When C(present), ensures that the key is uploaded to the device. When
           C(absent), ensures that the key is removed from the device. If the key
           is currently in use, the module will not be able to remove the key.
       default: present
       choices:
         - present
         - absent
     partition:
       description:
         - Device partition to manage resources on.
       default: Common
   extends_documentation_fragment: f5
   requirements:
     - BIG-IP >= v12.1.0
   author:
     - Tim Rupp (@caphrim007)
   '''

The first key take-away from this documentation blob is that the order of the keys is
completely irrelevant.

This is a variable in Python that contains a string that is formatted in YAML. YAML
has a number of data structures that it supports; one of those being a *dictionary*.

Dictionaries are unordered. What is useful about a dictionary is that you can refer to
values in a dictionary by their keys, or names. The above documentation blob is one large
dictionary containing a number of other datatypes.

Most documentation variables have a common set of keys and only differ in the values of
those keys.

Commonly-used keys are:

* ``module``
* ``short_description``
* ``description``
* ``version_added``
* ``options``
* ``notes``
* ``requirements``
* ``author``
* ``extends_documentation_fragment``

.. note::

   The ``extends_documentation_fragment`` key is special as it automatically injects the
   variables ``user``, ``password``, ``server``, ``server_port``, and ``validate_certs``
   into your documentation. You should use it for all modules.

Documentation header
--------------------

Starting at the top, we include the following

.. code-block:: python

   module: bigip_policy_rule
   short_description: Manage LTM policy rules on a BIG-IP
   description:
     - This module will manage LTM policy rules on a BIG-IP.
   version_added: 2.5

This set of documentation tells you

- What the name of the module is.
- Provides a title for the module as will be seen in Ansible's documentation.
- Provides an area for a more full description of what the module is used for, including
  its capabilities and limitations.
- The version that the module was added to Ansible.

If you were developing your own module (and not re-creating an existing one) you would
want to change these fragments to reflect your situation.

A note on raw string literals
-----------------------------

Take special note of how the string content of this variable is *started*. There is
an ``r`` character before the string. What is that?

When an ``r`` character prefixes a string, Python considers that string a "raw" string
literal.

Alex Martelli has a `great explanation of this on Stack Overflow`_.

::

  A "raw string literal" is a slightly different syntax for a string literal, in which a
  backslash, \, is taken as meaning "just a backslash" (except when it comes right before
  a quote that would otherwise terminate the literal) -- no "escape sequences" to represent
  newlines, tabs, backspaces, form-feeds, and so on. In normal string literals, each
  backslash must be doubled up to avoid being taken as the start of an escape sequence.

What this means is that nowhere in the string do you need to do things like escape
characters.

Consider the string "C:\Users\John Smith\Documents\test.txt"

This variable contains documentation, so you would want to present that full string to
a user when they were reading the documentation. Python, however, will interpret the
``\`` characters as an escape sequence and will attempt to escape them for you when
rendering the documentation. The above example would ``print()`` in Python as

::

  C:\Users\John Smith\Documents   est.txt

Which is definitely not what a user expects. By attaching the ``r`` character though, the
documentation renders like this instead.

::

  C:\Users\John Smith\Documents\test.txt

This is much more likely what you want the documentation to look like. So always use ``r``
strings for the documentation related variables at the top of a module. These include,

* ``DOCUMENTATION``
* ``EXAMPLES``
* ``RETURN``

If you do, you will never need to worry about escape sequences.

Specifying options (parameters)
-------------------------------

Next up there are a series of options,

.. code-block:: python

   options:
     description:
       description:
         - Description of the policy rule.
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
           required: True
           choices: [ 'forward', 'enable', 'ignore' ]
         pool:
           description:
             - Pool that you want to forward traffic to.
             - This parameter is only valid with the C(forward) type.
         asm_policy:
           description:
             - ASM policy to enable.
             - This parameter is only valid with the C(enable) type.
     policy:
       description:
         - The name of the policy that you want to associate this rule with.
       required: True

I've only selected a few here so-as to touch upon the key points.

First, the top-level key for this block is called ``options``. Yours should be the same.
This is how Ansible knows to report this section of documentation in the module's parameters
table.

The first parameter that is listed above is the ``description`` parameter. It itself has
a ``description`` field which describes what the purpose of the ``description`` parameter
is.

The next parameter is one called ``actions``. Like the previous parameter, this one also
has a ``description`` field that describes what its purpose in the module it. In fact, it
has many descriptions.

This is actually a recommended way of writing documentation bits about your parameter.
You may have many thoughts about what a parameter does. Instead of cramming them into one
long line, it is recommended that you define them as a list (indicated by the leading hyphen).

This parameter has another field; ``suboptions``. This field, itself, acts in the same
was as the top-level ``options`` field does. It allows you to define a series of fields that
can be specified to the parameter. This is a great way to spell out what is *exactly* required
by the parameter. It is also a great way to enforce compliance with input. Were these not here,
the user may expect that they need to provide a free-form string of data when providing
the ``actions``. Such as,

.. code-block:: python

   actions: Are these actions that I put here?

Instead, however, the ``suboptions`` tells the user that the module will ``require`` the field
``type``, and can optionally accept a ``pool`` field and ``asm_policy`` field. Each of those
fields themselves has their own documentation. The end result is that the user will know
that their ``action`` will resemble the following when used in a playbook.

.. code-block:: python

   # one possible option
   actions:
     - type: enable
       asm_policy: foo-policy

   # another possible option
   actions:
     - type: pool
       pool: my-pool

   # another possible option
   actions:
     - type: ignore

Now, you have not yet *codified* that enforcement, but you *have* made known to the user
your plan on doing so. This is a great approach.

The final parameter in the snippet above is the ``policy`` parameter. Note that it is similar
to the first parameter (``description``) but it includes another field; ``required``.

Ansible does not require you to specify ``False`` or ``default: None`` in either your
documentation or ``ArgumentSpec`` (we'll get to that). It does, however, require that
you specify truthiness. Therefore, since this parameter will be required by the module,
we specify in the documentation that it is indeed required.

If you leave anything out
-------------------------

Note that Ansible upstream has several rules for their documentation blocks.
At the time of this writing, some of the rules are,

- If a parameter is *not* required, **do not** include a ``required: false`` field in the
  parameter's ``DOCUMENTATION`` section.
- A period (.) must be placed at the end of all sentences.
- The ``short_description`` field **does not** end with a period.
- The ``version_added`` field **must** match the current ``devel`` version of Ansible
  if the module is a new module.
- If you are adding new parameters to an *existing* module, then those parameters must
  have a ``version_added`` field that matches the current ``devel`` version of Ansible.

There are a number of other rules that Ansible enforces. All of them will be checked for
when you attempt to upstream a new module.

Conclusion
----------

This puts in place the first important part of the module. It gets you thinking on what
you want in the module, as well as what is even possible. Since a module will be flagged
as incorrect if any of this information is wrong or missing, it is also a great way to
ensure that *all modules have user facing documentation*.

Turn the page to continue with the tutorial, where we will cover the next section of the
module.

.. _great explanation of this on Stack Overflow: https://stackoverflow.com/a/2081708
