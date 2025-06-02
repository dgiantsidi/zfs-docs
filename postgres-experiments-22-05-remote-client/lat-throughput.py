import matplotlib.pyplot as plt
import numpy as np

# Sample data for latency and throughput
latency_ext4 = [
    10.42,  # prev_latency: 10.46, 
    13.92333333, # prev_latency: 14.78,
    25.12333333, # prev_latency: 26.96,
    29.95666667 # prev_latency: 30.52
]

throughput_ext4 = [
    959.5833333, # prev_throughput: 955.69,
    1436.47, # prev_throughput: 1352.83,
    1990.46, #prev_throughput: 1854.7,
    2003.39 # prev_throughput: 1965.87,
]

clients = [
    10,
    20,
    50,
    60
]

latency_default_zfs = [
    13.16,
    17.88,
    31.9,
    36.66
]

throughput_default_zfs = [
    760.04,
    1118.28,
    1566.97,
    1636.67
]

latency_shielded_zfs = [
    13.16,
    18,
    31.99,
    37.75
]

throughput_shielded_zfs =[
    759.62,
    1111,
    1562.86,
    1589.42
]



# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(throughput_shielded_zfs, latency_shielded_zfs, marker='X', label="shielded-zfs (no CCF)")
plt.plot(throughput_default_zfs, latency_default_zfs, marker='^', label="zfs-default")
plt.plot(throughput_ext4, latency_ext4, marker='1', label="ext4")



# Add text on top of the data points
for i in range(len(throughput_shielded_zfs)):
    plt.text(throughput_shielded_zfs[i], latency_shielded_zfs[i], f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(throughput_default_zfs)):
    plt.text(throughput_default_zfs[i], latency_default_zfs[i],  f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(throughput_ext4)):
    plt.text(throughput_ext4[i], latency_ext4[i], f'({clients[i]})', fontsize=9, ha='right')
 

# Add title and labels
plt.title('Throughput vs latency (TPC-C with 10 W over postgres)')
plt.xlabel('tps')
plt.ylabel('Latency (ms)')

# Show grid
plt.legend(loc="upper left")

plt.grid(True)
plt.savefig('latency_throughput_plot.png')

# Show the plot
plt.show()