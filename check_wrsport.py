#!/usr/bin/python2
# -*- coding: utf-8 -*-


#--------------------------
# check_wrsport.py
#
# GSI 
# m.zweig 
# 09.12.2015 
# 
# read port information with snmp and give it out
# give ok back if all values under thershold
# if not gives a critical and a error message back
# -------------------------


import re,sys,commands, getopt, subprocess
from subprocess import Popen, PIPE


# pfad/name of snmp command  
_PFAD_chsnmp = "/usr/lib64/nagios/plugins/check_snmp"

# main snmp
_main_snmp = "1.3.6.1.4.1.96.100.2.1."

# snmp entpunkte
_snmp_ctr = (["RX_Overrun",".2", " -c5"], ["RX_Invalid_Code",".3", " -w5 -c10"], 
		["RX_Sync_Lost",".4", " -c5"], ["RX_PCS_Errors",".7"," -w5 -c10"], 
		["RX_Giant_Frames",".8"," -w5 -c10"], ["RX_CRC_Errors",".10"," -w5 -c10"], 
		["TX_Frames",".19"," "], ["RX_Frames",".20"," "])


# status check_snmp 
_unknow  = -1
_ok	 = 0
_warning = 1
_critical= 2


# answer from the smnp request
_list_messages=[]


# head message
_message_head = "Everything is fine !"
_exit = _ok

# ------------------------
# main
# ------------------------


_hostadress = " -H "+str(sys.argv[1])
_snmp_wrs_port = str(sys.argv[2])


for x in range(0, len(_snmp_ctr)):
	snmp_command = _PFAD_chsnmp+str(" -C public"+_hostadress+" -l "+_snmp_ctr[x][0]+" -o "+_main_snmp+_snmp_wrs_port\
	+_snmp_ctr[x][1]+_snmp_ctr[x][2])

	process = Popen(snmp_command,shell=True,stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	_list_messages.append(stdout)


for line in _list_messages:
        if "WARNING" in line:
		_error = line.split("|")
                _message_head="A WARNING has occured :"+_error[0]
		_exit=_warning

for line in _list_messages:
	if "CRITICAL" in line:
		_error = line.split("|")
		_message_head="A CRITICAL error has occured :"+_error[0]	
		_exit=_critical


print _message_head
for line in _list_messages:
	_print_line=line.split("|")
	print _print_line[0]


sys.exit(_exit)


#snmp_command = _PFAD_chsnmp+str(" -C public"+_hostadress+" -l "+_snmp_ctr[6][0]+" -o "+_main_snmp+_snmp_wrs_port\
#		+_snmp_ctr[6][1]+_snmp_ctr[6][2])



#" -C public"+_hostadress+" -l "+_snmp_ctr[0][0]+" -o "+_main_snmp+_snmp_wrs_port+_snmp_ctr[0][1]+_snmp_ctr[0][2]



#print snmp_command 


#process = Popen(snmp_command,shell=True,stdout=PIPE, stderr=PIPE)
#stdout, stderr = process.communicate()
#print stdout
#print stderr









#print "BULLSHIT ! The dog is on the rocket ! | DATA 12 18 50"
#print "Arguments",str(sys.argv[1]),' ',str(sys.argv[2])
#print "The sensor 8 is on the top"
#print "The sensor 12 is off"
#print "Fan is running | Prefdata 12"
#print "Prefdata 23 :245: 00"
#print "Prefdata 4711 :ON: OFF"
#sys.exit(2)

