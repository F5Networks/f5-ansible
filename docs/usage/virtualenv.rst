:orphan: true

Install Ansible by using virtualenv
===================================

To keep up with the latest version of Ansible and the F5 modules, F5 recommends using virtualenv.

Install virtualenv
------------------

.. note:: To install Python virtualenv, you need administrative/root access. Use caution if you are installing on a shared system to ensure you do not impact your co-workers.

Mac OS
``````

Pip does not come pre-installed on Mac. To install pip, run the following commands:

.. code-block:: bash

   sudo easy_install pip
   sudo pip install --upgrade pip

.. code-block:: bash

   pip install virtualenv

RHEL/CentOS 7
`````````````

On RHEL/CentOS, you can install by using yum.

.. code-block:: bash

   sudo yum install python-virtualenv

Ubuntu/Debian
`````````````

On Ubuntu/Debian, you can install by using apt.

.. code-block:: bash

   sudo apt install python-virtualenv

Set up virtualenv
-----------------

After you install virtualenv, you can create a "virtual environment" to host your local copy of Ansible.

.. code-block:: bash

   virtualenv myansible

This command creates a directory called ``myansible`` in your current working directory.

This directory contains a copy of Python that will install modules in the ``myansible`` directory. This keeps them separate from other modules.

To use this new location, you must activate it.

.. code-block:: bash

   source myansible/bin/activate

You should see the prompt change to include the virtualenv name. For example:

.. code-block:: bash

  (myansible) $

Now that the virtualenv is active, all future Python commands (such as pip) will install modules into the virtualenv.

Let's install Ansible to make it possible to use the modules.

First, make sure you installed Ansible.

.. code-block:: bash

   (myansible) $ pip install ansible

You should be able to verify that you are running Ansible by using the ``--version`` argument to the ``ansible`` command, for example:

.. code-block:: bash

   (myansible) $ ansible --version

The output should resemble the following:

.. code-block:: bash

   (myansible) $ ansible --version
   ansible 2.4.0
     config file =
     configured module search path = Default w/o overrides

Now you can create your first playbook. The remainder of the Ansible playbooks will be in a file called ``site.yaml``.

Configure your ansible_python_interpreter
-----------------------------------------

When using Ansible in a ``virtualenv``, it is necessary that you change your ``ansible_python_interpreter`` variable. This
can be done in several places, including,

* group_vars
* host_vars
* directly in the inventory file (on the hosts line)

The recommended place to put it though is in the ``group_vars`` directory in the ``all.yaml`` file. This will ensure that it
is used by all of the hosts in your playbooks. Additionally, you can remove it from this central location if you move your
playbooks to a non-``virtualenv`` host.

Below is an example of what your ``inventory/group_vars/all.yaml`` file might look like after you have set the ``ansible_python_interpreter``.

.. code-block:: yaml

   ---

   ansible_python_interpreter: /usr/local/bin/python

The same format would apply if you included it in your ``inventory/host_vars/HOST.yaml`` host files. To include it directly in inventory,
the format looks a little different.

.. code-block:: bash

   [f5-cli]
   bigip5 ansible_host=1.2.3.4 ansible_python_interpreter=/opt/envs/my-venv/bin/python

In the above example, a single BIG-IP named ``bigip5`` is specified. It is a member of the ``f5-cli`` group, and has a host
address of ``1.2.3.4``. It also has an ``ansible_python_interpreter`` set to ``/opt/envs/my-venv/bin/python``. When Ansible is run,
this host will use a different python binary than what comes installed on the system. This is, similarly, how a ``virtualenv``'s
Python interpreter would be specified.

Install modules
---------------

Refer to the documentation on :ref:`installing the modules here <installunstable>`_.

This is useful if you want to run the latest/development version of the F5 modules for Ansible.

If you are using Ansible 2.4.0 or later you may want to skip this step.

Upgrade Ansible
---------------

If you need to upgrade Ansible (i.e., from 2.3.0 to 2.4.0), you can run the following command:

.. code-block:: bash

   (myansible) $ pip install --upgrade ansible


Install the latest development version of Ansible and F5 modules
----------------------------------------------------------------

The following example shows how to install the latest development version of Ansible and the F5 Modules for Ansible.

.. warning:: This is an unsupported example. Use only if you want to use experimental/unstable features and/or contribute code/tests.

.. code-block:: bash

   mkdir f5-ansible-devel
   cd f5-ansible-devel
   virtualenv ansibledev
   . ansibledev/bin/activate
   pip install git+git://github.com/ansible/ansible.git@devel
   git clone -b devel https://github.com/F5Networks/f5-ansible
   mkdir library
   echo -n "[default]\nlibrary=./library\n" > ansible.cfg
   cp f5-ansible/library/*.py library
