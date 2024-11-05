# 

`cd CCF/getting_started/setup_vm`

`sudo -E ./run.sh ccf-dev.yml --extra-vars "platform=virtual" --extra-vars "clang_version=15"`

`mkdir build && cd build`

`cmake -GNinja -DCOMPILE_TARGET=virtual ..`

`ninja`

`sudo ninja install`

`../tests/sandbox/sandbox.sh -p samples/apps/logging/liblogging.virtual.so  -v -n local://127.0.0.1 -n local://127.0.0.
2 -n local://127.0.0.3`
