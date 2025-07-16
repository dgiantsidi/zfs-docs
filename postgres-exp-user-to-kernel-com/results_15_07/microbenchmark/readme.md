# Readme

In this directory zfs refers to shielded zfs w/o cmts acknowledgement, zfs_acks refers to shielded zfs with cmts acknowledgements from user-space (no delay) and zfs_acks_delay* refers to shielded zfs with cmts acknowledgements from user-space with mocked CCF-delay.


## Microbenchmarks results

| Filesystem | Avg Latency (ms) | Threads | no of synchronous writes | Total execution time (seconds) |
|------------|------------------|-------------------|----------------|----------------------|
| shielded zfs        |  3.0252      | 64    (approx 25% CPU util)  |    100K       | 302.5920 |
| shielded zfs w/ user-space cmts acks       |   3.2022     | same     | 100K          |    320.3760 |
| shielded zfs w/ user-space cmts acks (delay 0.5ms)       |    3.9742    | approx 10% CPU util    | 100K          |   397.5571 |



We found that:

*~6%* performance degradation of `shielded zfs w/ user-space cmts acks` and `shielded zfs`

*~31%* performance degradation of `shielded zfs w/ user-space cmts acks (delay 0.5ms)` and `shielded zfs`

