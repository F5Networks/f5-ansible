Installing via virtualenv
-------------------------

This method is recommended for keeping up with the latest version of Ansible and F5 Ansible modules.

Installing virtualenv
=====================

.. note:: You will need administrative/root access to install Python virtualenv.  Please use caution if installing on a shared system to ensure you do not impact your co-workers!

Mac OS
^^^^^^

Pip does not come pre-installed on a mac. To install run.

.. code-block:: bash

  sudo easy_install pip
  sudo pip install --upgrade pip

.. code-block:: bash

  pip install virtualenv

RHEL/Cent OS 7
^^^^^^^^^^^^^^

You can install via yum. 

.. code-block:: bash

  sudo yum install python-virtualenv

Ubuntu/Debian
^^^^^^^^^^^^^

Install via apt

.. code-block:: bash

  sudo apt install python-virtualenv

Setting up virtualenv
---------------------

After install virtualenv you can create a "virtual environment" to host your local copy of ansible.

.. code-block:: bash

  virtualenv myansible

In your current working directory, you will find a new directory called myansible (you do not have to call it "myansible", I just chose that name as an example, you could also call it "ansible24", etc...). In this directory resides a copy of Python that is configured to install any modules inside of that local directory. Via this method, we can install Python modules without stomping on the system wide ones.

To use this new location, you must activate it.

.. code-block:: bash

  source myansible/bin/activate

You should see your prompt change so that the name of the virtualenv is prefixing the normal prompt. For example (your prompt may differ, the important part is that you see "(myansible)".

.. code-block:: bash

  (myansible) $

Now that our virtualenv is active, all future Python commands (such as pip) will install modules into the virtualenv. So let’s install the development copy of ansible.
  
Let's install Ansible to make it possible to use the modules.

First, make sure `ansible` is installed.

.. code-block:: bash

   (myansible) $ pip install ansible


You should be able to verify that you are running Ansible by using the
`--version` argument to the `ansible` command, like so.

.. code-block:: bash

   (myansible) $ ansible --version

You should be presented with output that resembles the following

.. code-block:: terminal

   (myansible) $ ansible --version
   ansible 2.4.0
     config file =
     configured module search path = Default w/o overrides

With this ready, you can create your first playbook. We'll write the remainder
of our Ansible playbooks in a file called ``site.yaml``

Installing Modules
------------------

Refer to the documentation on `installing the modules here <installing-modules.html>`_.

This is useful if you want to run the latest/development version of the F5 Ansible module.  If you are using Ansible 2.4.0 or newer you may want to skip this step.

Upgrading Ansible
-----------------

If you need to upgrade Ansible (i.e. from 2.3.0 to 2.4.0) you can run the following.


.. code-block:: bash

   (myansible) $ pip install --upgrade ansible
   
Installing Latest Development of Ansible + F5 Ansible
------------------------------------------------------
The following is an example of installing the latest development version of Ansible + F5 Ansible

.. warning:: Only provided as an example, not recommended for day-to-day use.  Do not expect any support. Only use if you want to use experimental/unstable features and/or contribute code/testing.

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

