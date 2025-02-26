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
plt.plot(latency_500us, throughput_500us, marker='o')

# Add text on top of the data points
for i in range(len(latency_500us)):
    plt.text(latency_500us[i], throughput_500us[i], f'({clients[i]})', fontsize=9, ha='right')

# Add title and labels
plt.title('Latency vs Throughput (10 W)')
plt.xlabel('Latency (ms)')
plt.ylabel('tps')

# Show grid
plt.grid(True)
plt.savefig('latency_throughput_plot.png')

# Show the plot
plt.show()