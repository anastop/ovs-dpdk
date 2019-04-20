#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

cpu_speed_ovs_dpdk0=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_dpdk0}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_ovs_dpdk1=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_dpdk1}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_ovs_dpdk2=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_dpdk2}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_ovs_dpdk3=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_dpdk3}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_ovs_vhost0=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_vhost0}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_ovs_vhost1=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_vhost1}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_ovs_vhost2=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_vhost2}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_ovs_vhost3=$(( `cat /sys/devices/system/cpu/cpu${cpu_ovs_vhost3}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm1_core0=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm1_core0}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm1_core1=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm1_core1}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm1_core2=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm1_core2}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm1_core3=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm1_core3}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm2_core0=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm2_core0}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm2_core1=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm2_core1}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm2_core2=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm2_core2}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_vm2_core3=$(( `cat /sys/devices/system/cpu/cpu${cpu_vm2_core3}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port0=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port0}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port1=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port1}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port2=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port2}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port3=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port3}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port4=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port4}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port5=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port5}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port6=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port6}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_port7=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_port7}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_master=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_master}/cpufreq/scaling_cur_freq` / 1000 ))
cpu_speed_trex_latency=$(( `cat /sys/devices/system/cpu/cpu${cpu_trex_latency}/cpufreq/scaling_cur_freq` / 1000 ))

clear
echo
echo "Activating SSTBF..."
${git_base_path}/scripts/sstbf.py -a > /dev/null
sleep 2
echo
echo
echo "The OVS CPU Core Assignments"
echo "----------------------------"
echo "OVS LCPU Mask: ${cpu_ovs_lcpu_mask}"
echo "OVS PMD Mask:  ${cpu_ovs_pmd_mask}"
echo "OVS DPDK0:     ${cpu_ovs_dpdk0}    Current Frequency: ${cpu_speed_ovs_dpdk0}MHz"
echo "OVS DPDK1:     ${cpu_ovs_dpdk1}    Current Frequency: ${cpu_speed_ovs_dpdk1}MHz"
echo "OVS DPDK2:     ${cpu_ovs_dpdk2}    Current Frequency: ${cpu_speed_ovs_dpdk2}MHz"
echo "OVS DPDK3:     ${cpu_ovs_dpdk3}    Current Frequency: ${cpu_speed_ovs_dpdk3}MHz"
echo "OVS VHOST0:    ${cpu_ovs_vhost0}    Current Frequency: ${cpu_speed_ovs_vhost0}MHz"
echo "OVS VHOST1:    ${cpu_ovs_vhost1}    Current Frequency: ${cpu_speed_ovs_vhost1}MHz"
echo "OVS VHOST2:    ${cpu_ovs_vhost2}    Current Frequency: ${cpu_speed_ovs_vhost2}MHz"
echo "OVS VHOST3:    ${cpu_ovs_vhost3}    Current Frequency: ${cpu_speed_ovs_vhost3}MHz"
echo
echo
echo "The Virtual Machine Cores"
echo "-------------------------"
echo "VM1 core 0:    ${cpu_vm1_core0}    Current Frequency: ${cpu_speed_vm1_core0}MHz"
echo "VM1 core 1:    ${cpu_vm1_core1}    Current Frequency: ${cpu_speed_vm1_core1}MHz"
echo "VM1 core 2:    ${cpu_vm1_core2}    Current Frequency: ${cpu_speed_vm1_core2}MHz"
echo "VM1 core 3:    ${cpu_vm1_core3}    Current Frequency: ${cpu_speed_vm1_core3}MHz"
echo
echo "VM2 core 0:    ${cpu_vm2_core0}    Current Frequency: ${cpu_speed_vm2_core0}MHz"
echo "VM2 core 1:    ${cpu_vm2_core1}    Current Frequency: ${cpu_speed_vm2_core1}MHz"
echo "VM2 core 2:    ${cpu_vm2_core2}    Current Frequency: ${cpu_speed_vm2_core2}MHz"
echo "VM2 core 3:    ${cpu_vm2_core3}    Current Frequency: ${cpu_speed_vm2_core3}MHz"
echo
echo
echo "TRex CPU Core Assignments"
echo "-------------------------"
echo "Master Core:   ${cpu_trex_master}    Current Frequency: ${cpu_speed_trex_master}MHz"
echo "Latency Core:  ${cpu_trex_latency}    Current Frequency: ${cpu_speed_trex_latency}MHz"
echo "NIC Core 0:    ${cpu_trex_port0}    Current Frequency: ${cpu_speed_trex_port0}MHz"
echo "NIC Core 1:    ${cpu_trex_port1}    Current Frequency: ${cpu_speed_trex_port1}MHz"
echo "NIC Core 2:    ${cpu_trex_port2}    Current Frequency: ${cpu_speed_trex_port2}MHz"
echo "NIC Core 3:    ${cpu_trex_port3}    Current Frequency: ${cpu_speed_trex_port3}MHz"
echo "NIC Core 4:    ${cpu_trex_port4}    Current Frequency: ${cpu_speed_trex_port4}MHz"
echo "NIC Core 5:    ${cpu_trex_port5}    Current Frequency: ${cpu_speed_trex_port5}MHz"
echo "NIC Core 6:    ${cpu_trex_port6}    Current Frequency: ${cpu_speed_trex_port6}MHz"
echo "NIC Core 7:    ${cpu_trex_port7}    Current Frequency: ${cpu_speed_trex_port7}MHz"
echo
echo 
echo "The high performance CPU cores should have a base frequency of: ${CPU_FREQ_HIGH_CORE}MHz"
echo
echo "The standard CPU cores should have a base frequency of: ${CPU_FREQ_LOW_CORE}MHz"

































