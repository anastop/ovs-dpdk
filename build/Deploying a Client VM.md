# Deploying a VM for the client
These steps include the deployment process for the client VM, an Ubuntu Desktop running on KVM.

Current state assumption:
* The desktop VM is running Ubuntu Desktop 18.04.2
* The username is `pid` with the password of `pid`
* The user is in the sudoers file and otherwise unrestricted.
* The NoMachine remote control software (server mode) is installed and running within the VM.
* The IP addressing is 192.168.120.1xx, where xx is the student server number.


## Connnect to the VM
These applications are used by the students in class.

1. Logon to the VM using the NoMachine client via the SSH Tunnel. NoMachine server listens on TCP/4000. Redirect an appropriate port to the VM's IP address on port 4000 to access the VM.

2. Login to the VM as the user `pid` using the password `password`.


## Install Java SDK
The Java SDK is needed to run the TRex client.

1. Open the terminal called "Konsole". Do not use the one called "Terminal" because it doesn't work properly.

2. In the Konsole window, update apt and install the following packages:
```
sudo apt update
sudo apt upgrade
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:linuxuprising/java
sudo apt update
sudo apt install -y oracle-java11-installer
sudo apt install oracle-java8-installer
```
Well, that didn't work.. trying another approach.
```
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt update
sudo apt install openjdk-8-jdk openjdk-8-jre
```

3. Update the environment variables.
```
sudo vi /etc/environment
```
Then add the following environment variables:
```
JAVA_HOME="/usr/lib/jvm/java-11-oracle"
JRE_PATH=
```
Save and exit.

4. Reboot the VM.
```
init 6
```

## Download and Install TRex Stateless GUI

1. In the VM, open a web browser and navigate to this address:
```
https://github.com/cisco-system-traffic-generator/trex-stateless-gui/releases/download/v4.5.4/trex-stateless-gui-v4.5.4-0-g7424e22.tgz
```
2. Download the file and extract it into the home folder of your user account (pid).


# Caveats and interesting notes
* As of 2019-04-16 it's no longer possible to download Oracle Java without a logon. Most of the repos are dead.  This significantly impacts our kit because we use Oracle Java 8 for TRex. Version 11 isn't fully compatible, and the Open JDK is not technically supported.  Refer to this link for more information. http://www.webupd8.org/2014/03/how-to-install-oracle-java-8-in-debian.html
  - This seems to be an alternative: https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-18-04
  
