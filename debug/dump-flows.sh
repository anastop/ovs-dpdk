#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


watch -n1 ${git_base_path}/ovs/utilities/ovs-ofctl dump-flows br0
