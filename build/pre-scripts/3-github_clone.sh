#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

# wake up the DNS resolver
systemd-resolve --status
sleep 2

git clone https://github.com/brianeiler/ovs-dpdk.git ${git_base_path}

