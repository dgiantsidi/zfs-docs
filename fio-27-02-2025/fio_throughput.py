import matplotlib.pyplot as plt
import numpy as np

## Sequential synchronous writes

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



## Seq asynchronous writes

throughput_ext4_seq_async_write = [
  183605,
  752075,
  183647,
  752114
]

throughput_zfs_default_seq_async_write = [
    754282,
    755611,
    751959,
    742352
]

throughput_zfs_500us_seq_async_write = [
    754355,
    744833,
    640078,
    746295
]

throughput_zfs_1ms_seq_async_write = [
    755997,
    749193,
    632666,
    741999 
]

x_axis_seq_async_writes = [
    "8K_16Jobs",
    "1M_16Jobs",
    "8K_32Jobs",
    "1m_32Jobs",
]
n = len(throughput_ext4_seq_async_write)
x = np.arange(n)
width = 0.2


# Create a plot
plt.figure(figsize=(10, 6))
#plt.errorbar(latency, throughput, xerr=latency_error, yerr=throughput_error, fmt='o', ecolor='r', capsize=5)
plt.bar(x-2*width, throughput_ext4_seq_async_write, width=width, label="ext4")
plt.bar(x-width, throughput_zfs_default_seq_async_write, width=width, label="zfs-default")
plt.bar(x, throughput_zfs_500us_seq_async_write, width=width, label="zil-delay-500us")
plt.bar(x+width,  throughput_zfs_1ms_seq_async_write, width=width, label="zil-delay-1ms")



# Add title and labels
plt.title('fio (sequential asynchronous writes)')
plt.ylabel('KiB/s (Max: 750 MB/s)')
plt.xticks(x, x_axis_seq_sync_writes)


# Show grid
plt.legend(loc="upper left")

plt.grid(True)
plt.savefig('seq_async_writes_fio_throughput_plot.png')


## Random synchronous writes

throughput_ext4_rand_sync_write = [
  28933,
  86534
]

throughput_zfs_default_rand_sync_write = [
   21171,
   61481
]

throughput_zfs_500us_rand_sync_write = [
  24329,
  59038
]

throughput_zfs_1ms_rand_sync_write = [
  20831,
  54960
]

x_axis_rand_sync_writes = [
    "8K_32Jobs",
    "8K_128Jobs"
]

n = len(throughput_ext4_rand_sync_write)
x = np.arange(n)
width = 0.2


# Create a plot
plt.figure(figsize=(10, 6))
#plt.errorbar(latency, throughput, xerr=latency_error, yerr=throughput_error, fmt='o', ecolor='r', capsize=5)
plt.bar(x-2*width, throughput_ext4_rand_sync_write, width=width, label="ext4")
plt.bar(x-width, throughput_zfs_default_rand_sync_write, width=width, label="zfs-default")
plt.bar(x, throughput_zfs_500us_rand_sync_write, width=width, label="zil-delay-500us")
plt.bar(x+width,  throughput_zfs_1ms_rand_sync_write, width=width, label="zil-delay-1ms")



# Add title and labels
plt.title('fio (random synchronous writes)')
plt.ylabel('KiB/s (Max: 750 MB/s)')
plt.xticks(x, x_axis_rand_sync_writes)


# Show grid
plt.legend(loc="upper left")

plt.grid(True)
plt.savefig('rand_sync_writes_fio_throughput_plot.png')