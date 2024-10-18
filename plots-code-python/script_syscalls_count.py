import matplotlib.pyplot as plt
import numpy as np

# Data
syscalls = ['wait4', 'sendto', 'lseek', 'recvfrom', 'pwrite64', 'pread64', 'futex', 'fdatasync', 'epoll_wait', 'fadvise64', 'fsync', 'sync_file_range', 'kill', 'write', 'brk', 'read', 'rt_sigprocmask', 'openat', 'pselect6', 'close', 'clone', 'setitimer', 'unlink', 'link', 'newfstatat', 'rt_sigreturn', 'getdents64', 'mmap', 'rt_sigaction', 'getpid', 'rename', 'munmap', 'epoll_ctl', 'setsid', 'epoll_create1', 'access', 'getrandom', 'getrusage', 'signalfd4', 'accept', 'prctl', 'setsockopt', 'fcntl', 'getsockname', 'ioctl', 'chown', 'set_robust_list']
calls = [55, 3566753, 7121854, 7394397, 1843257, 2484716, 298674, 74269, 343727, 213162, 1349, 163719, 29421, 24989, 15153, 30766, 38077, 11537, 7800, 5925, 27, 3375, 905, 297, 758, 1820, 72, 141, 331, 203, 11, 79, 134, 27, 27, 27, 27, 42, 27, 8, 27, 16, 16, 8, 3, 1, 27]

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
index = np.arange(len(syscalls))

bars = ax.barh(index, calls, color='skyblue')

ax.set_xlabel('Number of Calls')
ax.set_ylabel('Syscall')
ax.set_title('Count of Calls per Syscall')
ax.set_yticks(index)
ax.set_yticklabels(syscalls)
ax.invert_yaxis()  # Invert y-axis to have the highest count at the top

# Adding the count labels on the bars
for bar in bars:
    width = bar.get_width()
    label_y_pos = bar.get_y() + bar.get_height() / 2
    ax.text(width, label_y_pos, f'{width}', va='center', ha='left')

plt.show()