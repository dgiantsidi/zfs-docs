import subprocess
import time
import paramiko
import sys

# Function to execute a command
def execute_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

# Function to run a command in the background
def run_cmd_background(cmd):
    return subprocess.Popen(cmd, shell=True)

# Function to SSH into another machine and run commands
def ssh_and_run_commands(host, username, key_filename, cmd1, cmd2, clients):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, key_filename=key_filename)
    print ("starting loading phase");

    # Run cmd1
    transport = ssh.get_transport()
    session = transport.open_session()
    session.get_pty()  # Request a pseudo-terminal
    session.exec_command(cmd1)
    stdout = session.makefile('rb', -1)
    stderr = session.makefile_stderr('rb', -1)
    stdout.channel.recv_exit_status()  # Wait for cmd1 to complete
    
    # Capture and print stdout and stderr for cmd1
    cmd1_output = stdout.read().decode()
    cmd1_error = stderr.read().decode()
    print(f"Output of cmd1: {cmd1_output}")
    print(f"Error of cmd1: {cmd1_error}")


    iostat_cmd = "iostat 2 >> iostat_output_" + clients + "clients_default_zfs.txt"
    iostat_process = run_cmd_background(iostat_cmd)

    # Run cmd2
    transport = ssh.get_transport()
    session = transport.open_session()
    session.get_pty()  # Request a pseudo-terminal
    session.exec_command(cmd2)
    stdout = session.makefile('rb', -1)
    stderr = session.makefile_stderr('rb', -1)
    stdout.channel.recv_exit_status()  # Wait for cmd1 to complete
    iostat_process.terminate()

    # Capture and print stdout and stderr for cmd1
    cmd2_output = stdout.read().decode()
    cmd2_error = stderr.read().decode()
    copy_out2 = cmd2_output
    print(f"Output of cmd2: {cmd2_output}")
    print(f"Error of cmd2: {cmd2_error}")
    ssh.close()


    return copy_out2

# Function to take arguments from the input
def main(args):
    # Print the arguments
    print("Arguments:", args)
    nthreads = args[0]
    iteration = args[1]
    # Run initial command in the background
    initial_cmd = "sudo docker run --name postgresql-server --rm -it --privileged --cap-add sys_admin --cap-add sys_ptrace --net host cloudsuite/data-serving-relational:server"
    killing_cmd = "sudo docker kill postgresql-server"
    initial_process = run_cmd_background(initial_cmd)
    print("docker launched")


    # Wait for 100 seconds
    time.sleep(40)
    print("timer done")


    # SSH into another machine and run commands
    host = "dimitra-ccf-1"
    username = "azureuser"
    key_filename = "/home/azureuser/dimitra_ccf_1_key"
    cmd1 = "sudo docker run --name sysbench-client -it --rm --net host cloudsuite/data-serving-relational:client --warmup --tpcc  --server-ip=10.5.0.8"
    cmd2 = "sudo docker run --name sysbench-client -it --rm --net host cloudsuite/data-serving-relational:client --run --tpcc  --server-ip=10.5.0.8 --threads " + nthreads


    output2 = ssh_and_run_commands(host, username, key_filename, cmd1, cmd2, nthreads)


    #paramiko.util.log_to_file("paramiko.log")

    # Kill the initial command process
    execute_command(killing_cmd)
    print("docker killed")
    time.sleep(5)

    print(output2)

    output_fname = "delay_1ms_"+ nthreads+"threads_"+iteration + ".txt"
    with open(output_fname, 'w') as file:
        file.write(output2)

# Check if the script is being run directly
if __name__ == "__main__":
    # Pass the command-line arguments to the main function
    main(sys.argv[1:])

