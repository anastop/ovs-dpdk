#!/usr/bin/python
#

from __future__ import print_function
import os
import sys, getopt
import re
import struct
import multiprocessing

DRV_FILE = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_driver"
BASE_FILE = "/sys/devices/system/cpu/cpu%d/cpufreq/base_frequency"
CPU_MAX_FILE = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"
CPU_MIN_FILE = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq"
MAX_FILE = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"
MIN_FILE = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq"

driver = ""
cpucount=0
P1cores = []

# Read a 64-byte value from an MSR through the sysfs interface.
# Returns an 8-byte binary packed string.
def rdmsr(core, msr):
	msr_filename = "/dev/cpu/" + str(core) + "/msr"
	msr_file = os.open(msr_filename, os.O_RDONLY)
	os.lseek(msr_file, msr, os.SEEK_SET)
	regstr = os.read(msr_file, 8)
	return regstr

# Writes a 64-byte value to an MSR through the sysfs interface.
# Expects an 8-byte binary packed string in regstr.
def wrmsr(core, msr, regstr):
        msr_filename = "/dev/cpu/" + str(core) + "/msr"
        msr_file = os.open(msr_filename, os.O_WRONLY)
        os.lseek(msr_file, msr, os.SEEK_SET)
        os.write(msr_file, regstr)


# Read the HWP_REQUEST MSR
def get_hwp_request(core):
        # rdmsr returns 8 bytes of packed binary data
        regstr = rdmsr(core,0x774)
        # Unpack the 8 bytes into array of unsigned chars
        bytes = struct.unpack('BBBBBBBB', regstr)
        minimum = bytes[0]
        maximum = bytes[1]
        desired = bytes[2]
        epp = bytes[3]
        return ( minimum, maximum, desired, epp )


# Read the HWP_ENABLED MSR
def get_hwp_enabled():
        # rdmsr returns 8 bytes of packed binary data
        regstr = rdmsr(0,0x770)
        # Unpack the 8 bytes into array of unsigned chars
        bytes = struct.unpack('BBBBBBBB', regstr)
	enabled = bytes[0]
        return enabled



# Read the HWP_CAPABILITIES MSR
def get_hwp_capabilities(core):
        # rdmsr returns 8 bytes of packed binary data
        regstr = rdmsr(core,0x771)
        # Unpack the 8 bytes into array of unsigned chars
        bytes = struct.unpack('BBBBBBBB', regstr)
	highest = bytes[0]
        guaranteed = bytes[1]
	lowest = bytes[2]
        return ( highest, guaranteed, lowest )


# Get the CPU base frequencey from the PLATFORM_INFO MSR
def get_cpu_base_frequency():
	regstr = rdmsr(0,0xCE) # MSR_PLATFORM_INFO
	# Unpack the 8 bytes into array of unsigned chars
	bytes = struct.unpack('BBBBBBBB', regstr)
	# Byte 1 contains the max non-turbo frequecy
	P1 = bytes[1]*100
	return P1


def check_driver():
	global driver
	global freq_P1

	try:
		drvFile = open(DRV_FILE,'r')
	except:
		print()
		print("ERROR: No pstate driver file found.")
		print("       Are P-States enabled in the system BIOS?")
		print()
		return 0

	driver = drvFile.readline().strip("\n")
	drvFile.close()
	# TODO does the driver name make any difference?
	if driver == "acpi-cpufreq":
		return 1
	elif driver == "intel_pstate":
		return 1
	else:
		return 1



def getcpucount():
	cpus = os.listdir("/sys/devices/system/cpu")
	regex = re.compile(r'cpu[0-9]')
	cpus = list(filter(regex.search, cpus))
	cpucount = len(cpus)
	return cpucount


