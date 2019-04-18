#!/bin/bash

declare -a CORE_BASE_FREQ

CPUPATH=/sys/devices/system/cpu
CPURANGE=$[$(cat /proc/cpuinfo | grep processor | wc -l)-1]

for i in $(seq 0 ${CPURANGE})
do
   cat ${CPUPATH}/cpu${i}/cpufreq/base_frequency 
   # > CORE_BASE_FREQ[${i}]
done

echo "core 4 = " ${CORE_BASE_FREQ[4]}

