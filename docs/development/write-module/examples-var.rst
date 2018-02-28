EXAMPLES variable
=================

The ``EXAMPLES`` variable contains the most common use cases for this module.

You are free to add any examples you think would help a user of the module solve a
problem quickly.

These examples also serve as a basis for the functional tests.

For this module, the ``EXAMPLES`` variable looks like this:

.. code-block:: python

   EXAMPLES = r'''
   - name: Create policies
     bigip_policy:
       name: Policy-Foo
       state: present
     delegate_to: localhost

   - name: Add a rule to the new policy
     bigip_policy_rule:
       policy: Policy-Foo
       name: rule3
       conditions:
         - type: http_uri
           path_begins_with_any: /ABC
       actions:
         - type: forward
           pool: pool-svrs
     delegate_to: localhost

   - name: Add multiple rules to the new policy
     bigip_policy_rule:
       policy: Policy-Foo
       name: "{{ item.name }}"
       conditions: "{{ item.conditions }}"
       actions: "{{ item.actions }}"
     delegate_to: localhost
     loop:
       - name: rule1
         actions:
           - type: forward
             pool: pool-svrs
         conditions:
           - type: http_uri
             path_starts_with: /euro
       - name: rule2
         actions:
           - type: forward
             pool: pool-svrs
         conditions:
           - type: http_uri
             path_starts_with: /HomePage/

   - name: Remove all rules and confitions from the rule
     bigip_policy_rule:
       policy: Policy-Foo
       name: rule1
       conditions:
         - type: all_traffic
       actions:
         - type: ignore
     delegate_to: localhost
   '''

This variable should go **after** the ``DOCUMENTATION`` variable.

The examples that you provide should always have the following:

**delegate_to: localhost**

You should run the BIG-IP modules on the Ansible controller only. The best practice is to
use ``delegate_to:`` here so that you get in the habit of using it.

The ``delegate_to`` keyword is **not** an argument to your module. It is an argument to
the Ansible Task. Therefore, it should align with the *module name*.

**common args**

The common args to modules include:

- ``password``. This should always be ``secret``
- ``server``. This should always be ``lb.mydomain.com``
- ``user``. This should always be ``admin``

Conclusion
----------

There is nothing unique about this documentation blob compared to the ``DOCUMENTATION``
variable mentioned earlier. It is still YAML, and therefore must follow the constraints covered earlier.

The next section covers the final documentation blob: the ``RETURN`` variable.
