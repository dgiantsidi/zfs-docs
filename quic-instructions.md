
### Experiment : QUIC protocol 2 VMs (w/ wolfssl)

| VMs   |  latency  |
|---|---|
| R-VMs (acc)  | **latency**=107569 ns ( approx 0.107 ms)|


### How to run

`./examples/wsslserver 10.5.0.6 1800 server.key server.crt`

`./examples/wsslclient 10.5.0.6 1800 https://10.5.0.6:1800 -d ./examples/text2.txt`
