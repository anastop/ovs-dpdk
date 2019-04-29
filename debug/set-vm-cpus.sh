#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh

echo
echo "Setting CPU affinity for VPP-VM1."
vm_1_pid=`ps awx | grep VPP-VM1 | grep -v grep | awk '{print $1}'`
taskset -pc -a ${cpu_vm1_core0},${cpu_vm1_core1} ${vm_1_pid}
qemu-affinity -k 2:${cpu_vm1_core2} 3:${cpu_vm1_core3} -- ${vm_1_pid}
taskset -pc -a ${vm_1_pid}
echo
echo "Setting CPU affinity for VPP-VM2."
vm-2-pid=`ps awx | grep VPP-VM2 | grep -v grep | awk '{print $1}'`
taskset -pc -a ${cpu_vm2_core0},${cpu_vm2_core1} ${vm_2_pid}
qemu-affinity -k 2:${cpu_vm2_core2} 3:${cpu_vm2_core3} -- ${vm_2_pid}
taskset -pc -a ${vm_2_pid}
echo
