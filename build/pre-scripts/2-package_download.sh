#!/bin/bash

# wake up the DNS resolver
systemd-resolve --status
sleep 2

# Copy the global variable file into place
mv 0-ovs-dpdk-global-variables.sh /etc
echo "source /etc/0-ovs-dpdk-global-variables.sh" >> /etc/bash.bashrc


apt update
apt install -y curl
apt install -y python
apt install -y git
apt install -y net-tools
apt install -y tmux
apt install -y screen
apt remove -y unattended-upgrades


