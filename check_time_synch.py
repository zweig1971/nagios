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

# var
_found_line=[]
_temp_mess =[]
_found_members	=[]
_found_hostgrpn =""
_found_wrsgrpn  =""
_found_master_ip=[]


# keywords
_detec_key	= "info:"
_detec_hgrpcnt	= "hostgroupcnt" 
_detec_hgrpcnt  = "hostgroupname"
_detec_hostfail = "NXDOMAIN"
_detec_hostgrpn = "hostgroup_name"
_detec_hostgred = "}"
_detec_hostwrs  = "WRS"
_detec_members  = "members"
_detec_master	= "MASTER"

# find hostename
_findhostname_cmd = "host"
_findhostname_par = "| cut -d ' ' -f5"
_findiphost_par	  = "| cut -d ' ' -f4"

# pfad/name of snmp command for date/time  
_snmpcmd        = "snmpwalk -v1 -c public "
_snmpinfo       = "1.3.6.1.4.1.96.100.3.1.1.0"

# pfad/name file for date/time (node)
_timecmd	= "/common/usr/monitoring/bin/./wr-datum udp/"

# pfad for the nagios information file (host.conf)
_hostfile	= "/etc/nagios/objects/hosts.cfg"

# endung for the nodes
_nodes_append = ".timgm.acc.de"

# script for the masterabfrage
_masterscript = "/home/bel/zweig/lnx/nagios_plugin/./check_wrs_master.py"



# ------------------------
# main
# ------------------------

_hostadress =" "+str(sys.argv[1])
_commandline = _findhostname_cmd+ _hostadress + _findhostname_par 

process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)

try:
        stdout, stderr = process.communicate()
except :
        print "Hostname not found"
        sys.exit(_unknow)


# -- datei öffnen
try:
	datei = open(_hostfile, "r")
except Exception:
	print "Cant open host file"
	sys.exit (_unknow)

# something wrong -> bye
if _detec_hostfail in stdout:
	print "Hostname not found"
	sys.exit (_unknow)

_hostname = stdout
_hostname = _hostname.split('.'[0])

# -- rausbekommen zu welcher gruppe das gesuchte device gehoert

for line in datei:
	if _detec_hostgrpn in line:
		_found_hostgrpn = line.split(_detec_hostgrpn)[1]

	if _hostname[0] in line:
		_found_hostgrpn = _found_hostgrpn.replace(" ","")
		_found_hostgrpn = _found_hostgrpn.rstrip()
		break

	if _detec_hostgred in line:
		 _found_hostgrpn = "nothing"

if _found_hostgrpn == "nothing":
        print "No hostgroup found"
        sys.exit (_unknow)

print _found_hostgrpn

# -- namen der dazugehoerigen WRS gruppe rausbekommen

datei.seek(0)# wieder von vorne beginnen
for line in datei:
	if (_detec_key in line) and (_found_hostgrpn in line):
		_temp_mess = line.split("/")		 	
		for name in _temp_mess:
			if _detec_hostwrs in name:
				_found_wrsgrpn= name

if _found_wrsgrpn == "":
	print "No suitable WRS Hostgroup found"
	sys.exit (_unknow)

print _found_wrsgrpn

# -- gefundene WRS hostgruppe suchen und member nach dem Timing-Master suchen

datei.seek(0) # wieder von vorne
for line in datei:
	if (_detec_hostgrpn in line) and (_found_wrsgrpn in line):	# -- suche nach hostgroup_name 
		for line in datei:
			if _detec_members in line:			# -- suche nach wrs
				line=line.rstrip()
				line=line.replace(" ","")
				_found_members = line.split(",")	
				_found_members[0] = _found_members[0].split(_detec_members)[1]	
				break	

                        if (_detec_hostgred in line):
                                print "End Of File. No members found "
                                sys.exit (_unknow)
				

if len(_found_members)== 0:
	print "No nwts found "
        sys.exit (_unknow)

print _found_members

# -- Gefundene switche nach dem master abklappern

# -- First find the IP out
for line in _found_members:

	# ip rausfinden
	_commandline = _findhostname_cmd+" "+line+_findiphost_par 	
        process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

	if len(stderr) > 0:
		print stderr
		sys.exit (_unknow)

	_ipadress=stdout.split("\n")[0] 

	# -- TM Master suchen
	_commandline = _masterscript+" "+ _ipadress

        process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
	_result = stdout


	print stdout

        if len(stderr) > 0:
                print stderr
                sys.exit (_unknow)

	if _detec_master in _result:
		_found_master_ip.append (_ipadress)
		_found_master_ip.append (line)
		break;


 
print _found_master_ip


#	print stdout








#	_commandline = _masterscript+" "+line+_nodes_append
#	print _commandline
#
#	process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
#	stdout, stderr = process.communicate()

#	print line+": "+stdout


		#_found_line.append(line.rstrip())
		



