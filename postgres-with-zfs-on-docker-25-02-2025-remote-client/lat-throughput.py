import matplotlib.pyplot as plt
import numpy as np

# Sample data for latency and throughput
latency_500us = [
    13.13666667, # 10 clients
    16.98333333, # 20 clients
    28.97333333, # 50 clients
    33.45666667, # 60 clients
    48.27666667  # 90 clients
]

throughput_500us = [
    761.2166667,
    1177.87,
    1725.93,
    1793,
    1865.62
]


# Sample data for latency and throughput
latency_1ms = [
    13.72, # 10 clients
    18.12333333,
    34.03,
    39.75,
    57.54
]

throughput_1ms = [
    728.8466667,
    1103.856667,
    1469.023333,
    1509.09,
    1563.2
]


latency_default = [
    12.47,
    15.79666667,
    28.02333333,
    34.8,
    50.8
]

throughput_default = [
    801.9166667,
    1269.796667,
    1797.94,
    1734.76,
    1791.866667
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
plt.plot( throughput_default, latency_default, marker='^', label="default")


# Add text on top of the data points
for i in range(len(latency_500us)):
    plt.text(throughput_500us[i], latency_500us[i], f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(latency_1ms)):
    plt.text(throughput_1ms[i],latency_1ms[i],  f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(latency_default)):
    plt.text( throughput_default[i], latency_default[i], f'({clients[i]})', fontsize=9, ha='right')

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