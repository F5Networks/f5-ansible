Allow new admin access of private data
======================================

In this tutorial I will outline the steps you need to take to add a new person to the
list of allowed admins for handling the encrypted data in this repository.

When should I do this?
----------------------

You should do this whenever you have deemed it necessary that a new person should be
assigned to handle secure information.

Our policy is that the developers responsible for this software will be granted
access to this repository.

Additionally, there may be an unspecified number of robot services that have subkeys
registered in the list of admins. These keys have no business editing the content
of the admin file. They must still be able to decrypt the content of the entire
repository as needed to do their job; run CI/CD testing and deployment.

Who should do this?
-------------------

This is a two step process that involves the following people

1. The person who wants to be added
2. The person who needs to do the adding

The process goes something like this

1. Admin chooses a new primary or secondary
2. Chosen person agrees and adds their public key in a PR
3. Admin merges this PR
4. Admin rebases their code to get the upstream changes
5. Admin imports the public keyring into their local keyring
6. Admin re-encrypts all the files and pushes those changes

As you can see, the admin will be doing most of the work, but that work largely needs
to be initiated by the user in the form of them adding their public key in a PR.

Let's look now at how to do that.

How do I do this?
-----------------

All of the work can be done inside of the development containers that are available
in the `./devtools/bin` directory. In this example I will use the `run-py2.7`
script to launch the relevant container.

We are going to begin with the person who wants to be added.

Creating a keypair
------------------

To perform these steps, start by firing up the py2.7 (or equivalent) container.

.. code-block:: bash

   SEA-ML-RUPP1:f5-ansible trupp$ ./devtools/bin/run-py2.7

Within this container, use the `gpg2 --gen-key` command to create the keypair you
will use. An example is shown below.

.. code-block:: bash

   root@d7f809815281:/here# gpg2 --gen-key
   gpg (GnuPG) 2.1.20; Copyright (C) 2017 Free Software Foundation, Inc.
   This is free software: you are free to change and redistribute it.
   There is NO WARRANTY, to the extent permitted by law.

   Note: Use "gpg2 --full-generate-key" for a full featured key generation dialog.

   GnuPG needs to construct a user ID to identify your key.

   Real name: Foo Bar
   Email address: foo.bar@f5.com
   You selected this USER-ID:
       "Foo Bar <foo.bar@f5.com>"

   Change (N)ame, (E)mail, or (O)kay/(Q)uit? O

   gpg: key DBB462DE79ADE8C9 marked as ultimately trusted
   gpg: directory '/gpg/openpgp-revocs.d' created
   gpg: revocation certificate stored as '/gpg/openpgp-revocs.d/80E..................................8C9.rev'
   public and secret key created and signed.

   pub   rsa2048 2017-10-11 [SC] [expires: 2019-10-11]
         80E..................................8C9
         80E..................................8C9
   uid                      Foo Bar <foo.bar@f5.com>
   sub   rsa2048 2017-10-11 [E] [expires: 2019-10-11]

   root@d7f809815281:/here#

With this complete, you should see your email address when using the `gpg2 --list-keys`
command.

For the person who wants to be added
------------------------------------

We assume that you have created an initial keypair to use for
encryption. If you have not yet done that, follow the instructions below in the
(Creating a keypair)[] section.

Begin by starting that container with the necessary script

.. code-block:: bash

   SEA-ML-RUPP1:f5-ansible trupp$ ./devtools/bin/run-py2.7

This command will leave you at a new shell prompt. Within this new prompt, the next
step is to create a new branch which will contain the pull request with your admin
addition in it. This can be done with git

.. code-block:: bash

   SEA-ML-RUPP1:f5-ansible trupp$ git checkout -b add-admin upstream/devel

`git` should notify you that you have changed branches.

Next you will run the `blackbox_addadmin` command to change the necessary files for
adding you as an admin. The single argument to this command is the email address that
you specified when you created your initial key pair.

.. code-block:: bash

   blackbox_addadmin foo.bar@f5.com

When this command finishes, there will be several new files which are shown as
modified. Additionally, the `blackbox_addadmin` command will instruct you on the
command you need to use to commit these changes.

.. code-block:: bash

   root@d7f809815281:/here# blackbox_addadmin foo.bar@f5.com
   gpg: key DBB462DE79ADE8C9: public key "Foo Bar <foo.bar@f5.com>" imported
   gpg: Total number processed: 1
   gpg:               imported: 1


   NEXT STEP: You need to manually check these in:
         git commit -m'NEW ADMIN: foo.bar@f5.com' keyrings/live/pubring.kbx keyrings/live/trustdb.gpg keyrings/live/blackbox-admins.txt
   root@d7f809815281:/here#

A `git status` command will also illustrate this.

.. code-block:: bash

   root@d7f809815281:/here# git status | grep keyrings
           modified:   keyrings/live/blackbox-admins.txt
           modified:   keyrings/live/pubring.kbx
   root@d7f809815281:/here#

Do as the instructions say above and commit those files

