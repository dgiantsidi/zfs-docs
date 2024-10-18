import matplotlib.pyplot as plt
import numpy as np

# Data from your file
from latencies import latencies


# Extracting latency types and delays
latency_types = ['min', 'avg', '95th percentile']
delays = list(latencies.keys())

# Preparing data for plotting
latency_data = {latency_type: [latencies[delay][latency_type] for delay in delays] for latency_type in latency_types}

# Number of bars per group
n_bars = len(latency_types)
bar_width = 0.2

# Positions of the bars on the x-axis
r = np.arange(len(delays))
positions = [r + i * bar_width for i in range(n_bars)]

# Plotting latency
plt.figure(figsize=(12, 6))

for i, latency_type in enumerate(latency_types):
    bars = plt.bar(positions[i], latency_data[latency_type], width=bar_width, label=latency_type)
    # Annotating the values on each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

plt.title('Latency (ms) across different delays (for commitments/rollback)')
#plt.xlabel('Delay')
plt.ylabel('Milliseconds')
plt.xticks([r + bar_width for r in range(len(delays))], delays)
plt.legend()
plt.tight_layout()
plt.show()