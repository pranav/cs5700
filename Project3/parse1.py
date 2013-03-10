#!/usr/bin/python

import sys, os
cmd = """/course/cs4700f12/ns-allinone-2.35/bin/ns ns-simple.tcl"""
count = 0       # total number of packets
drops = 0       # dropped packets
bytes = 0       # total bytes transferred

# Aggregates the bytes in received
def calculate_throughput(line):
    global bytes
    if line[0] == "r":
        bytes = bytes + int(line[5])
    else:
        pass

def calculate_droprate(line):
    global drops, count
    if line[0] == "d":
        drops = drops + 1
    elif line[0] == "+":
        count = count + 1
    else:
        pass

def calculate_latency():
    pass


cbr_bw = 1

for cbr_bw in range(1, 100):
    # Run the script for the current bandwidth
    os.system("""{cmd} {cbr_bw}mb e1_{cbr_bw}.tr""".format(cmd=cmd,cbr_bw=cbr_bw))


    # Parse File
    f = open( """e1_{cbr_bw}.tr""".format(cbr_bw=cbr_bw), "r" )

    count = 0       # total number of packets
    drops = 0       # dropped packets
    bytes = 0       # total bytes transferred


    for line in f:
        lst = line.split()

        calculate_throughput(lst)
        calculate_droprate(lst)
        # calculate_latency(lst)

    throughput = bytes / 5
    droprate = drops / count

    print ""
    print "Calculations for bandwith of", cbr_bw, "mb"
    print "  Throughput (bytes per second): ", throughput
    print "  Droprate (percent)           : ", droprate
    print ""

    f.close()

print "fin"