.. code-block:: bash

   git commit -m'NEW ADMIN: foo.bar@f5.com' keyrings/live/pubring.kbx keyrings/live/trustdb.gpg keyrings/live/blackbox-admins.txt

You may now push the PR to the Github repository and follow the normal PR process.

For the existing admin doing the adding
---------------------------------------

First, verify and merge the PR sent by the user wishing to be added.

.. note::

   Adding a new user to the public key chain in the steps above is not, immediately,
   a security risk. This is because you have not yet re-encrypted the files. If you
   mistakenly merge a PR from a bad actor, you should immediately reverse this merge
   by using the `blackbox_removeadmin` command.

   If you have already re-encrypted all of the files with this new key, then you
   still have the ability to undo your mistake by re-checking out the modified `*.gpg`
   files.

   If you have committed those files, you have one last chance to save yourself by
   undoing the merge in question **before** you push your changes to the upstream
   repository.

   If you have failed to catch yourself at the numerous places above, your only
   remaining option is to either re-write history (bad idea) or legitimately remove
   the bad key, change all secrets, and re-encrypt as normal.

Next, merge the aforementioned PR into the repository. After that, you will want to
rebase your own fork of the code to include this new merge commit

.. code-block:: bash

   git fetch upstream
   git stash
   git rebase upstream/devel
   git stash apply

The above follows a simple set of steps where-by we

- Get any changes from the upstream source code (which would include the PR that the
  user who wanted to be added just made)
- Stash any changes that we may have been working on. This prevents the next step from
  failing.
- Rebase the upstream code-base onto your current code-base. This will allow the new
  user's PR to land in your local source tree.
- Re-apply the code that you previously stashed away. This will put you back to where
  you left off.

With the new changes in your source tree, it's time that you re-encrypted all of the
private files with the new users public key. To do that, you can use the
`blackbox_update_all_files` command from inside of any of the development containers.

.. code-block:: bash

   root@a710b12b1e97:/here# blackbox_update_all_files
   ========== blackbox administrators are:
   caphrim007@gmail.com
   HypePDSvc
   k.austria@f5.com
   ========== Importing keychain: START
   gpg: key DBE7B40B4ACC6C92: public key "Kat Austria <k.austria@f5.com>" imported
   gpg: Total number processed: 10
   gpg:               imported: 1
   gpg:              unchanged: 9
   ========== Importing keychain: DONE
   ========== ENCRYPTED FILES TO BE RE-ENCRYPTED:
       devtools/secrets/jenkins_jobs.ini.secret.gpg
   ...
       test/runner/roles/harness/vars/TwoArmed-bigiq-5.3.0.yaml.gpg
       test/runner/roles/harness/vars/TwoArmed-iworkflow-2.1.0.yaml.gpg
   ========== FILES IN THE WAY:
       devtools/secrets/jenkins_jobs.ini.secret
       test/heat/jenkins-secondary-params.yaml
       test/pipeline/ci.f5.f5-ansible-public-to-private-parameters.include.yaml
       test/runner/roles/harness/vars/TwoArmed-bigip-12.1.2-hf1.yaml

   WARNING: This will overwrite any unencrypted files laying about.
   Press CTRL-C now to stop. ENTER to continue:

Press **ENTER** to proceed and re-encrypt all of the secrets. You will be asked for
your own encryption password in the process.

.. code-block:: bash

   ...
   ========== RE-ENCRYPTING FILES:
   ========== PROCESSING "devtools/secrets/jenkins_jobs.ini.secret"
   ========== Encrypting: devtools/secrets/jenkins_jobs.ini.secret
   ========== Encrypting: DONE
   ...
   ========== PROCESSING "test/runner/roles/harness/vars/TwoArmed-iworkflow-2.1.0.yaml"
   ========== EXTRACTED test/runner/roles/harness/vars/TwoArmed-iworkflow-2.1.0.yaml
   ========== Encrypting: test/runner/roles/harness/vars/TwoArmed-iworkflow-2.1.0.yaml
   ========== Encrypting: DONE
   ========== COMMITING TO VCS:
   [devel f7021f1] Re-encrypted keys
    35 files changed, 49 insertions(+)
    rewrite devtools/secrets/jenkins_jobs.ini.secret.gpg (100%)
   ...
    rewrite test/runner/roles/harness/vars/TwoArmed-bigiq-5.3.0.yaml.gpg (100%)
    rewrite test/runner/roles/harness/vars/TwoArmed-iworkflow-2.1.0.yaml.gpg (100%)
   ========== DONE.
   Likely next step:
       git push

`blackbox` will end with telling you what the likely next step is; `git push`. Indeed,
if you view the `git` log, you can see there is a new commit there for the re-encryption
process.

.. code-block:: bash

   commit f7021f14193d7d81f22920c2dbe0f16d90f08f17
   Author: Tim Rupp <caphrim007@gmail.com>
   Date:   Tue Nov 7 00:30:07 2017 +0000

       Re-encrypted keys

Therefore, do the push as requested. Once this is done, the new maintainer will have the
ability to decrypt the secrets.
