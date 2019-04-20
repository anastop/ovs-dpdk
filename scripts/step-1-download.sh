#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

# Cleanup pre-setup files -- the updated versions are kept in the ${git_base_path}/pre-scripts folder
rm /root/1-kernel_upgrade.sh
rm /root/2-package_download.sh
rm /root/3-github_clone.sh
rm /root/build-1.sh
rm /root/build-2.sh
rm /root/prep.sh
rm /root/pbf.py

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
# wget https://www.dropbox.com/s/zflruubvu9cd2ni/ubuntu-16.04-vpp-1.img.tgz
# wget https://www.dropbox.com/s/p0ohwtodtohlkkb/ubuntu-16.04-vpp-2.img.tgz
wget https://www.dropbox.com/s/bnjocs6a886gk4e/images_ubuntu-vpp.tgz
echo
echo "Done Downloading Virtual Router VM images"
echo
echo "Expanding Virtual Router VM images..."
# tar xvf ubuntu-16.04-vpp-1.img.tgz
# tar xvf ubuntu-16.04-vpp-2.img.tgz
tar xvf images_ubuntu-vpp.tgz
echo
echo "Done Expanding Virtual Router VM images"
echo
echo

echo "Generating the CPU core environment variables."
# Set the CPU to operate in Base Frequency (non-turbo) mode
${git_base_path}/scripts/sstbf.py -d

# Inventory the CPU cores, use the -c argument to create BASH environment variables and arrays for the CPU core.s
# Append the output to our global variable files - both the live version in /etc and the backup copy in /pre-scripts.
# Remember, these values are unique to this motherboard and cannot be copied to another host. The Core ID mappings WILL be different.
${git_base_path}/scripts/sstbf.py -c >> /etc/0-ovs-dpdk-global-variables.sh
${git_base_path}/scripts/sstbf.py -c >> ${git_base_path}/pre-scripts/0-ovs-dpdk-global-variables.sh

# Because we updated the file, we need to re-run the source command to update our shell with the new variables
source /etc/0-ovs-dpdk-global-variables.sh

echo
echo
echo "Build step 1 is complete. Now run the second build script."
echo
