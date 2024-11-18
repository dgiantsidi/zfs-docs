# How to build

1. `cd CCF/getting_started/setup_vm` or `cd CCF-bench/getting_started/setup_vm`

2. `sudo -E ./run.sh ccf-dev.yml --extra-vars "platform=virtual" --extra-vars "clang_version=15"`

3. `mkdir build && cd build`

4. `cmake -GNinja -DCOMPILE_TARGET=virtual ..`

5. `ninja`

6. `sudo ninja install`


# How to run

1. `../tests/sandbox/sandbox.sh -p samples/apps/logging/liblogging.virtual.so  -v -n local://127.0.0.1 -n local://127.0.0.
2 -n local://127.0.0.3`
