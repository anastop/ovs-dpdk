#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


cd ${git_base_path}/source
echo
echo "Downloading source packages..."
wget https://trex-tgn.cisco.com/trex/release/v2.56.tar.gz
wget https://www.openvswitch.org/releases/openvswitch-2.11.0.tar.gz
wget https://download.qemu.org/qemu-3.1.0.tar.xz
wget https://fast.dpdk.org/rel/dpdk-18.11.1.tar.xz

mv v2.56.tar.gz trex-v2.56.tar.gz

echo
echo "Done Downloading source packages."
echo
mkdir ${git_base_path}/vm-images
cd ${git_base_path}/vm-images
echo
echo "Downloading Virtual Router VM images..."
wget https://www.dropbox.com/s/zflruubvu9cd2ni/ubuntu-16.04-vpp-1.img.tgz
wget https://www.dropbox.com/s/p0ohwtodtohlkkb/ubuntu-16.04-vpp-2.img.tgz
echo
echo "Done Downloading Virtual Router VM images"
echo
echo "Expanding Virtual Router VM images..."
tar xvf ubuntu-16.04-vpp-1.img.tgz
tar xvf ubuntu-16.04-vpp-2.img.tgz
echo
echo "Done Expanding Virtual Router VM images"
echo
echo
echo "Generating the CPU core environment variables."
${git_base_path}/scripts/sstbf.py -c >> /etc/0-ovs-dpdk-global-variables.sh
${git_base_path}/scripts/sstbf.py -c >> ${git_base_path}/pre-scripts/0-ovs-dpdk-global-variables.sh
source /etc/0-ovs-dpdk-global-variables.sh
echo
echo
echo "Build step 1 is complete. Now run the second build script."
echo
