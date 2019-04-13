#!/bin/sh
#cd /opt/ovs-dpdk-lab/
#cp ./configs/trex_cfg-4ports.yaml /etc
echo 8192 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
umount /mnt/huge
mount -t hugetlbfs nodev /mnt/huge -o pagesize=2M
cat /proc/meminfo
mount
echo "Starting Trex server"
cd /opt/ovs-dpdk-lab/trex/
./t-rex-64 -i  --cfg /etc/trex_cfg-4ports.yaml
