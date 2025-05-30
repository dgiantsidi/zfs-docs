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

cleanup_docker() {
    find_disks
    echo "disks are: $DISKS"
    sudo umount /var/lib/docker
    sudo rm -rf /var/lib/docker
    sudo mdadm --stop /dev/md0
    sudo mdadm --zero-superblock /dev/md0
    sudo wipefs -a $DISKS
}

stop_docker() {
    echo "Stopping docker ..."
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    cleanup_docker
}

mount_docker() {
    sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=$(echo "$DISKS" | awk '{print NF}') $DISKS
    sudo mkdir -p /var/lib/docker
    sudo mkfs.ext4 -F /dev/md0
    sudo mount /dev/md0 /var/lib/docker
}

start_docker() {
    sudo systemctl start docker
    if ! sudo docker info | grep -q "Backing Filesystem: extfs"; then
        echo "Error: Backing Filesystem is not extfs. Aborting."
        stop_docker
        exit 1
    fi

    echo "Docker started successfully."
}

stop_docker
mount_docker
start_docker