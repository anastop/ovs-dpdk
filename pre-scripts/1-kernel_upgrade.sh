#!/bin/bash

cd /tmp/
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-headers-4.20.0-042000_4.20.0-042000.201812232030_all.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-headers-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-image-unsigned-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-modules-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
dpkg -i *.deb
update-grub

modprobe -rv ipmi_si
modprobe -rv ipmi_devintf
systemctl stop openipmi
systemctl start openipmi

init 6
