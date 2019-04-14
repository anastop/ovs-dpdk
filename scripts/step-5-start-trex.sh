#!/bin/sh

cp /opt/ovs-dpdk-lab/configs/trex/trex_cfg.yaml /etc
echo "Starting Trex server"
cd /opt/ovs-dpdk-lab/trex/
./t-rex-64 -i --cfg /etc/trex_cfg.yaml
