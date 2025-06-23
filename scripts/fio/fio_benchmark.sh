#!/bin/bash


echo "Running benchmark with: $DISKS"

POOL_NAME="perfpool"
FS_NAME="perffs"

DISKS=""
OUTPUT_PATH="/home/azureuser/zfs-docs/scripts/fio/results"
RESULTS_DIR=""

export DIRECTORY="/${POOL_NAME}/${FS_NAME}"
# 50% of the storage pool
export TOTALSIZE='16000000000'
export FIO_FORMAT='json'
export EXT4_MOUNTDIR="/ext4-bench"
export ZFS_MOUNTDIR="/zfs-bench"
export SHIELDED_ZFS_MOUNTDIR="/shielded-zfs-bench"



setup_folder() {
    # Create a results directory if it doesn't exist
    serialized_date=$(date +%Y%m%d)
    RESULTS_DIR=$(pwd)/results_${serialized_date}
    if [ ! -d ${RESULTS_DIR} ]; then
        mkdir -p ${RESULTS_DIR}
    fi
    echo "Results directory is set to: $RESULTS_DIR"
}

# get disk list
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



# one dataset pool
create_pool () {
    zpool create -f $POOL_NAME $DISKS
}

create_dataset() {
    zfs create -o checksum=sha256 $POOL_NAME/$FS_NAME
}

clean_pool() {
    zpool destroy $POOL_NAME
    wipefs -a $DISKS
}

reset_zinject() {
    zinject -c all
}

# reset before each write benchmark
reset_pool() {
    # kill fio
    pkill fio
    clean_pool
    reset_zinject
    create_pool
    create_dataset
}

# clean arc cache
# reset before read benchmark
function clear_arc {
    zinject -a
}



#create_pool



TEST_ITERATION=1

sequential_sync_writes() {
	export NUM_JOBS='16 32'
	export BLOCK_SIZES='8k 1m'
	if [ "$1" == "ext4" ]; then
		DIRECTORY=${EXT4_MOUNTDIR}
	elif [ "$1" == "zfs" ]; then
		DIRECTORY=${ZFS_MOUNTDIR}
	elif [ "$1" == "shielded_zfs" ]; then
		DIRECTORY=${SHIELDED_ZFS_MOUNTDIR}
	fi

	# sequential sync write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))
			#reset_pool
			if [ "$1" == "ext4" ]; then
				cleanup_ext4
				sleep 20
				setup_ext4
			elif [ "$1" == "zfs" ]; then
				cleanup_zfs
				sleep 20
				setup_zfs
			elif [ "$1" == "shielded_zfs" ]; then
				cleanup_shielded_zfs
				sleep 20
				setup_shielded_zfs
			fi
			for i in $(seq 1 $TEST_ITERATION)
			do
				echo "[!] Running Sequential Sync Write in "$1""
				echo "[!] BS: $BLOCKSIZE"
				echo "[!] Num jobs: $NUMJOBS"
				fio sequential_sync_writes.fio --output-format=${FIO_FORMAT} --output="${RESULTS_DIR}/seq_sync_write_$1.bs-$bs.thread-$thread.run-$i.json"
			done
		done
	done

	# sequential sync write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))
			bw=""
			iops=""
			touch  ${RESULTS_DIR}/seq_sync_write_$1.txt
			for i in $(seq 1 $TEST_ITERATION)
			do
				bw_value=$(jq '.jobs[0].write.bw' "${RESULTS_DIR}/seq_sync_write_$1.bs-$bs.thread-$thread.run-$i.json")
				iops_value=$(jq '.jobs[0].write.iops' "${RESULTS_DIR}/seq_sync_write_$1.bs-$bs.thread-$thread.run-$i.json")
				bw+="$bw_value"
				iops+="$iops_value"
			done
			echo "[!] Running Sequential Sync Write in "$1"" >> ${RESULTS_DIR}/seq_sync_write_$1.txt
			echo "Block size, Num jobs, Throughput (KiB/s), IOPS" >> ${RESULTS_DIR}/seq_sync_write_$1.txt
			echo "$BLOCKSIZE, $NUMJOBS, $bw, $iops" >> ${RESULTS_DIR}/seq_sync_write_$1.txt
	
		done
	done
}

sequential_async_writes() {
	export NUM_JOBS='16 32'
	export BLOCK_SIZES='8k 1m'
	# sequential async write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))	
			reset_pool
			echo "[!] Running Sequential Async Write"
			echo "[!] BS: $BLOCKSIZE"
			echo "[!] Num jobs: $NUMJOBS"
			fio sequential_async_writes.fio --output-format=${FIO_FORMAT} --output="${RESULTS_DIR}/seq_async_write.bs-$bs.thread-$thread.run-$i.json"
		done
	done
}

