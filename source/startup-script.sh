#!/bin/bash

# Wake up DNS
systemd-resolve --status
sleep 2

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

#Clear any accidentally mounted points to /mnt
umount /mnt
mkdir /mnt/huge

# Disable services
echo 0 > /proc/sys/kernel/nmi_watchdog
systemctl restart systemd-sysctl.service
systemctl disable irqbalance.service
systemctl stop firewalld
cat /proc/sys/kernel/randomize_va_space
service iptables stop
cat /proc/sys/net/ipv4/ip_forward
ufw disable
#pkill -9 crond
#pkill -9 atd
#pkill -9 cron

echo never > /sys/kernel/mm/transparent_hugepage/defrag
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo 0 > /sys/kernel/mm/transparent_hugepage/khugepaged/defrag
sysctl -w vm.swappiness=0
sysctl -w vm.zone_reclaim_mode=0
service irqbalance stop

cp ${git_base_path}/debug/update_ovs-dpdk-lab.sh /root

# Ensure these services are not running at boot
rmmod igb_uio > /dev/null
rmmod cuse > /dev/null
rmmod fuse > /dev/null
rmmod openvswitch > /dev/null
rmmod uio > /dev/null
rmmod eventfd_link > /dev/null
rmmod ioeventfd > /dev/null
rm -rf /dev/vhost-net > /dev/null

modprobe uio
insmod ${DPDK_DIR}/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko
#insmod ${trex_dir}/ko/src/igb_uio.ko
modprobe msr

echo 24 > /sys/devices/system/node/node0/hugepages/hugepages-1048576kB/nr_hugepages
echo 24 > /sys/devices/system/node/node1/hugepages/hugepages-1048576kB/nr_hugepages
umount /dev/hugepages
mount -t hugetlbfs nodev /dev/hugepages -o pagesize=1G
echo 8192 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
echo 8192 > /sys/devices/system/node/node1/hugepages/hugepages-2048kB/nr_hugepages
mount -t hugetlbfs nodev /mnt/huge -o pagesize=2MB
#echo "[Resolve]" > /etc/systemd/resolved.conf
#echo "DNS=8.8.8.8" >> /etc/systemd/resolved.conf
#systemctl restart systemd-resolved.service

# Reset the CPU cores to the base frequency P1
${git_base_path}/scripts/sstbf.py -d

cp ${git_base_path}/lab/start-all.sh /root
cp ${git_base_path}/debug/update_ovs-dpdk-lab.sh /root
echo "Startup Script last run on: " `date` > /root/report-startup-script.txt
