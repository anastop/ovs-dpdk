#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

# Wake up DNS
${git_base_path}/debug/restart-dns.sh
sleep 2

modprobe msr
# Cleanup pre-setup files -- the updated versions are kept in the ${git_base_path}/pre-scripts folder
rm /root/1-kernel_upgrade.sh
rm /root/2-package_download.sh
rm /root/3-github_clone.sh


cd ${git_base_path}/source
echo
echo "Downloading source packages..."
wget https://trex-tgn.cisco.com/trex/release/v2.56.tar.gz
wget https://www.openvswitch.org/releases/openvswitch-2.11.0.tar.gz
wget https://download.qemu.org/qemu-3.1.0.tar.xz
wget https://fast.dpdk.org/rel/dpdk-18.11.1.tar.xz

# Rename the TRex file to make it intelligible. This is also done to the extracted directory name after it's unzipped in a later script.
mv v2.56.tar.gz trex-v2.56.tar.gz

echo
echo "Done Downloading source packages."
echo
mkdir ${git_base_path}/vm-images
cd ${git_base_path}/vm-images
echo
echo "Downloading Virtual Router VM images..."
wget https://www.dropbox.com/s/bnjocs6a886gk4e/images_ubuntu-vpp.tgz
echo
echo "Done Downloading Virtual Router VM images"
echo
echo "Expanding Virtual Router VM images..."
tar xvf images_ubuntu-vpp.tgz
echo
echo "Done Expanding Virtual Router VM images"
echo
echo

echo "Generating the CPU core environment variables."
# Set the CPU to operate in Base Frequency (non-turbo) mode
# Setting modprobe msr to run again. Sometimes the key is rejected on the first attempt.
modprobe msr
${git_base_path}/scripts/sstbf.py -d

# Inventory the CPU cores, use the -c argument to create BASH environment variables and arrays for the CPU core.s
# Append the output to our global variable files - both the live version in /etc and the backup copy in /pre-scripts.
# Remember, these values are unique to this motherboard and cannot be copied to another host. The Core ID mappings WILL be different.
${git_base_path}/scripts/sstbf.py -c >> /etc/0-ovs-dpdk-global-variables.sh
${git_base_path}/scripts/sstbf.py -c >> ${git_base_path}/build/pre-scripts/0-ovs-dpdk-global-variables.sh

# Because we updated the file, we need to re-run the source command to update our shell with the new variables
source /etc/0-ovs-dpdk-global-variables.sh


echo
# Run apt update just in case the compiler scripts change later.
apt update

cd ${git_base_path}/source

echo
echo "Installing DPDK..."
tar xf dpdk-18.11.1.tar.xz -C /opt
ln -sv /opt/dpdk-stable-18.11.1 ${git_base_path}/dpdk
${git_base_path}/source/compile_dpdk.sh 
echo
echo "Done Installing DPDK."
echo
echo "Installing OVS..."
tar xf openvswitch-2.11.0.tar.gz -C /opt
ln -sv /opt/openvswitch-2.11.0 ${git_base_path}/ovs
${git_base_path}/source/compile_ovs.sh 
echo
echo "Done Installing OVS."
echo
echo "Installing QEMU..."
tar xf qemu-3.1.0.tar.xz -C /opt
ln -sv /opt/qemu-3.1.0 ${git_base_path}/qemu
${git_base_path}/source/compile_qemu.sh
echo
echo "Done Installing QEMU."
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
echo
echo "Setting up the Startup Script and system parameters..."
echo "@reboot root ${git_base_path}/source/startup-script.sh" >> /etc/crontab
echo
echo "#Disable Address Space Layout Randomization (ASLR)" > /etc/sysctl.d/aslr.conf
echo "kernel.randomize_va_space=0" >> /etc/sysctl.d/aslr.conf
echo "# Enable IPv4 Forwarding" > /etc/sysctl.d/ip_forward.conf
echo "net.ipv4.ip_forward=0" >> /etc/sysctl.d/ip_forward.conf

echo
echo "Done Setting up the Startup script"
echo
echo
echo "Setting up the GRUB boot loader"
sed -i -e '/^GRUB_CMDLINE_LINUX/ s/"$/ default_hugepagesz=1G hugepagesz=1G hugepages=48 hugepagesz=2MB hugepages=16384"/' /etc/default/grub
sed -i -e "/^GRUB_CMDLINE_LINUX/ s/\"\$/ isolcpus=${CPU_CORES_TO_ISOLATE}\"/" /etc/default/grub
sed -i -e "/^GRUB_CMDLINE_LINUX/ s/\"\$/ rcu_nocbs=${CPU_CORES_TO_ISOLATE}\"/" /etc/default/grub
sed -i -e '/^GRUB_CMDLINE_LINUX/ s/"$/ nmi_watchdog=0 audit=0 nosoftlockup processor.max_cstate=1 intel_idle.max_cstate=1 hpet=disable mce=off tsc=reliable numa_balancing=disable"/' /etc/default/grub
update-grub
echo
echo "Done Setting up the GRUB boot loader"
echo
echo
echo "You must reboot to complete the installation."
echo 
echo
read -r -p "Check the screen for errors. If all OK, press the ENTER key to REBOOT. Press Ctrl-C to abort the script." key
echo
