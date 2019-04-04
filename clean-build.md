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
1. Logon to the host as "pid"
```
ssh pid@<hostname>
```
2. Enter Super User mode and allow root to logon via SSH. The root password is `password`
```
su
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
service sshd restart
```


### Install basic utilities
These are tools and utilities that are required by all, or nearly all labs. The tools must be non-commercial and the installations cannot include unique identifiers that would conflict with a server imaging/deployment process.

Software to install:
* tmux
* curl

Copy/Paste this code:
```
apt update
apt install -y curl
apt install -y tmux
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

