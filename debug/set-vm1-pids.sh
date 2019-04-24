#!/bin/bash

taskset -pc -a $1
taskset -pc -a ${cpu_vm1_core0},${cpu_vm1_core1} $1
taskset -pc ${cpu_vm1_core2} $2
taskset -pc ${cpu_vm1_core3} $3
taskset -pc -a $1