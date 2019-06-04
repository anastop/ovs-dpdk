# Remote Cold Build of a Lab Server

This set of instructions is intended for the lab staff to remotely build or rebuild one of the lab servers. 

**CAUTION!**
> These instructions contain values that are specific to a particular lab environment, and therefore will not be suitable for everyone. Please take care when adapting these instructions to your own environment as many of the addresses, hostnames, and passwords will differ.

#### Process Overview
These instructions walk though through the setup process for a lab server. There is a pre-build section that contains the steps needed to prepare a "jump server" with the appropriate scripts. Following this, the build section outlines the process to reload the OS of the server and then start the automation scripts that complete the lab server setup.

#### Expected Outcome
Upon completion of these steps, the lab server will be loaded with the software required to run the student lab exercises; however none of these services will be started upon boot. The student performs the start of the services in the lab exercise.

Additionally, the automated build process also accounts for the unique CPU chips in each server. For instance, in the Speed Select lab, the build script automatically identifies the number of cores and determines which of those cores is "High_P1" vs. "Low_P1" and then stores this information in a shell environment variable that is loaded on boot via cron.

&nbsp;

## Choose your own adventure:
* [ ] **[Preparing the Jump Server:](#preparing-the-jump-server)** This process is only run the first time you need to reload a lab server. Skip this section for all subsequent reloads.
* [ ] **[Reloading the Lab Server:](#reloading-the-lab-server** Follow this section for each lab server you wish to reload.

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

&nbsp;

**Your jump server is ready for use!**

&nbsp;

&nbsp;

## Reloading a Lab Server
Perform these steps each time you want to refresh a server.

There are two parts to the lab server reload process:
* [ ] **[RELOAD THE SERVER OS:](#reload-the-server-os)** Unattended (~5-10 minutes) - Reinstall the operating system via the PXE boot loader.
* [ ] **[EXECUTE THE BUILD SCRIPT:](#execute-the-build-script)** Unattended (~15 minutes) - Execute the "remote-cold-build" script to install the software.


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
	![cold_build_doc-reload_os-power_reset](/images/cold_build_doc-reload_os-power_reset.png)
	
5. Click INSIDE the remote console window to ensure it has the focus of your keyboard and mouse.
6. Wait patiently for a few minutes and watch the remote console window while the lab server reboots. 
	* During the first few minutes the lab server will initiate a network (PXE) boot sequence.
	* The PXE boot process launches a boot menu.
	* The boot menu will time out after 10 seconds, after which it will boot from the local hard drive. 
7. In the boot menu, before the menu times out, use the arrow keys to select **Ubuntu 18.04 for CLX**. 
	![cold_build_doc-reload_os-pxe_boot_menu](/images/cold_build_doc-reload_os-pxe_boot_menu.png)

8. The server will immediately initiate a scripted OS reinstallation, which may take up to 10 minutes to complete. 
	![cold_build_doc-reload_os-ubuntu_install](/images/cold_build_doc-reload_os-ubuntu_install.png)

9. Upon completion, the remote console will show the server logon prompt. No other indication is made that the OS installation script has completed successfully. You do **NOT** need to logon to the server.
	![cold_build_doc-reload_os-process_completed](/images/cold_build_doc-reload_os-process_completed.png)



&nbsp;

**The Lab Server OS has been successfully reloaded.**

&nbsp;


### Execute the Build Script
> After reloading the operating system of the lab server, you must execute an automation script to download and configure the lab server.

1. Logon to your jump server via SSH using your own non-superuser account. This is the jump server configured earlier in this guide. For example:
```
ssh <your-username>@iln01
```
2. Change to the directory of the GitHub repository and perform an update of the scripts. This command "pulls" the current scripts from the internet to your jumpt server. 
> You only need to perform this command once per day, or if you suspect the scripts have changed since you last pulled the source.
```
cd $HOME/ovs-dpdk-lab
git pull
```

3. Enter the `build` directory and launch the remote-cold-build script, using the following parameters:
> ```
> Remote Server Build Script for OVS-DPDK Lab
> ------------------------------------------------
> 
> You must enter exactly 4 command line argument
> 
> Usage: './remote-cold-build.sh <SERVER_NAME> <UNPRIV_USER> <UNPRIV_PASS> <ROOT_PASS>'
> 
> Where:
>   <SERVER_NAME> is the name of the server you wish to build.
>   <UNPRIV_USER> is the unprivileged username.
>   <UNPRIV_PASS> is the password for the unprivileged user.
>   <ROOT_PASS> is the password for root.
> 
> This script will first logon as pid and then enable root ssh
> It will then start the server build process by updating the kernel.
> Upon reboot the script will automatically resume, downloading the github repo, and then starting the install.sh script in the git repo.
> 
> Example: './remote-cold-build.sh icn01 pid password password'
> ```

```
cd build
./remote-cold-build.sh <SERVER_NAME> <UNPRIV_USER> <UNPRIV_PASS> <ROOT_PASS>
```
8. The `remote-cold-build` script will run several commands that may wait for a second or two before continuing to execute. This is normal. Do **NOT** interrupt the script or press any keys until the script has completed (approximately 1-2 minutes). 
	![cold_build_doc-build_script-initial_pause](/images/cold_build_doc-build_script-initial_pause.png)

9. Upon completion, the remote console will show the server logon prompt. No other indication is made that the OS installation script has completed successfully. You do **NOT** need to logon to the server.
	![cold_build_doc-build_script-completion](/images/cold_build_doc-build_script-completion.png)



&nbsp;
# Lab Server Setup Completed!

**The Lab Server installation script has been successfully started.**

**Wait approximately 15 minutes before proceeding to test the server.**

&nbsp;

# Appendix A: Additional Build Script Details

### Build script assumptions
The automation script `remote-cold-build.sh` performs the initial connection to the Ubuntu server as the user `pid` and then enables root SSH access for the remainder of the lab setup process. It then launches a series of additional scripts to complete the installation and configuration of the server.

Current state assumption:
* The server is a fresh installation of Ubuntu 18.04.2 (Kernel 4.15)
* The root account is not yet permitted to logon via SSH
* The credentials are: `username: pid` and `password: password`
* The user `pid` is not yet in the sudoers file, 


#### Tasks performed in the remote-cold-build script
1. Enable the root user to logon via SSH and upload SSH keys
	* Logon to the host as `pid`, password `password`
	* Enter Super User mode and allow root to logon via SSH.
	* Enable root to logon via SSH.
2. Push your workstation's public SSH key to the lab server.
3. Use SCP to upload the "pre-scripts" to the lab server.
4. Use SSH to remotely execute the first pre-script, which:
	* Upgrades the Linux kernel to 4.20
	* Puts the next script into the rc.local file (so it runs upon next reboot)
	* Reboots the lab server

&nbsp;

# Appendix B: Testing the server

Please refer to the following guide for testing and verification processes.
[Testing the System](/build/Testing the System.md)

&nbsp;


# Appendix C: Lab Server Exercise
The lab server is ready for the lab exercise. 
Please refer to the guide: [SST-BF Lab Guide](/lab/SST-BF Lab Guide.md)



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


