#!/usr/bin/env python

import os

files = os.listdir('/here/library/modules')
print(','.join([os.path.splitext(x)[0] for x in files]))
