# Building a New Lab Server

This set of instructions walks you through building a lab server from a fresh installation through to the point the student may logon and execute the configuration scripts for each lab.
After a student completes a lab, they must only reboot the host to reset the configuration for the next lab. 
No service should automatically startup unless it will be used in every lab. 



## Initial Connection to the Lab Server
This section guides you through the initial connection to the Ubuntu server as the user `pid` and then helps you enable root SSH access for the remainder of the lab setup process.

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
```
4. Exit Super User mode.
```
exit
```
5. Type `exit` again to logout of the host as user `pid`, and return to your workstation.
```
exit
```

### Enable password-less SSH connections from your workstation
1. Push your public SSH key to the server.
```
ssh-copy-id -i ~/.ssh/id_rsa.pub root@<hostname>
```
2. Enter the root password of `password` when prompted to save the key.

3. From now on, you may logon to the host as root via SSH without using a password.
```
ssh root@<hostname>
```


## Prepare the lab server using the Pre-Scripts
This git repo contains a set of scripts that will be uploaded to the lab server to aid in the server configuration. You will then remotely execute some of these scripts via SSH to complete the setup process. 

**Note:**
> You may wish to clone the git repository to your local workstation (or your jump box) so that you have easy access to the `/build/pre-scripts` directory and its contents.
> To clone the repo to your current directory use the commend: `git clone https://github.com/brianeiler/ovs-dpdk.git ovs-dpdk-lab` 
> This will create a folder called `ovs-dpdk-lab` and synchronize the git repo to that folder.
> To update this folder in the future, enter the directory and then type `git pull`. Your workstation will automatically download the newest version of the scripts and documentation.


### Edit the Pre-scripts
All the scripts in this repo rely upon the file `0-ovs-dpdk-global-variables.sh`. The generic template version of this file is located at `/build/pre-scripts/0-ovs-dpdk-global-variables.sh`.
You **ABSOLUTELY MUST** edit this file to adjust the destination directories and other particulars of your configuration and system.


### Upload the scripts
After you have adjusted the file `/pre-scripts/0-ovs-dpdk-global-variables.sh` to match your desired folder paths, you may upload the scripts to your lab servers using these steps.

1. As noted above, you must first either clone this git repo to your workstation, or download the shell scripts contained in the `/build/pre-scripts` directory of this repo. For these instructions, we will assume that the script files are on your workstation and are located in the `./build/pre-scripts` subdirectory of your current working directory.

2. Use SCP to copy the files to the lab server.
```
scp ./build/pre-scripts/*.sh root@<hostname>:~
```

### Execute the pre-scripts
You will now use SSH to remotely execute the pre-scripts. Alternatively, you may logon to the servers via SSH and run the scripts interactively as normal. These instructions are designed to minimize the interactive logon requirements when building a number of lab servers.

1. Run the first script: `ssh root@<hostname> './1-kernel_upgrade.sh'`

2. Wait for the server to reboot. the first script downloads an updated kernel, installs it, and then reboots the server. This may take 2-3 minutes.

3. Run the package installation script: `ssh root@<hostname> './2-package_download.sh'`

4. If there are no errors, run the git hub script:  `ssh root@<hostname> './3-github_clone.sh'`



# Initial Setup Completed!
To complete the configuration of the lab server, follow these tasks.


## Download and Install the remaining components
There are build scripts that perform many of the remaining steps for you. These scripts are only run one time and should NOT be run again unless the server has been rebuilt.

Logon to the host as root via SSH:
```
ssh root@<hostname>
```

1. Run the first build script to download the remaining files from the Internet.
```
cd ${git_base_path}
git pull
./build/install.sh
```
2. Reboot the server as directed by the script. 


## Review/Adjust the Global Variables
Logon to your lab server and verify that the custom script file `/etc/0-ovs-dpdk-global-variables.sh` matched the CPU cores in your server. Each server **WILL** be different, and the installation script attempts to auto-detect and map the cores, but it will fail if hyper-threading is disabled due to the difference in the core count. Also, make no assumptions about the CPU core IDs of the high performance cores between hosts, as they are set on a per-chip basis at the factory and cannot be modified.
Additionally, the server must have certain BIOS settings enabled to expose these cores. These BIOS instructions are not provided in this Git Repo at this time.



# Lab Server Configuration Completed!
The lab server is ready for the lab exercise. 
Please refer to the next guide in the `/lab` directory. The guide is entitled **"SST-BF Lab Guide.md"**.



**Note:**
> Occasionally DNS on the lab server may fail to resolve public addresses.
> If DNS fails to resolve the name, restart DNS:
> `systemctl restart systemd-resolved.service`
>
> If that fails, you may need to manually add a DNS server:
> ```
> echo "DNS=8.8.8.8" >> /etc/systemd/resolved.conf
> systemctl restart systemd-resolved.service
> ```


