#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np
import datetime as dt
import logging 
from logging import handlers 
import time
from collections import OrderedDict
import paramiko
import get_info
from scp import SCPClient
import sys
import subprocess
import os 
import math
sys.path.append(os.getcwd() + '/isg_hw_meas_tools-pyixia')
from PyIxia import * 
from PyIxia.Ixia import Ixia
from Test import Test 
from collections import defaultdict

### Globals 
parser = argparse.ArgumentParser(description='Comms-workload automation. Configure and run successive comms workloads powered by Ixia or T-Rex(WIP) traffic generators.')
parser.add_argument('-i','--iter-file', dest='iter', default='auto_iter.txt', help='Filename for storing workload configuration')
parser.add_argument('-d','--rte-sdk', dest='rte_sdk', default='/home/dpdk', help='Location of the DPDK root directory')
args = vars(parser.parse_args())
iter_file=args['iter']
RTE_SDK=args['rte_sdk']


USR_EMAIL='georgii.tkachuk@intel.com'
#USR_EMAIL='pynthamilselvanx.ramanathan@intel.com'
EMON_DUT='/home/hw_meas_tools/sep/bin64/emon'

RTE_TARGET='x86_64-native-linuxapp-gcc'

user = 'root'
password = 'root245'
component='DPDK' 
workload_name = 'ipsec'
	

### Platform and NIC definitions:
model_to_arch = {
	26 : 'NEHALEM_EP' ,
	30 : 'NEHALEM' ,
	28 : 'ATOM' ,
	53 : 'ATOM_2' ,
	54 : 'ATOM_CENTERTON' ,
	55 : 'ATOM_BAYTRAIL' ,
	77 : 'ATOM_AVOTON' ,
	92 : 'ATOM_APOLLO_LAKE' ,
	95 : 'ATOM_DENVERTON' ,
	37 : 'CLARKDALE' ,
	44 : 'WESTMERE_EP' ,
	46 : 'NEHALEM_EX' ,
	47 : 'WESTMERE_EX' ,
	42 : 'SANDY_BRIDGE' ,
	45 : 'JAKETOWN' ,
	58 : 'IVY_BRIDGE' ,
	69 : 'HASWELL_ULT' ,
	70 : 'HASWELL_2' ,
	62 : 'IVYTOWN' ,
	63 : 'HASWELLX' ,
	61 : 'BROADWELL' ,
	71 : 'BROADWELL_XEON_E3' ,
	86 : 'BDX_DE' ,
	78 : 'SKL_UY' ,
	158 : 'KBL' ,
	142 : 'KBL_1' ,
	79 : 'BDX' ,
	87 : 'KNL' ,
	94 : 'SKL' ,
	85 : 'SKX' 
}



platform_channels = {
	'SKX': 6,
	'ATOM_DENVERTON': 2,
	'bdw-de-ns': 2,
	'BDX': 4
}

platform_ports = {
	'SKX': [2,4,6,8,12],
	'ATOM_DENVERTON': [2,4],
	'bdw-de-ns': [2,4,6,8],
	'BDX': [2,4,6,8]
}
	

platform_cdev = {
	'SKX': '37c9',
	'ATOM_DENVERTON': '19e3',
	'bdw-de-ns': '6f55',
	'BDX': '443'
}

nic_ids = {
	'X710': '1572',
	'FPK?': '19e3',
	'bdw-de-ns': '6f55',
	'DNV?': '15ac'
}

core_combinations_list = {
	'2': ["1c1t","1c2t","2c2t"],
	'4': ["1c1t","1c2t","2c2t","2c4t","4c4t"],
	'6': ["1c1t","1c2t","2c2t","3c3t","3c6t","6c6t"],
	'8': ["1c1t","1c2t","2c2t","2c4t","4c4t","4c8t","8c8t"],
	'12': ["1c1t","1c2t","2c2t","2c4t","4c4t","3c3t","3c6t","6c6t","6c12t","12c12t"]
}
microserver_core_combinations_list = {
	'2':["1c","2c","4c"],
	'4':["1c","2c","4c"]
}

platform_name = {
	'SKX': 'Neon City',
	'bdw-de-ns': 'Durango-NS',
	'ATOM_DENVERTON': 'Harcuvar',
	'BDX': 'SuperMicro'
}

platform_chipset = {
	'SKX': 'Lewisburg',
	'bdw-de-ns': '',
	'ATOM_DENVERTON': 'N/A',
	'BDX': ''
}

accelerator_name = {
	'SKX': "Lewisburg",
	'bdw-de-ns': '',
	'ATOM_DENVERTON': 'nCPM QAT',
	'BDX': 'Coleto Creek'
}

### IPSec command line 
ll = {
	'l':" -l ",
	'n':"",
	'm':" --socket-mem 1024,0 ",
	'w_crypto':"",
	'w_nic':"",
	'dash':" -- ",
	'p':"",
	'u':"",
	'config':"",
	'f':"",
	'P':" -P"
}

