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
def ssh_and_run_commands(host, username, key_filename, cmd1, cmd2, cmd3, clients, filesystem):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, key_filename=key_filename)
    print ("start the loading phase ...");

    # Run cmd1 (loading)
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

    print ("start the warm up phase ...");
    # Run cmd2 (warmup)
    transport = ssh.get_transport()
    session = transport.open_session()
    session.get_pty()  # Request a pseudo-terminal
    session.exec_command(cmd2)
    stdout = session.makefile('rb', -1)
    stderr = session.makefile_stderr('rb', -1)
    stdout.channel.recv_exit_status()  # Wait for cmd1 to complete
    
    time.sleep(30)
    print ("start the experiment phase ...");

    iostat_cmd = "iostat 10 >> long_runs_iostat_output_" + filesystem + "_" + clients + "clients.txt"
    iostat_process = run_cmd_background(iostat_cmd)

    # Run cmd3
    transport = ssh.get_transport()
    session = transport.open_session()
    session.get_pty()  # Request a pseudo-terminal
    session.exec_command(cmd3)
    stdout = session.makefile('rb', -1)
    stderr = session.makefile_stderr('rb', -1)
    stdout.channel.recv_exit_status()  # Wait for cmd1 to complete
    iostat_process.terminate()
    execute_command("sudo pkill iostat")

    # Capture and print stdout and stderr for cmd1
    cmd3_output = stdout.read().decode()
    cmd3_error = stderr.read().decode()
    copy_out3 = cmd3_output
    print(f"Output of cmd2: {cmd3_output}")
    print(f"Error of cmd2: {cmd3_error}")
    ssh.close()

    return copy_out3

# Function to take arguments from the input
def main(args):
    # Print the arguments
    print("Arguments:", args)
    nthreads = args[0]
    iteration = args[1]
    filesystem = args[2]
    # Run initial command in the background
    initial_cmd = "sudo docker run --name postgresql-server --rm -it --privileged --cap-add sys_admin --cap-add sys_ptrace --net host cloudsuite/data-serving-relational:server"
    killing_cmd = "sudo docker kill postgresql-server"
    initial_process = run_cmd_background(initial_cmd)
    print("docker launched")


    # Wait for 100 seconds
    time.sleep(40)
    print("timer done")


    # SSH into another machine and run commands
    host = "10.5.0.7" #"dimitra-ccf-1"
    username = "azureuser"
    my_ip = "10.7.0.4"
    key_filename = "/home/azureuser/dimitra_ccf_1_key"
    cmd1 = "sudo docker run --name sysbench-client -it --rm --net host cloudsuite/data-serving-relational:client --warmup --tpcc  --server-ip=10.7.0.4"
    cmd2 = "sudo docker run --name sysbench-client -it --rm --net host cloudsuite/data-serving-relational:client --run --tpcc  --server-ip=10.7.0.4   --time 150 --threads " + nthreads
    cmd3 = "sudo docker run --name sysbench-client -it --rm --net host cloudsuite/data-serving-relational:client --run --tpcc  --server-ip=10.7.0.4   --time 300 --threads " + nthreads


    output2 = ssh_and_run_commands(host, username, key_filename, cmd1, cmd2, cmd3, nthreads, filesystem)


    #paramiko.util.log_to_file("paramiko.log")

    # Kill the initial command process
    execute_command(killing_cmd)
    print("docker killed")
    time.sleep(5)

    print(output2)

    output_fname = "results_"+ filesystem + "_"+ nthreads+"threads_"+iteration + ".txt"
    with open(output_fname, 'w') as file:
        file.write(output2)

# Check if the script is being run directly
if __name__ == "__main__":
    # Pass the command-line arguments to the main function
    main(sys.argv[1:])
