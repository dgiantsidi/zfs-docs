# How to build

1. `cd CCF/getting_started/setup_vm` or `cd CCF-bench/getting_started/setup_vm`

2. `sudo -E ./run.sh ccf-dev.yml --extra-vars "platform=virtual" --extra-vars "clang_version=15"`

3. `mkdir build && cd build`

4. `cmake -GNinja -DCOMPILE_TARGET=virtual ..` . You may add ``` -DUSE_AUTHENTICATOR=1``` for message integrity

5. `ninja`

6. `sudo ninja install`


# How to run

1. `../tests/sandbox/sandbox.sh -p samples/apps/logging/liblogging.virtual.so  -v -n local://127.0.0.1 -n local://127.0.0.
2 -n local://127.0.0.3`


# Evaluation

### Code:
  We extended raft_driver.cpp in [link](https://github.com/dgiantsidi/CCF-bench), (tag=ccf-6.0.0-dev4). We need `g++/gcc --version 9.4.0`
  
  **Cmd to run**: `./raft_driver` and then the process id, e.g., 0 or 1. 

### Experiment 1: 2 VMs (no failures)

| VMs   | CCF w/ sha256 | CCF (native) | netperf | latency_bench w/ sha256 | latency_bench (native) |
|---|---|---|---|---|---|
| R-VMs (acc)  | **tput**=6051.04 op/s, **latency**=0.165 ms| **tput**=6542.3004 op/s, **latency**=0.1528ms| **tput**=8678.294 op/s, **latency**=0.115ms |**tput**=6935 op/s **latency**=0.1441 ms|**tput**=8181.94 ops, **latency**=0.122 ms |
| CVMs (w/o acc) |  **tput**=3741.8 op/s, **latency**=0.267 ms | **tput**=3931.4 op/s, **latency**=0.254 ms | **tput**=4567.294 op/s, **latency**=0.218ms | **tput**=4321.8 op/s, **latency**=0.231 ms| **tput**= 4364.947 op/s, **latency**= 0.2290 ms|

Notes on the code/implementation:
- send msg (leader) = 114B (w/o any data)
- recv msg (leader) = 33B (ACKs)
- ledger implemented as a vector of entries and grows infinitely
- latency_bench: 1e6 txs (Request/Response), 64B msg_sz


### Experiment 2: QUIC protocol 2 VMs

| VMs   |  latency  |
|---|---|
| R-VMs (acc)  | **latency**=107569 ns ( approx 0.107 ms)|
