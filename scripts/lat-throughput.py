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



# Example standard deviations
latency_ext4_stdev = [
    2.109802518,
    2.188825789,
    2.68418827,
    2.381419395
]

throughput_ext4_stdev = [
    140.4561807,
    169.8792352,
    188.9855772,
    154.845375
]

latency_default_zfs_stdev = [
    2.474947811,
    2.260905055,
    2.546479596,
    2.429284874
]

throughput_default_zfs_stdev = [
    137.9327528,
    155.5306509,
    142.5215317,
    125.7470596
]

latency_shielded_zfs_stdev = [
    2.27428377,
    2.087125216,
    1.875053333,
    2.335842104
]

throughput_shielded_zfs_stdev = [
    118.7437624,
    131.7191272,
    95.67615847,
    116.1841103
]




# Create a plot
plt.figure(figsize=(10, 6))
plt.errorbar(throughput_shielded_zfs, latency_shielded_zfs, xerr=throughput_shielded_zfs_stdev, yerr=latency_shielded_zfs_stdev, marker='X', label="shielded-zfs (no CCF)")
plt.errorbar(throughput_default_zfs, latency_default_zfs, xerr=throughput_default_zfs_stdev, yerr=latency_default_zfs_stdev, marker='^', label="zfs-default")
plt.errorbar(throughput_ext4, latency_ext4, xerr=throughput_ext4_stdev, yerr=latency_ext4_stdev, marker='1', label="ext4")



# Add text on top of the data points
for i in range(len(throughput_shielded_zfs)):
    plt.text(throughput_shielded_zfs[i], latency_shielded_zfs[i], f'({clients[i]}, ±{latency_shielded_zfs_stdev[i]:.2f}ms, ±{throughput_shielded_zfs_stdev[i]:.1f} TPS)',fontsize=9, ha='right'
)

for i in range(len(throughput_default_zfs)):
    plt.text(throughput_default_zfs[i], latency_default_zfs[i],  f'({clients[i]})', fontsize=9, ha='right')

for i in range(len(throughput_ext4)):
    plt.text(throughput_ext4[i], latency_ext4[i], f'({clients[i]})', fontsize=9, ha='right')
 


stats_text = f"""
tps slowdown %:
 - zfs w.r.t. ext4: 7-12% 
 - shielded-zfs w.r.t. zfs: 3-5%

latency slowdown %:
 - zfs w.r.t. ext4: 7-13% 
 - shielded-zfs w.r.t. zfs: 3-5%

"""

# Add statistics text box
plt.gcf().text(0.02, 0.6, stats_text, fontsize=9, va='center', bbox=dict(facecolor='white', alpha=1))



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