#!/bin/bash

taskset -pc -a $1
taskset -pc -a ${cpu_vm2_core0},${cpu_vm2_core1} $1
taskset -pc ${cpu_vm2_core2} $2
taskset -pc ${cpu_vm2_core3} $3
taskset -pc -a $1
