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
numa1_cores_low = []
numa1_cores_high = []
numa2_cores_low = []
numa2_cores_high = []



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



def enable_sstbf():
	global cpucount

	print("CPU Count = " + str(cpucount))

	high_perf_core=0
	standard_core=0
	
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

		# Set the frequency to base
		min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
		minFile = open(min_file,'w')
		minFile.write(str(base*1000))
		minFile.close()
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'w')
		maxFile.write(str(base*1000))
		maxFile.close()
			
		# Read and display the Min/Max values to confirm the SSTBF setting worked
		max_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_max_freq"
		maxFile = open(max_file,'r')
		max = int(maxFile.readline().strip("\n"))
		maxFile.close()
		min_file = "/sys/devices/system/cpu/cpu" + str(core) + "/cpufreq/scaling_min_freq"
		minFile = open(min_file,'r')
		min = int(minFile.readline().strip("\n"))
		minFile.close()

		if base > P1:
			if base > high_perf_core: high_perf_core = base
			print("Core " + str(core).rjust(3) + ": *Base Frequency: " + str(base).rjust(4) + "MHz* |  Actual Speeds --> Minimum: " + str(min/1000).rjust(4) + "MHz / Maximum: " + str(max/1000).rjust(4) + "MHz  <-- High Performance Core")
		else:
			if base > standard_core: standard_core = base
			print("Core " + str(core).rjust(3) + ":  Base Frequency: " + str(base).rjust(4) + "MHz  |  Actual Speeds --> Minimum: " + str(min/1000).rjust(4) + "MHz / Maximum: " + str(max/1000).rjust(4) + "MHz")
	print("--------------------------------------------------------------------------------------------")
	print()
	print("The high performance cores have been increased to " + str(high_perf_core) + "MHz")
	print()
	print("All other cores have been reduced to " + str(standard_core) + "MHz")
	print()



def revert_to_P1():
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
		
		if base > P1:
			print("Core " + str(core).rjust(3) + ": *Base Frequency: " + str(base).rjust(4) + "MHz* |  Actual Speeds --> Minimum: " + str(min/1000).rjust(4) + "MHz / Maximum: " + str(max/1000).rjust(4) + "MHz  <-- High Performance Core")
		else:
			print("Core " + str(core).rjust(3) + ":  Base Frequency: " + str(base).rjust(4) + "MHz  |  Actual Speeds --> Minimum: " + str(min/1000).rjust(4) + "MHz / Maximum: " + str(max/1000).rjust(4) + "MHz")
	print("--------------------------------------------------------------------------------------------")
	print()
	print("All cores have been reset to the same default frequency of (" + str(P1) + "MHz)")
	print()
	print("All cores will now perform equally.")
	print()
	


def get_high_perf_cores():
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




def inspect_cpu_cores():
	global cpucount

	print("CPU Count = " + str(cpucount))

	P1 = get_cpu_base_frequency()
	print("P1 Frequency = " + str(P1) + "MHz")
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
		if base > P1:
		 	P1hi = P1hi + 1
			print("Core " + str(core).rjust(3) + ": *Base Frequency: " + str(base).rjust(4) + "MHz* |  Actual Speeds --> Minimum: " + str(min/1000).rjust(4) + "MHz / Maximum: " + str(max/1000).rjust(4) + "MHz  <-- High Performance Core")
		else:
			print("Core " + str(core).rjust(3) + ":  Base Frequency: " + str(base).rjust(4) + "MHz  |  Actual Speeds --> Minimum: " + str(min/1000).rjust(4) + "MHz / Maximum: " + str(max/1000).rjust(4) + "MHz")

	# Print the core listing
	lim_p1_cores_2 = len(P1cores)/2
	lim_p1_cores_4 = len(P1cores)/4
	step_p1_cores_to_ht = lim_p1_cores_4 * 2
	numa_1_p1_cores = ""
	numa_2_p1_cores = ""
	
	# iterate through NUMA node 1 to find the hyperthreaded pairs
	for i in range(0,lim_p1_cores_4):
		j = i + step_p1_cores_to_ht
		a = str(P1cores[i])
		b = str(P1cores[j])
		c = a + "/" + b
		numa_1_p1_cores = numa_1_p1_cores + c + " "
	
	# iterate through NUMA node 2 to find the hyperthreaded pairs
	for i in range(lim_p1_cores_4,lim_p1_cores_2):
		j = i + step_p1_cores_to_ht
		a = str(P1cores[i])
		b = str(P1cores[j])
		c = a + "/" + b
		numa_2_p1_cores = numa_2_p1_cores + c + " "

	print("--------------------------------------------------------------------------------------------")
	print("We have " + str(P1hi) + " high priority cores according to sysfs base_frequency.")
	print()
	print()
	print("The list of high priority cores are:")
	print(*P1cores, sep = ", ")
	print()
	print()
	print("These cores are grouped by NUMA node, and paired with their Hyperthreaded 'sister core' as follows:")
	print("---------------------------------------------------------------------------------------------------")
	print("NUMA 1: " + numa_1_p1_cores)
	print()
	print("NUMA 2: " + numa_2_p1_cores)
	print()



