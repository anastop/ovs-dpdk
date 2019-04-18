#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


cd ${git_base_path}/source
apt update

echo
echo "Installing DPDK..."
tar xf dpdk-18.11.1.tar.xz -C /opt
ln -sv /opt/dpdk-stable-18.11.1 ${git_base_path}/dpdk
${git_base_path}/source/compile_dpdk.sh 
echo
echo "Done Installing DPDK."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing OVS..."
tar xf openvswitch-2.11.0.tar.gz -C /opt
ln -sv /opt/openvswitch-2.11.0 ${git_base_path}/ovs
${git_base_path}/source/compile_ovs.sh 
echo
echo "Done Installing OVS."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing QEMU..."
tar xf qemu-3.1.0.tar.xz -C /opt
ln -sv /opt/qemu-3.1.0 ${git_base_path}/qemu
${git_base_path}/source/compile_qemu.sh
echo
echo "Done Installing QEMU."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Installing TRex..."
tar xf trex-v2.56.tar.gz -C /opt
mv /opt/v2.56 /opt/trex-v2.56
ln -sv /opt/trex-v2.56 ${git_base_path}/trex
dpdk_igb_file=${git_base_path}/dpdk/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko
trex_igb_dir=${git_base_path}/trex/ko/`uname -r`
mkdir $trex_igb_dir
if [ ! -f $dpdk_igb_file ];
then
	echo
	echo The DPDK version of igb_uio.ko is missing. Cannot copy file.
	echo
else
	cp $dpdk_igb_file $trex_igb_dir
	echo
	echo DPDK version of igb_uio.ko copied successfully.
	echo
fi
${git_base_path}/source/compile_trex.sh
echo
echo "Done Installing TRex."
echo
read -r -p "Check for errors. If all OK, press the ENTER key to continue. Press Ctrl-C to abort the script." key
echo
echo
echo "Setting up the Startup Script..."
echo "@reboot root ${git_base_path}/source/startup-script.sh" >> /etc/crontab
echo
echo "Done Setting up the Startup script"
echo
echo
echo "Setting up the GRUB boot loader"
cp -f ${git_base_path}/source/grub /etc/default/grub
update-grub
echo
echo "Done Setting up the GRUB boot loader"
echo
echo
echo "You must reboot to complete the changes."
echo "===> Type 'init 6' and press ENTER."
echo
