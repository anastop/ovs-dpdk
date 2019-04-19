#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh

# The purpose of this script is to provide the lab administrator with a reliable location
# from which he/she can remotely invoke an update to the lab configuration via SSH without
# knowing in advance the path to this server's local git repo clone.

# At every reboot, this script is copied from the git repo to the /root directory.
# This ensures that future modifications to the update script will automatically become available.

# IMPORTANT!!!
# This script is only copied to the /root directory at boot. 
# This script is *NOT* executed automatically at boot because changes could impact a lab.
# To use this update script, issue an SSH command as follows:
#     ssh root@<hostname> './update_ovs-dpdk-lab.sh'

# Also notice that this script can take additional arguments and run them as commands


# Also execute any additional parameter passed to this script. Just in case.

if [ $# -lt 2 ]; then
	# Pull the latest set of files from the Git Hub repo
	cd ${git_base_path}
	git pull

    echo "Reminder, this script can do more if you give it arguments:"
    echo
    echo "   To just update the Git Repo, just use: $0"
    echo 
    echo "   To instead remotely execute a command in a directory, use:  $0 <directory> <command to execute> [command options]"
    echo
    echo "   Note: For safety, if this script is used to execute a remote command, it does *NOT* also update the Git Repo."
    echo
    exit 1
fi

dir="$1"
shift

for file in "$dir"/*; do
    "$@" "$file"
done

echo
echo "$0 Completed."
echo
