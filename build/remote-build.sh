#!/bin/bash
prepserver=$1

if [ "$#" -ne 1 ]; then
    echo
    echo "Remote Server Build Script for OVS-DPDK Lab"
    echo "------------------------------------------------"
    echo
    echo "You must enter exactly 1 command line argument"
    echo
    echo "Usage: 'remote-build.sh <SERVER_NAME>'"
    echo
    echo "Where:"
    echo "  <SERVER_NAME> is the name of the server you wish to build."
    echo
    echo "This script will first logon as pid and then enable root ssh"
    echo "It will then start the server build process by updating the kernel."
    echo "Upon reboot the script will automatically resume, downloading the github repo,"
    echo "and then starting the install.sh script in the git repo."
    echo
    echo "Example: 'remote-build.sh icn01'"
    echo
else

	ssh-keygen -f "~/.ssh/known_hosts" -R ${prepserver}

	sshpass -p "password" scp ./pre-scripts/prep_unlock.sh pid@${prepserver}:~
	sshpass -p "password" scp ./pre-scripts/prep_start.sh pid@${prepserver}:~
	sshpass -p "password" ssh -tt pid@${prepserver} bash -c "/home/pid/prep_start.sh"

	sshpass -p "password" ssh-copy-id -i ~/.ssh/id_rsa.pub root@${prepserver}
	sshpass -p "password" ssh-copy-id -i ./keys/ivm_id_rsa.pub root@${prepserver}

fi