def enable_pbf(mode):
	global cpucount

	print("CPU Count = " + str(cpucount))

	P1 = get_cpu_base_frequency()

	for core in range(0,cpucount):
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/cpuinfo_max_freq"
		maxFile = open(max_file,'r')
		max = int(maxFile.readline().strip("\n"))
		maxFile.close()
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'w')
		maxFile.write(str(max))
		maxFile.close()
		( highest, guaranteed, lowest ) = get_hwp_capabilities(core)
		base = 0
		try:
			base_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/base_frequency"
			baseFile = open(base_file,'r')
			base = int(baseFile.readline().strip("\n"))/1000
			baseFile.close()
		except:
			print("WARNING: base_frequency sysfs entry not found, using default values")
			( minimum, maximum, desired, epp ) = get_hwp_request(core)
			if minimum > 0:
				# Available via 0x774 msr min.
				base = minimum * 100
			else:
				base = 2100

		if mode == 2:
			if cpucount == 16 or cpucount == 32 or cpucount == 64:
				if pbf_cores_16[core] == 1:
					base = 2700
				else:
					base = 2100
			if cpucount == 20 or cpucount == 40 or cpucount == 80:
				if pbf_cores_20[core] == 1:
					base = 2700
				else:
					base = 2100
			if cpucount == 24 or cpucount == 48 or cpucount == 96:
				if pbf_cores_24[core] == 1:
					base = 2800
				else:
					base = 2100

		if mode == 0:
			print("Core " + str(core) + ": P1 " + str(P1) + " : min/max " + str(base))
			min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
			minFile = open(min_file,'w')
			minFile.write(str(base*1000))
			minFile.close()
			max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
			maxFile = open(max_file,'w')
			maxFile.write(str(base*1000))
			maxFile.close()
		if mode == 1 and base > P1:
			print("Core " + str(core) + ": P1 " + str(P1) + " : min/max " + str(base))
			min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
			minFile = open(min_file,'w')
			minFile.write(str(base*1000))
			minFile.close()


def reverse_pbf():
	global cpucount

	print("CPU Count = " + str(cpucount))

	P1 = get_cpu_base_frequency()

	for core in range(0,cpucount):
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/cpuinfo_max_freq"
		maxFile = open(max_file,'r')
		max = int(maxFile.readline().strip("\n"))
		maxFile.close()
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'w')
		maxFile.write(str(max))
		maxFile.close()

		min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/cpuinfo_min_freq"
		minFile = open(min_file,'r')
		min = int(minFile.readline().strip("\n"))
		minFile.close()
		min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
		minFile = open(min_file,'w')
		minFile.write(str(min))
		minFile.close()
		print("Core " + str(core) + ": base " + str(P1) + " : min " + str(min/1000) + " : max " + str(max/1000))

def reverse_pbf_to_P1():
	global cpucount

	print("CPU Count = " + str(cpucount))

	P1 = get_cpu_base_frequency()

	for core in range(0,cpucount):
		# Temporarily set the core to max, so that we avoid an error if the minimum is currently above P1
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/cpuinfo_max_freq"
		maxFile = open(max_file,'r')
		max = int(maxFile.readline().strip("\n"))
		maxFile.close()
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'w')
		maxFile.write(str(max))
		maxFile.close()

		# Set the Minimim and Maximum frequencies to P1 (base)
		min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
		minFile = open(min_file,'w')
		minFile.write(str(P1*1000))
		minFile.close()
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'w')
		maxFile.write(str(P1*1000))
		maxFile.close()
		
		# Read and display the Min/Max values to confirm the P1 setting worked
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'r')
		max = int(maxFile.readline().strip("\n"))
		maxFile.close()
		min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
		minFile = open(min_file,'r')
		min = int(minFile.readline().strip("\n"))
		minFile.close()
		
		print("Core " + str(core) + ": base " + str(P1) + " : min " + str(min/1000) + " : max " + str(min/1000))


def get_highcores():
	global cpucount
	global P1cores

	P1 = get_cpu_base_frequency()
	
	for core in range(0,cpucount):
		base = 0
		base_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/base_frequency"
		try:
			baseFile = open(base_file,'r')
			base = int(baseFile.readline().strip("\n"))/1000
			baseFile.close()
		except:
			( minimum, maximum, desired, epp ) = get_hwp_request(core)
			if minimum > 0:
				base = minimum * 100
		( highest, guaranteed, lowest ) = get_hwp_capabilities(core)
		if base > P1:
		 	P1cores.append(core)

