Parameter classes
=================

The modules make use of a Parameter class that acts as a rudimentary two-way adapter.
This class adapts data in the following ways,

* Ansible module parameters submitted by the user into REST API attributes
* REST API attributes into Ansible module parameters for comparison and internal
  data structures.

This method has served most modules well, for a number of modules though, the
abstraction has been difficult to work with. This largely stems from instances where,

* The `api_map` maps resource attribute names to Ansible module parameter names which
  are similarly named but have wildly different values
* When a name conflict results in not knowing "how to best" determine if you are
  dealing with the API's values or the Module's values. We have side-stepped this
  problem in certain situations by checking for the existence of the `kind` key and
  comparing it to what we know to be the _real_ `kind` key for the resource
* We need to include resource attributes in the `updatables` key because there is no
  other way to get them into the `api_params` method. The error is doing this even
  if that `updatables` addition is not an Ansible module parameter. The `updatables`
  list is intended to be a list of **only** Ansible module parameter names.
* It has been difficult to do Difference engine comparisons if the values that need
  to be compared (API values) are not in the `updatables` array because only those
  values are diff'd.

In an attempt to settle the difficulty of using the "big adapter", as I lovingly call
it, a different pattern is being tested where different classes (inheriting from a
`Parameters` base class) will be used for the Ansible module parameters
(`ModuleParameters`) and the REST API parameters (`ApiParameters`).

Additionally, the base `Parameters` class will be changing its base definition to
remove the `__getattr__` definition that it has. This definition has introduced an
added layer of difficulty when debugging problems because it implicitly swallows
and errors that may be raised by invalid "dot" attribute access. For example,
`self.want.baz` where exceptions raised in `baz` may be swallowed. The only indication
that this has happened is that a post `q.q` call will never happen.

For example,

.. code-block:: python

   ...
   q.q("started here")
   self.want.baz   # <-- raises exception internally
   q.q("ended here")

In the above (when the situation that I described above happens) the second `q.q` call
will never happen. There will be no entry in the `q` log file location, but success of
the module may actually happen! This is a can of worms, so we need to eliminate it
before we regret it.

The base `Parameters` class will also have it's signature changed from,

.. code-block:: python

   def __init__(self, params=None):

to a version that allows for a free-form of parameters and selectively chooses "special"
parameters to do key things with. The new signature is,

.. code-block:: python

   def __init__(self, *args, **kwargs):

This allows us to expand on what the "valid" kwargs to the init method are. To begin
with, there are two args that the base `Parameters` classes will know about. They are,

* `params`
* `client`

The former is no different than the way things work today; the exception being that
you will need to be explicit when supplies params to a `Parameters` derived class
because `params` is no longer just assumed to be the default. To change you code, would
require the following be done,

.. code-block:: python

   # legacy version
   self.want = Parameters(self.client.module.params)

be changed to

.. code-block:: python

   # current version
   self.want = ModuleParameters(params=self.client.module.params)

The later `client` parameter is new to the `Parameters` base class. In existing code
bases it is possible to add this functionality to your concrete `Parameter` classes,
but it is not obvious how, nor well-documented.

For example, today the following would need to be accomplished,

.. code-block:: python

   self.want = Parameters()
   self.want.client = self.client
   self.want.update(self.client.module.params)

This will be able to be changed to the following,

.. code-block:: python

   self.want = ModuleParameters(
       client=self.client,
       params=self.client.module.params
   )

Any concrete params class that inherits from the `Parameters` base class will be able
to use the method show above.

The `client=` feature seems like it was added only to make the above easier and more
explicit. That, however, was more an unintended consequence than a goal. The *real*
purpose for doing the above was for the following

* BIG-IQ
* Unit tests (for BIG-IQ)

.. note::

   My assumptions here are based on the work that others have done in this area.
   When I wrote this, I did not have first-hand experience with BIG-IQ; only the
   iWorkflow codebase (which was originally a fork of BIG-IQ).

You see, the BIG-IQ code-base will require situations where the concrete `Parameters`
classes themselves will be responsible for reading data from the remote device.

This is because, in many circumstances, we cannot know all of the resources and their
attributes that we need to deal without, without querying for data using a resource
attribute itself as input.

Surprisingly, we know this is going to be a problem, because we've already experienced
it. Where? In iWorkflow.

You see, iWorkflow's REST API was created from a fork (long ago in a galaxy far far
away) of an older BIG-IQ code base. Many of the similarities have disappeared over
time, but the one thing that has remained constant is that BIG-IQ's API is one where
you have to do a **HUGE** amount of "extra" work to just do what you need to do.

That means that concrete Parameters will need to do this work so that the user does
not need to. For example, you're setting yourself up for failure if you plan on
using `Postman` to work with your BIG-IQ. Good luck with that. The Ansible modules
deliberately provide a layer of "niceness" that you simply do not get with direct
API communication.

But that's A-OK, because all that direct API stuff and what concrete class needs to
have a client really all boils down to "implementation details". The developers (you
because you're reading this) need to worry about it; the users do not.
