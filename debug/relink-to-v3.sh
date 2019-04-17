#!/bin/bash

rm /opt/ovs-dpdk-lab/dpdk
rm /opt/ovs-dpdk-lab/ovs
rm /opt/ovs-dpdk-lab/qemu
rm /opt/ovs-dpdk-lab/trex

ln -sv /opt/dpdk-stable-18.11.1 /opt/ovs-dpdk-lab/dpdk
ln -sv /opt/openvswitch-2.11.0 /opt/ovs-dpdk-lab/ovs
ln -sv /opt/qemu-3.1.0 /opt/ovs-dpdk-lab/qemu
ln -sv /opt/trex-v2.53 /opt/ovs-dpdk-lab/trex
