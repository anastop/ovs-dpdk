#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

$OVS_DIR/utilities/ovs-appctl -t ovsdb-server exit
$OVS_DIR/utilities/ovs-appctl -t ovs-vswitchd exit

