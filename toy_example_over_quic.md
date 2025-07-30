# Toy kernel-module example with QUIC

## Documentation

We run one kernel module that produces numbers and cmts, a user-space process (i.e., the client) which queries the kernel about these cmts and sends them over QUIC to a server.

The user-space process has two threads, one for quering the kernel module (`thread_func_get_cmt`) and another one for submitting the reqs to the QUIC-server. 

## How to build

We work on the `commitments-protocol-dev` branch of the ngtcp2 repo.

1) ```sh
    git clone https://github.com/dgiantsidi/genltest && cd genltest && make && sudo insmod netlink_module.ko && cd ..
    ```

2) ```sh
    git clone git@github.com:dgiantsidi/ngtcp2.git ngtcp2-client && git checkout commitments-protocol-dev
    ```
3) follow the instructions [here](https://github.com/dgiantsidi/zfs-docs/blob/main/quic-instructions.md#how-to-build)

4) repeat steps 2 and 3 for the server-side.

(on the server side) You might also want to execute `export LDFLAGS="-lpthread"` before `autoreconf -i` if the linker is complaining about undefined references of
pthreads, etc.

## How to run


### Server:
```sh
./examples/ptlsserver <server_ip> <server_port> server.key server.crt
```

For example, 
`./examples/ptlsserver 10.5.0.7 6800 server.key server.crt`


### Client:
```sh
./examples/ptlsclient <server_ip> <server_port https://<ip>:<port> -d ./examples/text2.txt
```

For example, `./examples/ptlsclient 10.5.0.7 6800 https://10.5.0.7:1800 -d ./examples/text2.txt`
