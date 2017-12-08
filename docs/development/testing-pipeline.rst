Testing pipeline
================

This repository provides a Jenkins Pipeline that you can use to drive the CI/CD process of testing the F5 Ansible modules.

In this document we will discuss the testing pipeline used by the F5 Ansible module developers.

File location
-------------

You can find the pipeline itself here:

- `test/runner/pipeline/ci.f5.f5-ansible.groovy`

This Pipeline is the same one that F5 uses internally. A `jenkins-job-builder` (JJB) job delivers this pipeline to Jenkins. This job is right next to the pipeline itself.

- `test/runner/pipeline/ci.f5.f5-ansible.yaml`

Dependencies
------------

You must install several tools to make the pipeline work correctly.

- Jenkins
- Docker (docker)
- Docker Compose (docker-compose)
- Jenkins Job Builder (jenkins-job-builder)

Installing Jenkins is beyond the scope of this document. If you are an F5'er who needs to know how to do this in the context of the F5 Ansible modules, refer to the `f5ansible/testing` repository for a HOT template that will do it for you.

You can download `jenkins-job-builder` (JJB) via `pip`:

.. code:: bash

   pip install jenkins-job-builder

You must configure Jenkins Job Builder to use your Jenkins instance.

Installing the pipeline
-----------------------

After Jenkins is in place, you should target the primary Jenkins server when installing the job. You can install the Pipeline with the following command:

.. code-block:: bash

   jenkins-jobs update test/runner/pipeline/ci.f5.f5-ansible.yaml

Your pipeline should now be available on the primary Jenkins server.
