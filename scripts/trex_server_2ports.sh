#!/bin/sh
echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
cd /root/ovs-dpdk
cp ./configs/trex_cfg-2ports.yaml /etc
echo "Starting Trex server"
cd /root/ovs-dpdk/trex/
./t-rex-64 -i  --cfg /etc/trex_cfg-2ports.yaml
