#!/bin/bash

# Wake up DNS
systemd-resolve --status
sleep 2

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


cd ${git_base_path}
git pull

${git_base_path}/lab/start-ovs.sh
${git_base_path}/lab/start-qemu.sh
${git_base_path}/lab/start-trex.sh
