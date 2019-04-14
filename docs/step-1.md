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

3. Logon to the host as root via SSH:
```
ssh root@<hostname>
```

### Update the Linux Kernel
Linux kernel v4.20 is the lowest version our lab exercises can use. Follow these steps to upgrade the kernel, GRUB, and then reboot the host.

**Note:**
> If DNS fails to resolve the name, reboot the host. If that still fails, you can perform these steps as a workaround:
> ```
> echo "DNS=8.8.8.8" >> /etc/systemd/resolved.conf
> systemctl restart systemd-resolved.service
> ```

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

# Continue to the next document in the build process.