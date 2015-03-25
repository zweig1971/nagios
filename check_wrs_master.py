#!/usr/bin/python2
# -*- coding: utf-8 -*-

#--------------------------
# check_wrs_master.py
#
# GSI 
# m.zweig 
# 01.2015 
# 
# read with snmpwalk the information
# if wrs is master
# # -------------------------


import os,re,sys,commands, getopt, subprocess
from subprocess import Popen, PIPE

# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2

# pfad/name of snmp command  
_command        = "snmpwalk -v1 -c public "
_snmpinfo       = "1.3.6.1.4.1.96.100.3.1.1.0"

# ------------------------
# main
# ------------------------

_listmess=[]

_hostadress =" "+str(sys.argv[1])
_commandline = _command+_hostadress+" "+_snmpinfo

process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)

try:
        stdout, stderr = process.communicate()
except :
        print "Device not responding"
        sys.exit(_critical)

# something wrong -> bye
if len(stderr) > 0 or len(stdout) == 0:
        print "No information available"
        sys.exit(_warning)


# prepairing data
_tempmess = stdout

_listmess = _tempmess.split("Hex-STRING:")
_listmess[1]= _listmess[1].replace(" ","")

_masterID=int(_listmess[1],16)

if _masterID > 0:
	print "CLOCK Slave"
	sys.exit(_ok)
elif _masterID == 0:
        print "CLOCK MASTER"
        sys.exit(_ok)
else:
        print "Undefined"
        sys.exit(_ok)



