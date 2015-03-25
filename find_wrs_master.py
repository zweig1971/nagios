#!/usr/bin/python2
# -*- coding: utf-8 -*-


#--------------------------
# find_wrs_master.py 
#
# GSI 
# m.zweig 
# 03.2015 
# 
# this script scan the host.cfg for wrs
# all found wrs checked if master
# the master info written in host file 
# set the icon for the master
# 
# # -------------------------


import os,re,sys,commands, getopt, subprocess
from subprocess import Popen, PIPE

# status check_snmp 
_unknow  = -1
_ok      = 0
_warning = 1
_critical= 2

# var
_found_members  =[]
_found_wrs	=[]
_ipadress	=[]

# keywords
_detec_host_name= "host_name"
_detec_wrs	= "nwt"
_detec_master   = "MASTER"
_detec_info	= "; info:"
_detec_no_master= "WARNING !"

# pfad for the nagios information file (host.conf)
_hostfile       = "/etc/nagios/objects/hosts.cfg"

# script for the masterabfrage
_masterscript = "/home/bel/zweig/lnx/nagios_plugin/./check_wrs_master.py"

# find hostename
_findhostname_cmd = "host"
_findhostname_par = "| cut -d ' ' -f5"
_findiphost_par   = "| cut -d ' ' -f4"

# cmd for master icon
_master_icon =["        statusmap_image	whiterabbit_logo4040.jpg\n","        icon_image      whiterabbit_logo4040.jpg\n"]


def inser_line(master_info):

        # -- datei öffnen
        try:
                datei = open(_hostfile, "rU")
        except Exception:
                print "Cant open host file"
                sys.exit (_unknow)

	_data = datei.readlines()

	for index, _line in enumerate(_data):
		if _detec_info in _line :
			_data[index] =_data[index].strip(' \t\n\r')
			_data[index] = _detec_info+master_info+'\n'


	# -- datei speichern
	datei = file(_hostfile, "w")
	datei.writelines(_data)

	datei.close() 



def searchForMaster():

	# -- datei öffnen
	try:
        	datei = open(_hostfile, "r")
	except Exception:
        	print "Cant open host file"
        	sys.exit (_unknow)


	# -- find all devices in host file
	for line in datei:
		if _detec_host_name in line:
			_temp = line.rstrip()
			_temp = _temp.replace(" ","")
			_temp = _temp.split(_detec_host_name)[1]
			_found_members.append(_temp.strip(' \t\n\r'))

	datei.close()

	# -- find the wrs 
	for line in _found_members:
		if _detec_wrs in line:
			_found_wrs.append(line)


	for line in _found_wrs:
		# ip rausfinden
		_commandline = _findhostname_cmd+" "+line+_findiphost_par
	        process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
	        stdout, stderr = process.communicate()

		if(len(stdout)> 8):
			_ipadress.append(line+";"+stdout.split("\n")[0])

	# -- TM Master suchen

	print "running please wait",

	for line in _ipadress:
		_ip_temp = line.split(";")[1]
		_commandline = _masterscript+" "+ _ip_temp
	
		sys.stdout.write('.')
		sys.stdout.flush()
       
		process = Popen(_commandline ,shell=True,stdout=PIPE, stderr=PIPE)
	        stdout, stderr = process.communicate()
	
		if len(stderr) > 0:
			print stderr
	                sys.exit (_unknow)

		_ipadress[_ipadress.index(line)]= _ipadress[_ipadress.index(line)] + ";" + stdout.rstrip()
	
	# -- pruefen ob mehrere master gefunden worden sind oder gar keiner
	_found_master_cnt = 0

	for line in _ipadress:
		if (_detec_master in line):
			_found_master_cnt= _found_master_cnt + 1 
			_master_info=line.rstrip()

	if _found_master_cnt == 0:
		print "WARNING ! NO TIMING MASTER FOUND"
		_master_info= "WARNING ! NO TIMING MASTER FOUND"

	if _found_master_cnt > 2:
	        print "WARNING ! MORE THEN ONE TIMING MASTER FOUND"
		_master_info= "WARNING ! MORE THEN ONE TIMING MASTER FOUND"

	print "\n"+_master_info


	# -- in datei schreiben
	inser_line(_master_info)




def inser_icon():

# ------
# liest host datei ein
# liest master informationen aus
# sucht in host nach dem eintrag des masters
# fuegt rabbit icon in datei ein
# ------

        # -- datei öffnen
        try:
                datei = open(_hostfile, "rU")
        except Exception:
                print "Cant open host file"
                sys.exit (_unknow)

        _data = datei.readlines()

        # -- alten master icon eintrag löschen
	try:
		_data.remove(_master_icon[0])
		_data.remove(_master_icon[1])

	except:	
		pass

        # -- pruefen :gibt es einen master
        _index = [i for i, item in enumerate(_data) if re.search(_detec_no_master, item)]
        if len(_index) > 0:
                print "No Master specified"
                sys.exit (_unknow)

	# -- info zeile auswerten
	_index = [i for i, item in enumerate(_data) if re.search(_detec_info, item)]	
        if len(_index) == 0:
                print "There is no info row"
                sys.exit (_unknow)

	_line = _data[_index[0]]
        _temp= _line.replace(_detec_info, "")
        _temp= _temp.split(';')
        _master_name = _temp[0]

	# -- neuen master icon eintrag einfügen
	_index = [i for i, item in enumerate(_data) if re.search("host_name.*nwt0028m66", item)]	
        _data.insert(_index[0]+1, _master_icon[0])
        _data.insert(_index[0]+2, _master_icon[1])

        # -- datei speichern
	datei = file(_hostfile, "w")
	datei.writelines(_data)

	datei.close()




# ------------------------
# main
# ------------------------

def main():
	searchForMaster()
	inser_icon()





if __name__ == "__main__":
    main()





