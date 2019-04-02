#!/bin/sh
cd /root/ovs-dpdk
cp ./configs/trex_cfg-4ports.yaml /etc
echo "Starting Trex server"
cd /root/ovs-dpdk/trex/
./t-rex-64 -i  --cfg /etc/trex_cfg-4ports.yaml

