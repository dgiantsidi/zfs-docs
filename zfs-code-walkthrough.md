# Documentation of ZFS codebase

`zil_sync()`:
-  called in syncing context to free committed log blocks and update log header

`zil_commit()`:
 -  commit ZIL transactions (itxs) to stable storage
 -  the in-memory ZIL representation is linked-lists of `itx_t` (defined in `zil.h`)
 -  the on-disk ZIL representation is `lwb_t` (defined in `zil_impl.h`)

`zil_alloc()`:
 -  allocates an in-memory structure (`kmem_zalloc()`) for the ZIL
 -  `os_zil`: the in-memory pointer to the ZIL (`zilog_t*`)
 -  `zil_header_t`: ZIL header buffer (`struct zil_header`)

`spa_sync_rewrite_vdev_config()`:

`vdev_config_sync()`:
 - sync the uberblock and any changes to the vdev configuration
 - calls into `uberblock_update()` which updates the in-memory state and then
   flushes the write cache of every disk that is dirty due to the current transaction group
   It makes sure that all blocks written in this txg will be first committed to the persistent storage
   before any uberblock that references them (atomic update). We first update the even labels (`vdev_label_sync_list()`) to the
   perstistent storage and then the uberblock (`vdev_uberblock_sync_list()`). Then we update the odd labels similarly to the even
   labels (`vdev_label_sync_list()`).

`uberblock_update()`: 
 - computes the in-memory uberblock data and returns
 - then, this in-memory uberblock is serialized into a buffer and flashed to the persistent storage at `vdev_uberblock_sync_list()`  (called by `vdev_config_sync()`)

`module/zfs/txg.c:58:txg_sync_thread()`: 
  -  runs continuously from a separate thread asynchronously that is spawn at `txg_sync_start()`
  -  calls into `spa_sync()`
  -  `txg_sync_start()` is called at `module/zfs/spa.c:spa_load_impl()` (to load an existing storage pool using the config provided) and at `module/zfs/spa.c:spa_create()` (to create a new pool)

`spa_sync()`:
  - calls into `spa_sync_iterate_to_convergence()` which calls into `dsl_pool_sync()` and then `dsl_dataset_sync()` and then `dmu_objset_sync()` and then `zil_sync()` and then `dsl_pool_sync_mos()` (which updates the MOS and sets the `ub_rootbp` with `spa_set_rootblkptr()`)

`space_map_write_seg()`:

`space_map_write()`:

`space_map_write_impl()`:

`metaslab.c:2445:metaslab_load_impl()`: also this is called asynchronously by a separate thread (might be other than the one that calls the `txg_sync_thread()`)


# Execution paths

POSIX-syscall `open()` &#8594; `zpl_file.c:57:zpl_open()` &#8594; `zfs_vnops_os.c:180:zfs_open()`

POSIX-syscall `fsync()` &#8594; `zfs_vnops.c:88:zfs_fsync()` &#8594; `zil.c:3568:zil_commit()` &#8594; `zil.c:3621:zil_commit_impl()` &#8594; `zil.c:3118:zil_commit_writer()` &#8594; `zil.c:2869:zil_process_commit_list()`

POSIX-syscall `write()` &#8594; `zpl_file.c:383:zpl_iter_write()` &#8594; `zpl_file.c:358:zpl_generic_write_checks()` &#8594; `zpl_file.c:256:zfs_io_flags()`  &#8594; `zfs_vnops.c:435:zfs_write()` 


# Data structures

- `Metaslabs` are data structures used to track memory allocations by the `spa` (storage pool allocator).
-  The bookkeeping information for the allocator is represented in-memory as a ```collection of range trees```.
-  The bookkeeping information for the allocator is represented on-disk as a ```space map```.

## Space map

-  A log of free or allocated space for a region. Records are appended as space becaomes freed/allocated from the region.
-  `ms_tree` is a range tree that represents the available space that is allocatable.
-  `ms_alloctree` contains all blocks that are allocated in a sync pass.
-  `ms_freetree` contains all blocks that are freed in a sync pass.
-  `metaslab_sync` all dirty metaslabs are synced; all dirty blocks from `ms_alloctree` and `ms_freetree` for the current (syncing) txg are written to the associated `space map`.


# Random notes (to be organized)

Everything in ZFS (compression, encryption, checksum, dedup, etc) works over logical blocks (dataset recordsize, zvol volblocksize, etc), each pointed by a block pointer, actually including the checksum, compression and encryption parameters, etc.

ZIL txg writes are not atomic: https://github.com/openzfs/zfs/discussions/17051. A txg might be spread into many lwbs which are written sequentially.
