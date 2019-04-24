#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

#Clear any accidentally mounted points to /mnt
umount /mnt
mkdir /mnt/huge

cp ${git_base_path}/debug/update_ovs-dpdk-lab.sh /root

${git_base_path}/debug/disable_services.sh > /dev/null
${git_base_path}/debug/stop_services.sh > /dev/null
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
echo "[Resolve]" > /etc/systemd/resolved.conf
echo "DNS=8.8.8.8" >> /etc/systemd/resolved.conf
systemctl restart systemd-resolved.service

# Reset the CPU cores to the base frequency P1
${git_base_path}/scripts/sstbf.py -d

cp ${git_base_path}/debug/update_ovs-dpdk-lab.sh /root
echo "Startup Script last run on: " `date` > /root/report-startup-script.txt
