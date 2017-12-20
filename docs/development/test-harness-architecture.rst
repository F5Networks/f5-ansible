:orphan: true

Test harness architecture
=========================

This repository contains within it a set of test harnesses that it uses to ensure that
the functionality and quality of the code meets our expectations before an Issue is
resolved or a PR is merged.

In this document we will take a look at that architecture and how to use it.

Requirements
------------

To make use of the test harnesses requires that several tools be available to you.
These are,

* OpenStack >= Mitaka
* Docker
* Docker Compose
* GPG
* GPG keys properly created and configured
* Jenkins Job Builder

Most of the above requirements are used by developers on the Mac platform. During CI/CD
however, the same tools are used on Linux.

In addition to having the above, it is also recommended that you have sufficient quota
to do the large amount of concurrent work that is required.

Concurrency is used extensively for the CI/CD versions of the tests. It is not used
to nearly the same degree for developer tests. Quota may be significantly lower for
developer's personal OpenStack tenants, but will require at least the minimum amount
of resources to run a BIG-IP.

Docker containers
-----------------

All of the test work (and by extension development work) is done within Docker containers.
By using this approach, we are able to encapsulate all of our tools inside containers
and deliver those containers to team members in an easy way.

Additionally, we leverage tools onsite that can automatically build these containers
for you if you are an F5'er.

If you are not an F5'er, you don't need to be left out though! We provide in this
repository a `docker-compose` file that can be used to build your own versions of the
containers that we use. This `docker-compose` file can be found here.

* `devtools/docker-compose.yaml`

Manually building dev/test containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are not an F5 employee, then you will need to build the dev/test containers
yourself.

We have provided convenience wrappers around this process. First, there is the
`docker-compose.yaml` file that contains all the configuration needed to build the
containers. Second, there are executable scripts in `devtools/bin` that can be invoked
to run the necessary build commands.

For example, should you want to build the container that contains an environment for
Python 2.7.10, the following command can be run

.. code-block:: bash

   SEA-ML-00028116:f5-ansible trupp$ ./devtools/bin/build-py2.7.10


Encryption
----------

There are files in this repository that contain sensitive information that we do not want
to directly expose to the outside world. To handle this, we use GPG excryption to make
sure the files are safe from wandering eyes.

The facilitate the usage of GPG, we use a tool called `blackbox`_ to manage encryption
and decryption of files as well as manage the list of administrators and their public keys.

This tool comes packaged with the Docker containers that are available to you. If you
are an F5'er, these containers will download for you automatically when you use the
`run-*` commands in `devtools/bin`. If you are outside of F5, then the docker-compose
file will build these for you automatically.

Filesystem
----------

The test automation is contained within three directories. They are,

* test/integration
* test/pipeline
* test/runner

These directories contain, respectively,

* The actual test code for the modules in the form of an Ansible Playbook and an
  Ansible Role.
* The Jenkins configuration files in the form of `jenkins-job-builder` YAML files and
  Jenkins Pipeline Groovy files
* A standard Ansible configuration that contains,
   * Test harness configurations in the form of OpenStack Heat templates and Ansible `vars`
   * Ansible playbooks to create, test, and teardown the stack
   * Ansible playbooks to provide an `openstack` CLI command to re-create test harnesses

The above directory trees contain information that is used in a very particular order,
we'll cover that order next so that you are
Let's further explore each of these so-as to gain a better understanding of what each of
them contains.

The test/integration directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inside of this

Encryption
----------

Playbooks
---------

Executing the full stack test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Getting the stack command
~~~~~~~~~~~~~~~~~~~~~~~~~


.. _Calulating quota:
.. _blackbox: https://github.com/StackExchange/blackbox
