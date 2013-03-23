#!/usr/bin/env python

from tcp import *

s = Shoe()
s.socket()
s.connect(('tripadvisor.com', 80))
