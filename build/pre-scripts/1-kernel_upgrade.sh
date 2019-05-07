#!/bin/bash

# wake up the DNS resolver
systemd-resolve --status
sleep 2

cd /tmp/
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-headers-4.20.0-042000_4.20.0-042000.201812232030_all.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-headers-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-image-unsigned-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
wget -c https://kernel.ubuntu.com/~kernel-ppa/mainline/v4.20/linux-modules-4.20.0-042000-generic_4.20.0-042000.201812232030_amd64.deb
dpkg -i *.deb
update-grub

modprobe -rv ipmi_si
modprobe -rv ipmi_devintf

apt remove -y openipmi
apt install -y openipmi
systemctl restart openipmi

echo '#!/bin/sh' > /etc/rc.local
echo '/root/2-package_download.sh' >> /etc/rc.local
echo >> /etc/rc.local
chmod +x /etc/rc.local

init 6
