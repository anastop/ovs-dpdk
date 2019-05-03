#!/bin/bash

# wake up the DNS resolver
systemd-resolve --status
sleep 2

# Copy the global variable file into place
mv 0-ovs-dpdk-global-variables.sh /etc
echo "source /etc/0-ovs-dpdk-global-variables.sh" >> /etc/bash.bashrc

source /etc/0-ovs-dpdk-global-variables.sh

apt update
apt install -y curl
apt install -y python
apt install -y git
apt install -y net-tools
apt install -y tmux
apt install -y screen
apt remove -y unattended-upgrades

git clone https://github.com/brianeiler/ovs-dpdk.git ${git_base_path}

echo
echo `hostname` has completed pre-setup. Logon and run ${git_base_path}/build/install.sh
echo