random_sync_writes() {
	export NUM_JOBS='32 128'
	export BLOCK_SIZES='8k'

	# random sync write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))
			reset_pool
			echo "[!] Running Random Sync Write"
			echo "[!] BS: $BLOCKSIZE"
			echo "[!] Num jobs: $NUMJOBS"
			fio random_sync_writes.fio --output-format=${FIO_FORMAT} --output="${RESULTS_DIR}/random_sync_write.bs-$bs.thread-$thread.run-$i.json"
		done
	done
}

random_async_write() {
	export NUM_JOBS='32 128'
	export BLOCK_SIZES='8k'
	# random async write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))
			reset_pool
			echo "[!] Running Random Async Write"
			echo "[!] BS: $BLOCKSIZE"
			echo "[!] Num jobs: $NUMJOBS"
			fio random_async_writes.fio --output-format=${FIO_FORMAT} --output="${RESULTS_DIR}/random_async_write.bs-$bs.thread-$thread.run-$i.json"
		done
	done
}

# Run experiments
run_fio() {
	for i in $(seq 1 $TEST_ITERATION)
	do
		
		sequential_sync_writes

		sequential_async_writes
		
		random_sync_writes

		random_async_writes

	done
	clean_pool
}

# Show results
collect_results() {
	export NUM_JOBS='16 32'
	export BLOCK_SIZES='8k 1m'

	# sequential sync write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))
			bw=""
			iops=""
			for i in $(seq 1 $TEST_ITERATION)
			do
				echo "[!] Running Sequential Sync Write"
				echo "[!] BS: $BLOCKSIZE"
				echo "[!] Num jobs: $NUMJOBS"
				bw_value=$(jq '.jobs[0].write.bw' "${RESULTS_DIR}/seq_sync_write.bs-$bs.thread-$thread.run-$i.json")
				iops_value=$(jq '.jobs[0].write.iops' "${RESULTS_DIR}/seq_sync_write.bs-$bs.thread-$thread.run-$i.json")
				bw+="$bw_value, "
				iops+="$iops_value, "
			done
			echo "[!] Throughput (KiB/s): $bw"
			echo "[!] IOPS: $iops"
		done
	done

	# sequential async write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))	
			bw=""
			iops=""
			for i in $(seq 1 $TEST_ITERATION)
			do
				echo "[!] Running Sequential Async Write"
				echo "[!] BS: $BLOCKSIZE"
				echo "[!] Num jobs: $NUMJOBS"
				bw_value=$(jq '.jobs[0].write.bw' "${RESULTS_DIR}/seq_async_write.bs-$bs.thread-$thread.run-$i.json")
				iops_value=$(jq '.jobs[0].write.iops' "${RESULTS_DIR}/seq_async_write.bs-$bs.thread-$thread.run-$i.json")
				bw+="$bw_value, "
				iops+="$iops_value, "
			done
			echo "[!] Throughput (KiB/s): $bw"
			echo "[!] IOPS: $iops"		
		done	
	done

	export NUM_JOBS='32 128'
	export BLOCK_SIZES='8k'

	# random sync write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))
			bw=""
			iops=""
			for i in $(seq 1 $TEST_ITERATION)
			do
				echo "[!] Running Random Sync Write"
				echo "[!] BS: $BLOCKSIZE"
				echo "[!] Num jobs: $NUMJOBS"
				bw_value=$(jq '.jobs[0].write.bw' "${RESULTS_DIR}/random_sync_write.bs-$bs.thread-$thread.run-$i.json")
				iops_value=$(jq '.jobs[0].write.iops' "${RESULTS_DIR}/random_sync_write.bs-$bs.thread-$thread.run-$i.json")
				bw+="$bw_value, "
				iops+="$iops_value, "
			done
			echo "[!] Throughput (KiB/s): $bw"
				echo "[!] IOPS: $iops"	
		done
	done

	# random async write
	for thread in $NUM_JOBS; do
		for bs in $BLOCK_SIZES; do
			export BLOCKSIZE=$bs
			export NUMJOBS=$thread
			export FILESIZE=$((TOTALSIZE/NUMJOBS))
			bw=""
			iops=""
			for i in $(seq 1 $TEST_ITERATION)
			do
				echo "[!] Running Random Async Write"
				echo "[!] BS: $BLOCKSIZE"
				echo "[!] Num jobs: $NUMJOBS"
				bw_value=$(jq '.jobs[0].write.bw' "${RESULTS_DIR}/random_async_write.bs-$bs.thread-$thread.run-$i.json")
				iops_value=$(jq '.jobs[0].write.iops' "${RESULTS_DIR}/random_async_write.bs-$bs.thread-$thread.run-$i.json")
				bw+="$bw_value, "
				iops+="$iops_value, "
			done	
			echo "[!] Throughput (KiB/s): $bw"
			echo "[!] IOPS: $iops"
		done	
	done
}


