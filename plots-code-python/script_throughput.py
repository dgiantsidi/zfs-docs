import matplotlib.pyplot as plt
import numpy as np

# Data from your file
from latencies import throughput

# Extracting delays and throughput data
delays = list(throughput.keys())
tps_values = [throughput[delay]['tps'] for delay in delays]
qps_values = [throughput[delay]['qps'] for delay in delays]
reads_values = [throughput[delay]['reads'] for delay in delays]
writes_values = [throughput[delay]['writes'] for delay in delays]
other_values = [throughput[delay]['other'] for delay in delays]

# Creating the first plot for TPS and QPS
fig, ax1 = plt.subplots(figsize=(8, 6))

# Plotting TPS
ax1.set_xlabel('Delay')
ax1.set_ylabel('TPS', color='tab:blue')
bars1 = ax1.bar(np.arange(len(delays)) - 0.2, tps_values, width=0.4, label='TPS', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Annotating TPS values
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

# Creating a second y-axis for QPS
ax2 = ax1.twinx()
ax2.set_ylabel('QPS', color='tab:green')
bars2 = ax2.bar(np.arange(len(delays)) + 0.2, qps_values, width=0.4, label='QPS', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

# Annotating QPS values
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

# Setting x-ticks and labels
plt.xticks(np.arange(len(delays)), delays)

# Adding title and legend
plt.title('Throughput (TPS and QPS) across different delays (for commitments/rollback)')
fig.tight_layout()

# Adding legends for both axes
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()

# Creating the second plot for stacked total_queries
fig, ax = plt.subplots(figsize=(8, 6))

# Plotting total_queries as stacked bars
bars3 = ax.bar(np.arange(len(delays)), reads_values, width=0.4, label='Reads', color='tab:orange')
bars4 = ax.bar(np.arange(len(delays)), writes_values, width=0.4, bottom=reads_values, label='Writes', color='tab:red')
bars5 = ax.bar(np.arange(len(delays)), other_values, width=0.4, bottom=np.array(reads_values) + np.array(writes_values), label='Other', color='tab:purple')

# Annotating total_queries values
for bar in bars5:
    yval = bar.get_height() + bar.get_y()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

# Setting x-ticks and labels
plt.xticks(np.arange(len(delays)), delays)

# Adding title and legend
plt.title('Total Queries (Reads, Writes, and Other) across different delays (for commitments/rollback)')
fig.tight_layout()
plt.legend(loc='upper left')

plt.show()