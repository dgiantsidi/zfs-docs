### Performance Metrics Table

| Configuration                  | TPC-C (10w) Latency | TPC-C (10w) TPS | Microbenchmark Latency | Latency Slowdown vs ZFS (%) | TPS Slowdown vs ZFS (%) | Microbenchmark Slowdown vs ZFS (%) |
|-------------------------------|---------------------|------------------|-------------------------|------------------------------|--------------------------|-------------------------------------|
| Shielded ZFS w/ CCF           | 33.86 ms            | 1771             | 3.82 ms                 | 10.51%                       | 9.51%                   | 77.67%                              |
| Shielded ZFS w/ Quick server  | 34.92 ms            | 1717             | 3.60 ms                 | 13.97%                       | 12.26%                  | 67.44%                              |
| Shielded ZFS w/ local         | 33.30 ms            | 1801             | 3.40 ms                 | 8.69%                        | 7.98%                   | 58.14%                              |
| Shielded ZFS                  | 31.88 ms            | 1881             | 3.08 ms                 | 4.05%                        | 3.89%                   | 43.26%                              |
| ZFS                           | 30.64 ms            | 1957             | 2.15 ms                 | 0.00%                        | 0.00%                   | 0.00%                               |
