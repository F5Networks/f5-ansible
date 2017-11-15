Pulling Docker Containers
=========================

If you are an F5'er, then you have access to an internal docker registry.

If you are reading this, then you should also know what that registry is. If not, then
`visit this link`_

These instructions are only relevant to you if you are an F5'er. If not, feel free
to skip over this document.

How it works
------------

At this registry there is an organization named `f5ansible`. There are several
repositories in this organization. For instance,

* f5ansible/py2.7
* f5ansible/py3.5
* f5ansible/py3.6
* etc

You get the idea.

Each of these images is, as their name implies, a different Docker environment for
each version of Python that we develop and test upon.

These containers are also named in the various `image` keys inside of the
docker-compose file contained in this repository. For example,

.. code-block:: yaml

   services:
     py2.7:
       image: f5ansible/py2.7:devel
       build:
         context: ..

All of the containers that you see are built nightly at midnight by a trigger that
is fired when a Jenkins job completes. That job is found in this jenkins-job-builder
file.

* `test/pipeline/ci.f5.f5-ansible-public-to-private.yaml`

Therefore, when you come in the next morning (assuming you work in Seattle) you will
have a new set of docker images available to you.

Configure registry authentication
---------------------------------

The first step required to get these updated containers on a regular basis is that
you must log in to the registry service mentioned above and get a set of
**encrypted credentials** that the service can provide you with.

Clicking the settings for your account (upper right corner of the registry) you will
be presented with the option of a **CLI password**.

Click the associated link and you will be asked to verify your current password.
Enter it as required.

In the modal dialog window that appears you have the option of choosing
**Docker Configuration**. Click that tab.

Follow the instructions on screen to properly configure your `~/.docker/config.json`
file.

Updating the site docker-compose
--------------------------------

F5 has its own registry for containers. To configure your docker-compose files to
use it, start by locating the following file

* `devtools/docker-compose.site.example.yaml`

Next, copy this file, renaming it to the following.

* `devtools/docker-compose.site.yaml`

Finally, open the file for editing. Inside of the file is a descriptive header that
will instruct you on how to edit the file. In particular, you need to add the URL
of the F5 Docker registry. If you do not know what this is, ask a co-worker for
assistance.

Getting the images
------------------

With the above setup and configured, you can pull the images using the `docker-compose`
command. For example,

.. code-block:: bash

   SEA-ML-00028116:f5-ansible trupp$ ./devtools/bin/f5ansible container-pull

This should initiate a download of the necessary containers.

.. _visit this link: go/ansible-docker-registry
