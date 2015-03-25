#!/usr/bin/python2
# -*- coding: utf-8 -*-

#--------------------------
# check_node_stat.py
#
# GSI 
# m.zweig 
# 09.12.2015 
# 
# check node with eb-ls if response
# if response everything is fine
# not -> node is dead
#-------------------------


import re,sys
import commands, getopt, subprocess
from subprocess import Popen, PIPE


# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2

# eb-ls commandline
orderline_scu = "eb-ls tcp/"
orderline_pex = "eb-ls udp/"

# ------------------------
# main
# ------------------------


_hostadress = str(sys.argv[1])
_node_type  = str(sys.argv[2])

# node type
if _node_type == "scu":
        orderline = orderline_scu
elif _node_type == "pex":
        orderline = orderline_pex
else:
        print "No information available"
        print "wrong node type"
        sys.exit(_warning)

orderline = orderline+_hostadress
process = Popen(orderline,shell=True,stdout=PIPE, stderr=PIPE)

try:
	stdout, stderr = process.communicate(timeout=10)
except :
        print "Node not responding"
        sys.exit(_critical)

# something wrong -> bye
if len(stderr) > 0 or len(stdout) == 0:
        print "This node have a problem"
        print stderr
        sys.exit(_critical)

print "Everything is fine !"
sys.exit(_ok)


