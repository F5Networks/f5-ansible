# Ansible F5 Role

## Overview

The F5 role provides the foundation for working with F5 BIG-IP devices
and Ansible. The F5 role for Ansible provides the ability to manage
configuration resources in BIG-IP. The architecture of the roles makes inherent
use of the BIG-IP SOAP and REST APIs as well as the tmsh API where required.

The Ansible F5 role is freely provided to the open source community for automating
BIG-IP device configurations using Ansible. Support for the modules is provided
on a best effort basis by the F5 community. Please file any bugs, questions or
enhancement requests using [Github Issues](https://github.com/F5Networks/ansible-f5/issues)

### Requirements

* BIG-IP 11.6.0 or later
* Advanced shell for user account enabled
* [bigsuds Python Client 1.0.3 or later] [bigsuds]

[bigsuds]: https://pypi.python.org/pypi/bigsuds/

### Purpose

The purpose of this repository is to serve as a staging ground for Ansible
modules that we would prefer to have upstreamed over the course of time.

With that said, the following should be taken into consideration.

  - The modules in this repository may be broken periodically due to
    experimentation or refactoring

  - Modules prefixed with underscores are considered deprecated

  - When a module is deprecated, it will have been upstreamed into the core
    Ansible product. From that point forward, the module will be maintained
    in Ansible's github repository. Changes may still take place in the
    deprecated modules in this repository, but it will be only for research
    and experimentation purposes.

  - This module will continue to be a place where code is tested and validated
    when changes are made in upstream Ansible or locally here.

### Your ideas

I'm curious to know what sort of modules you want to see created. If you have
a use case and can sufficiently describe the behavior you want to see, open
an issue in this repository and we will hammer out the details.
