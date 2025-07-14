# Readme

In this directory zfs refers to shielded zfs w/o cmts acknowledgement and zfs_acks refers to shielded zfs with cmts acknowledgements from user-space (no delay).


## Microbenchmarks results

| Filesystem | Avg Latency (ms) | Threads | no of synchronous writes | Total execution time (seconds) |
|------------|------------------|-------------------|----------------|----------------------|
| shielded zfs        |  3.19 / 3.01 / 3.15      | 64    (approx 25% CPU util)  |    50K       | 159.44 / 150.74 / 157.56 |
| shielded zfs w/ user-space cmts acks       |    3.43 / 3.22 / 3.53     | same     | 50K          |    171.60 / 161.30  / 176.92 |


*~7%* performance degradation