def query_pbf():
	global cpucount

	print("CPU Count = " + str(cpucount))

	P1 = get_cpu_base_frequency()
	print("Base = " + str(P1))
	P1hi = 0

	for core in range(0,cpucount):
		base = 0
		base_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/base_frequency"
		try:
			baseFile = open(base_file,'r')
			base = int(baseFile.readline().strip("\n"))/1000
			baseFile.close()
		except:
			( minimum, maximum, desired, epp ) = get_hwp_request(core)
			if minimum > 0:
				base = minimum * 100
		( highest, guaranteed, lowest ) = get_hwp_capabilities(core)
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'r')
		max = int(maxFile.readline().strip("\n"))
		maxFile.close()
		min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
		minFile = open(min_file,'r')
		min = int(minFile.readline().strip("\n"))
		minFile.close()
		print("Core " + str(core).rjust(3) + ": base_frequency " + str(base).rjust(4) + " : min " + str(min/1000).rjust(4) + " : max " + str(max/1000).rjust(4))
		if base > P1:
		 	P1hi = P1hi + 1
	
	print("We have " + str(P1hi) + " high priority cores according to sysfs base_frequency.")
	print(*P1cores, sep = ", ")
	print()
	inc = len(P1cores)/4
	r1 = 0
	r2 = r1 + inc
	r3 = r2 + inc
	r4 = r3 + inc
	print("NUMA 1: " + P1cores[r1] + "/" + P1cores[r3] + ", " + P1cores[(r1+1)] + "/" + P1cores[(r3+1)] + ", " + P1cores[(r1+2)] + "/" + P1cores[(r3+2)] + ", " + P1cores[(r1+3)] + "/" + P1cores[(r3+3)] )
	print()
	print("NUMA 2: " + P1cores[r2] + "/" + P1cores[r4] + ", " + P1cores[(r2+1)] + "/" + P1cores[(r4+1)] + ", " + P1cores[(r2+2)] + "/" + P1cores[(r4+2)] + ", " + P1cores[(r2+3)] + "/" + P1cores[(r4+3)] )

def range_expand(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            r+= range(l,h+1)
    return r

def print_banner():
	print("----------------------------------------------------------")
	print("  LAB SCRIPT:  Cascade Lake SST-BF Test (2019-04-18 v.1.0)")
	print("")  
	print("  This script should only be used for testing purposes!")
	print("----------------------------------------------------------")

def show_help():
	print("")
	print_banner()
	print("")
	print(scriptname + ' <option>')
	print("")
	print('   <no params>   use interactive menu')
	print("   -a            Activate SST-BF")
	print("   -d            Deactivate SST-BF (Revert to default frequency configuration)")
	print("   -i            Display CPU core information")
	print("   -h            Help")
	print()


def do_menu():
	print("")
	print_banner()
	print("")
	print("[a] Activate SST-BF")
	print("[d] Deactivate SST-BF (Revert to default frequency configuration)")
	print("[i] Display CPU core information")
	print("[h] Help")
	print("")
	print("[q] Exit Script")
	print("----------------------------------------------------------")
	text = raw_input("Option: ")

	#("[1] Display Available Settings")
	if (text == "a"):
		enable_pbf(0)
	elif (text == "d"):
		reverse_pbf_to_P1()
	elif (text == "h"):
		show_help()
	elif (text == "i"):
		query_pbf()
	elif (text == "q"):
		sys.exit(0)
	else:
		print("")
		print("Unknown Option")

#
# Do some prerequesite checks.
#
ret = os.system("lsmod | grep msr >/dev/null")
if (ret != 0):
	print("ERROR: Need the 'msr' kernel module when " +
		"using the '" + driver + "' driver")
	print("Please run 'modprobe msr'")
	sys.exit(1)

if (get_hwp_enabled() == 0):
	print("ERROR: HWP not enabled in BIOS. Exiting.")
	sys.exit(1)

if (check_driver() == 0):
	print("Invalid Driver : [" + driver + "]")
	sys.exit(1)

scriptname = sys.argv[0]

try:
	opts, args = getopt.getopt(sys.argv[1:],"smerthi")
except getopt.GetoptError:
	print('"' + scriptname + ' -h" for help')
	sys.exit(-1)

cpucount = getcpucount()
cpurange = range_expand('0-' + str(cpucount-1))
get_highcores()

for opt, arg in opts:
        if opt in ("-a"):
		enable_pbf(0)
		sys.exit(0)
        if opt in ("-d"):
		reverse_pbf_to_P1()
		sys.exit(0)
        if opt in ("-h"):
		show_help()
		sys.exit(0)
        if opt in ("-i"):
		query_pbf()
		sys.exit(0)

if (len(opts)==0):
	while(1):
		do_menu()
		print("")
		raw_input("Press enter to continue ... ")
		print("")

