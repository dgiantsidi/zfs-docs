import matplotlib.pyplot as plt
import numpy as np
from datetime import date


today = date.today()

date_string = today.strftime("%Y-%m-%d")
clients = [
    10,
    20,
    50,
    60
]

# data
latency_zfs = [13.20,  17.47, 29.31, 31.28]
throughput_zfs = [757.64, 1144.59, 1705.83, 1917.97]

latency_szfs = [13.28, 17.10, 29.26, 31.41]
throughput_szfs = [752.90, 1169.50, 1708.38, 1909.79]

# Plot
plt.figure(figsize=(8, 6))

plt.plot(throughput_zfs, latency_zfs, 'o-', label='Shielded ZFS', color='blue')
plt.plot(throughput_szfs, latency_szfs, 's--', label='Shielded ZFS w/ acked cmts from userspace', color='green')

# Add text on top of the data points
for i in range(len(latency_szfs)):
    plt.text(throughput_szfs[i], latency_szfs[i], f'({clients[i]}, {100*((latency_szfs[i] - latency_zfs[i])/latency_zfs[i]):.2f}%)',fontsize=9, ha='right'
)

title = f'TPC-C with 10 W over postgres ({date_string})'
# Add title and labels
plt.title(title)
plt.xlabel('TPS')
plt.ylabel('Latency (ms)')
# Show grid
plt.legend(loc="upper left")

plt.grid(True)
plt.savefig('latency_throughput_plot_'+date_string+'.png')
