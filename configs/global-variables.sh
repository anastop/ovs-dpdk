#!/bin/bash
#
# This is a list of environment variables that should be included in scripts by using the bash "source" command.
# These are intended to be global variables across all the OVS-DPDK related scripts.
#



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
cpu_numa1_high=(x x x)
cpu_numa1_low=(y y y)
cpu_numa2_high=(x x x)
cpu_numa2_low=(y y y)

# These are the global variables that contain the core number you want used by that service
cpu_ovs_lcpu_mask="0x200000"
cpu_ovs_pmd_mask="0xCC00000000CC000000"   #4C8T -- uses CPUs 26,27,30,31,66,67,70,71
cpu_ovs_dpdk0=
cpu_ovs_dpdk1=
cpu_ovs_dpdk2=
cpu_ovs_dpdk3=
cpu_ovs_vhost0=
cpu_ovs_vhost1=
cpu_ovs_vhost2=
cpu_ovs_vhost3=

cpu_vm1_core0=
cpu_vm1_core1=
cpu_vm1_core2=
cpu_vm1_core3=
cpu_vm2_core0=
cpu_vm2_core1=
cpu_vm2_core2=
cpu_vm2_core3=

cpu_trex_port0=
cpu_trex_port1=
cpu_trex_port2=
cpu_trex_port3=
cpu_trex_port4=
cpu_trex_port5=
cpu_trex_port6=
cpu_trex_port7=
cpu_trex_master=
cpu_trex_latency=