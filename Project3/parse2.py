#!/usr/bin/python

import sys, os
cmd = """/course/cs4700f12/ns-allinone-2.35/bin/ns ex2.tcl"""
tcpvar1 = sys.argv[1]
tcpvar2 = sys.argv[2]

tcpvar = ""

t1 = tcpvar1.split("/")

if len(t1) == 2:
    tcpvar += t1[1]
else:
    tcpvar += "Tahoe"


t2 = tcpvar2.split("/")

if len(t2) == 2:
    tcpvar += t2[1]
else:
    tcpvar += "Tahoe"



cbr_bw = 1

for cbr_bw in range(1, 100):
    # Run the script for the current bandwidth
    os.system("""{cmd} {cbr_bw}mb e2_{tcpvar}_{cbr_bw}.tr {tcpvar1} {tcpvar2}""".format(cmd=cmd,cbr_bw=cbr_bw, tcpvar1=tcpvar1, tcpvar2=tcpvar2, tcpvar=tcpvar))


    # Parse File
    #f = open( """e1_{tcpvar}_{cbr_bw}.tr""".format(cbr_bw=cbr_bw, tcpvar=tcpvar), "r" )
    #f.close()

print "fin"
