#!/bin/bash

apt update
apt install -y curl
apt install -y tmux
apt install -y git
apt install -y python
apt remove -y unattended-upgrades

cd /opt
git clone https://github.com/brianeiler/ovs-dpdk.git ovs-dpdk-lab

