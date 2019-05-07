#!/bin/bash
sh -c 'sleep 1; echo password' | script -qc 'su - root -c /home/pid/prep_unlock.sh'| tail +2
echo "SSH for root unlocked"