setup_ext4() {
	sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=$(echo "$DISKS" | awk '{print NF}') $DISKS
    sudo mkdir -p ${EXT4_MOUNTDIR}
    sudo mkfs.ext4 -F /dev/md0
    sudo mount /dev/md0 ${EXT4_MOUNTDIR}
}

cleanup_ext4() {
    echo "disks are: $DISKS"
    sudo umount ${EXT4_MOUNTDIR}
    sudo rm -rf ${EXT4_MOUNTDIR}
    sudo mdadm --stop /dev/md0
    sudo mdadm --zero-superblock /dev/md0
    sudo wipefs -a $DISKS
}

unmount_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/original_zfs"
    cd ${ZFS_DIR}

    sudo ./scripts/zfs.sh -u
    sudo make uninstall > /dev/null ; sudo ldconfig > /dev/null; sudo depmod
    make clean && export list="$(find -name .deps)" && for elem in $list; do sudo rm -rf $elem; done && sudo rm -rf __pycache__/ aclocal.m4 build/ config.log config.status  configure libtool stamp-h1 zfs_config.h.in zfs_config.h Makefile.in Makefile zfs.release configure~ zfs_config.h.in~ > /dev/null
    cd ${CUR_DIR}
    sudo wipefs -a $DISKS
}


unmount_shielded_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/zfs"
    cd ${ZFS_DIR}

    sudo ./scripts/zfs.sh -u
    sudo make uninstall > /dev/null ; sudo ldconfig; sudo depmod
    make clean && export list="$(find -name .deps)" && for elem in $list; do sudo rm -rf $elem; done && sudo rm -rf __pycache__/ aclocal.m4 build/ config.log config.status  configure libtool stamp-h1 zfs_config.h.in zfs_config.h Makefile.in Makefile zfs.release configure~ zfs_config.h.in~ > /dev/null
    cd ${CUR_DIR}
    sudo wipefs -a $DISKS
}

setup_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/original_zfs"
    cd ${ZFS_DIR}
    sh autogen.sh > /dev/null && ./configure  > /dev/null && make -s -j > /dev/null
    sudo make install > /dev/null && sudo ldconfig && sudo depmod && sudo ./scripts/zfs.sh 
    cd ${CUR_DIR}
    sudo zpool create -f zpool-mount -m ${ZFS_MOUNTDIR} ${DISKS}
}

setup_shielded_zfs() {
    CUR_DIR=$(pwd)
    ZFS_DIR="/home/azureuser/zfs"
    cd ${ZFS_DIR}
    sh autogen.sh && ./configure && make -s -j
    sudo make install && sudo ldconfig && sudo depmod && sudo ./scripts/zfs.sh
    cd ${CUR_DIR}
    sudo zpool create -f zpool-mount -m ${SHIELDED_ZFS_MOUNTDIR} ${DISKS}
}


cleanup_shielded_zfs() {
    echo "disks are: $DISKS"
    sudo zpool destroy zpool-mount
    sudo rm -rf ${SHIELDED_ZFS_MOUNTDIR}
	unmount_shielded_zfs
    sudo wipefs -a $DISKS
}

cleanup_zfs() {
    echo "disks are: $DISKS"
    sudo zpool destroy zpool-mount
    sudo rm -rf ${ZFS_MOUNTDIR}
	unmount_zfs
    sudo wipefs -a $DISKS
}

find_disks
setup_folder
mkdir -p $RESULTS_DIR
echo "*** ext4 ***"
cleanup_ext4
sleep 20
#setup_ext4
#sequential_sync_writes ext4
#cleanup_ext4
sleep 20

echo "*** zfs ***"
sleep 20
#setup_zfs
sequential_sync_writes zfs
cleanup_zfs
#sleep 20

echo "*** shielded zfs ***"
sleep 20
setup_shielded_zfs
sequential_sync_writes shielded_zfs
cleanup_shielded_zfs
sleep 20


#echo "*** gathering results ... ***"
