#!/bin/bash

# wake up the DNS resolver
systemd-resolve --status > /root/install_phase_2.log 2>&1
sleep 2

# Copy the global variable file into place
mv 0-ovs-dpdk-global-variables.sh /etc
echo "source /etc/0-ovs-dpdk-global-variables.sh" >> /etc/bash.bashrc

source /etc/0-ovs-dpdk-global-variables.sh

apt update >> /root/install_phase_2.log 2>&1
apt install -y curl >> /root/install_phase_2.log 2>&1
apt install -y python >> /root/install_phase_2.log 2>&1
apt install -y git >> /root/install_phase_2.log 2>&1
apt install -y net-tools >> /root/install_phase_2.log 2>&1
apt install -y tmux >> /root/install_phase_2.log 2>&1
apt install -y screen >> /root/install_phase_2.log 2>&1
apt remove -y unattended-upgrades >> /root/install_phase_2.log 2>&1

rm /etc/rc.local

git clone https://github.com/brianeiler/ovs-dpdk.git ${git_base_path} >> /root/install_phase_2.log 2>&1

echo
echo `hostname` has completed pre-setup.  >> /root/install_phase_2.log 2>&1
echo

cd ${git_base_path}/build
${git_base_path}/build/install.sh > /root/install_phase_3.log 2>&1
