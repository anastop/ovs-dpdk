#!/bin/bash
main_pid=$1
core_2_pid=$2 #(( main_pid + 11 ))
core_3_pid=$3 #(( main_pid + 12 ))
${cpu_vm1_core0}
${cpu_vm1_core1}
${cpu_vm1_core2}
${cpu_vm1_core3}

taskset -pc -a ${cpu_vm1_core0},${cpu_vm1_core1} $1
taskset -pc ${cpu_vm1_core2} ${core_2_pid}
taskset -pc ${cpu_vm1_core3} ${core_3_pid}
taskset -pc -a ${main_pid}
