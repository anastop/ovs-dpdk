#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh

echo
echo "Setting CPU affinity for VPP-VM1."
vm_1_pid=`ps awx | grep VPP-VM1 | grep -v grep | awk '{print $1}'`
vm_1_cpu0_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 0" | awk '{print $1}'`
vm_1_cpu1_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 1" | awk '{print $1}'`
vm_1_cpu2_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 2" | awk '{print $1}'`
vm_1_cpu3_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 3" | awk '{print $1}'`
taskset -pc -a ${cpu_vm1_core0} ${vm_1_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm1_core0} ${vm_1_cpu0_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm1_core1} ${vm_1_cpu1_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm1_core2} ${vm_1_cpu2_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm1_core3} ${vm_1_cpu3_pid} > /dev/null 2>&1
echo
echo "New CPU affinity for VPP-VM1:"
taskset -pc -a ${vm_1_pid}
echo
echo
echo "Setting CPU affinity for VPP-VM2."
vm_2_pid=`ps awx | grep VPP-VM2 | grep -v grep | awk '{print $1}'`
vm_2_cpu0_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 0" | awk '{print $1}'`
vm_2_cpu1_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 1" | awk '{print $1}'`
vm_2_cpu2_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 2" | awk '{print $1}'`
vm_2_cpu3_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 3" | awk '{print $1}'`
taskset -pc -a ${cpu_vm2_core0} ${vm_2_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm2_core0} ${vm_2_cpu0_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm2_core1} ${vm_2_cpu1_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm2_core2} ${vm_2_cpu2_pid} > /dev/null 2>&1
taskset -pc ${cpu_vm2_core3} ${vm_2_cpu3_pid} > /dev/null 2>&1
echo
echo "New CPU affinity for VPP-VM2:"
taskset -pc -a ${vm_2_pid}
echo
echo "Done settings VM CPU Affinity."
echo