#!/usr/bin/python

import sys, os
cmd = """/course/cs4700f12/ns-allinone-2.35/bin/ns ex3.tcl"""
queuetype = sys.argv[1]


# Run the script for the current bandwidth
os.system("""{cmd} {queuetype} e3_{queuetype}.tr""".format(cmd=cmd,queuetype=queuetype))

print "fin"
