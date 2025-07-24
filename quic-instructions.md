### Documentation

To experiment with QUIC protocol as a stand-alone client/server implementation use the `picotls-dev` branch.

For the integration w/ CCF on the CCF side you should use the `picotls-dev-server`.

The directories organization should be (for cmake to find the correct paths in the `CMakeLists.txt`)
```
<parent_dir>/CCF-bench
<parent_dir>/ngtcp2
```



### Preliminary experiments 

#### QUIC protocol (stand-alone) with 2 VMs (w/ wolfssl) 

- 16/01/2025
  
| VMs   |  latency  |
|---|---|
| R-VMs (acc)  | **latency**=107569 ns ( approx 0.107 ms)|

The results have been verified with `picotls` too.


#### CCF integration with 2 VMs (w/ picotls) 

**Experimental setup: 3 VMs**
- one for workload generation, runs `ptlsclient`
- two for CCF
  
**16/01/2025**
  
| VMs   |  latency  |
|---|---|
| R-VMs (acc)  | **latency**= 0.23 ms (stddev = 0.015 ms) |

**17/01/2025**
  
| VMs   |  latency  |
|---|---|
| R-VMs (acc)  | **latency**= 0.393 ms (stddev=0.014 ms, QUIC lat=0.18 ms, CCF lat=0.2 ms)|
| C-VMs   | **latency**= 1.12 ms (stddev=0.54 ms, QUIC lat=0.4 ms, CCF lat=fluctuations)|


**20/01/2025**
  
| VMs   |  latency  |
|---|---|
| R-VMs (acc)  | **latency**= 0.22 ms|
| R-VMs (w/o acc)  | **latency**= 0.943648 ms (stddev=0.441688 ms)|
| C-VMs   | **latency**= 1.02 ms|


The results have been verified with `picotls` too.
With accelarated networking CCF and QUIC had no significant overhead for "large" data transfers (1K for QUIC and 816-1K for CCF).

### How to run

**Quick stand-alone**

`./examples/wsslserver 10.5.0.6 6800 server.key server.crt` or `ptlsserver`

`./examples/wsslclient <server_ip> (e.g., 10.5.0.6) <port> (e.g., 6800) https://10.5.0.6:1800 -d ./examples/text2.txt` or `ptlsclient`

**CCF integration**

follower(s): `sudo -E LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$(realpath ../../ngtcp2/lib/.libs):$(realpath ../../ngtcp2/nghttp3/build/lib) ./raft_driver <args>`

primary: `sudo -E LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$(realpath ../../ngtcp2/lib/.libs):$(realpath ../../ngtcp2/nghttp3/build/lib) ./raft_driver 10.5.0.7 6800 server.key server.crt`



### How to build

Instructions followed from the following references:

1)
```sh
git clone git@github.com:dgiantsidi/ngtcp2.git && cd ngtcp2 && git submodule update --init && sudo apt-get update && sudo apt-get install libtool  libev-dev libssl-dev pkg-config cmake
```
2)  Build `picotls` (for resolving OpenSSL conficts)
  - `git clone git@github.com:h2o/picotls.git`
  - `cd picotls && git checkout 402544bb65b35c3231a8912f25919de7e7922659`
  - `git submodule init && git submodule update`
  - `cmake . && make`
  - `cd ..`
    
3) Build `nghttp3`
  - `git clone --recursive https://github.com/ngtcp2/nghttp3`
  - `cd nghttp3`
  - `autoreconf -i`
  - `./configure --prefix=$PWD/build --enable-lib-only`
  - `make -j$(nproc) check`
  - `make install`
    
4) Build `ngtcp2`
  - `cd ..`
  - `autoreconf -i`
  - `./configure --with-picotls PICOTLS_CFLAGS="-I$PWD/picotls/include/" PICOTLS_LIBS="-L$PWD/picotls -lpicotls-openssl -lpicotls-core" PKG_CONFIG_PATH=$PWD/nghttp3/build/lib/pkgconfig`
  - `make -C third-party/`
  - `make`
