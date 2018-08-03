Integration test tags
=====================

Integration tests in the `f5-ansible`_ repository may include a number of tags
throughout the various tests.

Tagging Scenarios
-----------------

Tagging in the integration tests is common in certain scenarios. The following
is a list of the common scenarios, the tags involved, and how to configure
the scenario for use

Github Issues
`````````````

This scenario is the one most frequently used in the integration tests. Its
purpose is to associate a specific Github Issue with a specific set of tests.
This allows the developer to focus their work on a smaller subset of the total
test playbook.

Tags are used to make the running of these targeted tests easier.

This scenario is implemented by the following procedure below.

- Create a new YAML file in the test/integration/targets/MODULE_NAME/tasks directory.
- Name this file ``issue-XXXXX.yaml``, where ``XXXXX`` is a 5 digit number (with
  leading 0's as needed) specifying the Github issue number. For example,
  ``issue-00798.yaml``.
- Add tests to this new file
- Add the following code snippet to the bottom of the ``main.yaml`` file in the
  ``tasks/`` directory.

  .. code-block:: yaml

     - import_tasks: issue-00798.yaml
       tags: issue-00798

  Alternatively, if you have many tags, you can specify them as needed along with
  the issue tag.

  .. code-block:: yaml

     - import_tasks: issue-00798.yaml
       tags:
         - issue-00798
         - vcmp-slots
         - vcmp-no-slots

By following the above procedure, your integration tests are able to be called when
specifying the ``--tags`` argument to ``ansible-playbook``. For instance,

.. code-block: bash

   ansible-playbook -i inventory/hosts bigip_vcmp_guest.yaml --tags issue-00798

Known tags
----------

The following tags are the ones that are known to be used at the time of this
writing. As more are added, this list should be updated accordingly.

+---------------------+-------------------------------------------------------------------+
| Tag                 | Description                                                       |
+=====================+===================================================================+
| issue-``XXXXX``     | * Used to specify that a subset of tasks is associated with       |
|                     |   a Github Issue.                                                 |
+---------------------+-------------------------------------------------------------------+
| module-provisioning | * Specifies that the task is involved with module provisioning    |
|                     |   on the system. This should **not** be used for modules that     |
|                     |   **test** provisioning. Only modules that **setup** provisioning |
+---------------------+-------------------------------------------------------------------+
| deprovision-module  | * The task is involved in deprovisioning of modules for **setup** |
|                     |   purposes                                                        |
+---------------------+-------------------------------------------------------------------+
