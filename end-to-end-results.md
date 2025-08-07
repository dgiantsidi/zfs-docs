### Performance Metrics Table

| Configuration                  | TPC-C (10W) Latency | TPC-C 10W) TPS | Microbenchmark Latency |
|-------------------------------|---------------------|------------------|-------------------------|
| Shielded ZFS w/ CCF           | 33.86 ms            | 1771             | 3.82 ms                 |
| Shielded ZFS w/ Quick server  | 34.92 ms            | 1717             | 3.60 ms                 |
| Shielded ZFS w/ local         | 33.30 ms            | 1801             | 3.40 ms                 |
| Shielded ZFS                  | 31.88 ms            | 1881             | 3.08 ms                 |
| ZFS                           | 30.64 ms            | 1957             | 2.15 ms                 |
