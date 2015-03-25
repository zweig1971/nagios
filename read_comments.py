#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re,sys,commands, getopt, subprocess
from subprocess import Popen, PIPE

# comment line start with
detec_co ="#"

# pfad / name from host for display comments
_PFAD_host = "/common/usr/dhcp/hosts.conf"


# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2


# ------------------------
# main
# ------------------------


_hostadress = str(sys.argv[1])

#open host file
try:
   datei = open(_PFAD_host,"r")
except Exception:
   print "UNKNOWN"
   sys.exit(_ok)


#search in host file for hostadress
for line in datei:
   if _hostadress in line:
     if not (line.startswith(detec_co)):
	line=line.split(detec_co)
	print line[1]		
	sys.exit(_ok)

print "UNKNOWN"
sys.exit(_ok)