def ui_loop(li, input_str, all_condition = False, max_out = -1, dups_allowed = True):
	ret = '-1'
	ret_list = []
	while ret != '0' and len(ret_list) != max_out:
		for i,j in zip(range(len(li)),li):
			print('{}) {}'.format(i+1,j.replace('\n','')))
		if all_condition:
			print("a) All")
		print("0) Done")
		valid = False
		while not valid:
			ret=input(input_str + "or 0 to continue:\n") or '0'
			if (ret.lower() == 'a'):
				if len(li) <= max_out:
					return li			
				else:
					print("Error: all is too many!")
			elif (int(ret)-1 <= len(li)):
				valid = True
			else:
				print("Error: incorrect index!")
			if (ret !='0' and ret != 'a'):
				ret_list.append(li[int(ret)-1])
		print("Your choices:" + str(ret_list))
	return ret_list


class Dut:
	def __init__(self, name):
		self.prepped = False
		self.ssh = paramiko.SSHClient()
		self.name = name
		self.cmdline = {}
		self.cc = []
		self.info = []
		self.ip_addr=""
		self.platform = "SKX"
		self.ports = 0
		self.cryptodev = ""
		self.nic = ""
		self.nic_list = []
		self.nic_dict = {
			'2': [],
			'4': [],
			'6': [],
			'8': [],
			'10': [],
			'12': []
		}
			

	def check(self):
		""

	def prep(self):
		info = []
		self.scp.put('get_info.py','/root/get_info.py')
		self.ssh.exec_command('apt-get install dmidecode')
		i,o,e = self.ssh.exec_command('/root/get_info.py')
		
		for line in o:
			info.append(line.replace('\n',''))
		

		self.ssh.exec_command('[ -d /mnt/huge ] || mkdir -p /mnt/huge')
		self.ssh.exec_command('echo 8 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages')
		self.ssh.exec_command('mount -t hugetlbfs -o pagesize=1G nodev /mnt/huge')

		self.ssh.exec_command('lsmod | grep -q i40e && rmmod i40e')
		self.ssh.exec_command('lsmod | grep -q -w "uio" || modprobe uio')
		self.ssh.exec_command('lsmod | grep -q igb_uio || insmod {}/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko'.format(RTE_SDK))
		self.ssh.exec_command('lsmod | grep -q i40e && rmmod i40e'.format(RTE_SDK))

		self.ssh.exec_command("{}/usertools/dpdk-devbind.py -b igb_uio $(lspci -d:{} | awk '{{ print $1 }}')".format(RTE_SDK, platform_cdev[self.platform]))
		for n in self.nic_list:
			self.ssh.exec_command("{}/usertools/dpdk-devbind.py -b igb_uio $(lspci -d:{} | awk {{'print $1'}})".format(RTE_SDK, n))

		for x in range(20):
			self.info.insert(x, "")
		self.info[0]= platform_name[self.platform]
		self.info[1]= info[0]
		self.info[2]= platform_chipset[self.platform]
		self.info[5]= info[10]
		
		self.info[7]= "{}x10G".format(self.ports)
		self.info[8]= '{} {} {}MB, {} Channels'.format(info[11], info[12], info[14], info[15])
		self.info[9]= "{} x Intel(r) Ethernet Controller {}".format(self.ports/4, self.nic)
		self.info[10]= info[17]
		self.info[11]= info[18]
		self.info[12]= accelerator_name[self.platform]
		self.info[15]= info[22]
		self.info[16]= info[23]
		self.info[17]= component + '-' + workload_name

		self.check()
		fd = open("results/{}.info".format(self.name), "w")
		for line in self.info:
			fd.write(line)
			fd.write('\n')
		fd.close()

	def create_nic(self, num_ports):
		ret = ""
		
		devs = []
		for n in self.nic_list:
			i,o,e = self.ssh.exec_command("lspci -d:{} | awk '{{ print $1 }}'".format(n))
			devs.extend(o.readlines())

		print(devs)
		if not self.nic_dict[str(num_ports)]:
			self.nic_dict[str(num_ports)] = ui_loop(devs, "Choose NICs to be used for {}: ".format(self.name), all_condition = True, max_out = num_ports, dups_allowed = False)
		#if not self.nic_dict[str(num_ports)]:
		#	while len(self.nic_dict[str(num_ports)]) != num_ports:
		#		for y,z in zip(range(len(devs)), devs):
		#			print("{}) {}".format(y+1,z.replace('\n','')))	
		#		print("0) First {} NICs".format(num_ports))
		#		
		#		input_str = input("Choose NICs to be used for {}:".format(self.name))
		#		if input_str == '0':
		#			self.nic_dict[str(num_ports)].extend(devs[0:num_ports])
		#		else:
		#			self.nic_dict[str(num_ports)].append(devs[int(input_str)-1])
		#		print("Your choices:")
		#		print(self.nic_dict[str(num_ports)])
		#print devs 
		for p in self.nic_dict[str(num_ports)]:
			ret = ret +  " -w " + str(p).replace('\n','')
		return ret 

	

dut = []
dut.insert(0,Dut("ep0"))
dut.insert(1,Dut("ep1"))

dut[0].ip_addr=input(dut[0].name + " IP address <10.2.63.81>:") or '10.2.63.81'
dut[1].ip_addr=input(dut[1].name + " IP address <10.2.63.37>:") or '10.2.63.37'

