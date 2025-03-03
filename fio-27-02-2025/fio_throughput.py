import matplotlib.pyplot as plt
import numpy as np


throughput_ext4_seq_sync_write = [
    19338,
    735718,
    34937,
    723037
]

throughput_zfs_default_seq_sync_write = [
    31876,
    748179,
    45990,
    747127
]

throughput_zfs_500us_seq_sync_write = [
    25830,
    747409,
    39729,
    742435
]

throughput_zfs_1ms_seq_sync_write = [
    23891,
    748005,
    33836,
    746223
]

x_axis_seq_sync_writes = [
    "8K_16Jobs",
    "1M_16Jobs",
    "8K_32Jobs",
    "1m_32Jobs",
]


# Create a plot
plt.figure(figsize=(10, 6))
#plt.errorbar(latency, throughput, xerr=latency_error, yerr=throughput_error, fmt='o', ecolor='r', capsize=5)
plt.plot(throughput_ext4_seq_sync_write, x_axis_seq_sync_writes,  marker='o', label="ext4")
plt.plot(throughput_zfs_default_seq_sync_write, x_axis_seq_sync_writes,  marker='o', label="zfs-default")
plt.plot(throughput_zfs_500us_seq_sync_write, x_axis_seq_sync_writes,  marker='o', label="zil-delay-500us")
plt.plot(throughput_zfs_1ms_seq_sync_write, x_axis_seq_sync_writes,  marker='o', label="zil-delay-1ms")



# Add title and labels
plt.title('fio)')
plt.xlabel('KiB/s (Max: 750 MB/s)')


# Show grid
plt.legend(loc="upper left")

plt.grid(True)
plt.savefig('seq_sync_writes_fio_throughput_plot.png')

# Show the plot
plt.show()