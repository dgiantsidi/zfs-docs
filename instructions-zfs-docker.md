# Build and install ZFS

Instructions taken from: https://openzfs.github.io/openzfs-docs/Developer%20Resources/Building%20ZFS.html

0)
   ```sh
   sudo apt-get update
   ```

1) 
   ```sh
   sudo apt install alien autoconf automake build-essential debhelper-compat dh-autoreconf dh-dkms dh-python dkms fakeroot gawk git libaio-dev libattr1-dev libblkid-dev libcurl4-openssl-dev libelf-dev libffi-dev libpam0g-dev libssl-dev libtirpc-dev libtool libudev-dev linux-headers-generic parallel po-debconf python3 python3-all-dev python3-cffi python3-dev python3-packaging python3-setuptools python3-sphinx uuid-dev zlib1g-dev -y
   ```

If you are on branch `zfs-2.3-release-ioctl`, to enable mocked CCF delays, please set the env variable `export CCF_MOCKED_DELAY_SH=1`. To disable them, you unset the variable like `unset CCF_MOCKED_DELAY_SH`. 

2) ```sh
   sh autogen.sh
   ```

3) ```sh
   ./configure --enable-debug
   ```
   Add `--enable-debug` for printing out the messages with `zfs_dbgmsg()`. Also to enable printing you need to set the following: `echo 1 >/sys/module/zfs/parameters/zfs_dbgmsg_enable`. Printed lines will be shown with `cat /proc/spl/kstat/zfs/dbgmsg`.

4) ```sh
   make -s -j$(nproc)
   ```
   **SOS**: do not tidy the code with `clang-format` as this re-orders some header files with alphanumerical order and breaks compilation.

5) ```sh
   sudo make install && sudo ldconfig && sudo depmod && sudo ./scripts/zfs.sh
   ```


# Uninstall and remove ZFS

0) ```sh
   sudo ./scripts/zfs.sh -u
   ```
   
2) ```sh 
   sudo make uninstall; sudo ldconfig; sudo depmod
   ```

3) ```sh
   make clean && export list="$(find -name .deps)" && for elem in $list; do sudo rm -rf $elem; done && sudo rm -rf __pycache__/ aclocal.m4 build/ config.log config.status  configure libtool stamp-h1 zfs_config.h.in zfs_config.h Makefile.in Makefile zfs.release configure~ zfs_config.h.in~
   ```


## Obsolete cmds
4) ```sh
   pkill zed
   ```

5) ```sh
   sudo modprobe -r zfs
   ```

6) ```sh
   lsmod | grep zfs
   ```

7) ```sh
   sudo depmod -a
   ```

8) ```sh
    sudo reboot
    ```



# Instructions for running ZFS natively

1) ```sh
   sudo zpool create <pool_name> /dev/sdb /dev/sdc /dev/sdd
   ```

   Note that you should first check with `lsblk` in which disk the OS mount point is. You should exclude that disk.
If you are running s-ZFS. This command is a blocking process.
   ```sh
   sudo zpool ccf <pool_name>
   ```

3) ```sh
   zfs unmount -a
   zpool destroy <pool_name>
   zpool list
   ```
   
4) ``` sh
   sudo zfs unmount <pool_name>
   sudo zfs mount <pool_name>
   ```

5) Testing the ZIL
   ```sh
   sudo zpool freeze <pool_name>
   <execute cmds that write data> // the data will be directly flushed to the ZIL
   sudo zpool export <pool_name>
   sudo zpool import <pool_name>
   ```

# Instructions for attaching docker to ZFS

1) ```sh
   sudo systemctl stop docker && sudo systemctl stop docker.socket
   ```
   
2) ```sh
   sudo cp -au /var/lib/docker/ /var/lib/docker.bk
   ```
 
3) ```sh
   sudo rm -rf /var/lib/docker
   ```

4) ```sh
   sudo zpool create -f zpool-docker -m /var/lib/docker /dev/sda /dev/sdb /dev/sdc
   ``` 

Note that you should first check with `lsblk` in which disk the OS mount point is.

5) If you are running s-ZFS. This command is a blocking process.
```sh
sudo zpool ccf <pool_name>
```

6) ```sh
    sudo systemctl start docker
    ```

7) ```sh
    sudo docker info
    ```



# Instructions for attaching docker to ext4

1) ```sh
   sudo systemctl stop docker && sudo systemctl stop docker.socket
   ```

Note that you should first check with `lsblk` in which disk the OS mount point is.

2) ```sh
   sudo export DISKS="/dev/sda /dev/sdb /dev/sdc
   ```
   
Cleanup:

3) ```sh
   sudo umount /var/lib/docker
   sudo rm -rf /var/lib/docker
   sudo mdadm --stop /dev/md0
   sudo mdadm --zero-superblock /dev/md0
   sudo wipefs -a /dev/sda /dev/sdb /dev/sdc
   ``` 

Construct the RAID and mount docker:

4) ```sh 
   sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=$(echo "$DISKS" | awk '{print NF}') $DISKS
   sudo mkdir -p /var/lib/docker
   sudo mkfs.ext4 -F /dev/md0
   sudo mount /dev/md0 /var/lib/docker
   ```


4) ```sh
    sudo systemctl start docker
    ```

5) ```sh
    sudo docker info
    ```




# Notes

kernel versions tested: `6.8.0-1021-azure #25-Ubuntu SMP`, `6.8.0-1020-azure #23-Ubuntu`
zfs-version: `tag: 2.2.4-1`

RSA-key generation for git:
```
ssh-keygen -t rsa -b 4096 -C "dimitra.giantsidi@gmail.com" && eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub
```
