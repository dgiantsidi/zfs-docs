# Instructions for cloudsuite:postgres

Instructions taken from https://github.com/parsa-epfl/cloudsuite/blob/main/docs/benchmarks/data-serving-relational.md

For TPCC workload:
- Running the server:
  
```sh 
sudo docker run --name postgresql-server --rm -it --privileged --cap-add sys_admin --cap-add sys_ptrace --net host cloudsuite/data-serving-relational:server
```

- Running the loader:

```sh 
sudo docker run --name sysbench-client -it --rm --net host cloudsuite/data-serving-relational:client --warmup --tpcc  --server-ip=127.0.0.1
```

- Running the workload:

```sh
sudo docker run --name sysbench-client -it --rm --net host cloudsuite/data-serving-relational:client --run --tpcc  --server-ip=127.0.0.1
```
