#!/bin/bash

/opt/ovs-dpdk-lab/debug/disable_services.sh > /dev/null
/opt/ovs-dpdk-lab/debug/stop_services.sh > /dev/null
rmmod igb_uio > /dev/null
rmmod cuse > /dev/null
rmmod fuse > /dev/null
rmmod openvswitch > /dev/null
rmmod uio > /dev/null
rmmod eventfd_link > /dev/null
rmmod ioeventfd > /dev/null
rm -rf /dev/vhost-net > /dev/null

modprobe uio
insmod /opt/ovs-dpdk-lab/trex/ko/src/igb_uio.ko


echo 24 > /sys/devices/system/node/node0/hugepages/hugepages-1048576kB/nr_hugepages
echo 24 > /sys/devices/system/node/node1/hugepages/hugepages-1048576kB/nr_hugepages
umount /dev/hugepages
mount -t hugetlbfs nodev /dev/hugepages -o pagesize=1G
echo 8192 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages 
mount -t hugetlbfs nodev /mnt/huge -o pagesize=2MB
echo "[Resolve]" > /etc/systemd/resolved.conf
echo "DNS=8.8.8.8" >> /etc/systemd/resolved.conf
systemctl restart systemd-resolved.service
touch /root/startup-script-ran