def inspect_brief():
	global cpucount

	print("CPU Count = " + str(cpucount))

	P1 = get_cpu_base_frequency()
	print("P1 Frequency = " + str(P1) + "MHz")
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
		if base > P1:
		 	P1hi = P1hi + 1

	# Print the core listing
	lim_p1_cores_2 = len(P1cores)/2
	lim_p1_cores_4 = len(P1cores)/4
	step_p1_cores_to_ht = lim_p1_cores_4 * 2
	numa_1_p1_cores = ""
	numa_2_p1_cores = ""
	
	# iterate through NUMA node 1 to find the hyperthreaded pairs
	for i in range(0,lim_p1_cores_4):
		j = i + step_p1_cores_to_ht
		a = str(P1cores[i])
		b = str(P1cores[j])
		c = a + "/" + b
		numa_1_p1_cores = numa_1_p1_cores + c + " "
	
	# iterate through NUMA node 2 to find the hyperthreaded pairs
	for i in range(lim_p1_cores_4,lim_p1_cores_2):
		j = i + step_p1_cores_to_ht
		a = str(P1cores[i])
		b = str(P1cores[j])
		c = a + "/" + b
		numa_2_p1_cores = numa_2_p1_cores + c + " "

	print("--------------------------------------------------------------------------------------------")
	print("We have " + str(P1hi) + " high priority cores according to sysfs base_frequency.")
	print()
	print()
	print("The list of high priority cores are:")
	print(*P1cores, sep = ", ")
	print()
	print()
	print("These cores are grouped by NUMA node, and paired with their Hyperthreaded 'sister core' as follows:")
	print("---------------------------------------------------------------------------------------------------")
	print("NUMA 1: " + numa_1_p1_cores)
	print()
	print("NUMA 2: " + numa_2_p1_cores)
	print()



