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

Cmd to run: `./raft_driver` and then 0 or 1. 

### Experiment 1: 2 VMs (no failures)

| VMs   | w/ sha256 | native | netperf |
|---|---|---|---|
| R-VMs (acc)  | **tput**=15084.9 op/s, **latency**=0.066 ms| | **tput**=11690.294 op/s, **latency**=0.085ms |
| R-VMs (w/o acc) |  | | |

Notes:
- send msg (leader) = 114B (w/o any data)
- recv msg (leader) = 33B (ACKs)
