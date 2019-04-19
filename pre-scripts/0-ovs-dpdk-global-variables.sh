#!/bin/bash
#
# This is a list of environment variables that should be included in scripts by using the bash "source" command.
# These are intended to be global variables across all the OVS-DPDK related scripts.
#
# This file should be copied to "/etc/0-ovs-dpdk-global-variables.sh"
#

# This is the master path for the project
git_base_path=/opt/ovs-dpdk-lab

# General path variables
tmp_dir=/tmp
trex_dir=${git_base_path}/trex
DPDK_DIR=${git_base_path}/dpdk
DPDK_BUILD=${git_base_path}/dpdk/x86_64-native-linuxapp-gcc
OVS_DIR=${git_base_path}/ovs
DB_SOCK=/usr/local/var/run/openvswitch/db.sock


# PCI Card Addresses
PCI_ADDR_NIC0="18:00.0"     # Used by TRex - Port 0
PCI_ADDR_NIC1="18:00.1"     # Used by TRex - Port 1
PCI_ADDR_NIC2="1a:00.0"     # Used by TRex - Port 2
PCI_ADDR_NIC3="1a:00.1"     # Used by TRex - Port 3
PCI_ADDR_NIC4="af:00.0"     # Used by OVS - dpdk0
PCI_ADDR_NIC5="af:00.1"     # Used by OVS - dpdk1
PCI_ADDR_NIC6="b1:00.0"     # Used by OVS - dpdk2
PCI_ADDR_NIC7="b1:00.1"     # Used by OVS - dpdk3


# High Power CPU Mapping - 0=Low 1=High
# -------------------------------------
# Note this reads RIGHT to LEFT
# This is for creating the CPU masks for OVS
# Copy the bits into a binary to hex converter
#
# 0000-0000-0000-0000-0000 0000-0000-0000-0000-0000 0000-0000-0000-0000-0000 0000-0000-0000-0000-0000 
#  (cores 79-60 - NUMA 2)   (cores 59-40 - NUMA 1)   (cores 39-20 - NUMA 2)   (cores 19-00 - NUMA 1)
#
# Example: 0xCC00000000CC000000  == Cores 26,27,30,31,66,67,70,71 (includes the Hyperthreads)
# These are the global variables that contain the core number you want used by that service


cpu_ovs_lcpu_mask="0x200000"              # CPU Core 21 - a binary CPU bit mask (choose only one CPU core)

cpu_ovs_pmd_mask="0xCC00000000CC000000"   # Create a bitmask of the CPU cores used for the dpdk and vhost threads below

cpu_ovs_dpdk0=26       # Use a high performance core within the OVS PMD CPU bit mask
cpu_ovs_dpdk1=27       # Use a high performance core within the OVS PMD CPU bit mask
cpu_ovs_dpdk2=30       # Use a high performance core within the OVS PMD CPU bit mask
cpu_ovs_dpdk3=31       # Use a high performance core within the OVS PMD CPU bit mask
cpu_ovs_vhost0=66      # Use the hyperthread of cpu_ovs_dpdk0
cpu_ovs_vhost1=67      # Use the hyperthread of cpu_ovs_dpdk1
cpu_ovs_vhost2=70      # Use the hyperthread of cpu_ovs_dpdk2
cpu_ovs_vhost3=71      # Use the hyperthread of cpu_ovs_dpdk3

cpu_vm1_core0=22       # Use a standard core
cpu_vm1_core1=23       # Use a standard core
cpu_vm1_core2=24       # Use a standard core
cpu_vm1_core3=25       # Use a standard core
cpu_vm2_core0=35       # Use a standard core
cpu_vm2_core1=36       # Use a standard core
cpu_vm2_core2=37       # Use a standard core
cpu_vm2_core3=38       # Use a standard core

cpu_trex_port0=2       # Use a standard core
cpu_trex_port1=3       # Use a standard core
cpu_trex_port2=4       # Use a standard core
cpu_trex_port3=5       # Use a standard core
cpu_trex_port4=12      # Use a standard core
cpu_trex_port5=13      # Use a standard core
cpu_trex_port6=14      # Use a standard core
cpu_trex_port7=15      # Use a standard core
cpu_trex_master=10     # Use a standard core
cpu_trex_latency=11    # Use a standard core