dut[0].ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
dut[0].ssh.connect(dut[0].ip_addr, username=user, password=password)
dut[0].scp = SCPClient(dut[0].ssh.get_transport())

dut[1].ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
dut[1].ssh.connect(dut[1].ip_addr, username=user, password=password)
dut[1].scp = SCPClient(dut[1].ssh.get_transport())

for i in range(2):
	stdin,o,stderr = dut[i].ssh.exec_command('lscpu')
	lscpu = defaultdict(list)
	for l in o.readlines():
		n = l.split(':')
		if len(n) == 2:
			lscpu[n[0]].append(n[1].strip())
	if (lscpu['Model'] != None):
		model = lscpu['Model']
		dut[i].platform = model_to_arch[int(''.join(model))]
	else:
		dut[i].platform=input(dut[i].name + " Platform type [SKX]/ATOM_DENVERTON/bdw-de-ns/BDX:") or 'SKX'
	print('dut{} architecture was found to be {}'.format(i, dut[i].platform))





def main():
	cont = 1
	while cont:
		print("\n")
		print("1) Prep. Insert DPDK drivers, bind NIC/QAT, crate hugepages")
		print("2) Add test cases to the list. ")
		print("3) Remove test cases from the list. ")
		print("4) Run Quick tests over the existing list")
		print("5) Run EMON over an exisiting test. WIP")
		print("6) Print current test cases" )
		print("0) Exit")
		ui = int(input("Choose a menu option: "))
		if ui == 1:
			run_prep()
		elif ui == 2:
			run_add(iter_file) 
		elif ui == 3:
			run_remove() 
		elif ui == 4:
			run_run_qt()
		elif ui == 5:
			run_emon()
		elif ui == 6:
			run_print()
		elif ui == 7:
			run_analyze()
		elif ui == 0:
			print("Exiting...")
			sys.exit(1)
	

def parse_cc(cc):
	ncores=int(cc[0:cc.index('c')])
	nthreads=int(cc[cc.index('c')+1:cc.index('t')])
	return ncores, nthreads

def gen_ipsec_cfg(ports):
	ep0gcm = open('cfg/ipsec/auto-ep0-bd-gcm-{}p.cfg'.format(ports),'w')
	ep1gcm = open('cfg/ipsec/auto-ep1-bd-gcm-{}p.cfg'.format(ports),'w')
	ep0cbc = open('cfg/ipsec/auto-ep0-bd-cbc-{}p.cfg'.format(ports),'w')
	ep1cbc = open('cfg/ipsec/auto-ep1-bd-cbc-{}p.cfg'.format(ports),'w')
	for line in open('cfg/ipsec/ep0-bd-gcm.cfg','r'):
		ep0gcm.write(line)
	for line in open('cfg/ipsec/ep1-bd-gcm.cfg','r'):
		ep1gcm.write(line)
	for line in open('cfg/ipsec/ep0-bd-cbc.cfg','r'):
		ep0cbc.write(line)
	for line in open('cfg/ipsec/ep1-bd-cbc.cfg','r'):
		ep1cbc.write(line)
		
	for i in range(int(ports/2)):
		ep0_line = 'rt ipv4 dst 192.168.1{:02d}.0/24 port {}\n'.format(11+i, i)
		ep1_line = 'rt ipv4 dst 192.168.1{:02d}.0/24 port {}\n'.format(5+i, i)
		ep0gcm.write(ep0_line)
		ep0cbc.write(ep0_line)
		ep1gcm.write(ep1_line)
		ep1cbc.write(ep1_line)

	for i in range(int(ports/2),ports):
		ep0_line = 'rt ipv4 dst 172.16.2.{}/32 port {}\n'.format(5+(i-int(ports/2)), i)
		ep1_line = 'rt ipv4 dst 172.16.2.{}/32 port {}\n'.format(11+(i-int(ports/2)), i)
		ep0gcm.write(ep0_line)
		ep0cbc.write(ep0_line)
		ep1gcm.write(ep1_line)
		ep1cbc.write(ep1_line)

	ep0gcm.close()
	ep1gcm.close()
	ep0cbc.close()
	ep1cbc.close()
	dut[0].scp.put('cfg/ipsec/auto-ep0-bd-gcm-{}p.cfg'.format(ports), RTE_SDK+'/examples/ipsec-secgw/.')
	dut[0].scp.put('cfg/ipsec/auto-ep0-bd-cbc-{}p.cfg'.format(ports), RTE_SDK+'/examples/ipsec-secgw/.')
	dut[1].scp.put('cfg/ipsec/auto-ep1-bd-gcm-{}p.cfg'.format(ports), RTE_SDK+'/examples/ipsec-secgw/.')
	dut[1].scp.put('cfg/ipsec/auto-ep1-bd-cbc-{}p.cfg'.format(ports), RTE_SDK+'/examples/ipsec-secgw/.')

