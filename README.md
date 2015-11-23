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

## License

The MIT License (MIT)

Copyright (c) 2015 F5 Networks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[bigsuds]: https://pypi.python.org/pypi/bigsuds/
