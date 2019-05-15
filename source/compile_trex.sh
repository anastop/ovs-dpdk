#!/bin/bash

# Wake up DNS
systemd-resolve --status > /dev/null 2>&1
sleep 2

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

cd ${trex_dir}/ko/src
make clean; make
cd ${git_base_path}
