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
    12.37428571,
    15.83142857,
    25.91428571,
    29.51857143
]

throughput_ext4 = [
   824.5485714,
   1281.358571,
   1943.417143,
   2045.984286
]



latency_default_zfs = [
   13.83,
   17.55571429,
   29.97571429,
   34.26428571
]

throughput_default_zfs = [
   737.9642857,
   1151.477143,
   1675.007143,
   1755.99
]

latency_shielded_zfs = [
    14.26857143,
    18.27428571,
    31.41428571,
    35.37142857
]

throughput_shielded_zfs =[
   713.3842857,
   1103.5,
   1595.814286,
   1700.992857
]



# Example standard deviations
latency_ext4_stdev = [
    1.865831871,
    2.019310349,
    2.424354602,
    2.568530245
]

throughput_ext4_stdev = [
    128.543507,
    168.3840208,
    180.3628634,
    185.5836392
]

latency_default_zfs_stdev = [
    2.088715714,
    1.942299815,
    2.140964402,
    2.017918541
]

throughput_default_zfs_stdev = [
    116.6560601,
    132.4175178,
    121.3645533,
    104.5007614
]

latency_shielded_zfs_stdev = [
    2.011628102,
    1.775676933,
    1.79579005,
    2.039439699
]

throughput_shielded_zfs_stdev = [
    104.5845618,
    111.1082874,
    93.51135829,
    100.3279788
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
 - zfs w.r.t. ext4: 7-13% 
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