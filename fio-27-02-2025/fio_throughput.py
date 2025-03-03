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
n = len(throughput_ext4_seq_sync_write)
x = np.arange(n)
width = 0.2


# Create a plot
plt.figure(figsize=(10, 6))
#plt.errorbar(latency, throughput, xerr=latency_error, yerr=throughput_error, fmt='o', ecolor='r', capsize=5)
plt.bar(x-2*width, throughput_ext4_seq_sync_write, width=width, label="ext4")
plt.bar(x-width, throughput_zfs_default_seq_sync_write, width=width, label="zfs-default")
plt.bar(x, throughput_zfs_500us_seq_sync_write, width=width, label="zil-delay-500us")
plt.bar(x+width,  throughput_zfs_1ms_seq_sync_write, width=width, label="zil-delay-1ms")



# Add title and labels
plt.title('fio (sequential synchronous writes)')
plt.ylabel('KiB/s (Max: 750 MB/s)')
plt.xticks(x, x_axis_seq_sync_writes)


# Show grid
plt.legend(loc="upper left")

plt.grid(True)
plt.savefig('seq_sync_writes_fio_throughput_plot.png')

# Show the plot
plt.show()