def create_env_vars():
	global cpucount
	P1 = get_cpu_base_frequency()
	P1hi = 0
	high_perf_core = 0
	standard_core = 0
	core_base_freq = []
	
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
		if base > P1:
			P1hi = P1hi + 1
			if base > high_perf_core: high_perf_core = base
		else:
			if base > standard_core: standard_core = base
		
		#Create an array containing the base frequency of each core. The array index is the core ID
		core_base_freq.append(base)

	# Auto-assign cores for NUMA 1 to ENV variables
	lim_all_cores_1 = len(core_base_freq)
	lim_all_cores_2 = len(core_base_freq)/2
	lim_all_cores_4 = len(core_base_freq)/4
	step_all_cores_to_ht = lim_all_cores_4 * 2
	# Find the high and low cores in NUMA node 1 - Skip the first core
	for i in range(1, lim_all_cores_4):
		if core_base_freq[i] < high_perf_core:
			numa1_cores_low.append(i)
		else:
			numa1_cores_high.append(i)
	# Find the high and low cores in NUMA node 2 - Skip the first core
	for i in range((lim_all_cores_4 + 1), lim_all_cores_2):
		if core_base_freq[i] < high_perf_core:
			numa2_cores_low.append(i)
		else:
			# Add the core and its hyperthread peer
			numa2_cores_high.append(i)
			numa2_cores_high.append(i + lim_all_cores_2)
		
	# Build the core listing
	lim_p1_cores_2 = len(P1cores)/2
	lim_p1_cores_4 = len(P1cores)/4
	step_p1_cores_to_ht = lim_p1_cores_4 * 2
	numa_1_p1_cores_a = ""
	numa_1_p1_cores_b = ""
	numa_2_p1_cores_a = ""
	numa_2_p1_cores_b = ""
	
	# iterate through NUMA node 1 to find the hyperthreaded pairs
	for i in range(0,lim_p1_cores_4):
		j = i + step_p1_cores_to_ht
		a = str(P1cores[i])
		b = str(P1cores[j])
		numa_1_p1_cores_a = numa_1_p1_cores_a + a + " "
		numa_1_p1_cores_b = numa_1_p1_cores_b + b + " "

	# iterate through NUMA node 2 to find the hyperthreaded pairs
	for i in range(lim_p1_cores_4,lim_p1_cores_2):
		j = i + step_p1_cores_to_ht
		a = str(P1cores[i])
		b = str(P1cores[j])
		numa_2_p1_cores_a = numa_2_p1_cores_a + a + " "
		numa_2_p1_cores_b = numa_2_p1_cores_b + b + " "
	
	
	#Set the OVS PMD thread mask to include the CPU cores selected above.
	pmd_bin_mask=(1 << numa2_cores_high[0])+(1 << numa2_cores_high[1])+(1 << numa2_cores_high[2])+(1 << numa2_cores_high[3])+(1 << numa2_cores_high[4])+(1 << numa2_cores_high[5])+(1 << numa2_cores_high[6])+(1 << numa2_cores_high[7])
	pmd_hex_mask=format(pmd_bin_mask, 'x')
	
	#Set the OVS control plane to use the first core on NUMA node 2
	lcpu_bin_mask=(1 << lim_all_cores_4)
	lcpu_hex_mask=format(lcpu_bin_mask, 'x')
	
	# Create the output for the BASH shell environment variables
	print("#")
	print("#")
	print("#")
	print("# --------------------------------------------------------------------------------------------")
	print("# These variables were generated by the SSTBF Python script")
	print("#")
	print("# The index of the CPU_CORE_BASE_FREQ array is the CPU Core ID (zero-based)")
	print("# --------------------------------------------------------------------------------------------")
	print("CPU_CORE_BASE_FREQ=(" + ' '.join(map(str, core_base_freq)) + ")")
	print("CPU_FREQ_HIGH_CORE=" + str(high_perf_core))
	print("CPU_FREQ_LOW_CORE=" + str(standard_core))
	print("CPU_P1_FREQ=" + str(P1))
	print("CPU_HIGH_PERF_CORES=(" + ' '.join(map(str, P1cores)) + ")")
	print("CPU_NUMA1_HIGH_CORES=(" + numa_1_p1_cores_a + numa_1_p1_cores_b + ")")
	print("CPU_NUMA2_HIGH_CORES=(" + numa_2_p1_cores_a + numa_2_p1_cores_b + ")")
	print("CPU_COUNT=" + str(cpucount))
	print()
	print("CPU_NUMA1_CORE_RANGE_BEGIN=0")
	print("CPU_NUMA1_CORE_RANGE_END=" + str(lim_all_cores_4 - 1))
	print("CPU_NUMA1_HT_CORE_RANGE_BEGIN=" + str(lim_all_cores_2))
	print("CPU_NUMA1_HT_CORE_RANGE_END=" + str(lim_all_cores_4 + lim_all_cores_2 - 1))
	print()
	print("CPU_NUMA2_CORE_RANGE_BEGIN=" + str(lim_all_cores_4))
	print("CPU_NUMA2_CORE_RANGE_END=" + str(lim_all_cores_2 - 1))
	print("CPU_NUMA2_HT_CORE_RANGE_BEGIN=" + str(lim_all_cores_4 + lim_all_cores_2))
	print("CPU_NUMA2_HT_CORE_RANGE_END=" + str(lim_all_cores_1 - 1))
	print()
	# Isolate all cores except 0 and its HT peer  -- eg. core 40 in a 20-core system
	print("CPU_CORES_TO_ISOLATE=\"1-" + str(lim_all_cores_2 - 1) + "," + str(lim_all_cores_2 + 1) + "-" + str(lim_all_cores_1 - 1) + "\"")
	print()
	print("# These variables assign CPU cores to services")
	# Use a standard core in NUMBA node 1
	print("cpu_trex_port0=" + str(numa1_cores_low[0]))
	print("cpu_trex_port1=" + str(numa1_cores_low[1]))
	print("cpu_trex_port2=" + str(numa1_cores_low[2]))
	print("cpu_trex_port3=" + str(numa1_cores_low[3]))
	print("cpu_trex_port4=" + str(numa1_cores_low[4]))
	print("cpu_trex_port5=" + str(numa1_cores_low[5]))
	print("cpu_trex_port6=" + str(numa1_cores_low[6]))
	print("cpu_trex_port7=" + str(numa1_cores_low[7]))
	print("cpu_trex_master=" + str(numa1_cores_low[8]))
	print("cpu_trex_latency=" + str(numa1_cores_low[9]))
	
	# Use a standard core in NUMBA node 2
	print("cpu_vm1_core0=" + str(numa2_cores_low[0]))
	print("cpu_vm1_core1=" + str(numa2_cores_low[1]))
	print("cpu_vm1_core2=" + str(numa2_cores_low[2]))
	print("cpu_vm1_core3=" + str(numa2_cores_low[3]))
	print("cpu_vm2_core0=" + str(numa2_cores_low[4]))
	print("cpu_vm2_core1=" + str(numa2_cores_low[5]))
	print("cpu_vm2_core2=" + str(numa2_cores_low[6]))
	print("cpu_vm2_core3=" + str(numa2_cores_low[7]))

	# Use a high performance core in NUMA node 2 and within the OVS PMD CPU bit mask
	print("cpu_ovs_dpdk0=" + str(numa2_cores_high[0]))
	print("cpu_ovs_vhost0=" + str(numa2_cores_high[1]))
	print("cpu_ovs_dpdk1=" + str(numa2_cores_high[2]))
	print("cpu_ovs_vhost1=" + str(numa2_cores_high[3]))
	print("cpu_ovs_dpdk2=" + str(numa2_cores_high[4]))
	print("cpu_ovs_vhost2=" + str(numa2_cores_high[5]))
	print("cpu_ovs_dpdk3=" + str(numa2_cores_high[6]))
	print("cpu_ovs_vhost3=" + str(numa2_cores_high[7]))

	print("cpu_ovs_pmd_mask=\"0x" + str(pmd_hex_mask) + "\"")
	print("cpu_ovs_lcpu_mask=\"0x" + str(lcpu_hex_mask) + "\"")
	print()
	print()

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
	print("  LAB SCRIPT:  Cascade Lake SST-BF Test (2019-04-19 v.1.0)")
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
	print("   -a            Activate SST-BF   (Favor the high performance cores)")
	print("   -d            Deactivate SST-BF (Revert all cores to Base Frequency)")
	print("   -i            Inspect the CPU cores")
	print("   -b            Show a brief version of the CPU core inspection")
	print("   -c            Create BASH Environment variables")
	print("   -h            Help")
	print()






