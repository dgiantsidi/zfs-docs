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

# Sample data for latency and throughput
latency_ext4 = [
    12.38,
    16.0975,
    26.66,
    30.3825
]

throughput_ext4 = [
   825.495,
   1259.465,
   1889.48,
   1983.6775
]



latency_default_zfs = [
   13.645,
   17.3075,
   30.2325,
   34.3825
]

throughput_default_zfs = [
   751.3825,
   1170.445,
   1662.33,
   1751.31
]

latency_shielded_zfs = [
    14.025,
    17.9825,
    31.6475,
    35.3975
]

throughput_shielded_zfs =[
   727.375,
   1123.39,
   1583.685,
   1700.5775
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
 
title = f'TPC-C with 10 W over postgres ({date_string})'
# Add title and labels
plt.title(title)
plt.xlabel('TPS')
plt.ylabel('Latency (ms)')

# Show grid
plt.legend(loc="upper left")

plt.grid(True)
plt.savefig('latency_throughput_plot_'+date_string+'.png')

# Show the plot
plt.show()