def run_qt(qt_cmd, test, add_emon):
	log = logging.getLogger(__name__)
	cfg_path = qt_cmd.replace('\n','')
	filename = test.name.replace('\n','')
	cfg_name = cfg_path.split('/')[-1].split('.')[0].replace('\n','')
	cfg = json.load(open(cfg_path,'r'))
	# If user defines custom logging, use it instead
	if 'log' in cfg:
	    dictConfig(cfg['log'])

	i = Ixia(cfg)

	###
	# User can insert customization here... i.e.
	#i.qt.create_test(i.trafficItem,pkt_sizes=(64,72,128,256,512,768,1024,1280,1420))
	#i.qt.ixobj.execute('help','execList','-all')
	i.qt.create_test(i.trafficItem,pkt_sizes=(test.packet_sizes))


	
	i.qt.run_test(test_id=0)
	qtl = i.qt.ixobj.getList(i.qt.ixobj.getRoot()+'/quickTest', 'rfc2544throughput')
	i.qt.ixobj.execute('waitForTest',qtl[0])
	if 'pass' not in i.qt.ixobj.getAttribute(qtl[0]+'/results','-result'):
		email_log('fail', test.name + 'Failed.\nFailed to start Ixia quick test' , USR_EMAIL)


	path = i.qt.ixobj.getAttribute(qtl[0]+'/results','-resultPath')
	if not os.path.exists('results/'+test.date):
		time.sleep(2)
		os.makedirs('results/'+test.date)
	print(i.qt.ixobj.execute('copyFile', i.qt.ixobj.readFrom(path + '/AggregateResults.csv','-ixNetRelative'),i.qt.ixobj.writeTo('results/' + test.date + '/' + filename + '.csv')))
	fd = open('results/'+test.date+'/'+filename+'.info', 'w')
	fd.write('\n')
	fd.write(test.name)
	fd.write(test.ep0_cmd)
	fd.write(test.ep1_cmd)
	fd.close()

	
	cfg['IxNetworkNewConfig'] = False
	with open('gen-'+cfg_name+'.json','w') as f:
		json.dump(cfg, f, indent=4, sort_keys=True)

	if 'yes' in add_emon:
		aggr = pd.read_csv('results/' + test.date + '/' + filename + '.csv')
		mbps = aggr['Agg Rx Throughput (Mbps)']
		rates  = aggr['Agg Rx Throughput (% Line Rate)']

		#if not i.trafficState.isStopped():
		#	i.stop()


		ev_fd = open('edp/' + test.platform + '.txt', 'r')
		cmd = EMON_DUT + ' ' + ''.join(ev_fd.readlines()).replace('\n',',')[0:-1]
		log.debug('EMON command:{}'.format(cmd))

		fdm = open('results/'+ test.date + '/emon-m.dat', 'w')
		fin, fout, ferr = dut[0].ssh.exec_command(EMON_DUT + ' -v')
		fdm.write(''.join(fout.readlines()))
		fdm.close()

		fdv = open('results/'+ test.date + '/emon-v.dat', 'w')
		fin, fout, ferr = dut[0].ssh.exec_command(EMON_DUT + ' -M')
		fdv.write(''.join(fout.readlines()))
		fdv.close()

		for size,rate,mbps in zip(test.packet_sizes,rates,mbps):
			log.info('Packet Size:{}, rate:{}'.format(size,rate))
			i.pktSize(size)
			i.rate(rate)
			i.start()
			time.sleep(5)
			now = dt.datetime.now().strftime("%yWW%W.%w_%HH-%MM-%SS")
			log.info('file prefix:{}-'.format(now))
			
			fin, fout, ferr = dut[0].ssh.exec_command(cmd)
			#fout = open('{}-{}Bytes-out.txt'.format(now,size),'w')
			#ferr = open('{}-{}Bytes-err.txt'.format(now,size),'w')

			#p = Popen(cmd.split(' '), stdout=fout, stderr=ferr)
			#p.wait() #Wait until it finish
			#         #other options are, time.sleep(N) and issue kill/stop signal
			fd = open('results/'+ test.date + '/emon_{}-{}B-{}mbps.dat'.format(test.name, size, mbps), 'w')
			log.info('collecting data for 1 minute')
			time.sleep(60)
			dut[0].ssh.exec_command(EMON_DUT + ' -stop')
			#print(ferr.readlines())
			#print(fd.write(''.join(ferr.readlines())))
			print(fd.write(''.join(fout.readlines())))
			time.sleep(1)
			fd.close()
			fout.close()
			ferr.close()
			i.stop()

		print('EMON results written to "results/'+ test.date + '"') 

