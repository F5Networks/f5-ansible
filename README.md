# Ansible F5

## Overview

This repository provides the foundation for working with F5 devices and Ansible.
The architecture of the modules makes inherent use of the BIG-IP SOAP and REST
APIs as well as the tmsh API where required.

These modules are freely provided to the open source community for automating
BIG-IP device configurations using Ansible. Support for the modules is provided
on a best effort basis by the F5 community. Please file any bugs, questions or
enhancement requests using [Github Issues](https://github.com/F5Networks/f5-ansible/issues)

### Requirements

* Advanced shell for user account enabled
* [bigsuds Python Client 1.0.4 or later] [bigsuds]

[bigsuds]: https://pypi.python.org/pypi/bigsuds/


### Purpose

The purpose of this repository is to serve as a staging ground for Ansible
modules that we would prefer to have upstreamed over the course of time.

The modules in this repository may be broken periodically due to experimentation
or refactoring

### Your ideas

I'm curious to know what sort of modules you want to see created. If you have
a use case and can sufficiently describe the behavior you want to see, open
an issue in this repository and we will hammer out the details.

### Support

The code provided in this repository should be considered F5 contributed, and
not F5 supported. If you are familiar with similar verbiage on DevCentral, then
you are familiar with what it means here.

#### Deprecated modules

Modules incubating in this repository will, over time, be considered for inclusion
in Ansible itself (where interest to have them exists). When a module is merged
upstream, the associated module in this repository will be renamed to an
underscore module.

  * bigip_user.py

becomes

  * _bigip_user.py

This is inline with Ansible's documentation [here] [deprecation].

When a module is deprecated, it will have been upstreamed into the core
Ansible product. From that point forward, the module will be maintained
in Ansible's github repository.

At that time, please open bugs and other issues by visiting Ansible's github
issue tracker.

Changes may still take place in the deprecated modules in this repository,
but it will be only for research and experimentation purposes.

[deprecation]: http://docs.ansible.com/ansible/developing_modules.html#deprecating-and-making-module-aliases

#### Support

I provide best effort support through this forum, but if you are interested in
more eyes capable of addressing your problem, I recommend asking on the 
[Ansible mailing list] [mlist]. There are F5'ers and DevCentral community
members who are subscribed to that list who can assist you with questions and
bugs.

Feel free to open bugs on this issue tracker for non-deprecated modules.

[mlist]: https://groups.google.com/forum/#!forum/Ansible-project

#### Testing

This repository will continue to be a place where code is tested and validated
when changes are made in upstream Ansible or locally here.
