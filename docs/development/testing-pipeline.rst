Testing Pipeline
================

This repository provides a Jenkins Pipeline that can be used to drive the CI/CD
process of testing the F5 Ansible modules. In this document we will discuss the
testing pipeline that is used by the F5 Ansible module developers.

File location
-------------

The pipeline itself can be found here,

* `test/runner/pipeline/ci.f5.f5-ansible.groovy`

This Pipeline is the same one that F5 uses internally. This pipeline is delivered
to Jenkins via a `jenkins-job-builder` (JJB) job. This job is located right next
to the pipeline itself.

* `test/runner/pipeline/ci.f5.f5-ansible.yaml`

Dependencies
------------

There are several tools that need to be installed to make the pipeline work
correctly.

* Jenkins
* docker
* docker-compose
* jenkins-job-builder

Installing Jenkins is beyond the scope of this document. If you are an F5'er who
needs to know how to do this in the context of the F5 Ansible modules, refer to
the `f5ansible/testing` repository for a HOT template that will do it for you.

`jenkins-job-builder` (JJB) can be downloaded via `pip`

.. code:: bash

   pip install jenkins-job-builder

JJB will additionally need to be configured to be use your Jenkins instance.

Installing the pipeline
-----------------------

Once Jenkins is in place, you will want to target the primary Jenkins server when
installing the job. You can install the Pipeline with the following command.

.. code-block:: bash

   jenkins-jobs update test/runner/pipeline/ci.f5.f5-ansible.yaml

Your pipeline should now be available on the primary Jenkins server.
