# Build and install ZFS

Instructions taken from: https://openzfs.github.io/openzfs-docs/Developer%20Resources/Building%20ZFS.html

1) `sh autogen.sh`

2) `./configure`,  add `--enable-debug` for printing out the messages with `zfs_dbgmsg()`. Also to enable printing you need to set the following: `echo 1 >/sys/module/zfs/parameters/zfs_dbgmsg_enable`. Printed lines will be shown with `cat /proc/spl/kstat/zfs/dbgmsg`.

3) `make -s -j$(nproc)`

4) `sudo make install; sudo ldconfig; sudo depmod; sudo ./scripts/zfs.sh`


# Uninstall and remove ZFS

1) `sudo make uninstall; sudo ldconfig; sudo depmod`

2) `make clean`

3) `pkill zed`

4) `sudo modprobe -r zfs`

5) `lsmod | grep zfs`

6) `sudo depmod -a`

7) `sudo reboot`


# Instructions for attaching docker to ZFS

1) `sudo systemctl stop docker` and `sudo systemctl stop docker.socket`
   
2) `cp -au /var/lib/docker/ /var/lib/docker.bk`
 
3) `sudo rm -rf /var/lib/docker`

4) `sudo zpool create -f zpool-docker -m /var/lib/docker /dev/sda /dev/sdb /dev/sdc`. Note that you should first check with 'lsblk' in which disk the OS mount point is.

5) `sudo systemctl start docker`

6) `sudo docker info`
