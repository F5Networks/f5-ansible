Module usage with Tower
=======================

The Ansible modules should work normally in either Ansible Tower or Ansible AWX. There are, however,
some things you should be aware of when using them within these environments.

Workers run in restricted environments
--------------------------------------

If you make use of any of the modules which download files to the Ansible controller (such as
``bigip_qkview`` or ``bigip_ucs``, you should be aware that the Ansible worker that executes
your job runs in a restricted environment.

In Tower, this environment is called a PRoot and functions nearly identically to a ``chroot``.
The net effect is that when files are saved by the job, they are saved (by default) into this
chrooted environment. When the job finishes, that environment is cleaned up (ie, deleted) and
your downloaded files will be deleted with it.

More background on the above can be `found here`_ and `here`_.

In AWX, the situation is slightly different. AWX is distributed in the form of a set of Docker
containers. Roughly the same restriction on the worker applies here, except that the worker is
run in a container instead of a ``chroot``.

In the end, the same situation applies though. The job will run on the container and the downloaded
file will be stored **in the container**.

To remedy the above problems, you may want to change the Tower/AWX environment to put the files
you download in a more durable location. This process is different for each of the products, so
let's look at some configuration

**Tower**

The Tower case is relatively easy to change.

First, we will be editing the ``/etc/tower/settings.py`` file. You can open that file for editing,
and at the bottom of it, add the following

.. code-block:: python

   AWX_PROOT_SHOW_PATHS = ['/scratch']

Next, create that directory on your Tower VM and change the permissions of it to mirror those of
the ``/tmp`` directory.

.. code-block::

   $ mkdir /scratch
   $ chmod 777

Finally, restart Tower and wait for it to come back online

.. code-block::

   $ ansible-tower-service restart

When Tower comes back online, its job runner will be able to write files into the ``/scratch``
directory of the Tower VM. This is one possible way to make the system able to persist downloads
longer than the lifetime of a particular job. Additionally, you maintain some of the safety
against accidents that the chroot provides.

**AWX**

The AWX case is slightly different because it is distributed (by default) in container form.

For the following solution, I will refer to the Docker Compose method of running AWX because it
is relatively simple and the same ideas can be applied to all major Container Orchestration
Environments.

Provided you instructed the AWX setup script to create a ``docker-compose.yaml`` file, you can
find the file in ``/var/lib/awx``. To enable the system to write files to a more durable location
on the AWX host, you can include a new bind mount to a location of your choice.

For instance, in the definition of my ``task`` service, I can specify the following

.. code-block::

   volumes:
     - "/scratch:/scratch:rw"

This will allow my ``task`` container (which runs the AWX jobs) to write to a durable location
on the AWX VM.

Note that I additionally include the bind-mount shown below so that I can make use of the
docker modules from within my AWX installation

.. code-block::

   volumes:
     - /var/run/docker.sock:/var/run/docker.sock

The above is handy to have.

After changing the ``docker-compose.yaml`` file, you can restart AWX by restarting the containers
using ``docker-compose``.

.. code-block::

   $ docker-compose stop
   $ docker-compose start

.. _found here: https://docs.ansible.com/ansible-tower/2.3.1/html/userguide/security.html#playbook-access-and-information-sharing
.. _here: https://docs.ansible.com/ansible-tower/2.2.0/html/installandreference/known_issues.html#playbooks-missing-access-to-necessary-data-due-to-proot-issues
