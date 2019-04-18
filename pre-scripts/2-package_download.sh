#!/bin/bash

# Copy the global variable file into place
cp 0-ovs-dpdk-global-variables.sh /etc

apt update
apt install -y curl
apt install -y tmux
apt install -y git
apt install -y python
apt remove -y unattended-upgrades


