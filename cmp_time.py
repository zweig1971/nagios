#!/usr/bin/python2
# -*- coding: utf-8 -*-


#--------------------------
# cmp_time.py 
#
# GSI 
# m.zweig 
# 03.2015 
#
# this shit read the master info from the host.conf
# it read the time/date from master
# it read the time/date from the ip what given
# it compare the date and the time from master and node
# it gives a ok or a failue back. 
# (by time compare : only hour an minutes, not sec. to slow sometimes) 
# -------------------------


import os,re,sys,commands, getopt, subprocess
from subprocess import Popen, PIPE

# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2

# keywords
_detec_host_name= "host_name"
_detec_wrs      = "nwt"
_detec_master   = "MASTER"
_detec_info     = "; info:"
_detec_no_master= "WARNING !"

# pfad for the nagios information file (host.conf)
_hostfile       = "/etc/nagios/objects/hosts.cfg"

# pfad for the time request wrs
_wrs_time 	= " /common/usr/monitoring/nagios/selfplugins/./read_wrs_time.py"

# pfad for the time request nodes
_node_time	= "/common/usr/monitoring/bin/./wr-datum udp/"

# find hostename
_findhostname_cmd = "host"
_findhostname_par = "| cut -d ' ' -f5"
_findiphost_par   = "| cut -d ' ' -f4"


# ------------------------
# main
# ------------------------

_listmess=[]

# check argument
try:
	_hostadress =str(sys.argv[1])
except Exception:
        print "No argument"
        sys.exit (_unknow)

# read the master info from host file
try:
	datei = open(_hostfile, "r")
except Exception:
        print "Cant open host file"
        sys.exit (_unknow)

_data = datei.readlines()

# pruefen :gibt es einen master
_index = [i for i, item in enumerate(_data) if re.search(_detec_no_master, item)]
if len(_index) > 0:
	print "No Master specified"
	sys.exit (_unknow)

# info zeile auswerten
_index = [i for i, item in enumerate(_data) if re.search(_detec_info, item)]
if len(_index) == 0:
	print "There is no info row"
	sys.exit (_unknow)

_line = _data[_index[0]]
_temp= _line.replace(_detec_info, "")
_temp= _temp.split(';')
_master_ip = _temp[1]

# i am the master
if (_master_ip == _hostadress):
        print "I AM THE MASTER"
        sys.exit (_ok)

# find the name of the ip
_commandline = _findhostname_cmd+" "+_hostadress+_findhostname_par
process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

if len(stderr) > 0:
	print stderr
	sys.exit (_unknow)

# time reqest from the node
if _detec_wrs in stdout:
	_commandline = _wrs_time+" "+_hostadress
else:
	_commandline = _node_time+_hostadress 

process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

if len(stderr) > 0:
        print stderr
        sys.exit (_unknow)

_node_time = stdout.rstrip()

# time request from the master
_commandline = _wrs_time+" "+_master_ip

process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

if len(stderr) > 0:
        print stderr
        sys.exit (_unknow)

_master_time = stdout.rstrip()

# extract time of the master
_master_date = _master_time.split(' ')[0]
_master_time = _master_time.split(' ')[1]

# extract time of the node
_node_date = _node_time.split(' ')[0]
_node_time = _node_time.split(' ')[1]

if (_master_date != _node_date):
	print "Date does not match"
	sys.exit (_critical)

if (_master_time[0:5] != _node_time[0:5]):
        print "Time does not match"
        sys.exit (_critical)

print "Date/Time is synchronous"








 