def run_test( ep0, ep1, filename='auto_iter.txt'):
	fd = open(filename, 'r')
	
	test = Test("blank")
	cont = 0
	ui = input("Run with default packet sizes? [64, 72, 128, 256, 512, 768, 1024, 1280, 1420] [yes]/no ") or 'yes'
	if ui == 'yes':
		test.packet_sizes = [64, 72, 128, 256, 512, 768, 1024, 1280, 1420] 
	else:
		while cont is 0:
			size = int(input("Add packet size to run Quick Test with. Enter 0 to continue: ") or 0)
			if size == 0:
				cont = 1
			else: 
				test.packet_sizes.append(size)

			print("Your choices: {}".format(test.packet_sizes))

	add_emon = input("Add emon for each test case? yes/[no]") or 'no'
	now = dt.datetime.now().strftime("%yWW%W.%w_%HH")
	test.date = now
	
	for line in fd:
		if "DPDKipsec" in line:
			test.name = line.replace('\n','')
			test.workload=line.split('_')[0]
			test.platform=line.split('_')[1]
			test.ports=line.split('_')[2][:-1]
			test.cores=parse_cc(line.split('_')[3])[0]
			test.threads=parse_cc(line.split('_')[3])[1]
			test.algorithm=line.split('_')[4]
			test.cryptodev=line.split('_')[5]
			test.ep0_cmd=""
			test.ep1_cmd=""
		elif "ixia" in line:
			test.qt_cmd = line
		elif test.ep0_cmd == "":
			test.ep0_cmd = line
		elif test.ep1_cmd == "":
			test.ep1_cmd = line
			print('Running ' + test.name)
			#print(ep1.ip_addr)
			#print(test.ep1_cmd)	
			passed = 0;
			while not passed:
				passed = 1;
				ep0.ssh.exec_command('pkill -INT ipsec-secgw')
				ep1.ssh.exec_command('pkill -INT ipsec-secgw')
				i,o,e = ep1.ssh.exec_command(test.ep1_cmd, get_pty=True)
				#for line in o.read(int(test.ports*50)).splitlines():
				for line in o.read(4000).splitlines():
					print(line)
				time.sleep(5)
				x, y, z = ep0.ssh.exec_command(test.ep0_cmd,get_pty=True)
				#for line in y.read(int(test.ports*50)).splitlines():
				for line in y.read(4000).splitlines():
					print(line)
				info  = open("results/{}.info".format(ep0.name), "a")
				info.write('\n')
				time.sleep(5)
				a,b,c = ep1.ssh.exec_command('ps -aux | grep ipsec')
				if 'ipsec-secgw' not in b.readlines()[0]:
					passed = 0;
					#email_log('Failed', 'IPSec failed to start on DUT 1', USR_EMAIL)
				a,b,c = ep0.ssh.exec_command('ps -aux | grep ipsec')
				if 'ipsec-secgw' not in b.readlines()[0]:
					passed = 0;
					#email_log('Failed', 'IPSec failed to start on DUT 0', USR_EMAIL)
				time.sleep(5)

			run_qt(test.qt_cmd, test, add_emon)
			o.flush()
			y.flush()
			
		else:
			print('Warning: unexpected line in iteration file')
	email_log(" Completed", "Test series completed for DUT="+dut[0].ip_addr, USR_EMAIL)
	print("Tests completed. Results written to {}.".format('results/'+test.date))


def create_corelist(dut, cc):
	corelist=""  
	nc,nt=parse_cc(cc)	
	if nc == nt:
		for i in range(0,nc):
			corelist=corelist + str(i+1) + ','	
		corelist=corelist[0:len(corelist)-1]
	else:
		for i in range(0,nc):
			x,o,e = dut.ssh.exec_command('cat /sys/devices/system/cpu/cpu{}/topology/thread_siblings_list'.format(str(i+1)))
			core_pair=','.join(o.readlines())
			#core_pair=subprocess.check_output("ssh {} 'cat /sys/devices/system/cpu/cpu{}/topology/thread_siblings_list'".format(ip_addr, str(i+1) ,shell=True))
			corelist=corelist + str(core_pair.replace("\n",""))+','
		corelist=corelist[0:len(corelist)-1]
	return corelist.split(",")
	#corelist
		
def create_crypto(dut, nthreads, algo):
	ret = ""
	devs = []
	if dut.cryptodev == "sw":

		#if "yes" not in subprocess.check_output('ssh ' + dut.ip_addr + ' "if [ -e /home/dpdk/examples/ipsec-secgw/build/ipsec-secgw ]; then echo yes; fi"',shell=True):
		#	print "Warning: " + dut.ip_addr + " IPSec application not built"
		#nm_ipsec = subprocess.check_output('ssh ' + dut.ip_addr + '  nm /home/dpdk/examples/ipsec-secgw/build/ipsec-secgw', shell=True)
		#if "sha256_ni" not in nm_ipsec:
		#	print "Warning: DPDK is built without the AESNI_MB cryptodev. check your .config file. "
		#if "isal" not in subprocess.check_output('ssh ' + dut.ip_addr + ' ' + 'ldd /home/dpdk/examples/ipsec-secgw/build/ipsec-secgw', shell=True):
		#	print "Warning: DPDK is built without the AESNI_GCM cryptodev. Check your .config file. "
		ndev = int(math.ceil(nthreads)*2)
		for i in range(0,int(ndev)):
			ret = ret + " --vdev crypto_aesni_" + ('mb' if algo == 'cbc' else 'gcm') + str(i) + ' '
	else: #cryptodev is hw
		#if "yes" not in subprocess.check_output('ssh ' + dut.ip_addr + ' if [ -e /home/dpdk/x86_64-native-linuxapp-gcc/lib/librte_pmd_qat.a ]; then echo yes; fi', shell=True):
		#	print "Warning: " + dut.ip_addr + " DPDK not built with QAT cryptodev."
		ndev = int(math.ceil(nthreads)*2)
		bus = []
		i,o,e = dut.ssh.exec_command('lspci -d:{} | grep -o "^.." | uniq'.format(platform_cdev[dut.platform]))
		bus.extend(o.readlines())
		if not bus:
			print("Error: No QAT cryptodevs found on " + str(dut.name) + ". Check if device has a crypto accelerator or Try installing QuickAssist with SRIOV Host. ")
			#sys.exit(1) 
		print(bus)
		devs = []
		if dut.platform == 'SKX':
			for i in range(3):
				x,o,e = dut.ssh.exec_command("lspci -d:{} | grep '^{}' | tail -n {} | awk '{{ print $1 }}'".format(platform_cdev[dut.platform], str(bus[i].replace('\n','')), str(int(math.ceil(nthreads*2/3.0)))))
				devs.extend(o.readlines())
			for i in range(ndev):
				ret = ret + " -w " + str(devs[i]).replace('\n','')
		else:	
			x,o,e = dut.ssh.exec_command("lspci -d:{} | tail -n {} | awk '{{ print $1 }}'".format(platform_cdev[dut.platform], str(int(nthreads)*2)))
			devs.extend(o.readlines())
			for i in range(ndev):
				ret = ret + " -w " + str(devs[i]).replace('\n','')
		#print ret
	return ret


