:orphan: true

Playbook metadata
=================

Our integration tests are made possible through the use of Ansible playbooks.
These playbooks can be found here:

* ``test/integration/``

Each playbook has a ``vars`` section that includes a ``__metadata__`` key. This key is used by other tools and processes in this
repository to provide the developers with information relevant to the module.

Different versions of metadata are valid in different Ansible versions.

Versions
--------

The version history below outlines the changes that have been made to the
metadata over time. The current version is at the top of this list. The original
version is at the bottom.

1.2
~~~

Release date: June 2018
Ansible version 2.6

New keys:

* ``upstream``. Used to determine (in our scripts) which modules to publish upstream in bulk. Values can be boolean-like values.
  ex. yes, no, True, False, 1, 0.

1.1
~~~

Release date: March 2018
Ansible version 2.5

New keys:

* ``tested_versions``
* ``supported_harnesses``
* ``coding_standards``
* Original ``tested_platforms`` values have been moved to ``tested_versions``

**Example**

.. code-block:: yaml

   __metadata__:
     version: 1.1
     tested_versions:
       - 11.5.4-hf1
       - 11.6.0
       - 12.0.0
       - 12.1.0
       - 12.1.0-hf1
       - 12.1.0-hf2
       - 12.1.1
       - 12.1.1-hf1
       - 12.1.1-hf2
       - 12.1.2
       - 12.1.2-hf1
       - 13.0.0
       - 13.0.0-hf1
     tested_platforms:
       - ve
       - viprion 4200
     supported_harnesses:
       - TwoArmed-bigip-12.1.1
     coding_standards: v3
     callgraph_exclude:
       - pycallgraph.*

       # Ansible related
       - ansible.module_utils.basic.AnsibleModule.*
       - ansible.module_utils.basic.*
       - ansible.module_utils.parsing.*
       - ansible.module_utils._text.*
       - ansible.module_utils.six.*


1.0 (unused)
~~~~~~~~~~~~

Release date: September 2017
Ansible version 2.4

Initial version of the playbook metadata keys include:

* ``version``
* ``tested_platforms``
* ``callgraph_exclude``
* Valid values for ``tested_platforms`` are N/A

**Example**

.. code-block:: yaml

   __metadata__:
     version: 1.0
     tested_platforms:
       - NA
     callgraph_exclude:
       - pycallgraph.*

       # Ansible related
       - ansible.module_utils.basic.AnsibleModule.*
       - ansible.module_utils.basic.*
       - ansible.module_utils.parsing.*
       - ansible.module_utils._text.*
       - ansible.module_utils.six.*
