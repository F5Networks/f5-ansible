Requirements
============

To develop modules, the following are required,

- docker
- docker-compose
- a ``git clone``d copy of the `f5-ansible source code`_.
- A copy of the development container built

The installation of ``docker`` and ``docker-compose`` are beyond the scope of this
document. We've included the following links to assist you in this though.

* https://docs.docker.com/install/#cloud
* https://docs.docker.com/compose/install/

Note that you will want to install the CE version of Docker. Depending on your operating
system, packages for one, or both, of these tools may already be available. You are
advised to use them if they are

.. note::

   For MacOSX systems, the ``docker-compose`` tool comes pre-installed with ``docker``
   if you install the pre-compiled binaries available for Mac from the Docker website.

For the general public
----------------------

To acquire a copy of the development container, you can issue the following command
once ``docker`` and ``docker-compose`` are installed

.. code-block:: shell

    $ docker-compose -f devtools/docker-compose.yaml build

This step can take some time to finish because each of the containers needs to built.

Once the containers are built, you should use the docker-compose command with the
``run`` argument to enter one of the containers. For example,

.. code-block:: shell

    $ docker-compose -f devtools/docker-compose.yaml run py2.7

All of the remaining steps can take place inside of this container. Actual writing of
code does not need to happen inside of the container due to ``docker-compose`` mounting
your source directory to the container's ``/here`` directory.

.. _f5-ansible source code: https://github.com/F5Networks/f5-ansible