def create_config(dut, core_combination):
	ret = " --config='"
	cc=create_corelist(dut, core_combination)
	nthreads=parse_cc(core_combination)[1]
	for x in range(int(dut.ports/nthreads)):
	#Queues are not supported
		for t in range(nthreads):
			ret = ret + "("+str(t+nthreads*x)+",0,"+cc[t]+"),"
	ret = ret[0:len(ret)-1] + "'"
	return ret 

def email_log(subject, body, to=USR_EMAIL):
	log = logging.getLogger()
	log.setLevel(logging.INFO)
	log.addHandler(handlers.SMTPHandler(mailhost='smtp.intel.com', fromaddr = 'lab_pyprofile@intel.com', toaddrs=to, subject='PyWorkloads log '+ subject))
	log.info(body)
	


def run_prep():
	print("assume ep0 is the DUT and ep1 is the supplemental platform")
	for ep in dut:
		if dut[0].platform == 'SKX':
			dut[0].ports=int(input("Number of ports to be used 2/4/6/8/[12]:") or 12)
		elif dut[0].platform == 'ATOM_DENVERTON':
			dut[0].ports=int(input("Number of ports to be used 2/[4]:") or 4)
		elif dut[0].platform == 'BDX':
			dut[0].ports=int(input("Number of ports to be used 2/[4]/6/8:") or 4)
		elif dut[0].platform == 'bdw-de-ns':
			dut[0].ports=int(input("Number of ports to be used 2/[4]/6/8:") or 4)

		dut[1].ports = dut[0].ports 
		print("Following NIC types were found on the system: ")
		stdi, stdo, stde = ep.ssh.exec_command("lspci -nn | grep 'Ethernet' | grep -o '[[0-9a-f]*\:[0-9a-f]*]' | tr ']' ' ' | uniq | cut -d':' -f2")
		li = stdo.readlines()
		for i in range(len(li)):
			li[i] = li[i].replace('\n','')
		ep.nic_list = ui_loop(li, "Add NIC type to use " )
		ep.prep()
		ep.prepped = True

