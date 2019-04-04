# New Lab Server

This set of instructions walks you through building a lab server from a fresh installation through to the point the student may logon and execute the configuration scripts for each lab.
After a student completes a lab, they must only reboot the host to reset the configuration for the next lab. 
No service should automatically startup unless it will be used in every lab. 

## Clean Build Stage
This section builds the server to a basic, clean level without custom applications. At the end of this process, an image could be taken of the server for rapid deployment.

Current state assumption:
* The server is a fresh installation of Ubuntu 18.04.2 (Kernel 4.15)
* The root account is not yet permitted to logon via SSH
* The credentials are: `username: pid` and `password: password`
* The user `pid` is not yet in the sudoers file, 

### Logon and gain root access to the Server
1. Logon to the host as `pid`, password `password`
```
ssh pid@<hostname>
```
2. Enter Super User mode and allow root to logon via SSH. The root password is `password`
```
su
```
3. Allow root to logon via SSH.
```
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
service sshd restart
exit
```
4. Logout of the host as user `pid`, and return to your workstation.
```
exit
```


### Install basic utilities
These are tools and utilities that are required by all, or nearly all labs. The tools must be non-commercial and the installations cannot include unique identifiers that would conflict with a server imaging/deployment process.

Software to install:
* tmux
* curl

1. Logon to the host as root via SSH:
```
ssh root@<hostname>
```

2. Update the repositories and install the basic utilities:
```
apt update
apt install -y curl
apt install -y tmux
```
3. Disable the automatic (background) upgrades that can create version mismatch. This is a security risk, but this is also a lab terminal and therefore should never be used in a production capacity or to host sensitive data. The important aspect of a lab terminal is the reliable execution of written procedures, and therefore automatic updates that could impact the behavior of the lab must be disabled. To do so, enter this command:
```
apt remove -y unattended-upgrades
```

### Update the Linux Kernel
Linux kernel v4.20 is the lowest version our lab exercises can use. Follow these steps to upgrade the kernel, GRUB, and then reboot the host.
1. Download the packages to the directory `/tmp`
```
cd /tmp/
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-headers-4.20.0-042000_4.20.0-042000.201812232030_all.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-headers-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-image-unsigned-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-modules-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
```
2. Install the packages
```
dpkg -i *.deb
```
3. Update the GRUB boot loader
```
update-grub
```
4. Reboot the host.
```
init 6
```



## Containerize
To keep the host as clean as possible, use containers were possible. Containers may also be used to pin uncooperative services to specific cores without the use of tasksets.





## Customization Stage
During this stage, install the applications specific to this collection of lab activities.

Applications/services to install:
* collectd
* grafana
* docker

Copy/Paste this code:
```
apt update
apt install -y collectd
apt install 
```

