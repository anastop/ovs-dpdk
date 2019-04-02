#!/bin/sh

cd /root/
echo "Starting Trex server"
cd /root/ovs-dpdk/trex/
./t-rex-64 -i  --cfg /etc/trex_cfg-6port.yaml