def run_add(iter_file):
	for ep in dut:
		if ep.prepped is False:
			print("Following NIC types were found on the system: ")
			stdi, stdo, stde = ep.ssh.exec_command("lspci -nn | grep 'Ethernet' | grep -o '[[0-9a-f]*\:[0-9a-f]*]' | tr ']' ' ' | uniq | cut -d':' -f2")
			li = stdo.readlines()
			for i in range(len(li)):
				li[i] = li[i].replace('\n','')
			ep.nic_list = ui_loop(li, "Add NIC type to use " )
	core_combinations=[]
	algo=input("Select cryptographic algorithm [cbc]/gcm:") or "cbc"
	dut[0].cryptodev=input("Select crypotdev hw/[sw]:") or "sw"
	dut[1].cryptodev=dut[0].cryptodev
	if dut[0].platform == 'SKX':
		dut[0].ports=int(input("Number of ports to be used 2/4/6/8/[12]:") or 12)
	elif dut[0].platform == 'ATOM_DENVERTON':
		dut[0].ports=int(input("Number of ports to be used 2/[4]:") or 4)
	elif dut[0].platform == 'BDX':
		dut[0].ports=int(input("Number of ports to be used 2/[4]/6/8:") or 4)
	elif dut[0].platform == 'bdw-de-ns':
		dut[0].ports=int(input("Number of ports to be used 2/[4]/6/8:") or 4)
	dut[1].ports = dut[0].ports
	gen_ipsec_cfg(dut[0].ports)
	ret = -1
	#select core combinations 
	while (ret != "0"):
		for i,j in zip(core_combinations_list.get(str(dut[0].ports)),range(1,len(core_combinations_list[str(dut[0].ports)])+1)):
			print("{}) {}".format(j,i))
		print("0) Done")
		valid = False
		while (not valid):
			print("Your choices:" + str(core_combinations))
			ret=input("Select the core combinations to run. Number of combination or 0 to continue:\n")
				
			if (ret == ''):
				print("Error incorrect input!")
			elif (int(ret)-1 <= len(core_combinations_list[str(dut[0].ports)])):
				valid = True
			else:
				print("Error: incorrect index!")
			
		if (ret !="0"):
			core_combinations.append(core_combinations_list[str(dut[0].ports)][int(ret)-1])
	#build command line 
	for ep in dut:
		n = 0
		for c in core_combinations:
			ep.cmdline[c] = RTE_SDK + "examples/ipsec-secgw/build/ipsec-secgw "
			#for i in create_corelist(ip_addr, c):
			#print ','.join(create_corelist(ip_addr,c))
			ll['l'] = ' -l ' + ','.join(create_corelist(ep,c))
			#ll['l'] = ll['l'][0:len(ll['l'])-1]
			ll['n'] = " -n " + str(platform_channels[ep.platform])
			ll['w_crypto'] = create_crypto(ep, parse_cc(c)[1], algo)
			ll['w_nic'] = ep.create_nic(dut[0].ports)
			ll['p'] = " -p " + hex(int(math.pow(2,dut[0].ports) - 1))
			ll['u'] = " -u " + hex(int(math.pow(2,dut[0].ports)-1) & ((int(math.pow(2,dut[0].ports)-1))) << int(dut[0].ports/2))
			ll['config'] = create_config(ep, c)
			ll['f'] = ' -f '+ RTE_SDK +'/examples/ipsec-secgw/auto-' + ep.name + '-bd-'+algo+'-''p.cfg'
			ll['f'] = ' -f ' + RTE_SDK + '/examples/ipsec-secgw/auto-{}-bd-{}-{}p.cfg'.format(ep.name, algo, dut[0].ports)
			ep.cmdline[c] = ep.cmdline[c] + ll['l'] + ll['n'] + ll['m'] + ll['w_crypto'] + ll['w_nic'] + ll['dash'] + ll['p'] + ll['u'] + ll['config'] + ll['f'] + ll['P']
			n = n+1
		
	#append test cases or create new iteration file
	fd = open(iter_file,"a")
	for c in core_combinations:
		#print dut[0].cmdline[c]
		name = '{}_{}_{}p_{}_{}_{}\n'.format(component + workload_name, dut[0].platform, dut[0].ports, c, algo, dut[0].cryptodev)
		if 'ixia' in name:
			print('Warning: String "ixia" not allowed in test name')
		fd.write(name)
		fd.write("ixia-ipsec-"+str(dut[0].ports)+"p.json\n")
		fd.write(dut[0].cmdline[c] + '\n')
		#print dut[1].cmdline[c]
		fd.write(dut[1].cmdline[c] + '\n')
	repeat=input("Do you want to add more tests? [no]/yes)") or 'no'
	if repeat == 'yes':
		core_combinations=[]
		run_add(iter_file)
	fd.close()

def run_remove():
	while True:
		old = open(iter_file, 'r')
		test_cases = []
		try: 
			for line,i in zip(old,range(1000)):
				test_cases.append(line)	
				#todo: add test prefix to all test names
				if 'DPDK' in line:
					print("{}) {}".format(int(i/4+1),line))
		
		except IndexError:
			print("a) All")
			print("0) Done")
				
		idx = input("Enter test case to remove. 0 to continue: " or 0)
		if idx == '0':
			return	
		if idx == 'a':
			new = open(iter_file,'w')
			new.write('')
			new.close()
			return
		old.close()
		del test_cases[(int(idx)-1)*4]
		del test_cases[(int(idx)-1)*4]
		del test_cases[(int(idx)-1)*4]
		del test_cases[(int(idx)-1)*4]
		new = open(iter_file, 'w')
		for line,i in zip(test_cases,range(len(test_cases))):
			new.write(line)
		new.close()

			
def run_print():
	fd = open(iter_file, 'r')
	#TODO: add TEST to prefix of test case names
	for line in fd:
		if 'DPDK' in line:
			print(line)

