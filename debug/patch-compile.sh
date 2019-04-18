#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


cd ${git_base_path}/source

echo "Installing DPDK 18.11.1..."
${git_base_path}/source/compile_dpdk.sh 
echo
echo "Done Installing DPDK 18.11.1"
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing OVS-2.11.0..."
${git_base_path}/source/compile_ovs.sh 
echo
echo "Done Installing OVS-2.11.0."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing qemu-3.1.0..."
${git_base_path}/source/compile_qemu.sh
echo
echo "Done Installing qemu-3.1.0"
echo
