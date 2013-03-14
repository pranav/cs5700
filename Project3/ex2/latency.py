#!/usr/bin/python

from __future__ import division
import sys

file = sys.argv[1]

"""
----
Usage:

    ./latency.py <input file>

Output:
    <average latency in seconds>


----
1. for each line in file:
        at = dict[srcadd] = dict()
        if line.srcnode == line.srcadd:
            at[seqnum]["+"] = line.time
        elif:
            at[seqnum]["r"] = line.time
        else:
            pass

2. average over it all
"""

f = open( file, "r" )


goo = dict()

for line in f:
    l = line.split()
    type = l[0]
    time = float(l[1])
    srcnode = int(l[2])
    destnode = int(l[3])

    srcadd = int(l[8].split(".")[0])
    destadd = int(l[9].split(".")[0])
    seqnum = l[10]

    # print srcnode, destnode, srcadd, destadd

    if srcadd not in goo:
        goo[srcadd] = dict()

    if seqnum not in goo[srcadd]:
        goo[srcadd][seqnum] = dict()

    if srcnode == srcadd and type == "+":
        goo[srcadd][seqnum]["+"] = time
    elif destnode == destadd and type == "r":
        goo[srcadd][seqnum]["r"] = time
    else:
        pass

for srcadd in goo:
    total = 0
    count = 0
    for seqnum in goo[srcadd]:
        at = goo[srcadd][seqnum]

        if "r" in at and "+" in at:
            count += 1
            total += goo[srcadd][seqnum]["r"] - goo[srcadd][seqnum]["+"]

    if count > 0: 
      print (total / count)



f.close()
