#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


cd ${git_base_path}source
echo
echo "Downloading source packages..."
wget https://www.dropbox.com/s/rby2eoaj07zoofd/trex-v2.53.tgz
wget https://www.dropbox.com/s/5y39v3hrgnk43b4/openvswitch-2.11.0.tar.gz
wget https://www.dropbox.com/s/bau0d0gxbo670qm/qemu-3.1.0.tar.xz
wget https://www.dropbox.com/s/ozk0i3baq7zxau9/dpdk-18.11.1.tar.xz

echo
echo "Done Downloading source packages."
echo
echo
echo
echo "Build step 1 is complete. Now run the second build script."
echo
