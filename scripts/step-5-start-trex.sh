#!/bin/sh

cat /proc/meminfo 
cat /proc/cmdline 
echo 24 > /sys/devices/system/node/node0/hugepages/hugepages-1048576kB/nr_hugepages 
echo 24 > /sys/devices/system/node/node1/hugepages/hugepages-1048576kB/nr_hugepages 
umount /dev/hugepages 
mount -t hugetlbfs nodev /dev/hugepages -o pagesize=1G
echo 8192 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages 
mount -t hugetlbfs nodev /mnt/huge -o pagesize=2MB


cp /opt/ovs-dpdk-lab/configs/trex/trex_cfg.yaml /etc
echo "Starting Trex server"
cd /opt/ovs-dpdk-lab/trex/
./t-rex-64 -i --cfg /etc/trex_cfg.yaml



