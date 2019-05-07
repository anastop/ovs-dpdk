#!/bin/bash

prepserver=$1
unprivuser=$2
unprivpass=$3
rootpass=$4

# prepserver=icn03
# unprivuser=pid
# unprivpass=password
# rootpass=password

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' sshpass |grep "install ok installed")
echo Checking for the package 'sshpass': $PKG_OK
if [ "" == "$PKG_OK" ]; then
  echo
  echo "ERROR!  This script requires the package: sshpass"
  echo
  echo "Install the package by typing: sudo apt install sshpass"
  echo
  echo "Exiting..."
  exit 1
fi

if [ ! -f ./keys/ivm_id_rsa.pub ]; then
	echo
	echo "ERROR! This script must be run from within the 'build' folder."
	echo
	echo "Exiting..."
	exit 1
fi

if [ "$#" -ne 4 ]; then
    echo
    echo "Remote Server Build Script for OVS-DPDK Lab"
    echo "------------------------------------------------"
    echo
    echo "You must enter exactly 4 command line argument"
    echo
    echo "Usage: '$0 <SERVER_NAME> <UNPRIV_USER> <UNPRIV_PASS> <ROOT_PASS>'"
    echo
    echo "Where:"
    echo "  <SERVER_NAME> is the name of the server you wish to build."
    echo "  <UNPRIV_USER> is the unprivileged username."
    echo "  <UNPRIV_PASS> is the password for the unprivileged user."
    echo "  <ROOT_PASS> is the password for root."
    echo
    echo "This script will first logon as pid and then enable root ssh"
    echo "It will then start the server build process by updating the kernel."
    echo "Upon reboot the script will automatically resume, downloading the github repo,"
    echo "and then starting the install.sh script in the git repo."
    echo
    echo "Example: '$0 icn01 pid password password'"
    echo
    echo "Exiting..."
	exit 1
else
	ssh-keygen -f "~/.ssh/known_hosts" -R ${prepserver}

	echo 'echo "PermitRootLogin yes" >> /etc/ssh/sshd_config' > prep_unlock.sh
	echo 'service sshd restart' >> prep_unlock.sh
	echo >> prep_unlock.sh
	chmod +x prep_unlock.sh
	echo "sh -c 'sleep 1; echo ${rootpass}' | script -qc 'su - root -c /home/${unprivuser}/prep_unlock.sh'" > prep_start.sh
	echo >> prep_start.sh
	chmod +x prep_start.sh
	sshpass -p "${unprivpass}" scp ./prep_unlock.sh ${unprivuser}@${prepserver}:~
	sshpass -p "${unprivpass}" scp ./prep_start.sh ${unprivuser}@${prepserver}:~
	sshpass -p "${rootpass}" ssh -tt ${unprivuser}@${prepserver} bash -c "/home/${unprivuser}/prep_start.sh"
	echo
	echo "SSH reconfigured to accept root user connections."
	echo

	sshpass -p "${rootpass}" ssh-copy-id -f -i ~/.ssh/id_rsa.pub root@${prepserver}
	sshpass -p "${rootpass}" ssh-copy-id -f -i ./keys/ivm_id_rsa.pub root@${prepserver}
	
	scp ./pre-scripts/*.sh root@${prepserver}:~
	ssh root@${prepserver} '/root/1-kernel_upgrade.sh' > ./install_${prepserver}_phase_1.log 2>&1
	
	# Cleanup
	# 	if [ -f ./prep_unlock.sh ]; then
	# 		rm ./prep_unlock.sh
	# 	fi
	# 	if [ -f ./prep_start.sh ]; then
	# 		rm ./prep_start.sh
	# 	fi
	echo
	echo "Script completed for: ${prepserver}"
	echo
	echo "Exiting..."
	exit 0
fi

