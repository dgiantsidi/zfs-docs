#!/bin/bash

export DISKS=""
# Check if the directory exists
if [ -d "/dev/disk/azure" ]; then
# Use tree if available, fallback to find
    if command -v tree >/dev/null 2>&1; then
        output=$(tree /dev/disk/azure)
        # Extract device names for LUN0, LUN1, and LUN2
        device_list=$(echo "$output" | grep -E 'lun0|lun1|lun2' | grep -oE 'sd[a-z]+')
        for device in $device_list; do
            echo "/dev/$device"
            DISKS+="/dev/$device "
        done
    else
        find /dev/disk/azure -type l | grep -E 'lun0|lun1|lun2'
    fi
else
    echo "/dev/disk/azure does not exist on this system."
fi
echo $DISKS
sudo wipefs -a $DISKS