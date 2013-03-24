#!/usr/bin/env python

from tcp import *

s = Shoe()
s.socket()
s.connect(('ccs.neu.edu', 80))
