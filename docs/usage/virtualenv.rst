:orphan: true

Install Ansible by using virtualenv
===================================

To keep up with the latest version of Ansible and F5 Ansible modules, F5 recommends using virtualenv.

Install virtualenv
------------------

.. note:: To install Python virtualenv, you need administrative/root access. Use caution if you are installing on a shared system to ensure you do not impact your co-workers!

Mac OS
``````

Pip does not come pre-installed on a Mac. To install pip, run the following commands:

.. code-block:: bash

   sudo easy_install pip
   sudo pip install --upgrade pip

.. code-block:: bash

   pip install virtualenv

RHEL/CentOS 7
`````````````

On RHEL/CentOS, You can install by using yum.

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

In your current working directory, you will find a new directory called myansible (you do not have to call it "myansible", I just chose that name as an example, you could also call it "ansible24", etc...).

This directory contains a copy of Python that will install any modules within that local directory. When you use this method, you can install Python modules without stomping on the system-wide ones.

To use this new location, you must activate it.

.. code-block:: bash

   source myansible/bin/activate

You should see your prompt change to include the virtualenv name. For example:

.. code-block:: bash

  (myansible) $

Your prompt may differ, but the important part is that you see "(myansible)".

Now that the virtualenv is active, all future Python commands (such as pip) will install modules into the virtualenv.
  
Let's install Ansible to make it possible to use the modules.

First, make sure you installed `ansible`.

.. code-block:: bash

   (myansible) $ pip install ansible

You should be able to verify that you are running Ansible by using the `--version` argument to the `ansible` command, for example:

.. code-block:: bash

   (myansible) $ ansible --version

The output should resemble the following:

.. code-block:: bash

   (myansible) $ ansible --version
   ansible 2.4.0
     config file =
     configured module search path = Default w/o overrides

Now you can create your first playbook. The remainder of the Ansible playbooks will be in a file called ``site.yaml``.

Install modules
---------------

Refer to the documentation on `installing the modules here <installing-modules.html>`_.

This is useful if you want to run the latest/development version of the F5 Ansible module.  If you are using Ansible 2.4.0 or newer you may want to skip this step.

Upgrade Ansible
---------------

If you need to upgrade Ansible (i.e. from 2.3.0 to 2.4.0) you can run the following command:

.. code-block:: bash

   (myansible) $ pip install --upgrade ansible
   

Install the latest development version of Ansible and F5 modules
----------------------------------------------------------------

The following example shows how to install the latest development version of Ansible and the F5 Ansible modules.

.. warning:: Only provided as an example, not recommended for day-to-day use. Do not expect any support. Use only if you want to use experimental/unstable features and/or contribute code/testing.

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

