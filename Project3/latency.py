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
1. Read everything in (sorted by packet id)
   - foreach line in file:
         at = arr[packetid]
         if line starts with +
           at.enqueue = line
         elif line starts with r
           at.receive = line
         elif line starts with d
           remove arr[packetid]
         else
           pass?

2. For each non-null entry in arr:
     print entry.receive.time - entry.enqueue.time

3. average over it all...


"""
f = open( file, "r" )


goo = dict()

for line in f:
    l = line.split()
    id = l[11]

    if id not in goo:
        goo[id] = dict()


    type = l[0]
    time = float(l[1])

    if type == "+":
        goo[id]["+"] = time
    elif type == "r":
        goo[id]["r"] = time
    else:
        del goo[id]

total = 0
count = 0
for id in goo:
    at = goo[id]
    if "r" in at and "+" in at:
        count += 1
        total += goo[id]["r"] - goo[id]["+"]

print (total / count)

f.close()
