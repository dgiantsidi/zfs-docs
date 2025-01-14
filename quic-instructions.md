
### Experiment : QUIC protocol 2 VMs (w/ wolfssl)

| VMs   |  latency  |
|---|---|
| R-VMs (acc)  | **latency**=107569 ns ( approx 0.107 ms)|


### How to run

`./examples/wsslserver 10.5.0.6 1800 server.key server.crt`

`./examples/wsslclient 10.5.0.6 1800 https://10.5.0.6:1800 -d ./examples/text2.txt`


### How to build

Instructions followed from the following references:

1) `autoreconf -i`
2) Build `picotls` (for resolving OpenSSL conficts)
  - `git clone git@github.com:h2o/picotls.git`
  - `cd picotls` and `git checkout 402544bb65b35c3231a8912f25919de7e7922659`
  - `git submodule init` and `git submodule update`
  - `cmake . && make`
3) Configure `ngtcp2`
  - `./configure --with-picotls PICOTLS_CFLAGS="-I$PWD/picotls/include/" PICOTLS_LIBS="-L$PWD/picotls -lpicotls-openssl -lpicotls-core" PKG_CONFIG_PATH=$PWD/nghttp3/build/lib/pkgconfig`
4) Build
  - `make`
