# GitHub Build Stage
The steps in this section prepare the host for the lab by cloning a GitHub repository.

Current state assumption:
* The server has been updated to Ubuntu 18.04.2 (Kernel 4.20)
* The root account is permitted to logon via SSH

## Install basic utilities
These are tools and utilities that are required by the lab.
Software to install:
* tmux (Terminal emulator)
* curl (CLI-based web browser)
* git (GitHub client for downloading the scripts)

1. Logon to the host as root via SSH:
```
ssh root@<hostname>
```

2. Update the repositories and install the basic utilities:
```
apt update
apt install -y curl
apt install -y tmux
apt install -y git
```
3. Disable the automatic (background) upgrades that can create version mismatch. This is a security risk, but this is also a lab terminal and therefore should never be used in a production capacity or to host sensitive data. The important aspect of a lab terminal is the reliable execution of written procedures, and therefore automatic updates that could impact the behavior of the lab must be disabled. To do so, enter this command:
```
apt remove -y unattended-upgrades
```

## Clone the GitHub repository for the lab
Clone the repository to the `/opt/ovs-dpdk-lab` directory
```
cd /opt
git clone https://github.com/brianeiler/ovs-dpdk.git ovs-dpdk-lab
cd /opt/ovs-dpdk-lab
```

