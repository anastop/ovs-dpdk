#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh

echo
echo "Setting CPU affinity for VPP-VM1."
# vm_1_pid=`ps awx | grep VPP-VM1 | grep -v grep | awk '{print $1}'`
# taskset -pc -a ${cpu_vm1_core0},${cpu_vm1_core1} ${vm_1_pid}
# qemu-affinity -k 2:${cpu_vm1_core2} 3:${cpu_vm1_core3} -- ${vm_1_pid}
# taskset -pc -a ${vm_1_pid}
vm_1_pid=`ps awx | grep VPP-VM1 | grep -v grep | awk '{print $1}'`
vm_1_cpu0_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 0" | awk '{print $1}'`
vm_1_cpu1_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 1" | awk '{print $1}'`
vm_1_cpu2_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 2" | awk '{print $1}'`
vm_1_cpu3_pid=`top -b -n 1 -H -p ${vm_1_pid} | grep "CPU 3" | awk '{print $1}'`
echo vm_1_cpu0_pid is ${vm_1_cpu0_pid} > /root/tmp1.txt
echo vm_1_cpu0_pid is ${vm_1_cpu0_pid}
echo vm_1_cpu1_pid is ${vm_1_cpu1_pid}
echo vm_1_cpu2_pid is ${vm_1_cpu2_pid}
echo vm_1_cpu3_pid is ${vm_1_cpu3_pid}
taskset -pc -a ${cpu_vm1_core0} ${vm_1_pid}
taskset -pc ${cpu_vm1_core0} ${vm_1_cpu0_pid}
taskset -pc ${cpu_vm1_core1} ${vm_1_cpu1_pid}
taskset -pc ${cpu_vm1_core2} ${vm_1_cpu2_pid}
taskset -pc ${cpu_vm1_core3} ${vm_1_cpu3_pid}

echo
echo "Setting CPU affinity for VPP-VM2."
# vm_2_pid=`ps awx | grep VPP-VM2 | grep -v grep | awk '{print $1}'`
# taskset -pc -a ${cpu_vm2_core0},${cpu_vm2_core1} ${vm_2_pid}
# qemu-affinity -k 2:${cpu_vm2_core2} 3:${cpu_vm2_core3} -- ${vm_2_pid}
# taskset -pc -a ${vm_2_pid}
vm_2_pid=`ps awx | grep VPP-VM2 | grep -v grep | awk '{print $1}'`
vm_2_cpu0_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 0" | awk '{print $1}'`
vm_2_cpu1_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 1" | awk '{print $1}'`
vm_2_cpu2_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 2" | awk '{print $1}'`
vm_2_cpu3_pid=`top -b -n 1 -H -p ${vm_2_pid} | grep "CPU 3" | awk '{print $1}'`
echo vm_2_cpu0_pid is ${vm_2_cpu0_pid} > /root/tmp2.txt
echo vm_2_cpu0_pid is ${vm_2_cpu0_pid}
echo vm_2_cpu1_pid is ${vm_2_cpu1_pid}
echo vm_2_cpu2_pid is ${vm_2_cpu2_pid}
echo vm_2_cpu3_pid is ${vm_2_cpu3_pid}
taskset -pc -a ${cpu_vm2_core0} ${vm_2_pid}
taskset -pc ${cpu_vm2_core0} ${vm_2_cpu0_pid}
taskset -pc ${cpu_vm2_core1} ${vm_2_cpu1_pid}
taskset -pc ${cpu_vm2_core2} ${vm_2_cpu2_pid}
taskset -pc ${cpu_vm2_core3} ${vm_2_cpu3_pid}
echo