def do_menu():
	print("")
	print_banner()
	print("")
	print("[a] Activate SST-BF   (Favor the high performance cores)")
	print("[d] Deactivate SST-BF (Revert all cores to Base Frequency)")
	print("[i] Inspect the CPU cores")
	print("[b] Show a brief version of the CPU core inspection")
	print("[h] Help")
	print("")
	print("[q] Exit Script")
	print("----------------------------------------------------------")
	text = raw_input("Option: ")

	#("[1] Display Available Settings")
	if (text == "a"):
		enable_sstbf()
	elif (text == "d"):
		revert_to_P1()
	elif (text == "h"):
		show_help()
	elif (text == "i"):
		inspect_cpu_cores()
	elif (text == "b"):
		inspect_brief()
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
	opts, args = getopt.getopt(sys.argv[1:],"adhibc")
except getopt.GetoptError:
	print('"' + scriptname + ' -h" for help')
	sys.exit(-1)

cpucount = getcpucount()
cpurange = range_expand('0-' + str(cpucount-1))
get_high_perf_cores()

for opt, arg in opts:
        if opt in ("-a"):
		enable_sstbf()
		sys.exit(0)
        if opt in ("-d"):
		revert_to_P1()
		sys.exit(0)
        if opt in ("-h"):
		show_help()
		sys.exit(0)
        if opt in ("-i"):
		inspect_cpu_cores()
		sys.exit(0)
        if opt in ("-b"):
		inspect_brief()
		sys.exit(0)
        if opt in ("-c"):
		create_env_vars()
		sys.exit(0)
		
if (len(opts)==0):
	while(1):
		do_menu()
		print("")
		raw_input("Press enter to continue ... ")
		print("")

