Parameter classes
=================

The modules use a Parameter class that acts as a rudimentary two-way adapter.

This class adapts data in the following ways:

- Ansible module parameters submitted by the user into REST API attributes.
- REST API attributes into Ansible module parameters for comparison and internal data structures.

This method works for most modules. However, there are instances where:

- The `api_map` maps resource attribute names to Ansible module parameter names that are similarly named but have very different values.
- A name conflict results in not knowing if you are dealing with the API's values or the module's values. You can check for the existence of the `kind` key and compare it to what you know to be the _real_ `kind` key for the resource.
- You need to include resource attributes in the `updatables` key because there is no other way to get them into the `api_params` method. The error is doing this even if that `updatables` addition is not an Ansible module parameter. The `updatables` list should be a list of **only** Ansible module parameter names.
- It can be difficult to do Difference engine comparisons if the API values are not in the `updatables` array because only those values are diff'd.

In an attempt to settle the difficulty of using the "big adapter", F5 is testing a different pattern, where different classes (inheriting from a `Parameters` base class) are used for the Ansible module parameters (`ModuleParameters`) and the REST API parameters (`ApiParameters`).

Additionally, the base `Parameters` class will be changing its base definition to remove the `__getattr__` definition that it has. This definition has introduced an added layer of difficulty when debugging problems because it implicitly swallows errors that invalid "dot" attribute access may raise. For example, `self.want.baz` where exceptions raised in `baz` may be swallowed. The only indication that this has happened is that a post `q.q` call will never happen.

For example:

.. code-block:: python

   ...
   q.q("started here")
   self.want.baz   # <-- raises exception internally
   q.q("ended here")

When this situation occurs, the second `q.q` call will never happen. There will be no entry in the `q` log file location, but success of the module may actually happen.

The base `Parameters` class will also have its signature changed from:

.. code-block:: python

   def __init__(self, params=None):

To a version that allows for a free-form of parameters and selectively chooses "special" parameters to do key things with. The new signature is:

.. code-block:: python

   def __init__(self, *args, **kwargs):

This allows you to expand on what the "valid" kwargs to the init method are. To begin with, there are two args that the base `Parameters` classes will know about. They are:

- `params`
- `client`

The former is no different than the way things work today; the exception being that you will need to be explicit when supplying params to a `Parameters` derived class because `params` is no longer just assumed to be the default. Change your code:

.. code-block:: python

   # legacy version
   self.want = Parameters(self.client.module.params)

To:

.. code-block:: python

   # current version
   self.want = ModuleParameters(params=self.client.module.params)

The later `client` parameter is new to the `Parameters` base class. In existing code bases it is possible to add this functionality to your concrete `Parameter` classes, but it is not obvious how, nor well-documented.

For example, you would need to do this:

.. code-block:: python

   self.want = Parameters()
   self.want.client = self.client
   self.want.update(self.client.module.params)

You can change this to the following:

.. code-block:: python

   self.want = ModuleParameters(
       client=self.client,
       params=self.client.module.params
   )

Any concrete params class that inherits from the `Parameters` base class will be able to use the method shown above.

The `client=` feature supports:

- BIG-IQ
- Unit tests (for BIG-IQ)

The BIG-IQ code-base sometimes requires the concrete `Parameters` classes themselves to be responsible for reading data from the remote device.

This is because, in many circumstances, you cannot know all of the resources and their attributes without querying for data using a resource attribute itself as input.
