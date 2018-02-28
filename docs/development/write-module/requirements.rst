Requirements
============

To develop modules, you need the following:

- ``docker``
- ``docker-compose``
- A copy of the `f5-ansible source code`_ that you cloned by using ``git clone``
- A built copy of the development container

Docker and docker-compose
-------------------------

The installation of ``docker`` and ``docker-compose`` are beyond the scope of this document. However, here are links to assist you:

* https://docs.docker.com/install/#cloud
* https://docs.docker.com/compose/install/

Note that you should install the CE version of Docker. Depending on your operating system, packages for one or both of these tools may already be available. You are advised to use them if they are.

.. note::

   On macOS X, if you install the pre-compiled binaries for Mac from the Docker website, the ``docker-compose`` tool comes pre-installed with ``docker``.

The development container
-------------------------

To acquire a copy of the development container, issue the following command after you install ``docker`` and ``docker-compose``.

.. code-block:: shell

    $ docker-compose -f devtools/docker-compose.yaml build

This step can take some time to finish because each of the containers needs to build.

After the containers are built, use the ``docker-compose`` command with the ``run`` argument to enter one of the containers. For example:

.. code-block:: shell

    $ docker-compose -f devtools/docker-compose.yaml run py2.7

The remaining steps can take place inside this container. Actual code writing does not need to happen inside the container, because ``docker-compose`` mounts your source directory to the container's ``/here`` directory.

.. _f5-ansible source code: https://github.com/F5Networks/f5-ansible
