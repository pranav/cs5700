#!/usr/bin/env python

from tcp import *

s = Shoe()
s.socket()
s.connect(('web.hybridfire.net', 80))
