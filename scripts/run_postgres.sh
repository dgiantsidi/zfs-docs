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

execute_command() {
    python3 long_runs.py $1 $2 $3

}

cleanup_docker_ext4() {
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

mount_docker_shielded_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/zfs"
    cd ${ZFS_DIR}
    sh autogen.sh && ./configure && make -s -j
    sudo make install && sudo ldconfig && sudo depmod && sudo ./scripts/zfs.sh
    cd ${CUR_DIR}
    sudo zpool create -f zpool-docker -m /var/lib/docker ${DISKS}
    sudo systemctl start docker
}

stop_docker_shielded_zfs() {
    echo "Stopping docker ..."
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    sudo systemctl stop docker && sudo systemctl stop docker.socket
    cleanup_docker_shielded_zfs
}

unmount_shielded_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/zfs"
    cd ${ZFS_DIR}

    sudo ./scripts/zfs.sh -u
    sudo make uninstall; sudo ldconfig; sudo depmod
    make clean && export list="$(find -name .deps)" && for elem in $list; do sudo rm -rf $elem; done && sudo rm -rf __pycache__/ aclocal.m4 build/ config.log config.status  configure libtool stamp-h1 zfs_config.h.in zfs_config.h Makefile.in Makefile zfs.release configure~ zfs_config.h.in~
    cd ${CUR_DIR}
    sudo wipefs -a $DISKS

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

cleanup_docker_shielded_zfs() {
    echo "disks are: $DISKS"
    sudo zpool destroy zpool-docker
    unmount_shielded_zfs
    sudo rm -rf /var/lib/docker
}

cleanup_docker_zfs() {
    echo "disks are: $DISKS"
    sudo zpool destroy /var/lib/docker
    sudo rm -rf /var/lib/docker
    unmount_zfs
    sudo wipefs -a $DISKS

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

    echo "docker started successfully.."
}

run_postgres_ext4() {
    echo "Running PostgreSQL container ..."
    serialized_date=$(date +%Y%m%d_%H%M)
    CUR_DIR=$(pwd)/ext4_${serialized_date}
    mkdir -p ${CUR_DIR}
    cd ${CUR_DIR}

    BASE_DIR_EXT4="/home/azureuser/zfs-docs/scripts"
    cp ${BASE_DIR_EXT4}/long_runs.py .
    #execute_command 10 11 ext4
    #execute_command 20 11 ext4 
    execute_command 60 11 ext4
    #execute_command 50 11 ext4
    cd ../
}

run_postgres_zfs() {
    echo "Running PostgreSQL container ..."
    serialized_date=$(date +%Y%m%d_%H%M)
    CUR_DIR=$(pwd)/zfs_${serialized_date}
    mkdir -p ${CUR_DIR}
    cd ${CUR_DIR}
    
    BASE_DIR_EXT4="/home/azureuser/zfs-docs/scripts"
    cp ${BASE_DIR_EXT4}/long_runs.py .
    #execute_command 10 11 zfs
    #execute_command 20 11 zfs
    execute_command 60 11 zfs
    execute_command 50 11 zfs
    cd ../
 
}

run_postgres_shielded_zfs() {
    echo "Running PostgreSQL container ..."
    serialized_date=$(date +%Y%m%d_%H%M)
    CUR_DIR=$(pwd)/shielded_zfs_${serialized_date}
    mkdir -p ${CUR_DIR}
    cd ${CUR_DIR}
    BASE_DIR_EXT4="/home/azureuser/zfs-docs/scripts"
    cp ${BASE_DIR_EXT4}/long_runs.py .
    #execute_command 10 11 shielded_zfs
    #execute_command 20 11 shielded_zfs
    execute_command 60 11 shielded_zfs
    execute_command 50 11 shielded_zfs
    cd ../
 
}


find_disks
echo "Start .."
stop_docker_ext4
sleep 20

echo "Mount docker at ext4 .."
mount_docker_ext4
sleep 20

echo "Start docker at ext4 .."
start_docker_ext4
sleep 20
echo "Run experiment (ext4) .."
run_postgres_ext4
sleep 20

stop_docker_ext4
sleep 20

#stop_docker_zfs

echo "Mount docker at zfs .."
mount_docker_zfs
sleep 20

echo "Run experiment (zfs) .."
run_postgres_zfs
sleep 20

echo "Stop docker (zfs) .."

stop_docker_zfs
sleep 20

echo "Mount docker (shielded zfs) .."
mount_docker_shielded_zfs
sleep 20

echo "Run experiment (shielded zfs) .."
run_postgres_shielded_zfs
sleep 20

echo "Stop docker (shielded zfs) .."
stop_docker_shielded_zfs
sleep 20
