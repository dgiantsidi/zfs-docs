# Readme

In this directory zfs refers to shielded zfs w/o cmts acknowledgement and zfs_acks refers to shielded zfs with cmts acknowledgements from user-space (no delay).


## Microbenchmarks results

| Filesystem | Avg Latency (ms) | Threads | no of synchronous writes | Total execution time (seconds) |
|------------|------------------|-------------------|----------------|----------------------|
| shielded zfs        |  3.1875 / 3.0138      | 64    (approx 25% CPU util)  |    50K       | 159.4436 / 150.7412 |
| shielded zfs w/ user-space cmts acks       |    3.4304 / 3.2247     | same     | 50K          |    171.6010 / 161.30   |


*~7%* performance degradation
