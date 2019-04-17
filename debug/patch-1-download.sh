#!/bin/sh

cd /opt/ovs-dpdk-lab/source
echo
echo "Downloading source packages..."
wget https://www.dropbox.com/s/rby2eoaj07zoofd/trex-v2.53.tgz
wget https://www.dropbox.com/s/5y39v3hrgnk43b4/openvswitch-2.11.0.tar.gz
wget https://www.dropbox.com/s/bau0d0gxbo670qm/qemu-3.1.0.tar.xz
wget https://www.dropbox.com/s/ozk0i3baq7zxau9/dpdk-18.11.1.tar.xz

echo
echo "Done Downloading source packages."
echo
# mkdir /opt/ovs-dpdk-lab/vm-images
# cd /opt/ovs-dpdk-lab/vm-images
# echo
# echo "Downloading Virtual Router VM images..."
# wget https://www.dropbox.com/s/zflruubvu9cd2ni/ubuntu-16.04-vpp-1.img.tgz
# wget https://www.dropbox.com/s/p0ohwtodtohlkkb/ubuntu-16.04-vpp-2.img.tgz
# echo
# echo "Done Downloading Virtual Router VM images"
# echo
# echo "Expanding Virtual Router VM images..."
# tar xvf ubuntu-16.04-vpp-1.img.tgz
# tar xvf ubuntu-16.04-vpp-2.img.tgz
# echo
# echo "Done Expanding Virtual Router VM images"
echo
echo
echo "Build step 1 is complete. Now run the second build script."
echo
