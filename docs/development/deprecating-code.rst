Deprecating Code
================

Our Ansible modules follow a strategy of deprecation which is intended to give
the user of the modules ample time to upgrade to a new version of Ansible.

New releases of Ansible happen, at the time of this writing, about once a quarter.

With this in mind, the following process should allow a user 3 to 6 months to
upgrade their Ansible installation to the new code. If the user misses this
3 to 6 month period, then they can upgrade incrementally (2.1 -> 2.2 -> 2.3)
instead of upgrading directly to the latest version and, in the process, test
that the incremental versions work with their playbooks.

Deprecation process
-------------------

Let's look at an example deprecation process

* 2.0 - version to deprecate
* 2.1 - deprecated version
* 2.2 - version with deprecated feature removed

During the second release noted above, the module developer *MUST* insert
adequate warnings for the user to see. Ansible will color warning messages
so that they stick out from regular messages.

Raising deprecated warnings
---------------------------

To raise warnings about deprecated functionality, the module developer should
add the following method to their `ModuleManager` class.

.. raw::python

   def _announce_deprecations(self, result):
       warnings = result.pop('__warnings', [])
       for warning in warnings:
           self.client.module.deprecate(
               msg=warning['msg'],
               version=warning['version']
           )

Additionally, the module developer should add the calling of that method
when they collect the `changes` to report to the user. For example,

.. raw::python

   changes = self.changes.to_return()
   result.update(**changes)
   result.update(dict(changed=changed))
   self._announce_deprecations(result)
   return result

And finally, the module developer should populate the `__warnings` key of their
`changes` attribute as needed. For example, in the `bigip_gtm_wide_ip` module,
the following is used in the `lb_method` property when it sees you are using
an option name that is deprecated. For example,

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


The `changes` attribute is typically updated during the call to
`_update_changed_options` during `update`, or `_set_changed_options`
during `create`.

If your module needs to detect changes outside of those two general methods,
you should be doing so inside of the `should_update` method.

.. note::

   To do your own ad-hoc detection inside of `should_update`, you will need to
   overload the base classes' method. If you do this, you should decide whether
   or not it is still necessary to call the base classes' method during the
   call to your overloaded method.

With that in place, you will find yourself with `warning` messages being raised
by Ansible when you use the deprecated functionality.

Deprecating parameters
----------------------

Below is an excerpt from how one might deprecate an option that we no longer
want to use. You may do this for a number of reasons, but in most cases it
is due to the original name not making sense in the context it is used.

For example, you might have named the original option `rules` when the more
appropriate name for the option would have been `irules`.

.. note::

   Ansible allows for aliasing of options so that specifying one is equivalent
   to specifying another. This is *not* the situation that we are referring to
   here. It is still perfectly acceptable to use option aliases if you want
   to. These guidelines are for when you specifically want to *remove* options
   that are presumably already in use.

Here is a sample `ArgumentSpec` from the version where we made the mistake.
Let's assume that this mistake was made in version 2.0.

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

Now, we wish to deprecate that option name. So, in version 2.1 of Ansible, we
would do something like this.

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

Additionally, we would include the warnings necessary to make the user of the
module aware that they are using deprecated functionality (the `rules` option).

Finally, during the release cycle of Ansible 2.2, we would want to change our
spec to look like so.

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

Thus, removing the deprecated functionality.

Also, do not forget to remove any mention of the deprecation inside the actual
module code. We don't want the legacy code to stick around. This helps keep
technical debt at bay.
