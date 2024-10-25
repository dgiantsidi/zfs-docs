# Documentation of ZFS codebase

`zil_sync()`:
-  called in syncing context to free committed log blocks and update log header

`zil_commit()`:
 -  commit ZIL transactions (itxs) to stable storage

`zil_alloc()`:
 -  allocates an in-memory structure (`kmem_zalloc()`) for the ZIL
 -  `os_zil`: the in-memory pointer to the ZIL (`zilog_t*`)
 -  `zil_header_t`: ZIL header buffer (`struct zil_header`)

`spa_sync_rewrite_vdev_config()`:

`vdev_config_sync()`:

`uberblock_update()`:

`module/zfs/txg.c:58:txg_sync_thread()`: 
  -  runs continuously from a separate thread asynchronously that is spawn at `txg_sync_start()`
  -  calls into `spa_sync()`
  -  `txg_sync_start()` is called at `module/zfs/spa.c:spa_load_impl()` (to load an existing storage pool using the config provided) and at `module/zfs/spa.c:spa_create()` (to create a new pool)

`spa_sync()`:
  - calls into `spa_sync_iterate_to_convergence()` which calls into `dsl_pool_sync()` and then `dsl_dataset_sync()` and then `dmu_objset_sync()` and then `zil_sync()` and then `dsl_pool_sync_mos()` (which updates the MOS and sets the `ub_rootbp` with `spa_set_rootblkptr()`)

`space_map_write_seg()`:

`space_map_write()`:

`space_map_write_impl()`:

`metaslab.c:2445:metaslab_load_impl()`: also this is called asynchronously by a separate thread (other than the one that calls the `txg_sync_thread()`)


# Execution paths

POSIX-syscall `open()` &#8594; `zpl_file.c:57:zpl_open()` &#8594; `zfs_vnops_os.c:180:zfs_open()`

POSIX-syscall `fsync()` &#8594; `zfs_vnops.c:88:zfs_fsync()` &#8594; `zil.c:3568:zil_commit()` &#8594; `zil.c:3621:zil_commit_impl()` &#8594; `zil.c:3118:zil_commit_writer()` &#8594; `zil.c:2869:zil_process_commit_list()`

POSIX-syscall `write()` &#8594; `zpl_file.c:383:zpl_iter_write()` &#8594; `zpl_file.c:358:zpl_generic_write_checks()` &#8594; `zpl_file.c:256:zfs_io_flags()`  &#8594; `zfs_vnops.c:435:zfs_write()` 


