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

* []Ansible 2.2.0 or greater][installing]
* Advanced shell for user account enabled
* [bigsuds Python Client 1.0.4 or later][bigsuds]
* [f5-sdk Python Client, latest available][f5-sdk]

### Documentation

All documentation is hosted on [ReadTheDocs][readthedocs].

When [writing new modules][writingnew], please refer to the
[Guidelines][guidelines] document.

### Purpose

The purpose of this repository is to serve as a **staging ground** for Ansible
modules that we would prefer to have upstreamed over the course of time.

The modules in this repository **may be broken** due to experimentation
or refactoring

### Your ideas

We are curious to know what sort of modules you want to see created. If you have
a use case and can sufficiently describe the behavior you want to see, open
an issue here and we will hammer out the details.

### Support

The code provided in this repository should be considered F5 contributed, and
not F5 supported. If you are familiar with similar verbiage on DevCentral, then
you are familiar with what it means here.


[bigsuds]: https://pypi.python.org/pypi/bigsuds/
[f5-sdk]: https://pypi.python.org/pypi/f5-sdk/
[readthedocs]: https://f5-ansible.readthedocs.io/en/latest/
[guidelines]: https://f5-ansible.readthedocs.io/en/latest/development/guidelines.html
[writingnew]: https://f5-ansible.readthedocs.io/en/latest/development/writing-a-module.html
[installing]: https://f5-ansible.readthedocs.io/en/latest/usage/getting_started.html#installing-ansible