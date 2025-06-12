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
   12.58444444,
   15.88333333,
   25.88111111,
   29.44222222
]

throughput_ext4 = [
   808.1211111,
   1273.252222,
   1942.785556,
   2048.286667
]



latency_default_zfs = [
   14.08444444,
   17.76666667,
   30.05555556,
   34.29666667
]

throughput_default_zfs = [
   722.3555556,
   1135.707778,
   1669.028889,
   1753.138889
]

latency_shielded_zfs = [
    14.51888889,
    18.47111111,
    31.48444444,
    35.50222222
]

throughput_shielded_zfs =[
   699.1588889,
   1090.221111,
   1591.326667,
   1693.775556
]



# Example standard deviations
latency_ext4_stdev = [
    1.670068196,
    1.753745991,
    2.102845955,
    2.229634375
]

throughput_ext4_stdev = [
   116.0535314,
   146.8411276,
   156.379864,
   160.7901027
]

latency_default_zfs_stdev = [
   1.878104837,
   1.73511527,
   1.866722469,
   1.751328067
]

throughput_default_zfs_stdev = [
   105.671042,
   118.9560323,
   106.0717753,
   90.80525734
]

latency_shielded_zfs_stdev = [
    1.811756361,
    1.588147068,
    1.562770865,
    1.806230728
]

throughput_shielded_zfs_stdev = [
    94.87648582,
    99.83438016,
    81.53434154,
    88.98617773
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
 - zfs w.r.t. ext4: 10-14% 
 - shielded-zfs w.r.t. zfs: 3-5%

latency slowdown %:
 - zfs w.r.t. ext4: 11-16% 
 - shielded-zfs w.r.t. zfs: 3-5%

"""

# Add statistics text box
plt.gcf().text(0.1, 0.6, stats_text, fontsize=9, va='center', bbox=dict(facecolor='white', alpha=1))



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