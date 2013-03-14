#!/usr/bin/python

import sys

file = sys.argv[1]

# Step 1: Readline (this should be the queue (+))
# Step 2: Store the time value (column 2)
# Step 3: Readline (this should be the recv (r))
# Step 4: Store the time value (column 2)
# Step 5: Output time2 - time1 (latency)

f = open( file, "r" )

for line in f:
  time1 = line.split()[2]
  line = f.readline()
  time2 = line.split()[2]
  print (time2 - time1)

f.close()

