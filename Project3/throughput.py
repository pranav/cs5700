#!/usr/bin/env python

import re
import sys
file = open(sys.argv[1], 'r')

recv = 0
for line in file:
  if re.match('r', line):
    recv += 1

print (recv*1000)/5 / 1000,

