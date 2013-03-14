#!/usr/bin/env python

from __future__ import division
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
        goo[srcadd]["+"] = 0
        goo[srcadd]["r"] = 0

    if srcnode == srcadd and type == "+":
        goo[srcadd]["+"] += packetsize
    elif destnode == destadd and type == "r":
        goo[srcadd]["r"] += packetsize


for srcadd in goo:
    print srcadd, goo[srcadd]["r"] / 5 / 1000



file.close()
