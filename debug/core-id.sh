#!/bin/bash
  
declare -a CPU_CORE_BASE_FREQ

CPU_MAX_CORES=$[$(cat /proc/cpuinfo | grep processor | wc -l)-1]

for i in $(seq 0 ${CPU_MAX_CORES})
do
   CPU_CORE_BASE_FREQ[${i}]=$(cat /sys/devices/system/cpu/cpu${i}/cpufreq/base_frequency)
done
