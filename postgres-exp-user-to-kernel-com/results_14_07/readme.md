# Readme

In this directory zfs refers to shielded zfs w/o cmts acknowledgement and zfs_acks refers to shielded zfs with cmts acknowledgements.


## Microbenchmarks results

| Filesystem | Avg Latency (ms) | Threads | no of synchronous writes | Total execution time (seconds) |
|------------|------------------|-------------------|----------------|----------------------|
| shielded zfs        |  3.1875       | 64    (approx 25% CPU util)  |    50K       | 159.4436 |
| shielded zfs w/ user-space cmts acks       |    3.4304     | same     | 50K          |    171.6010   |


*~7%* performance degradation
