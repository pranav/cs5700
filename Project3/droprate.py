#!/usr/bin/env python

from __future__ import division
"""
Takes 1 file and calculates drop rate
"""

import re
import sys
file = open(sys.argv[1], 'r')


total = 0
drop = 0
for line in file:
  if re.match('d', line):
    drop += 1
  if re.match('\+', line):
    total += 1

print drop / total

