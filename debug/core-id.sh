#!/bin/bash


/sys/devices/system/cpu/cpu*/cpufreq/base_frequency


# for (( c=0; c<=5; c++ ))
# do  
#    echo "Welcome $c times"
# done

declare -a CORE_BASE_FREQ

CPUPATH=/sys/devices/system/cpu
CPURANGE=$[$(cat /proc/cpuinfo | grep processor | wc -l)-1]

for i in $(seq 0 ${CPURANGE})
do
   CORE_BASE_FREQ[i] = `cat ${CPUPATH}/cpu${i}/cpufreq/base_frequency`
done

echo "core 4 = " ${CORE_BASE_FREQ[4]}

