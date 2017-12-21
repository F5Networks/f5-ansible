Securing sensitive information
==============================

The f5-ansible repository contains sensitive information and needs to be secure.

This sensitive information includes, but is not limited to:

- Product keys
- Internal URLs
- System configurations not relevant to the general public

To prevent exposing this information in plain text, F5 uses a series of GPG encrypted files.

Tools used to secure information
--------------------------------

Many tools help prevent the storage of secret information in an otherwise public place. These include, but are not limited to:

- blackbox (from StackExchange)
- git-crypt
- git-secret
- Keyringer
- Pass
- Transcrypt

The tool that F5 uses is blackbox, primarily because:

- It works in Docker containers
- It has many stars and forks
- It is just shell wrappers around GPG
- It automatically ignores registered files
- StackExchange

Create a key
````````````

Start by creating a set of GPG keys to use for encryption and decryption of secrets.

Use the `gpg` command to create a key. For example:

.. code-block:: bash

   gpg --gen-key

This command will ask for your name and address.

For example:

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

To proceed, answer `O` (the letter, not the number) and the command will ask you for a passphrase in a separate window.

.. code-block:: bash

   6──────────────────────────────────────────────────────^@
   < Please enter the passphrase to                       │
   < protect your new key                                 │
   <                                                      │
   < Passphrase: ________________________________________ │
   <                                                      │
   <       <OK>                              <Cancel>     │
   ^@─────────────────────────────────────────────────────5

If you do nothing else correctly for this procedure, you must **absolutely** get this step correct.

Your passphrase decrypts and encrypts sensitive data in the f5-ansible repository. If your passphrase is compromised, then the information contained within the `gpg`-encrypted files is compromised.

Now, because you include these `gpg` files in `git`, the compromised versions are accessible even if you rotate the keys.

It is **your** job to choose a passphrase (not just pass**word**) that is sufficiently long to hedge the risk of having it discovered computationally.

Create a passphrase
```````````````````

A practice referred to as `Diceware` allows you to choose a passphrase that is sufficiently difficult to computationally discover.

You can read about Diceware in detail here:

- http://world.std.com/~reinhold/diceware.html

The idea is that you toss a dice and record the number. The numbers correspond to words in a list of words.

Your passphrase should be *at least* six words and a symbol, in any order.

If you do not have a pair of dice to roll, the next best option is to use an online service that rolls digitally or generates word lists on the fly. For example:

- https://www.rempe.us/diceware/

Complete your key
`````````````````

After you choose a passphrase, enter it in the aforementioned box. Press `Enter` and re-enter the passphrase.

.. code-block:: bash

   6──────────────────────────────────────────────────────^@
   < Please re-enter this passphrase                      │
   <                                                      │
   < Passphrase: ________________________________________ │
   <                                                      │
   <       <OK>                              <Cancel>     │
   ^@─────────────────────────────────────────────────────5

Pressing `Enter` after typing the passphrase a second time will generate the necessary public and private keys for you, as well as add them to your GPG keychain locally on disk.

For example:

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

You can verify that your keys exist in your keyring with the following command:

.. code-block:: bash

   gpg --list-keys

If you were successful, you will see your key in the list.

.. code-block:: bash

   pub   2048R/5871BDA3 2017-09-26 [expires: 2019-09-26]
   uid                  Alice User <a.user@organization.com>
   sub   2048R/0B29438A 2017-09-26 [expires: 2019-09-26]

.. note::

   By default, your key has an expiration date two years in the future. You must renew your key before it expires. Instructions can be `found here`_.

Include your key in the test environment
````````````````````````````````````````

After you generate your keys, you can include them in the Docker development containers that come with f5-ansible.

In the `devtools/docker-compose.yaml` file in this repository, a configuration section instructs `docker-compose` to create a path in your container at runtime. This path maps the `.gnupg` directory in your home directory to the `/gpg` directory in the container.

.. code-block:: yaml

   - type: bind
     source: ~/.gnupg
     target: /gpg

To change the local file system location where the GPG keys are, change it in this configuration.

Encrypt files
`````````````

Determining what you should and should not encrypt is the first step in this process.

Generally speaking, F5 encrypts anything that is "F5-specific". Some examples are:

- Websites that are internal to F5
- License keys used for integration tests
- System configuration that is irrelevant to the public (insofar as it would not help them in any way to have)

For all of those, and more, instances, encrypt.

Adding new files to the encryption process starts with the following command:

.. code-block:: bash

   blackbox_register_new_file path/to/file.ext

.. note::

   The suite of `blackbox_` commands is your interface to the process of encryption and decryption. The commands you are most likely to use are:

   * blackbox_register_new_file
   * blackbox_decrypt_all_files
   * blackbox_deregister_file
   * blackbox_edit_start
   * blackbox_edit_end
   * blackbox_list_files


.. _found here: https://www.g-loaded.eu/2010/11/01/change-expiration-date-gpg-key/
