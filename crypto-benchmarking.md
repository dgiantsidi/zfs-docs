On regural VM: 

```openssl speed -evp aes-128-gcm sha hmac-sha256```

```
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes  16384 bytes
hmac(md5)        55344.79k   167232.75k   385013.42k   570295.64k   663489.19k   671312.55k
aes-128-gcm     587849.01k  1178748.48k  2845301.76k  3711603.71k  4238289.58k  4290270.55k
sha256          226223.19k   549139.61k  1086471.85k  1433621.50k  1581189.80k  1592841.56k
```
