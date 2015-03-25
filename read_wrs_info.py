#!/usr/bin/python2
# -*- coding: utf-8 -*-


#--------------------------
# read_wrs_info.py
#
# GSI 
# m.zweig 
# 11.12.2015 
# 
# read with snmpwalk the information
# prepairing the data and give it back
# # -------------------------


import re,sys,commands, getopt, subprocess
from subprocess import Popen, PIPE

# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2

# pfad/name of snmp command  
_command	= "snmpwalk -v1 -c public "
_snmpinfo	= "1.3.6.1.4.1.96.100.4"	

# ------------------------
# main
# ------------------------

_tempmess=[]
_listmess=[]

_hostadress =" "+str(sys.argv[1])
_commandline = _command+_hostadress+" "+_snmpinfo

process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)

try:
	stdout, stderr = process.communicate()
except :
        print "WRS not responding"
        sys.exit(_critical)


# something wrong -> bye
if len(stderr) > 0 or len(stdout) == 0:
        print "No information available"
        print stderr
        sys.exit(_warning)


# prepairing data
_tempmess = stdout.splitlines()

for line in _tempmess:
	_listmess.append(line.split("STRING:")[1].lstrip().replace('"',""))


print "White Rabbite SW VS:",_listmess[0]
print "Producer:",_listmess[6]
print "Platform:",_listmess[5]
print "HW Version:",_listmess[4]
print "Git hash info:"
print _listmess[1]
print _listmess[2]
print _listmess[3]

