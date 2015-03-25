#!/usr/bin/python2
# -*- coding: utf-8 -*-

#--------------------------
# read the wrs date/time 
#
# GSI 
# m.zweig 
# 03.2015 
# 
# read with snmpwalk date and time
# -------------------------


import re,sys,commands, getopt, subprocess
from subprocess import Popen, PIPE

# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2

# pfad/name of snmp command  
_command        = "snmpwalk -v1 -c public "
_snmpinfo       = "1.3.6.1.4.1.96.100.5.2.0"

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
        print "WRS not responding"
        sys.exit(_critical)

# something wrong -> bye
if len(stderr) > 0 or len(stdout) == 0:
        print "No information available"
        print stderr
        sys.exit(_warning)


# prepairing data
_tempmess = stdout

_listmess = _tempmess.split("STRING: ")
_listmess[1]=_listmess[1].strip()
_listmess[1]=_listmess[1].replace(chr(34),"")

_temp = _listmess[1].split('-')
print _temp[0].lstrip()+"-"+ _temp[1]+"-"+ _temp[2]+" "+_temp[3]

