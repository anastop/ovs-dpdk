#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

echo
echo "The OVS CPU Core Assignments"
echo "----------------------------"
echo "OVS LCPU Mask: ${cpu_ovs_lcpu_mask}"
echo "OVS PMD Mask:  ${cpu_ovs_pmd_mask}"
echo "OVS DPDK0:     ${cpu_ovs_dpdk0}"
echo "OVS DPDK1:     ${cpu_ovs_dpdk1}"
echo "OVS DPDK2:     ${cpu_ovs_dpdk2}"
echo "OVS DPDK3:     ${cpu_ovs_dpdk3}"
echo "OVS VHOST0:    ${cpu_ovs_vhost0}"
echo "OVS VHOST1:    ${cpu_ovs_vhost1}"
echo "OVS VHOST2:    ${cpu_ovs_vhost2}"
echo "OVS VHOST3:    ${cpu_ovs_vhost3}"
echo
echo
echo "The Virtual Machine Cores"
echo "-------------------------"
echo "VM1 core 0:    ${cpu_vm1_core0}"
echo "VM1 core 1:    ${cpu_vm1_core1}"
echo "VM1 core 2:    ${cpu_vm1_core2}"
echo "VM1 core 3:    ${cpu_vm1_core3}"
echo
echo "VM2 core 0:    ${cpu_vm2_core0}"
echo "VM2 core 1:    ${cpu_vm2_core1}"
echo "VM2 core 2:    ${cpu_vm2_core2}"
echo "VM2 core 3:    ${cpu_vm2_core3}"
echo
echo
echo "TRex CPU Core Assignments"
echo "-------------------------"
echo "Master Core:   ${cpu_trex_master}"
echo "Latency Core:  ${cpu_trex_latency}"
echo "NIC Core 0:    ${cpu_trex_port0}"
echo "NIC Core 1:    ${cpu_trex_port1}"
echo "NIC Core 2:    ${cpu_trex_port2}"
echo "NIC Core 3:    ${cpu_trex_port3}"
echo "NIC Core 4:    ${cpu_trex_port4}"
echo "NIC Core 5:    ${cpu_trex_port5}"
echo "NIC Core 6:    ${cpu_trex_port6}"
echo "NIC Core 7:    ${cpu_trex_port7}"
echo
