#!/bin/bash
#
# 29-Mar-2019, rdahring
echo "============="
echo "CPU config"
echo "============="
lscpu | grep -E "Socket|Thread|Model\ name|NUMA.*CPU|Virtualization"
grep microcode /proc/cpuinfo | uniq

echo
echo "============="
echo "memory config"
echo "============="
dmidecode -t memory | grep Size | grep MB | uniq -c
dmidecode -t memory | grep Speed  | sort  | uniq -c | grep -v Un
grep HugePages_Total /proc/meminfo
grep Hugepagesize /proc/meminfo

echo
echo "============="
echo "BIOS config"
echo "============="
dmidecode -t bios | grep Ver

echo
echo "============="
echo "PCI config"
echo "============="
# lspci | grep -E "QAT|QuickAssist|Ethernet|NVMe"
for D in `lspci | grep -E "QAT|QuickAssist|Ethernet|NVMe" | cut -d' ' -f1`;
        do lspci -vv -s $D | grep -E "${D}|NUMA|LnkSta:"
        echo
done

echo
echo "============="
echo "Ethernet config"
echo "============="

for E in `ip link | grep -v -i loop | grep -v link | cut -d : -f 2` ; do
        echo -e -n "${E}:\t" MAC: `ip link show dev ${E} | grep eth | awk '{print $2}'` `ethtool -i $E | grep bus-info`
        echo
done


echo
echo "============="
echo "OS Info"
echo "============="

if [ -a /etc/lsb-release ] ; then
        cat /etc/lsb-release
fi
if [ -a /etc/centos-release ] ; then
        cat /etc/centos-release
fi

echo
echo "Kernel version: " `uname -r`
echo "Kernel boot parameters: " `cat /proc/cmdline`
echo
