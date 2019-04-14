#!/bin/bash

cd /opt/ovs-dpdk-lab/source
apt update
echo
echo "Installing DPDK 17.11.4..."
echo
echo "Done Installing DPDK 17.11.4."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing OVS-2.10.1..."
echo
echo "Done Installing OVS-2.10.1."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing qemu-2.12.1..."
echo
echo "Done Installing qemu-2.12.1"
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing TREX-2.53..."
echo "Done Installing TREX-2.53."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Setting up the GRUB boot loader"
echo
echo "Done Setting up the GRUB boot loader"
echo
echo
echo "You must reboot to complete the changes."
echo "===> Type 'init 6' and press ENTER."
echo
