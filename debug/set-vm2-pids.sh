#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh

echo Original...
taskset -pc -a $1
echo
taskset -pc -a ${cpu_vm2_core0},${cpu_vm2_core1} $1
echo 
taskset -pc ${cpu_vm2_core2} $2
echo
taskset -pc ${cpu_vm2_core3} $3
echo
echo Now...
taskset -pc -a $1