def run_emon():
	old = open(iter_file, 'r')
	test_cases = []
	try: 
		for line,i in zip(old,range(1000)):
			test_cases.append(line)	
			#todo: add test prefix to all test names
			if 'DPDK' in line:
				print("{}) {}".format(int(i/4+1),line))
	
	except IndexError:
		print("0) Done")
			
	idx = input("Enter test case to run emon over. 0 to continue: " or 0)
	if idx == '0':
		return	
	old.close()
	test = Test('blank')
	test.name = test_cases[(int(idx)-1)*4].replace('\n','')
	test.platform=dut[0].platform
	test.qt_cmd = test_cases[(int(idx)-1)*4+1]
	test.ports = int(test.qt_cmd.split('-')[2].split('p')[0])
	test.ep0_cmd = test_cases[(int(idx)-1)*4+2]
	test.ep1_cmd = test_cases[(int(idx)-1)*4+3]

	
	ui = input("Run with default packet sizes? [64, 72, 128, 256, 512, 768, 1024, 1280, 1420] [yes]/no ") or 'yes'
	cont = 0
	if ui == 'yes':
		test.packet_sizes = [64, 72, 128, 256, 512, 768, 1024, 1280, 1420] 
	else:
		while cont is 0:
			size = int(input("Add packet size to run Quick Test with. Enter 0 to continue: ") or 0)
			if size == 0:
				cont = 1
			else: 
				test.packet_sizes.append(size)

			print("Your choices: {}".format(test.packet_sizes))

	for size in test.packet_sizes:
		rate = input("Enter desired % rate for {}B test: ".format(size)) or 100.0
		test.rates.append(float(rate))
	now = dt.datetime.now().strftime("%yWW%W.%w_%HH")
	test.date = now
	passed = 0;
	while not passed:
		passed = 1;
		dut[0].ssh.exec_command('pkill -INT ipsec-secgw')
		dut[1].ssh.exec_command('pkill -INT ipsec-secgw')
		i,o,e = dut[1].ssh.exec_command(RTE_SDK + '/examples/ipsec-secgw/' + test.ep1_cmd, get_pty=True)
		#for line in o.read(int(test.ports*50)).splitlines():
		for line in o.read(2000).splitlines():
			print(line)
		time.sleep(5)
		x, y, z = dut[0].ssh.exec_command(RTE_SDK + '/examples/ipsec-secgw/' + test.ep0_cmd,get_pty=True)
		#for line in y.read(int(test.ports*50)).splitlines():
		for line in y.read(2000).splitlines():
			print(line)
		info  = open("results/{}.info".format(dut[0].name), "a")
		info.write('\n')
		time.sleep(5)
		a,b,c = dut[1].ssh.exec_command('ps -aux | grep ipsec')
		if 'ipsec-secgw' not in b.readlines()[0]:
			passed = 0;
			#email_log('Failed', 'IPSec failed to start on DUT 1', USR_EMAIL)
		a,b,c = dut[0].ssh.exec_command('ps -aux | grep ipsec')
		if 'ipsec-secgw' not in b.readlines()[0]:
			passed = 0;
			#email_log('Failed', 'IPSec failed to start on DUT 0', USR_EMAIL)
		time.sleep(5)
		
	ev_fd = open('edp/' + test.platform + '.txt', 'r')
	cmd = EMON_DUT + ' ' + ''.join(ev_fd.readlines()).replace('\n',',')[0:-1]

	log = logging.getLogger(__name__)
	cfg_path = test.qt_cmd.replace('\n','')
	filename = test.name.replace('\n','')
	cfg_name = cfg_path.split('/')[-1].split('.')[0].replace('\n','')
	cfg = json.load(open(cfg_path,'r'))
	# If user defines custom logging, use it instead
	if 'log' in cfg:
	    dictConfig(cfg['log'])

	i = Ixia(cfg)
	if not os.path.exists('results/'+test.date):
		time.sleep(2)
		os.makedirs('results/'+test.date)
	fdm = open('results/'+ test.date + '/emon-m.dat', 'w')
	fin, fout, ferr = dut[0].ssh.exec_command(EMON_DUT + ' -M')
	fdm.write(''.join(fout.readlines()))
	fdm.close()
	fdv = open('results/'+ test.date + '/emon-v.dat', 'w')
	fin, fout, ferr = dut[0].ssh.exec_command(EMON_DUT + ' -v')
	fdv.write(''.join(fout.readlines()))
	fdv.close()


	for size,rate in zip(test.packet_sizes,test.rates):
		i.pktSize(size)
		i.rate(rate)
		i.start()
		time.sleep(5)
		now = dt.datetime.now().strftime("%yWW%W.%w_%HH-%MM-%SS")
		
		fin, fout, ferr = dut[0].ssh.exec_command(cmd)
		#fout = open('{}-{}Bytes-out.txt'.format(now,size),'w')
		#ferr = open('{}-{}Bytes-err.txt'.format(now,size),'w')

		#p = Popen(cmd.split(' '), stdout=fout, stderr=ferr)
		#p.wait() #Wait until it finish
		#         #other options are, time.sleep(N) and issue kill/stop signal
		fd = open('results/'+ test.date + '/emon_{}-{}B-{}mbps.dat'.format(test.name, size, rate*test.ports*10000/100), 'w')
		time.sleep(60)
		dut[0].ssh.exec_command(EMON_DUT + ' -stop')
		#print(ferr.readlines())
		#print(fd.write(''.join(ferr.readlines())))
		print(fd.write(''.join(fout.readlines())))
		time.sleep(1)
		fd.close()
		fout.close()
		ferr.close()
		i.stop()
	


	print('EMON results written to "results/'+ test.date + '"') 
	o.flush()
	y.flush()

	
	#choose the test case
	#choose packet size
	#specify rate per packet size
def run_run_qt():
	run_test(dut[0], dut[1], iter_file)


def run_analyze():
	print("need implement")

main()
