#!/usr/bin/python2
# -*- coding: utf-8 -*-

# -------------------------
# read_scu_info.py
#
# GSI 
# m.zweig 
# 10.12.2015 
# 
# 
# read information from the scu
# platform / date / githash version
# -------------------------


import os,re,sys,commands, getopt, subprocess

from subprocess import Popen, PIPE

# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2


# key words 
_key_typeofscu = "Platform"
_key_builddate = "Build date"


# answer from the eb-info request
_list_mess = []
_mess_head = ""
_mess_date = ""

# eb-info commandline
orderline_scu = "/common/usr/bin/eb-info tcp/"
orderline_pex = "/common/usr/bin/eb-info udp/"


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
	stdout, stderr = process.communicate(timeout=15)
except :
        print "Node not responding"
        sys.exit(_critical)


# something wrong -> bye
if len(stderr) > 0 or len(stdout) == 0:
	print "No information available"
	print stderr
	sys.exit(_warning)


# prepairing data
_list_mess=stdout.strip("\x00").splitlines()

# find keywords
for line in _list_mess:
	if _key_typeofscu in line:
		_mess_head = line

	if _key_builddate in line:
		_mess_date = line


# find git hash
_list_mess=stdout.strip("\x00").split( "\n\n")

# output
print _mess_head
print _mess_date
print "Git hash info:"
print _list_mess[1]
sys.exit(_ok)



