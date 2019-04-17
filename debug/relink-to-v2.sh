#!/bin/bash

rm /opt/ovs-dpdk-lab/dpdk
rm /opt/ovs-dpdk-lab/ovs
rm /opt/ovs-dpdk-lab/qemu
rm /opt/ovs-dpdk-lab/trex

ln -sv /opt/dpdk-stable-17.11.4 /opt/ovs-dpdk-lab/dpdk
ln -sv /opt/openvswitch-2.10.1 /opt/ovs-dpdk-lab/ovs
ln -sv /opt/qemu-2.12.1 /opt/ovs-dpdk-lab/qemu
ln -sv /opt/trex-v2.53 /opt/ovs-dpdk-lab/trex
