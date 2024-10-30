# Measuring latency between two VMs

- `ping`
  -  `ping -c 100 10.1.0.5` (100 packets of 64 bytes)
  -  `ping -c 100 10.1.0.4 -i 0.002` (set interval to 2ms)

- `netperf`
  - `netperf -H 10.1.0.4 -t TCP_RR -r 64 -b 1 -v 2 -f g -- -O min_latency,mean_latency,max_latency,stddev_latency,transaction_rate`

# References
- What a trip! Measuring network latency in the cloud (https://cloud.google.com/blog/products/networking/using-netperf-and-ping-to-measure-network-latency)

# Results
| VMs   | `ping` (ms) | `netperf` (ms) |
|---|---|---|
| CVMs (test1)   |  min=0.487, avg=0.781, max=2.115, mdev=0.390 w/ interval = 1 (1s) |  cannot set interval for netperf w/ package manager |
| CVMs  (test2) | min=0.179, avg=**0.318**, max=0.986, mdev=0.159 w/ interval = 0.002 (2ms) | min=0.141, avg=**0.358**, max=4.673, mdev=0.26, (tran/s=2778/s) | 
| R-VMs  |   |   |
