# Remote Cold Build of a Lab Server

This set of instructions is intended for the lab staff to remotely build or rebuild one of the lab servers. 

**CAUTION!**
> These instructions contain values that are specific to a particular lab environment, and therefore will not be suitable for everyone. Please take care when adapting these instructions to your own environment as many of the addresses, hostnames, and passwords will differ.


### Overview
These instructions walk though through the setup process for a lab server. There is a pre-build section that contains the steps needed to prepare a "jump server" with the appropriate scripts. Following this, the build section outlines the process to reload the OS of the server and then start the automation scripts that complete the lab server setup.

### Expected Outcome
Upon completion of these steps, the lab server will be loaded with the software required to run the student lab exercises; however none of these services will be started upon boot. The student performs the start of the services in the lab exercise.

Additionally, the automated build process also accounts for the unique CPU chips in each server. For instance, in the Speed Select lab, the build script automatically identifies the number of cores and determines which of those cores is "High_P1" vs. "Low_P1" and then stores this information in a shell environment variable that is loaded on boot via cron.

&nbsp;

&nbsp;

## Preparing the Jump Server

These instructions are intended to be run only once. Once your jump server is prepared with the requisite scripts, you may proceed to the server reload section below.

1. Logon to the jump server as yourself. You do not require superuser or root access. For example:
```
ssh <your-username>@iln01
```
2. Clone the following GitHub repo to your home folder. This will bring down a set of scripts that will enable you to prep the server after the OS has been reinstalled.
```
git clone https://github.com/brianeiler/ovs-dpdk.git $HOME/ovs-dpdk-lab
```

The scripts will be in the subfolder "$HOME/ovs-dpdk-lab/build"

**Your jump server is ready for use**

&nbsp;

&nbsp;

## Reloading a Lab Server
Perform these steps each time you want to refresh a server.

There are two parts to the lab server reload process:
* [ ] **[RELOAD THE SERVER OS:](#reload-the-server-os)** Unattended (~10 minutes) - Reinstall the operating system via the PXE boot loader.
* [ ] **[EXECUTE THE BUILD SCRIPT:](#execute-the-build-script)** Unattended (~20 minutes) - Execute the "remote-cold-build" script to install the software.


### Reload the Server OS
To perform this process you must either use a VM within the lab network, or you must use an SSH tunnel to redirect the ports.

1. On your workstation, open an HTTPS connection to the Remote Management Module (RMM) of the lab server you wish to reload. 
	* In this lab, the 3rd octet of the server's IP address determines whether you are connecting to the RMM or the host.
	* The fourth octet of the server's IP address matches between the RMM and the host IP.
	* For instance, you can SSH insto ICN01 using 192.168.120.1; however you will access the RMM (via HTTPS) using 192.168.123.1.
	
	![cold_build_doc-reload_os-logon_screen](/images/cold_build_doc-reload_os-logon_screen.png)

2. Logon to the RMM using administrative credentials.
3. In the RMM, use the HTML5 Remote Console to gain access to the lab server.
	![cold_build_doc-reload_os-remote_control](/images/cold_build_doc-reload_os-remote_control.png)
	
4. In the RMM, within the HTML5 Remote Console window, use the server power control to reboot the lab server.
5. Click INSIDE the remote console window to ensure it has the focus of your keyboard and mouse.
6. Wait patiently for a few minutes and watch the remote console window while the lab server reboots. 
	* During the first few minutes the lab server will initiate a network (PXE) boot sequence.
	* The PXE boot process launches a boot menu.
	* The boot menu will time out after 10 seconds, after which it will boot from the local hard drive. 
7. In the boot menu, before the menu times out, use the arrow keys to select **Ubuntu 18.04 for CLX**. 
8. The server will immediately initiate a scripted OS reinstallation, which may take up to 10 minutes to complete. Upon completion, the remote console will show the server logon prompt. No other indication is made that the OS installation script has completed successfully.


### Execute the Build Script
> After reloading the operating system of the lab server, you must execute an automation script to download and configure the lab server.

1. Logon to your jump server via SSH using your own non-superuser account. This is the jump server configured earlier in this guide. For example:
```
ssh <your-username>@iln01
```
2. Change to the directory of the GitHub repository and perform an update of the scripts. This command "pulls" the current scripts from the internet and loads thewhere the build scripts are located



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
> You should clone the git repository to your local workstation (or your jump box) so that you have easy access to the `/build/pre-scripts` directory and its contents.

1. Clone this repo to your current directory using the commend below. This will create a folder called `ovs-dpdk-lab` and synchronize the git repo to that folder.
```
git clone https://github.com/brianeiler/ovs-dpdk.git ovs-dpdk-lab
```
> To update this folder in the future, enter the directory and then type `git pull`. Your workstation will automatically download the newest version of the scripts and documentation.

2. Edit the Pre-scripts. All the scripts in this repo rely upon the file `0-ovs-dpdk-global-variables.sh`. The generic template version of this file is located at `/build/pre-scripts/0-ovs-dpdk-global-variables.sh`.
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

&nbsp;


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
./build/install.sh
```
2. Review the command history for errors and if OK, reboot the server as directed by the script. 



## Review/Adjust the Global Variables
Logon to your lab server and verify that the custom script file `/etc/0-ovs-dpdk-global-variables.sh` matched the CPU cores in your server. Each server **WILL** be different, and the installation script attempts to auto-detect and map the cores, but it will fail if hyper-threading is disabled due to the difference in the core count. Also, make no assumptions about the CPU core IDs of the high performance cores between hosts, as they are set on a per-chip basis at the factory and cannot be modified.
Additionally, the server must have certain BIOS settings enabled to expose these cores. These BIOS instructions are not provided in this Git Repo at this time.



# Lab Server Configuration Completed!
The lab server is ready for the lab exercise. 
Please refer to the next guide: [SST-BF Lab Guide](/lab/SST-BF Lab Guide.md)



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


