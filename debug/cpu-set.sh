#!/bin/bash

# --------------------------------------------------------
# CPU Affinity Configuration Script for QEMU VMs
# Written by Brian Eiler
# Version 1.0 (2019-04-29)
#
# Note: This is written for 4 CPUs per VM.
# --------------------------------------------------------

if [ "$#" -ne 5 ]; then
    echo
    echo "CPU Affinity Configuration Script for QEMU VMs"
    echo "------------------------------------------------"
    echo
    echo "You must enter exactly 5 command line arguments"
    echo
    echo "Usage: 'cpu-set.sh <VM_NAME> <Core_0> <Core_1> <Core_2> <Core_3>'"
    echo
    echo "Where:"
    echo "  <VM_NAME> is the name of the virtual machine. The text following -name in the QEMU command."
    echo "  <Core_#> is the CPU core number (of the host) to be assigned to the VM CPU #."
    echo
    echo "Example: 'cpu-set.sh VPP-VM1 23 24 25 26'"
    echo
else

	vm_name=$1
	vm_cpu_core0=$2
	vm_cpu_core1=$3
	vm_cpu_core2=$4
	vm_cpu_core3=$5

	echo
	echo "Setting CPU affinity for ${vm_name}..."
	echo
	vm_pid=`ps awx | grep ${vm_name} | grep -v grep | awk "'{print \$1}'"`
	vm_cpu0_pid=`top -b -n 1 -H -p ${vm_pid} | grep "CPU 0" | awk '{print $1}'`
	vm_cpu1_pid=`top -b -n 1 -H -p ${vm_pid} | grep "CPU 1" | awk '{print $1}'`
	vm_cpu2_pid=`top -b -n 1 -H -p ${vm_pid} | grep "CPU 2" | awk '{print $1}'`
	vm_cpu3_pid=`top -b -n 1 -H -p ${vm_pid} | grep "CPU 3" | awk '{print $1}'`
	taskset -pc -a ${vm_cpu_core0} ${vm_pid} > /dev/null 2>&1
	taskset -pc ${vm_cpu_core0} ${vm_cpu0_pid} > /dev/null 2>&1
	taskset -pc ${vm_cpu_core1} ${vm_cpu1_pid} > /dev/null 2>&1
	taskset -pc ${vm_cpu_core2} ${vm_cpu2_pid} > /dev/null 2>&1
	taskset -pc ${vm_cpu_core3} ${vm_cpu3_pid} > /dev/null 2>&1
	echo "${vm_name} Parent Process" $(taskset -pc ${vm_pid} | awk '{$1=$2=""; print $0}')
	echo "------------------------------------------------"
	echo "${vm_name} KVM CPU Core 0" $(taskset -pc ${vm_cpu0_pid} | awk '{$1=$2=""; print $0}')
	echo "${vm_name} KVM CPU Core 1" $(taskset -pc ${vm_cpu1_pid} | awk '{$1=$2=""; print $0}')
	echo "${vm_name} KVM CPU Core 2" $(taskset -pc ${vm_cpu2_pid} | awk '{$1=$2=""; print $0}')
	echo "${vm_name} KVM CPU Core 3" $(taskset -pc ${vm_cpu3_pid} | awk '{$1=$2=""; print $0}')
	echo

fi