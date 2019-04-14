#!/bin/sh

cd /opt/ovs-dpdk-lab/source
apt update
echo
echo "Installing DPDK 17.11.4..."
tar xvf dpdk-17.11.4.tar.xz -C /opt
ln -sv /opt/dpdk-stable-17.11.4 /opt/ovs-dpdk-lab/dpdk
/opt/ovs-dpdk-lab/source/compile_dpdk.sh 
echo
echo "Done Installing DPDK 17.11.4."
echo
echo
echo "Installing OVS-2.10.1..."
tar xvf openvswitch-2.10.1.tar.gz -C /opt
ln -sv /opt/openvswitch-2.10.1 /opt/ovs-dpdk-lab/ovs
/opt/ovs-dpdk-lab/source/compile_ovs.sh 
echo
echo "Done Installing OVS-2.10.1."
echo
echo
echo "Installing qemu-2.12.1..."
tar xvf qemu-2.12.1.tar.xz -C /opt
ln -sv /opt/qemu-2.12.1 /opt/ovs-dpdk-lab/qemu
/opt/ovs-dpdk-lab/source/compile_qemu.sh
echo
echo "Done Installing qemu-2.12.1"
echo
echo
echo "Installing TREX-2.53..."
tar xvf trex-v2.53.tgz -C /opt
ln -sv /opt/trex-v2.53 /opt/ovs-dpdk-lab/trex
mkdir /opt/ovs-dpdk-lab/trex/ko/`uname -r`
cp /opt/ovs-dpdk-lab/dpdk/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko /opt/ovs-dpdk-lab/trex/ko/`uname -r`/
echo
echo "Done Installing TREX-2.53."
echo
echo
echo "Setting up the GRUB boot loader"
cp -f /opt/ovs-dpdk-lab/source/grub /etc/default/grub
update-grub
echo
echo "Done Setting up the GRUB boot loader"
echo
echo
echo "You must reboot to complete the changes."
echo "===> Type 'init 6' and press ENTER."
echo
