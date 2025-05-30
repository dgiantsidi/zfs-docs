#!/bin/bash


DISKS=""

find_disks() {
    # Check if the directory exists
    if [ -d "/dev/disk/azure" ]; then
    # Use tree if available, fallback to find
        if command -v tree >/dev/null 2>&1; then
            output=$(tree /dev/disk/azure)
            # Extract device names for LUN0, LUN1, and LUN2
            device_list=$(echo "$output" | grep -E 'lun0|lun1|lun2' | grep -oE 'sd[a-z]+')
            for device in $device_list; do
                #echo "/dev/$device"
                DISKS+="/dev/$device "
            done
        else
            find /dev/disk/azure -type l | grep -E 'lun0|lun1|lun2'
        fi
    else
        echo "/dev/disk/azure does not exist on this system."
    fi
    echo $DISKS
}

cleanup_docker_ext4() {
    find_disks
    echo "disks are: $DISKS"
    sudo umount /var/lib/docker
    sudo rm -rf /var/lib/docker
    sudo mdadm --stop /dev/md0
    sudo mdadm --zero-superblock /dev/md0
    sudo wipefs -a $DISKS
}

mount_docker_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/original_zfs"
    cd ${ZFS_DIR}
    sh autogen.sh && ./configure && make -s -j
    sudo make install && sudo ldconfig && sudo depmod && sudo ./scripts/zfs.sh
    cd ${CUR_DIR}
    sudo zpool create -f zpool-docker -m /var/lib/docker ${DISKS}
    sudo systemctl start docker
}


unmount_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/original_zfs"
    cd ${ZFS_DIR}

    sudo ./scripts/zfs.sh -u
    sudo make uninstall; sudo ldconfig; sudo depmod
    make clean && export list="$(find -name .deps)" && for elem in $list; do sudo rm -rf $elem; done && sudo rm -rf __pycache__/ aclocal.m4 build/ config.log config.status  configure libtool stamp-h1 zfs_config.h.in zfs_config.h Makefile.in Makefile zfs.release configure~ zfs_config.h.in~
    cd ${CUR_DIR}
    sudo wipefs -a $DISKS

}

cleanup_docker_zfs() {
    find_disks
    echo "disks are: $DISKS"
    sudo zpool destroy /var/lib/docker
    sudo rm -rf /var/lib/docker
    sudo wipefs -a $DISKS
    unmount_zfs
}


stop_docker_ext4() {
    echo "Stopping docker ..."
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    cleanup_docker_ext4
}

stop_docker_zfs() {
    echo "Stopping docker ..."
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    cleanup_docker_zfs
}

mount_docker_ext4() {
    sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=$(echo "$DISKS" | awk '{print NF}') $DISKS
    sudo mkdir -p /var/lib/docker
    sudo mkfs.ext4 -F /dev/md0
    sudo mount /dev/md0 /var/lib/docker
}

start_docker_ext4() {
    sudo systemctl start docker
    if ! sudo docker info | grep -q "Backing Filesystem: extfs"; then
        echo "Error: Backing Filesystem is not extfs. Aborting."
        stop_docker
        exit 1
    fi

    echo "Docker started successfully."
}

run_postgres_ext4() {
    echo "Running PostgreSQL container ..."
    serialized_date=$(date +%Y%m%d_%H%M)

    mkdir -p $(pwd)/ext4_${serialized_date}

    BASE_DIR_EXT4="/home/azureuser/zfs-docs/postgres-experiments-22-05-remote-client/ext4"
    cp ${BASE_DIR_EXT4}/long_runs.py .
    #python3 long_runs.py 10 1
 
}

run_postgres_zfs() {
    echo "Running PostgreSQL container ..."
    serialized_date=$(date +%Y%m%d_%H%M)

    mkdir -p $(pwd)/zfs_${serialized_date}

    BASE_DIR_EXT4="/home/azureuser/zfs-docs/postgres-experiments-22-05-remote-client/zfs"
    cp ${BASE_DIR_EXT4}/long_runs.py .
    #python3 long_runs.py 10 1
 
}


stop_docker_ext4

mount_docker_ext4
start_docker_ext4
run_postgres_ext4

stop_docker_ext4

mount_docker_zfs
run_postgres_zfs
unmount_zfs
