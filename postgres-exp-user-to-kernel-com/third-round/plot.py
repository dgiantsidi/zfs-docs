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
latency_zfs = [16.54,  19.98, 31.69, 34.09]
throughput_zfs = [604.61, 1000.67, 1577.67, 1759.90]

latency_szfs = [16.50, 20.12, 32.10, 34.44]
throughput_szfs = [606.17, 993.87, 1557.39, 1741.99]

# Plot
plt.figure(figsize=(8, 6))

plt.plot(throughput_zfs, latency_zfs, 'o-', label='ZFS', color='blue')
plt.plot(throughput_szfs, latency_szfs, 's--', label='Shielded ZFS', color='green')

# Add text on top of the data points
for i in range(len(latency_szfs)):
    plt.text(throughput_szfs[i], latency_szfs[i], f'({clients[i]}, ({100*((latency_szfs[i] - latency_zfs[i])/latency_zfs[i])})%)',fontsize=9, ha='right'
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