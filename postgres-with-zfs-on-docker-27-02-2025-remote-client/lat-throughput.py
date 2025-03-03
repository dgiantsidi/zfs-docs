import matplotlib.pyplot as plt
import numpy as np

# Sample data for latency and throughput
latency_500us = [
    12.66,
    17.35,
    30.6,
    35.2,
    49.89
]

throughput_500us = [
    790.05,
    1152.8,
    1633.95,
    1704.24,
    1803.8

]


# Sample data for latency and throughput
latency_1ms = [
    13.41,
    18.11,
    31.68,
    35.8,
    51.56
]

throughput_1ms = [
    745.52,
    1104.22,
    1578.26,
    1675.88,
    1745.27
]


latency_default = [
    11.91,
    16.42,
    29.07,
    34.33,
    48.84
]

throughput_default = [
    839.49,
    1217.62,
    1720.1,
    1747.62,
    1842.54
]

latency_ext4 = [
    10.46, 
    14.78,
    26.96,
    30.52,
    43.43
]

throughput_ext4 = [
    955.69,
    1352.83,
    1854.7,
    1965.87,
    2072.01
]

clients = [
    10,
    20,
    50,
    60,
    90
]

# Sample data for error bars (standard deviation)
#latency_error = [
#
#]

#throughput_error = [
#
#]

# Create a plot
plt.figure(figsize=(10, 6))
#plt.errorbar(latency, throughput, xerr=latency_error, yerr=throughput_error, fmt='o', ecolor='r', capsize=5)
plt.plot(throughput_500us, latency_500us,  marker='o', label="fsync-delay-500us")
plt.plot(throughput_1ms, latency_1ms, marker='X', label="fsync-delay-1ms")
plt.plot( throughput_default, latency_default, marker='^', label="zfs-default")
plt.plot( throughput_ext4, latency_ext4, marker='1', label="ext4")



# Add text on top of the data points
for i in range(len(latency_500us)):
    plt.text(throughput_500us[i], latency_500us[i], f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(latency_1ms)):
    plt.text(throughput_1ms[i],latency_1ms[i],  f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(latency_default)):
    plt.text( throughput_default[i], latency_default[i], f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(latency_ext4)):
    plt.text( throughput_ext4[i], latency_ext4[i], f'({clients[i]})', fontsize=9, ha='right')   

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