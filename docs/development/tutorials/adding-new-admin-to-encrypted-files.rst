Allow new admin access of private data
======================================

In this tutorial I will outline the steps you need to take to add a new person to the
list of allowed admins for handling the encrypted data in this repository.

When should I do this?
----------------------

You should do this whenever you have deemed it necessary that a new person should be
assigned to handle secure information.

Our policy is that, at most, two (2) people need to be granted this responsibility.
These two people will be named the **primary** and **secondary** respectively.

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
in the `./devtools/bin` directory. In this example I will use the `run-py2.7.10`
script to launch the relevant container.

We are going to begin with the person who wants to be added.

For the person who wants to be added
------------------------------------

Before you begin, we assume that you have created an initial keypair to use for
encryption. If you have not yet done that, follow the instructions below in the
(Creating a keypair)[] section.

Begin by starting that container with the necessary script

.. code-block:: bash

   SEA-ML-RUPP1:f5-ansible trupp$ ./devtools/bin/run-py2.7.10

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


Creating a keypair
------------------

To perform these steps, start by firing up the py2.7.10 (or equivalent) container.

.. code-block:: bash

   SEA-ML-RUPP1:f5-ansible trupp$ ./devtools/bin/run-py2.7.10

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
