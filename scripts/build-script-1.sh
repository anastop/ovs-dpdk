#!/bin/sh

echo "Setting up the GRUB boot loader"
cd
cp -f /opt/ovs-dpdk-lab/source/grub /etc/default/grub
update-grub
echo
echo "Done"
echo
echo
echo "You must reboot to complete the changes."
echo "===> Type 'init 6' and press ENTER."
echo
