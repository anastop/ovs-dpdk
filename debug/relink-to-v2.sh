#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

rm ${git_base_path}/dpdk
rm ${git_base_path}/ovs
rm ${git_base_path}/qemu
rm ${git_base_path}/trex

ln -sv /opt/dpdk-stable-17.11.4 ${git_base_path}/dpdk
ln -sv /opt/openvswitch-2.10.1 ${git_base_path}/ovs
ln -sv /opt/qemu-2.12.1 ${git_base_path}/qemu
ln -sv /opt/trex-v2.53 ${git_base_path}/trex
