#!/bin/sh

cd /opt/ovs-dpdk-lab/trex/ko/src
make clean; make

rmmod igb_uio uio
modprobe uio
insmod /opt/ovs-dpdk-lab/trex/ko/src/igb_uio.ko

cd /opt/ovs-dpdk-lab
