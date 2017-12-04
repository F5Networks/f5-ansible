Deprecating Modules
===================

F5 sometimes deprecates modules. However, before the modules go away, you should have enough time to upgrade to a new version of Ansible.

New releases of Ansible happen approximately once a quarter.

With this in mind, the following process should allow you between three and six months to upgrade your Ansible installation to the new code.

If you miss this timeframe, you can upgrade incrementally (2.1 -> 2.2 -> 2.3) instead of upgrading directly to the latest version and, in the process, test that the incremental versions work with your playbooks.

Deprecation process
-------------------

Here is a sample deprecation process:

- 2.0 - version to deprecate
- 2.1 - deprecated version
- 2.2 - version with deprecated feature removed

During the second release, you *MUST* insert adequate warnings for the user to see. Ansible highlights warning messages so that they're more visible than regular messages.

Raise deprecated warnings
-------------------------

To raise warnings about deprecated functionality, add the following method to your `ModuleManager` class.

.. code-block:: python

   def _announce_deprecations(self, result):
       warnings = result.pop('__warnings', [])
       for warning in warnings:
           self.client.module.deprecate(
               msg=warning['msg'],
               version=warning['version']
           )

Additionally, you should call that method when you collect the `changes` to report to the user. For example:

.. raw::python

   changes = self.changes.to_return()
   result.update(**changes)
   result.update(dict(changed=changed))
   self._announce_deprecations(result)
   return result

And finally, you should populate the `__warnings` key of your `changes` attribute as needed.

For example, in the `bigip_gtm_wide_ip` module, the `lb_method` property uses this code when it sees you are using a deprecated option.

For example:

.. raw::python

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


The `changes` attribute is typically updated during the call to `_update_changed_options`, during `update`, or `_set_changed_options` during `create`.

If your module needs to detect changes outside of those two general methods, you should do so inside of the `should_update` method.

.. note::

   To do your own ad-hoc detection inside of `should_update`, you must overload the base classes' method. If you do this, you should decide whether or not it is still necessary to call the base classes' method during the call to your overloaded method.

With that in place, you will find yourself with `warning` messages raised by Ansible when you use the deprecated functionality.

Deprecating parameters
----------------------

Below is an excerpt that shows how you might deprecate an option you no longer want to use. You may do this for a number of reasons, but in most cases it is because the original name does not make sense in the context you're using it in.

For example, you might have named the original option `rules`, when the more appropriate name for the option would have been `irules`.

.. note::

   Ansible allows for aliasing of options so that specifying one is equivalent to specifying another. This is *not* the situation that we are referring to here. It is still perfectly acceptable to use option aliases if you want to. These guidelines are for when you specifically want to *remove* options that are presumably already in use.

Here is a sample `ArgumentSpec` from the version where we made the mistake. Let's assume we made this mistake in version 2.0.

.. raw::python

   class ArgumentSpec(object):
       def __init__(self):
           self.supports_check_mode = True
           self.argument_spec = dict(
               rules=dict(
                   required=False,
                   default=None
               ),
               name=dict(
                   required=True,
                   aliases=['wide_ip']
               )
           )
           self.f5_product_name = 'bigip'

Now, we wish to deprecate that option name. In version 2.1 of Ansible, we would do something like this:

.. raw::python

   class ArgumentSpec(object):
       def __init__(self):
           self.supports_check_mode = True
           self.argument_spec = dict(
               rules=dict(
                   required=False,
                   default=None
               ),
               irules=dict(
                   required=False,
                   default=None
               ),
               name=dict(
                   required=True,
                   aliases=['wide_ip']
               )
           )
           self.f5_product_name = 'bigip'

Additionally, we would include the warnings necessary to make the user aware that they are using deprecated functionality (the `rules` option).

Finally, during the release cycle of Ansible 2.2, we would want to change our spec to look like this:

.. raw::python

   class ArgumentSpec(object):
       def __init__(self):
           self.supports_check_mode = True
           self.argument_spec = dict(
               irules=dict(
                   required=False,
                   default=None
               ),
               name=dict(
                   required=True,
                   aliases=['wide_ip']
               )
           )
           self.f5_product_name = 'bigip'

This removes the deprecated functionality.

Also, do not forget to remove any mention of the deprecation inside the actual module code. We don't want the legacy code to stick around. This helps keep technical debt at bay.
