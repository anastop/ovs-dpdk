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

# The build script will append the unique machine CPU core assignments below this point.
# The sstbf.py script calculates the high/low cores and the appropriate CPU bitmasks of OVS.
#
