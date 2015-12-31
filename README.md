# Ansible BIG-IP Role

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
