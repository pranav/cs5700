#!/usr/bin/env python

from __future__ import division
"""
Takes 1 file and calculates drop rate
"""

import re
import sys
file = open(sys.argv[1], 'r')

goo = dict()

for line in file:
    l = line.split()
    type = l[0]
    time = float(l[1])
    srcnode = int(l[2])
    destnode = int(l[3])

    packetsize = int(l[5])

    srcadd = int(l[8].split(".")[0])
    destadd = int(l[9].split(".")[0])
    seqnum = l[10]

    if srcadd not in goo:
        goo[srcadd] = dict()
        goo[srcadd]["d"] = 0
        goo[srcadd]["+"] = 0

    if srcnode == srcadd and type == "+":
        goo[srcadd]["+"] += 1
    else type == "d":
        goo[srcadd]["d"] += 1


for srcadd in goo:
    print srcadd, goo[srcadd]["d"] / goo[srcadd]["+"]



file.close()
