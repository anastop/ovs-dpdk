#!/bin/sh

cd /opt/ovs-dpdk-lab/source
apt update
echo
echo "Installing DPDK 17.11.4..."
mkdir /opt/dpdk
tar xvf dpdk-17.11.4.tar.xz -C /opt
ln -sv /opt/dpdk-stable-17.11.4 /opt/ovs-dpdk-lab/dpdk
/opt/ovs-dpdk-lab/scripts/compile_dpdk.sh 
echo
echo "Done"
echo
echo "Installing OVS-2.10.1..."
tar xvf openvswitch-2.10.1.tar.gz -C /opt
ln -sv /opt/openvswitch-2.10.1 /opt/ovs-dpdk-lab/ovs
/opt/ovs-dpdk-lab/scripts/compile_ovs.sh 
echo
echo "Done"
echo
echo " Installing qemu-2.12.1..."
tar xvf qemu-2.12.1.tar.xz -C /opt
ln -sv /opt/qemu-2.12.1 /opt/ovs-dpdk-lab/qemu
/opt/ovs-dpdk-lab/scripts/compile_qemu.sh
echo
echo "Done"
echo
echo " Installing TREX-2.53..."
tar xvf trex-v2.53.tgz -C /opt
ln -sv /opt/trex-v2.53 /opt/ovs-dpdk-lab/trex
echo
echo "Done"
echo
echo
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
