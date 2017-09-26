Securing sensitive information
==============================

Parts of the f5-ansible repository contain information that is considered sensitive
in nature, and therefore needs to have a particular amount of due-diligence applied
when handling it.

Information of that sort includes, but is not limited to,

* Product keys
* Internal URLs
* System configurations that are not relevant to the general public

To address the concerns of exposing this information in a plain-text manner, the
authors have put in place a series of GPG encrypted files. The remainder of this
document explains how this system works.

Tools used
----------

There are many existing tools that can help address the problem of storing
secret information in an otherwise public place. These include, but are not
limited to,

* blackbox (from StackExchange)
* git-crypt
* git-secret
* Keyringer
* Pass
* Transcrypt

The tool that we use is blackbox primarily because

* It works in our docker containers
* It has a large number of stars and forks
* It is just shell wrappers around GPG
* It automatically ignores files that have been registered
* StackExchange was a reason too

I won't go into any philosophical arguments on the others, suffice it to say that
`blackbox` does the job we needed to do.

Using it
--------

To make use of the system, the first thing you must do is create a set of GPG
keys to be used for encryption and decryption of secrets.

Creating a key can be done with the `gpg` command. Consider the following example

.. code-block: bash

   gpg --gen-key

This command will ask you a couple of questions related to your new keypair.
They are,

* Real name
* Email address

For example,

.. code-block:: bash

   root@9f1cc7b78557:~# gpg --gen-key
   gpg (GnuPG) 2.1.20; Copyright (C) 2017 Free Software Foundation, Inc.
   This is free software: you are free to change and redistribute it.
   There is NO WARRANTY, to the extent permitted by law.

   GnuPG needs to construct a user ID to identify your key.

   Real name: Alice User
   Email address: a.user@organization.com
   You selected this USER-ID:
       "Alice User <a.user@organization.com>"

   Change (N)ame, (E)mail, or (O)kay/(Q)uit?

To proceed, answer `O` (the letter, not the number) and the command will proceed
to ask you for a passphrase in a separate window.

.. code-block:: bash

   6──────────────────────────────────────────────────────^@
   < Please enter the passphrase to                       │
   < protect your new key                                 │
   <                                                      │
   < Passphrase: ________________________________________ │
   <                                                      │
   <       <OK>                              <Cancel>     │
   ^@─────────────────────────────────────────────────────5

If you do nothing else correctly for this procedure, you must **absolutely**
get this step correct. Your passphrase is considered hallowed ground. If Tim
had his way, it would be a fire-able offense to disclose it. This is **super**
important, so listen.

Your passphrase is what is used to decrypt and encrypt sensitive data in the
f5-ansible repository. If it is compromised, then the information contained
withing the `gpg` encrypted files is assumed to be compromised.

Now, because we include these `gpg` files in `git`, this also means that the
compromised versions are accessible even if we rotate the keys.

So it is **your** job to choose a passphrase (note I did not say pass**word**)
that is sufficiently long to hedge the risk of having it discovered computationally.

How do you do that?

There is a practice referred to as `Diceware` that allows you to choose a
passphrase that is sufficiently difficult to computationally discover.

Diceware is elaborated on in much greater detail here

* http://world.std.com/~reinhold/diceware.html

In a nutshell, you toss a dice and record the number. Those numbers correspond
to words in a word list.

It is recommended that the passphrase you create is *at least* six words and
a symbol; in any order.

Don't have a pair of dice to roll?
----------------------------------

Then you have a problem.

If you do not have a pair of dice to roll to make your word list, the next best
option is using an online service. There are ones that allow you to roll
digitally, as well as those that will generate word lists for you on the fly.

For example,

* https://www.rempe.us/diceware/#eff

Finishing up your key
---------------------

Once you have a passphrase chosen, enter it in the aforementioned box. Pressing
`Enter` will ask you to re-enter the passphrase.

.. code-block:: bash

   6──────────────────────────────────────────────────────^@
   < Please re-enter this passphrase                      │
   <                                                      │
   < Passphrase: ________________________________________ │
   <                                                      │
   <       <OK>                              <Cancel>     │
   ^@─────────────────────────────────────────────────────5

Pressing `Enter` after typing the passphrase a second time will generate the
necessary public and private keys for you, as well as add them to your GPG
keychain locally on disk.

For example,

.. code-block:: bash

   gpg: key 5FE19AB05871BDA3 marked as ultimately trusted
   gpg: revocation certificate stored as '/gpg//openpgp-revocs.d/6CA2078812CBB7F6112BDADF5FE19AB05871BDA3.rev'
   public and secret key created and signed.

   pub   rsa2048 2017-09-26 [SC] [expires: 2019-09-26]
         6CA2078812CBB7F6112BDADF5FE19AB05871BDA3
         6CA2078812CBB7F6112BDADF5FE19AB05871BDA3
   uid                      Alice User <a.user@organization.com>
   sub   rsa2048 2017-09-26 [E] [expires: 2019-09-26]

   root@9f1cc7b78557:~#

You can verify that your keys exist in your keyring with the following command

.. code-block:: bash

   gpg --list-keys

If you were successful, you will see your key in the list.

.. code-block:: bash

   pub   2048R/5871BDA3 2017-09-26 [expires: 2019-09-26]
   uid                  Alice User <a.user@organization.com>
   sub   2048R/0B29438A 2017-09-26 [expires: 2019-09-26]

.. note::

   Be aware that when you created your key, it was given an expiration date
   a couple years (two by default) in the future. It is critical that you
   perform a key renewal as your key becomes due for expiration. Instructions
   for doing this can be `found here`_

Including your key in the test environment
------------------------------------------

With your keys generated, you can now include them in the Docker development
containers that are provided with f5-ansible.

In the `devtools/docker-compose.yaml` file in this repository is a config
section that resembles the following

.. code-block:: yaml

   - type: bind
     source: ~/.gnupg
     target: /gpg

This configuration instructs `docker-compose` to create a path in your container
(at runtime) that maps the `.gnupg` directory in your home directory to the
`/gpg` directory in the container.

If you need to change the location in which your GPG keys are found on your
local filesystem, the recommended place to change that is in the configuration
above.

Encrypting files
----------------

Determining what you should and should not encrypt is the first step in this
process.

Generally speaking we encrypt anything that is "F5 specific". This is kind of
vague though, so here are some examples,

* Websites that are internal to F5
* License keys used for integration tests
* Configuration of system that is irrelevant to the public (insofar as it would
  not help them in any way to have)

For all of those, and more, instances, we encrypt.

Adding new files to the encryption process starts with the following command

.. code-block:: bash

   blackbox_register_new_file path/to/file.ext

.. note::

   The suite of `blackbox_` commands is your interface to the process of
   encryption and decryption. There are many commands that one can use.
   The ones you are most likely to use are,

   * blackbox_register_new_file
   * blackbox_decrypt_all_files
   * blackbox_deregister_file
   * blackbox_edit_start
   * blackbox_edit_end
   * blackbox_list_files

For a video demonstration of the above encryption process, refer to
[go/f5ansible-video-6609](go/f5ansible-video-6609)


.. _found here: https://www.g-loaded.eu/2010/11/01/change-expiration-date-gpg-key/
