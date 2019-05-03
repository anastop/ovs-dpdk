#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


${git_base_path}/lab/start-ovs.sh
${git_base_path}/lab/start-qemu.sh
${git_base_path}/lab/start-trex.sh
