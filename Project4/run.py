#!/usr/bin/env python

from tcp import *
import sys

s = Shoe()
s.socket()
s.connect((sys.argv[1], 80))

