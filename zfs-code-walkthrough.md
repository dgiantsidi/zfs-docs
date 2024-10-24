# Documentation of ZFS codebase

`zil_sync()`:

`spa_sync_rewrite_vdev_config()`:

`vdev_config_sync()`:

`uberblock_update()`:

`txg_sync_thread()`: runs from a separate thread asynchronously

`spa_sync()`:

`space_map_write_seg()`:

`space_map_write()`:

`space_map_write_impl()`:

`metaslab.c:2445:metaslab_load_impl()`: also this is called asynchronously by a separate thread (other than the one that calls the `txg_sync_thread()`)


# Execution paths

POSIX-syscall `open()` &#8594; `zpl_file.c:57:zpl_open()` &#8594; `zfs_vnops_os.c:180:zfs_open()`

POSIX-syscall `fsync()` &#8594; `zfs_vnops.c:88:zfs_fsync()` &#8594; `zil.c:3568:zil_commit()` &#8594; `zil.c:3621:zil_commit_impl()` &#8594; `zil.c:3118:zil_commit_writer()` &#8594; `zil.c:2869:zil_process_commit_list()`

POSIX-syscall `write()` &#8594; `zpl_file.c:383:zpl_iter_write()` &#8594; `zpl_file.c:358:zpl_generic_write_checks()` &#8594; `zpl_file.c:256:zfs_io_flags()`  &#8594; `zfs_vnops.c:435:zfs_write()` 


