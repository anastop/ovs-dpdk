#!/bin/bash
#
# This is a list of environment variables that should be included in scripts by using the bash "source" command.
# These are intended to be global variables across all the OVS-DPDK related scripts.
#
# This file should be copied to "/etc/0-ovs-dpdk-global-variables.sh"
#

# This is the master path for the project
export git_base_path=/opt/ovs-dpdk-lab

# General path variables
export tmp_dir=/tmp
export trex_dir=${git_base_path}/trex
export DPDK_DIR=${git_base_path}/dpdk
export DPDK_BUILD=${git_base_path}/dpdk/x86_64-native-linuxapp-gcc
export OVS_DIR=${git_base_path}/ovs
export DB_SOCK=/usr/local/var/run/openvswitch/db.sock


# PCI Card Addresses
export PCI_ADDR_NIC0="18:00.0"     # Used by TRex - Port 0
export PCI_ADDR_NIC1="18:00.1"     # Used by TRex - Port 1
export PCI_ADDR_NIC2="1a:00.0"     # Used by TRex - Port 2
export PCI_ADDR_NIC3="1a:00.1"     # Used by TRex - Port 3
export PCI_ADDR_NIC4="af:00.0"     # Used by OVS - dpdk0
export PCI_ADDR_NIC5="af:00.1"     # Used by OVS - dpdk1
export PCI_ADDR_NIC6="b1:00.0"     # Used by OVS - dpdk2
export PCI_ADDR_NIC7="b1:00.1"     # Used by OVS - dpdk3


# High Power CPU Mapping - 0=Low 1=High
# -------------------------------------
# Note this reads RIGHT to LEFT
# This is for creating the CPU masks for OVS
# Copy the bits into a binary to hex converter
#
# 0000-0000-0000-0000-0000 0000-0000-0000-0000-0000 0000-0000-0000-0000-0000 0000-0000-0000-0000-0000 
#  (cores 79-60 - NUMA 2)   (cores 59-40 - NUMA 1)   (cores 39-20 - NUMA 2)   (cores 19-00 - NUMA 1)
#

# These are arrays mainly for human eyes, but can also be used as a variable array.
# This list doesn't include the hyper-threads. Easy to calculate them. 
# Divide the total cores in half (eg. 80/2=40), then add that to the core to find its hyperthread. eg. 16+40=56, the pair is 16 and 56.
# They are also not in these arrays because we typically don't use the hyperthread sisters.
export cpu_numa1_high=(1 6 7 8 9 16)
export cpu_numa2_high=(26 27 30 31 33 34)

# These are the global variables that contain the core number you want used by that service
export cpu_ovs_lcpu_mask="0x200000"              # CPU 21 - a binary CPU bit mask (choose only one CPU core)
export cpu_ovs_pmd_mask="0xCC00000000CC000000"   # CPUs 26,27,30,31,66,67,70,71 (include the Hyperthreads)
export cpu_ovs_dpdk0=26       # Use a high performance core within the OVS PMD CPU bit mask
export cpu_ovs_dpdk1=27       # Use a high performance core within the OVS PMD CPU bit mask
export cpu_ovs_dpdk2=30       # Use a high performance core within the OVS PMD CPU bit mask
export cpu_ovs_dpdk3=31       # Use a high performance core within the OVS PMD CPU bit mask
export cpu_ovs_vhost0=66      # Use the hyperthread of cpu_ovs_dpdk0
export cpu_ovs_vhost1=67      # Use the hyperthread of cpu_ovs_dpdk1
export cpu_ovs_vhost2=70      # Use the hyperthread of cpu_ovs_dpdk2
export cpu_ovs_vhost3=71      # Use the hyperthread of cpu_ovs_dpdk3

export cpu_vm1_core0=22       # Use a standard core
export cpu_vm1_core1=23       # Use a standard core
export cpu_vm1_core2=24       # Use a standard core
export cpu_vm1_core3=25       # Use a standard core
export cpu_vm2_core0=35       # Use a standard core
export cpu_vm2_core1=36       # Use a standard core
export cpu_vm2_core2=37       # Use a standard core
export cpu_vm2_core3=38       # Use a standard core

export cpu_trex_port0=2       # Use a standard core
export cpu_trex_port1=3       # Use a standard core
export cpu_trex_port2=4       # Use a standard core
export cpu_trex_port3=5       # Use a standard core
export cpu_trex_port4=12      # Use a standard core
export cpu_trex_port5=13      # Use a standard core
export cpu_trex_port6=14      # Use a standard core
export cpu_trex_port7=15      # Use a standard core
export cpu_trex_master=10     # Use a standard core
export cpu_trex_latency=11    # Use a standard core